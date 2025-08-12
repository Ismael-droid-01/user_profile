import tkinter as tk
from tkinter import ttk
from functools import partial
from gui.screens.labeler_screen import LabelerScreen

class BowScreen(tk.Tk):
    _subwindow = None

    def __init__(self, data_list):
        super().__init__()
        self.title("Bolsa de palabras")
        self.geometry("1200x600")

        self.data_list = data_list
        self.bow = {}
        self.all_words = []
        self.MAX_COLUMNS = 20

        self._setup_data()
        self._create_widgets()
        self._layout_widgets()
        self._bind_events()

    def _setup_data(self):
        for record in self.data_list:
            user_id = record.get("user_id")
            user_bow = record.get("bow", {})
            self.bow[user_id] = user_bow

        all_words = set()
        for words in self.bow.values():
            all_words.update(words.keys())
        all_words = sorted(all_words)

        if len(all_words) > self.MAX_COLUMNS:
            all_words = all_words[:self.MAX_COLUMNS]
        
        self.all_words = all_words

    def _create_widgets(self):
        self.frame = ttk.Frame(self)
        self.vsb = ttk.Scrollbar(self.frame, orient="vertical")
        self.hsb = ttk.Scrollbar(self.frame, orient="horizontal")

        columns = self.all_words
        self.tree = ttk.Treeview(
            self.frame,
            columns=columns,
            show="tree headings",
            yscrollcommand=self.vsb.set,
            xscrollcommand=self.hsb.set
        )

        self.vsb.config(command=self.tree.yview)
        self.hsb.config(command=self.tree.xview)

        
        self.tree.bind("<Button-1>", lambda e: "break" if self.tree.identify_region(e.x, e.y) == "separator" else None)

        self.tree.heading('#0', text='User')
        self.tree.column('#0', width=250, stretch=False)

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100, stretch=False)

        self.item_to_record = {}

        for user_id, counter in self.bow.items():
            row = [counter.get(word, 0) for word in self.all_words]
            item_id = self.tree.insert("", tk.END, text=user_id, values=row)
            record = next(r for r in self.data_list if r.get('user_id') == user_id)
            self.item_to_record[item_id] = record
        
    def _layout_widgets(self):
        self.frame.pack(expand=True, fill="both")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ew")

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.vsb.grid_remove()
        self.hsb.grid_remove()
    
    def _bind_events(self):
        def update_scrollbars(event=None):
            if self.tree.yview() != (0.0, 1.0):
                self.vsb.grid()
            else:
                self.vsb.grid_remove()

            if self.tree.xview() != (0.0, 1.0):
                self.hsb.grid()
            else:
                self.hsb.grid_remove()

        self.tree.bind("<Configure>", update_scrollbars)
        self.tree.bind("<Motion>", update_scrollbars)

        self.tree.bind("<Double-1>", partial(self._on_double_click, self.tree, self.item_to_record))

    def _on_double_click(self, tree, item_to_record, event):
        selected_item = tree.focus()
        if selected_item:
            record = item_to_record.get(selected_item)
            if record:
                if BowScreen._subwindow is None or not BowScreen._subwindow.winfo_exists():
                    BowScreen._subwindow = LabelerScreen(record, parent=self)
                else:
                    BowScreen._subwindow.lift()