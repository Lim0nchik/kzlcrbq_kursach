import functools
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import layout
import data
import plot
import config
import typing


class App(tk.Frame):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        self.icons = {
            k: tk.PhotoImage(file=v) for k, v in config.paths_icons.items()
        }
        self.init_toolbar(self.icons).pack(anchor='n')

        self.tree = self.init_tree(root)

        self.dataset = data.join_from_csv()
        for row in self.dataset.itertuples(index=False):
            self.tree.insert('', tk.END, values=App.dataset_row_slice(row))

    def init_toolbar(self, icons: dict) -> tk.Frame:
        toolbar = tk.Frame(bg=config.color_bg, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        button_params = [
            'text',
            'command',
            'image'
        ]

        buttons = [
            ('Добавить', self.on_add_record, icons['add']),
            ('Удалить', self.delete_record, icons['delete']),
            ('Изменить', self.on_edit_record, icons['edit']),
            ('Сохранить', self.dataset_save, icons['save']),
            ('Графики', self.activity_graph_selector, icons['plot_view']),
            ('Поиск', lambda: print('Not implemented'), icons['search'])
        ]

        for btn in buttons:
            tk.Button(
                toolbar,
                bg=config.color_bg,
                bd=0,
                compound=tk.TOP,
                **dict(zip(button_params, btn))
            ).pack(side=tk.LEFT)

        return toolbar

    @staticmethod
    def dataset_row_slice(row) -> typing.Tuple:
        return row[0:4] + row[6:]

    def init_tree(self, root: tk.Tk) -> ttk.Treeview:
        tree = ttk.Treeview(root, height=30, show='headings')

        columns = {
            'actor_name': (200, 'Актёр'),
            'actor_year_of_birth': (200, 'Год рождение'),
            'actor_country': (175, 'Страна'),
            'actor_played_movies': (200, 'Количество фильмов'),
            'movie_name': (175, 'Самый популярный фильм'),
            'movie_score': (175, 'Оценка фильма')
        }

        tree['columns'] = list(columns.keys())
        for col, values in columns.items():
            tree.column(col, width=values[0], anchor=tk.CENTER)
            tree.heading(col, text=values[1])

        tree.bind('<Double-Button-1>', lambda event: self.on_edit_record)

        tree.pack()
        return tree

    def dataset_save(self) -> None:
        data.save_to_csv(self.dataset)

    def activity_record_edit(self, callback: typing.Callable) -> None:
        popup = tk.Toplevel()
        popup.title('Параметры актёра')
        popup.geometry('520x280+400+300')
        popup.resizable(False, False)

        def make_label(params: dict) -> None:
            label = tk.Label(popup, text=params['text'])
            label.place(x=params['x'], y=params['y'])

        def make_entry(params: dict) -> tk.Entry:
            entry = tk.Entry(popup)
            entry.place(x=params['x'], y=params['y'])
            return entry

        labels = {
            k: make_label(v[0]) for k, v in layout.activity_record_edit.items()
        }
        entries = {
            k: make_entry(v[1]) for k, v in layout.activity_record_edit.items()
        }

        row = self.tree.item(self.tree.focus())['values']
        for key, value in zip(self.tree['columns'], row):
            entries[key].insert(0, value)

        def on_cancel():
            popup.destroy()
            callback(None)

        def on_ok():
            values = {k: v.get() for k, v in entries.items()}
            popup.destroy()
            callback(values)

        btn_cancel = ttk.Button(popup, text='Отмена', command=on_cancel)
        btn_cancel.place(x=300, y=240)

        btn_ok = ttk.Button(popup, text='ОК', command=on_ok)
        btn_ok.place(x=220, y=240)

        popup.grab_set()
        popup.focus_set()

    def on_add_record(self):
        self.activity_record_edit(lambda values: self.add_record(values))

    def on_edit_record(self):
        self.activity_record_edit(lambda values: self.edit_record(values))

    def add_record(self, entries: dict) -> None:
        actor = self.dataset[self.dataset.actor_name == entries['actor_name']]
        movie = self.dataset[self.dataset.movie_name == entries['movie_name']]
        if actor.size == movie.size == 0:
            self.dataset = data.insert_record(self.dataset, entries)
            self.tree.insert("", tk.END, values=tuple(entries.values()))
        messagebox.showinfo(title='Успешно', message='Successful!!')

    def edit_record(self, entries: dict) -> None:
        actor = self.dataset[self.dataset.actor_name == entries['actor_name']]
        movie = self.dataset[self.dataset.movie_name == entries['movie_name']]
        if actor.size == 0:
            messagebox.showerror(title='Ошибка', message='Актёр не найден')
        elif movie.size == 0:
            messagebox.showerror(title='Ошибка', message='Фильм не найден')
        else:
            data.edit_record(
                self.dataset,
                list(entries.values())[:4] + [actor.iloc[0]['actor_best_movie_id']],
                list(entries.values())[4:] + [movie.iloc[0]['movie_id']]
            )
            self.tree.item(self.tree.focus(), values=tuple(entries.values()))
            messagebox.showinfo(title='Успешно', message='Successful!!')

    def delete_record(self):
        item = self.tree.focus()
        data.delete_record(self.dataset, self.tree.item(item)['values'][0])
        self.tree.delete(item)

    def activity_graph_selector(self) -> None:
        popup = tk.Toplevel()
        popup.title('Выбор графика')
        popup.geometry('50x50')

        def make_on_click(fn):
            return lambda: plot.draw_plot(*fn(self.dataset))

        button_params = [
            'text',
            'command'
        ]

        buttons = [
            (
                'Категоризированная диаграмма рассеивания',
                make_on_click(plot.plot_scatter)
            ),
            (
                'Кластеризованная столбчатая диаграмма',
                make_on_click(plot.plot_bar)
            )
        ]

        for btn in buttons:
            tk.Button(
                popup,
                **dict(zip(button_params, btn))
            ).pack()


def main():
    root_window = tk.Tk()
    app = App(root_window)
    app.pack()
    root_window.title("Актёры")
    root_window.geometry("1125x550+300+150")
    root_window.resizable(False, False)
    root_window.mainloop()


if __name__ == "__main__":
    main()
