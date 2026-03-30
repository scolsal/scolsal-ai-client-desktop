"""
AI Client Desktop - A simple desktop client for AI interactions using Tkinter.
Connects to the OpenAI API to send prompts and display responses.
"""

import os
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def get_ai_response(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Send a prompt to the OpenAI API and return the response text."""
    if not OPENAI_AVAILABLE:
        raise RuntimeError(
            "La biblioteca 'openai' no está instalada. "
            "Ejecuta: pip install -r requirements.txt"
        )

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "No se encontró la clave API de OpenAI. "
            "Configura la variable de entorno OPENAI_API_KEY en el archivo .env"
        )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        timeout=30,
    )
    return response.choices[0].message.content.strip()


class AIClientApp(tk.Tk):
    """Main application window for the AI desktop client."""

    def __init__(self):
        super().__init__()
        self.title("AI Client Desktop")
        self.geometry("700x520")
        self.resizable(True, True)
        self._build_ui()

    def _build_ui(self):
        """Build and lay out all UI widgets."""
        # ── Response area ──────────────────────────────────────────────────
        response_frame = tk.Frame(self)
        response_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        tk.Label(response_frame, text="Respuesta de la IA:", anchor="w").pack(fill=tk.X)
        self.response_area = scrolledtext.ScrolledText(
            response_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Helvetica", 11),
            bg="#f9f9f9",
        )
        self.response_area.pack(fill=tk.BOTH, expand=True)

        # ── Prompt input ───────────────────────────────────────────────────
        input_frame = tk.Frame(self)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

        tk.Label(input_frame, text="Ingresa tu mensaje:", anchor="w").pack(fill=tk.X)
        self.prompt_input = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            height=5,
            font=("Helvetica", 11),
        )
        self.prompt_input.pack(fill=tk.X)
        # Allow Ctrl+Enter to send
        self.prompt_input.bind("<Control-Return>", lambda _e: self._on_send())

        # ── Controls ───────────────────────────────────────────────────────
        controls_frame = tk.Frame(self)
        controls_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.status_label = tk.Label(
            controls_frame, text="", fg="gray", anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.send_button = tk.Button(
            controls_frame,
            text="Enviar",
            width=12,
            command=self._on_send,
        )
        self.send_button.pack(side=tk.RIGHT)

        clear_button = tk.Button(
            controls_frame,
            text="Limpiar",
            width=10,
            command=self._on_clear,
        )
        clear_button.pack(side=tk.RIGHT, padx=(0, 5))

    # ── Event handlers ─────────────────────────────────────────────────────

    def _on_send(self):
        """Validate input and dispatch the API call in a background thread."""
        prompt = self.prompt_input.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showwarning("Prompt vacío", "Por favor ingresa un prompt antes de enviar.")
            return

        self._set_busy(True)
        threading.Thread(target=self._fetch_response, args=(prompt,), daemon=True).start()

    def _fetch_response(self, prompt: str):
        """Call the AI API and update the UI (runs in a worker thread)."""
        try:
            response_text = get_ai_response(prompt)
            self.after(0, self._show_response, response_text)
        except (ValueError, RuntimeError) as exc:
            self.after(0, self._show_error, str(exc))
        except Exception as exc:
            # Covers AuthenticationError, RateLimitError, APIConnectionError, etc.
            self.after(0, self._show_error, f"Error al comunicarse con la API:\n{exc}")

    def _show_response(self, text: str):
        """Display a successful response and restore the UI."""
        self.response_area.configure(state=tk.NORMAL)
        self.response_area.delete("1.0", tk.END)
        self.response_area.insert(tk.END, text)
        self.response_area.configure(state=tk.DISABLED)
        self._set_busy(False)

    def _show_error(self, message: str):
        """Show an error dialog and restore the UI."""
        self._set_busy(False)
        messagebox.showerror("Error", message)

    def _on_clear(self):
        """Clear both the prompt and the response areas."""
        self.prompt_input.delete("1.0", tk.END)
        self.response_area.configure(state=tk.NORMAL)
        self.response_area.delete("1.0", tk.END)
        self.response_area.configure(state=tk.DISABLED)
        self.status_label.configure(text="")

    def _set_busy(self, busy: bool):
        """Toggle the loading state of the UI."""
        if busy:
            self.send_button.configure(state=tk.DISABLED)
            self.status_label.configure(text="Enviando…")
        else:
            self.send_button.configure(state=tk.NORMAL)
            self.status_label.configure(text="")


def main():
    app = AIClientApp()
    app.mainloop()


if __name__ == "__main__":
    main()
