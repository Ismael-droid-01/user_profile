from collections import Counter
from utils.preprocessing import normalize_text, parse_and_tokenize
import tkinter as tk
from tkinter import ttk


def build_bow(data, language="en"):
    bow = {}
    for record in data:
        user_id = record["user_id"]
        clean_text, _ = normalize_text(record["text"], language=language)
        tokens = parse_and_tokenize(clean_text, language=language)
        # Actualizar bolsa de palabras en caso de obtener una segunda publicación de un usuario existente
        if user_id not in bow:
            bow[user_id] = Counter(tokens)
        else:
            bow[user_id].update(Counter(tokens))
    
    return bow

def show_bow(bow):
    all_words = set()
    for words in bow.values():
        all_words.update(words.keys())
    all_words = sorted(all_words)

    MAX_COLUMNS = 20
    if len(all_words) > MAX_COLUMNS:
        all_words = all_words[:MAX_COLUMNS]

    view = tk.Tk()
    view.title("Bolsa de palabras")
    view.geometry("1200x600")

    columns = all_words

    frame = ttk.Frame(view)
    frame.pack(expand=True, fill="both")

    vsb = ttk.Scrollbar(frame, orient="vertical")
    hsb = ttk.Scrollbar(frame, orient="horizontal")

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="tree headings",
        yscrollcommand=vsb.set,
        xscrollcommand=hsb.set
    )

    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    # Bloque de redimensión de columnas
    tree.bind("<Button-1>", lambda e: "break" if tree.identify_region(e.x, e.y) == "separator" else None)

    tree.heading('#0', text='usuario')
    tree.column('#0', width=250, stretch=False)

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=100, stretch=False)

    for user_id, counter in bow.items():
        row = [counter.get(word, 0) for word in all_words]
        tree.insert("", tk.END, text=user_id, values=row)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    vsb.grid_remove()
    hsb.grid_remove()

    tree.bind("<Configure>", lambda e: (vsb.grid() if tree.yview() != (0.0,1.0) else vsb.grid_remove()) or (hsb.grid() if tree.xview() != (0.0,1.0) else hsb.grid_remove()))
    tree.bind("<Motion>", lambda e: (vsb.grid() if tree.yview() != (0.0,1.0) else vsb.grid_remove()) or (hsb.grid() if tree.xview() != (0.0,1.0) else hsb.grid_remove()))


    view.mainloop()

