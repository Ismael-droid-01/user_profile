import tkinter as tk
from tkinter import ttk, messagebox
from utils.preprocessing import normalize_text

class LabelerScreen(tk.Toplevel):
    def __init__(self, user_vector, parent=None):
        super().__init__(parent)
        self.user_vector = user_vector
        self.title(user_vector.get("user_id", "Detalle"))
        self.geometry("625x800")
        self.resizable(False, False)

        self._create_scrollable_area()

        self._create_widgets()
    
    def _create_scrollable_area(self):
        self.canvas = tk.Canvas(self)
        self.v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame interior donde se colocan los widgets
        self.content_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.content_frame, anchor="nw")

        # Actualizar scrollregion cuando cambia tamaño content_frame
        self.content_frame.bind("<Configure>", self._on_frame_configure)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _create_widgets(self):
        info_frame = tk.Frame(self.content_frame)
        info_frame.pack(fill="x", padx=10, pady=(10,5))

        # Información general con Labels en grid
        tk.Label(info_frame, text=f"Idioma: {self.user_vector.get('language', 'N/A')}", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(info_frame, text=f"Días de cuenta: {self.user_vector.get('account_age_days', 'N/A')}", font=("Arial", 10)).grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(info_frame, text=f"Popularidad: {self.user_vector.get('popularity_score', 'N/A')}", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5)
        tk.Label(info_frame, text=f"Engagement: {self.user_vector.get('engagement_score', 'N/A')}", font=("Arial", 10)).grid(row=1, column=1, sticky="w", padx=5)
        tk.Label(info_frame, text=f"Alcance: {self.user_vector.get('reach_score', 'N/A')}", font=("Arial", 10)).grid(row=1, column=2, sticky="w", padx=5)

        # Datos variables del content_meta
        meta = self.user_vector.get('content_meta', {})
        if meta:
            row_idx = 2
            for key, value in meta.items():
                tk.Label(info_frame, text=f"{self._format_meta_key(key)}: {value}", font=("Arial", 10)).grid(row=row_idx, column=0, columnspan=3, sticky="w", padx=5, pady=(0,2))
                row_idx += 1

        # Texto original
        lbl_original_title = tk.Label(self.content_frame, text="Texto original:", font=("Arial", 10, "bold"))
        lbl_original_title.pack(anchor="w", padx=10, pady=(10,0))

        self.original_text_frame = self._create_text_viewer(self.content_frame, self.user_vector["text"])
        self.original_text_frame.pack(fill="both", padx=20, pady=(0, 10), expand=False)

        # Texto limpio y porcentaje de cambios
        clean_text, percentage_change = normalize_text(self.user_vector["text"])

        lbl_clean_title = tk.Label(self.content_frame, text="Texto limpio:", font=("Arial", 10, "bold"))
        lbl_clean_title.pack(anchor="w", padx=10)

        self.clean_text_frame = self._create_text_viewer(self.content_frame, clean_text)
        self.clean_text_frame.pack(fill="both", padx=20, pady=(0, 10), expand=False)

        lbl_changes = tk.Label(self.content_frame, text=f"{percentage_change} % de cambios", font=("Arial", 10, "bold"))
        lbl_changes.pack(anchor="w", padx=10, pady=(0,10))

        # Tabla de tokens
        tokens_table = self._create_tokens_table(self.content_frame, self.user_vector['bow'])
        tokens_table.pack(fill="both", padx=20, pady=(0, 10), expand=False)

        # Selectores para etiquetas
        self.selectors_frame = tk.Frame(self.content_frame)
        self.selectors_frame.pack(fill="x", padx=10, pady=(10, 20))

        tk.Label(self.selectors_frame, text="Selector personalidad:").grid(row=0, column=0, sticky="w", padx=(0,5))
        self.combo_personality = ttk.Combobox(self.selectors_frame, values=["Formal", "Casual", "Amigable"], width=15)
        self.combo_personality.grid(row=0, column=1, sticky="w", padx=(0,15))

        tk.Label(self.selectors_frame, text="Selector profesional:").grid(row=0, column=2, sticky="w", padx=(0,5))
        self.combo_professional = ttk.Combobox(self.selectors_frame, values=["Programador", "Diseñador", "Analista"], width=15)
        self.combo_professional.grid(row=0, column=3, sticky="w")

        self.btn_save = tk.Button(
            self.content_frame,
            text="Guardar etiqueta",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self._save_labels
        )
        self.btn_save.pack(pady=10)
    
    def _create_text_viewer(self, parent, content):
        frame = tk.Frame(parent)
        text_widget = tk.Text(frame, wrap="word", height=10, font=("Arial", 10))
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")  # solo lectura

        scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return frame

    def _create_tokens_table(self, parent, bow_data):
        frame = tk.Frame(parent)
        columns = ("token", "count")

        tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        tree.heading("token", text="Token")
        tree.heading("count", text="Frecuencia")
        tree.column("token", width=150, anchor="w")
        tree.column("count", width=80, anchor="center")

        for token, count in bow_data.items():
            tree.insert("", "end", values=(token, count))

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return frame

    def _format_meta_key(self, key):
        translations = {
            "video_title": "Título del video",
            "country": "País",
            "is_mod": "Moderador"
        }
        return translations.get(key, key)

    def _save_labels(self):
        personality = self.combo_personality.get()
        professional = self.combo_professional.get()

        if personality and professional:
            messagebox.showinfo("Éxito", f"Etiquetas guardadas")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona ambas etiquetas antes de guardar.")