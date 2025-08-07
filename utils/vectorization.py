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

    view = tk.Tk()
    view.title("Bolsa de palabras")

    columns = ["usuario"] + all_words
    tree = ttk.Treeview(view, columns=columns, show="headings")
    # Bloque de redimensión de columnas
    tree.bind("<Button-1>", lambda e: "break" if tree.identify_region(e.x, e.y) == "separator" else None)

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=100, stretch=False)

    for user_id, counter in bow.items():
        row = [user_id] + [counter.get(word, 0) for word in all_words]
        tree.insert("", tk.END, values=row)

    tree.pack(expand=True, fill="both")
    view.mainloop()

