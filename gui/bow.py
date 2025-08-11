import tkinter as tk
from tkinter import ttk
import gui.labeler as labeler
from functools import partial

def on_double_click(tree, item_to_record, event):
    selected_item = tree.focus()
    if selected_item:
        record = item_to_record.get(selected_item)
        if record:
            labeler.show_viewer(record)

def show_viewer(data_list):
    # Convertir la lista a diccionario dentro de la función
    bow = {}
    for record in data_list:
        user_id = record.get('user_id', 'Desconocido')
        user_bow = record.get('bow', {})
        bow[user_id] = user_bow

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

    item_to_record = {}

    for user_id, counter in bow.items():
        row = [counter.get(word, 0) for word in all_words]
        item_id = tree.insert("", tk.END, text=user_id, values=row)
        record = next(r for r in data_list if r.get('user_id') == user_id)
        item_to_record[item_id] = record

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    vsb.grid_remove()
    hsb.grid_remove()

    tree.bind("<Configure>", lambda e: (vsb.grid() if tree.yview() != (0.0,1.0) else vsb.grid_remove()) or (hsb.grid() if tree.xview() != (0.0,1.0) else hsb.grid_remove()))
    tree.bind("<Motion>", lambda e: (vsb.grid() if tree.yview() != (0.0,1.0) else vsb.grid_remove()) or (hsb.grid() if tree.xview() != (0.0,1.0) else hsb.grid_remove()))

    tree.bind("<Double-1>", partial(on_double_click, tree, item_to_record))

    view.mainloop()

