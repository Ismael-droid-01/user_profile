import tkinter as tk
from tkinter import ttk
from utils.preprocessing import normalize_text

def show_viewer(user_vector, parent=None):
    view = tk.Toplevel(parent)
    view.title(user_vector["user_id"])
    view.geometry("400x800")
    view.resizable(False, False)

    # Texto original
    lbl_original_title = tk.Label(view, text="Texto original:", font=("Arial", 10, "bold"))
    lbl_original_title.pack(anchor="w", padx=10, pady=(10,0))
    lbl_original_text = tk.Label(view, text=user_vector["text"], font=("Arial", 10))
    lbl_original_text.pack(anchor="w", padx=20, pady=(0,10))

    # Normalizar el texto
    clean_text, percentage_change = normalize_text(user_vector["text"])

    # Texto limpio
    lbl_clean_title = tk.Label(view, text="Texto limpio:", font=("Arial", 10, "bold"))
    lbl_clean_title.pack(anchor="w", padx=10)
    lbl_clean_text = tk.Label(view, text=clean_text, font=("Arial", 10))
    lbl_clean_text.pack(anchor="w", padx=20, pady=(0,10))

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