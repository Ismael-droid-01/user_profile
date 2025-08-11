import tkinter as tk
from tkinter import ttk
from utils.preprocessing import normalize_text

def create_text_viewer(parent, content):
    frame = tk.Frame(parent)
    text_widget = tk.Text(frame, wrap="word", height=10, font=("Arial", 10))
    text_widget.insert("1.0", content)
    text_widget.config(state="disabled")  # solo lectura
    scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)

    text_widget.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return frame


def show_viewer(user_vector, parent=None):
    print(user_vector)
    view = tk.Toplevel(parent)
    view.title(user_vector["user_id"])
    view.geometry("400x800")
    view.resizable(False, False)

    # Texto original
    lbl_original_title = tk.Label(view, text="Texto original:", font=("Arial", 10, "bold"))
    lbl_original_title.pack(anchor="w", padx=10, pady=(10,0))
    original_text_frame = create_text_viewer(view, user_vector["text"])
    original_text_frame.pack(fill="both", padx=20, pady=(0, 10), expand=False)

    # Normalizar el texto
    clean_text, percentage_change = normalize_text(user_vector["text"])

    # Texto limpio
    lbl_clean_title = tk.Label(view, text="Texto limpio:", font=("Arial", 10, "bold"))
    lbl_clean_title.pack(anchor="w", padx=10)
    clean_text_frame = create_text_viewer(view, clean_text)
    clean_text_frame.pack(fill="both", padx=20, pady=(0, 10), expand=False)

    # Porcentaje cambios
    lbl_changes = tk.Label(view, text=f"% cambios: {percentage_change} %", font=("Arial", 10, "bold"))
    lbl_changes.pack(anchor="w", padx=10, pady=(0,10))

    # Tokens con conteo
    lbl_tokens_title = tk.Label(view, text="Tokens (frecuencia):", font=("Arial", 10, "bold"))
    lbl_tokens_title.pack(anchor="w", padx=10)

    for token, count in user_vector['bow'].items():
        tk.Label(view, text=f"{token}: {count}").pack(anchor="w", padx=20)

    # Selector personalidad
    lbl_personality = tk.Label(view, text="Selector personalidad:")
    lbl_personality.pack(anchor="w", padx=10, pady=(10,0))
    combo_personality = ttk.Combobox(view, values=["Formal", "Casual", "Amigable"])
    combo_personality.pack(anchor="w", padx=20, pady=(0,10))

    # Selector profesional
    lbl_professional = tk.Label(view, text="Selector profesional:")
    lbl_professional.pack(anchor="w", padx=10)
    combo_professional = ttk.Combobox(view, values=["Programador", "Diseñador", "Analista"])
    combo_professional.pack(anchor="w", padx=20, pady=(0,20))

    # Botón
    btn_save = tk.Button(view, text="Guardar etiqueta", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    btn_save.pack(pady=10)

    return view