import tkinter as tk
from tkinter import ttk, messagebox
from utils.vectorization import generate_vector
from gui.screens.bow_screen import BowScreen
from threading import Thread

class VectorConfigScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configuración del Vector")
        self.geometry("400x300")
        self.resizable(False, False)

        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        # Etiquetas y controles
        self.lbl_source = tk.Label(self, text="Fuente de datos:")
        self.combo_source = ttk.Combobox(self, values=["reddit", "youtube"], state="readonly")
        self.combo_source.current(0)

        self.lbl_limit = tk.Label(self, text="Límite de posts:")
        self.entry_limit = tk.Entry(self)
        self.entry_limit.insert(0, "100")

        self.lbl_language = tk.Label(self, text="Idioma:")
        self.combo_language = ttk.Combobox(self, values=["es", "en"], state="readonly")
        self.combo_language.current(0)

        self.btn_generate = tk.Button(self, text="Generar Vector", command=self._on_generate)

        self.status_text = tk.StringVar()
        self.lbl_status = tk.Label(self, textvariable=self.status_text, fg="blue")

    def _layout_widgets(self):
        padx = 20
        pady = 10

        self.lbl_source.pack(anchor="w", padx=padx, pady=(pady, 0))
        self.combo_source.pack(fill="x", padx=padx)

        self.lbl_limit.pack(anchor="w", padx=padx, pady=(pady, 0))
        self.entry_limit.pack(fill="x", padx=padx)

        self.lbl_language.pack(anchor="w", padx=padx, pady=(pady, 0))
        self.combo_language.pack(fill="x", padx=padx)

        self.btn_generate.pack(pady=25)

        self.lbl_status.pack(fill="x", padx=padx)

    def _on_generate(self):
        limit_str = self.entry_limit.get()
        if not limit_str.isdigit() or int(limit_str) <= 0:
            messagebox.showerror("Error", "El límite de posts debe ser un número entero positivo.")
            return

        source = self.combo_source.get()
        limit = int(limit_str)
        language = self.combo_language.get()

        self._set_widgets_state("disabled")
        self.status_text.set("Generando vector, por favor espera...")

        def task():
            try:
                data = generate_vector(source=source, limit=limit, language=language)
            except Exception as e:
                self.after(0, lambda: self._on_generation_error(str(e)))
            else:
                self.after(0, lambda: self._on_generation_success(data))

        Thread(target=task, daemon=True).start()
        
    def _on_generation_success(self, data):
        self._set_widgets_state("normal")
        self.status_text.set("Vector generado correctamente.")
        if data:
            self.withdraw()  # Cierra esta ventana antes de abrir BowScreen
            bow_screen = BowScreen(data, parent=None)
            bow_screen.grab_set()
            bow_screen.focus_set()
            bow_screen.protocol("WM_DELETE_WINDOW", lambda: (self.deiconify(), bow_screen.destroy()))
        else:
            messagebox.showinfo("Información", "No se generaron datos para mostrar.")

    def _on_generation_error(self, message):
        self._set_widgets_state("normal")
        self.status_text.set("")
        messagebox.showerror("Error", f"No se pudo generar el vector:\n{message}")

    def _set_widgets_state(self, state):
        self.combo_source.config(state=state)
        self.entry_limit.config(state=state)
        self.combo_language.config(state=state)
        self.btn_generate.config(state=state)