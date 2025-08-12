import tkinter as tk
from tkinter import ttk
from functools import partial
from gui.screens.labeler_screen import LabelerScreen

class BowScreen(tk.Toplevel):
    _subwindow = None

    def __init__(self, data_list, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Bolsa de palabras")
        self.geometry("1200x600")

        self.data_list = data_list
        self.bow = {}
        self.all_words = []
        self.MAX_COLUMNS = 20
        self.current_page = 0
        self.words_per_page = self.MAX_COLUMNS
        
        self._setup_data()
        self._create_widgets()
        self._layout_widgets()
        self._bind_events()

        # Funcion de debugeo de la lista de palabras
        word = set()
        for user in data_list:
            for w in user["bow"]:
                word.add(w)
        
        print(word)
        print(len(word))

    def _get_all_words(self):
        all_words = set()
        for words in self.bow.values():
            all_words.update(words.keys())
        all_words = sorted(all_words)
        return sorted(all_words)

    def _setup_data(self):
        for record in self.data_list:
            user_id = record.get("user_id")
            user_bow = record.get("bow", {})
            self.bow[user_id] = user_bow

        all_words = self._get_all_words()
        start = self.current_page * self.words_per_page
        end = start + self.words_per_page
        self.all_words = all_words[start:end]
        self.total_pages = max(1, (len(self._get_all_words()) + self.words_per_page - 1) // self.words_per_page)

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
        
        # Botones de navegación y etiqueta de página
        self.nav_frame = ttk.Frame(self)
        self.prev_button = ttk.Button(self.nav_frame, text="Anterior", command=self._prev_page)
        self.page_label = ttk.Label(self.nav_frame, text="")
        self.next_button = ttk.Button(self.nav_frame, text="Siguiente", command=self._next_page)
        
    def _layout_widgets(self):
        self.frame.pack(expand=True, fill="both")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ew")

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.vsb.grid_remove()
        self.hsb.grid_remove()

        self.nav_frame.pack(pady=10)
        self.prev_button.pack(side="left", padx=5)
        self.page_label.pack(side="left", padx=5)
        self.next_button.pack(side="left", padx=5)

        self._update_page_label()

    def _next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._refresh_view()

    def _prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._refresh_view()

    def _update_page_label(self):
        self.page_label.config(text=f"Página {self.current_page + 1} de {self.total_pages}")
        # self.prev_button.config(state="normal" if self.current_page > 0 else "disabled")
        # self.next_button.config(state="normal" if self.current_page < self.total_pages - 1 else "disabled")


    def _refresh_view(self):
        self._setup_data()

        # Destruir el treeview viejo
        self.tree.destroy()

        # Crear nuevo Treeview con las nuevas columnas (palabras de la página actual)
        self.tree = ttk.Treeview(
            self.frame,
            columns=self.all_words,
            show="tree headings",
            yscrollcommand=self.vsb.set,
            xscrollcommand=self.hsb.set
        )

        self.tree.heading('#0', text='User')
        self.tree.column('#0', width=250, stretch=False)

        for column in self.all_words:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100, stretch=False)

        self.tree.grid(row=0, column=0, sticky="nsew")

        self.vsb.config(command=self.tree.yview)
        self.hsb.config(command=self.tree.xview)

        self.tree.bind("<Button-1>", lambda e: "break" if self.tree.identify_region(e.x, e.y) == "separator" else None)

        # Volver a agregar las filas
        self.item_to_record.clear()
        for user_id, counter in self.bow.items():
            row = [counter.get(word, 0) for word in self.all_words]
            item_id = self.tree.insert("", tk.END, text=user_id, values=row)
            record = next(r for r in self.data_list if r.get('user_id') == user_id)
            self.item_to_record[item_id] = record

        # Reenlazar eventos
        self._bind_events()

        # Actualizar etiqueta de página
        self._update_page_label()


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