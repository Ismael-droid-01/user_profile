import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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

def create_tokens_table(parent, bow_data):
    frame = tk.Frame(parent)

    columns = ("token", "count")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
    tree.heading("token", text="Token")
    tree.heading("count", text="Frecuencia")
    tree.column("token", width=150, anchor="w")
    tree.column("count", width=80, anchor="center")

    # Insertar datos
    for token, count in bow_data.items():
        tree.insert("", "end", values=(token, count))

    # Scrollbar vertical para la tabla
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return frame

# Función para actualizar scrollregion cuando cambie tamaño
def on_frame_configure(event, canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def save_labels(combo_personality, combo_professional):
    personality = combo_personality.get()
    professional = combo_personality.get()

    if personality and professional:
        messagebox.showinfo("Éxito", f"Etiquetas guardadas")
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona ambas etiquetas antes de guardar.")

def show_viewer(user_vector, parent=None):
    print(user_vector)
    view = tk.Toplevel(parent)
    view.title(user_vector["user_id"])
    view.geometry("800x800")
    view.resizable(False, False)

    # Crear canvas y scrollbar principal
    canvas = tk.Canvas(view)
    scrollbar = tk.Scrollbar(view, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Frame interior
    content_frame = tk.Frame(canvas)
    canvas.create_window((0,0), window=content_frame, anchor="nw")

    content_frame.bind("<Configure>", lambda event: on_frame_configure(event, canvas))

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

    tokens_table = create_tokens_table(content_frame, user_vector['bow'])
    tokens_table.pack(fill="both", padx=20, pady=(0, 10), expand=False)

    # Contenedor para los selectores en una fila
    selectors_frame = tk.Frame(content_frame)
    selectors_frame.pack(fill="x", padx=10, pady=(10, 20))

    # Etiqueta y combo para personalidad
    lbl_personality = tk.Label(selectors_frame, text="Selector personalidad:")
    lbl_personality.grid(row=0, column=0, sticky="w", padx=(0,5))
    combo_personality = ttk.Combobox(selectors_frame, values=["Formal", "Casual", "Amigable"], width=15)
    combo_personality.grid(row=0, column=1, sticky="w", padx=(0,15))

    # Etiqueta y combo para profesional
    lbl_professional = tk.Label(selectors_frame, text="Selector profesional:")
    lbl_professional.grid(row=0, column=2, sticky="w", padx=(0,5))
    combo_professional = ttk.Combobox(selectors_frame, values=["Programador", "Diseñador", "Analista"], width=15)
    combo_professional.grid(row=0, column=3, sticky="w")

    btn_save = tk.Button(content_frame, text="Guardar etiqueta", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=lambda: save_labels(combo_personality, combo_professional))
    btn_save.pack(pady=10)

    return view
