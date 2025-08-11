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

    # Crear canvas y scrollbar principal
    canvas = tk.Canvas(view)
    scrollbar = tk.Scrollbar(view, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Frame interior donde irán todos los widgets
    content_frame = tk.Frame(canvas)
    canvas.create_window((0,0), window=content_frame, anchor="nw")

    # Función para actualizar scrollregion cuando cambie tamaño
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_frame.bind("<Configure>", on_frame_configure)

    # Ahora ponemos todos tus widgets dentro de content_frame en lugar de view
    lbl_original_title = tk.Label(content_frame, text="Texto original:", font=("Arial", 10, "bold"))
    lbl_original_title.pack(anchor="w", padx=10, pady=(10,0))
    original_text_frame = create_text_viewer(content_frame, user_vector["text"])
    original_text_frame.pack(fill="both", padx=20, pady=(0, 10), expand=False)

    clean_text, percentage_change = normalize_text(user_vector["text"])

    lbl_clean_title = tk.Label(content_frame, text="Texto limpio:", font=("Arial", 10, "bold"))
    lbl_clean_title.pack(anchor="w", padx=10)
    clean_text_frame = create_text_viewer(content_frame, clean_text)
    clean_text_frame.pack(fill="both", padx=20, pady=(0, 10), expand=False)

    lbl_changes = tk.Label(content_frame, text=f"% cambios: {percentage_change} %", font=("Arial", 10, "bold"))
    lbl_changes.pack(anchor="w", padx=10, pady=(0,10))

    lbl_tokens_title = tk.Label(content_frame, text="Tokens (frecuencia):", font=("Arial", 10, "bold"))
    lbl_tokens_title.pack(anchor="w", padx=10)

    for token, count in user_vector['bow'].items():
        tk.Label(content_frame, text=f"{token}: {count}").pack(anchor="w", padx=20)

    lbl_personality = tk.Label(content_frame, text="Selector personalidad:")
    lbl_personality.pack(anchor="w", padx=10, pady=(10,0))
    combo_personality = ttk.Combobox(content_frame, values=["Formal", "Casual", "Amigable"])
    combo_personality.pack(anchor="w", padx=20, pady=(0,10))

    lbl_professional = tk.Label(content_frame, text="Selector profesional:")
    lbl_professional.pack(anchor="w", padx=10)
    combo_professional = ttk.Combobox(content_frame, values=["Programador", "Diseñador", "Analista"])
    combo_professional.pack(anchor="w", padx=20, pady=(0,20))

    btn_save = tk.Button(content_frame, text="Guardar etiqueta", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    btn_save.pack(pady=10)

    return view
