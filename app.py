import functools
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
            self.tree.insert('', tk.END, values=row)

    def init_toolbar(self, icons: dict) -> tk.Frame:
        toolbar = tk.Frame(bg=config.color_bg, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        button_params = [
            'text',
            'command',
            'image'
        ]

        buttons = [
            ('Добавить', self.add_item, icons['add']),
            ('Удалить', self.delete_item, icons['delete']),
            ('Изменить', self.change_actor, icons['edit']),
            ('Сохранить', self.save, icons['save']),
            ('Графики', self.activity_graph_selector, icons['plot_view']),
            ('Поиск', lambda: print('Not implemented'), icons['search'])
        ]

        for btn in buttons:
            print(dict(zip(button_params, btn)))
            tk.Button(
                toolbar,
                bg=config.color_bg,
                bd=0,
                compound=tk.TOP,
                **dict(zip(button_params, btn))
            ).pack(side=tk.LEFT)

        return toolbar

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

        tree.bind('<Double-Button-1>', lambda event: self.change_actor())

        tree.pack()
        return tree

    def save(self) -> None:
        data.save_to_csv(self.dataset)

    def change_actor(self):
        top = tk.Toplevel()
        top.title('Изменить/добавить актёра')
        top.geometry('520x280+400+300')
        top.resizable(False, False)

        label_name = tk.Label(top, text='Имя:')
        label_name.place(x=50, y=50)
        entry_name = ttk.Entry(top)
        entry_name.place(x=200, y=50)

        label_year = tk.Label(top, text='Год рождения:')
        label_year.place(x=50, y=80)
        entry_year = ttk.Entry(top)
        entry_year.place(x=200, y=80)

        label_country = tk.Label(top, text='Страна:')
        label_country.place(x=50, y=110)
        entry_country = ttk.Entry(top)
        entry_country.place(x=200, y=110)

        label_films = tk.Label(top, text='Число фильмов:')
        label_films.place(x=50, y=140)
        entry_films = ttk.Entry(top)
        entry_films.place(x=200, y=140)

        label_best_film = tk.Label(top, text='Самый популярный фильм:')
        label_best_film.place(x=50, y=170)
        entry_best_film = ttk.Entry(top)
        entry_best_film.place(x=200, y=170)

        label_best_score = tk.Label(top, text='Оценка самого популярного фильма:')
        label_best_score.place(x=50, y=200)
        entry_best_score = ttk.Entry(top)
        entry_best_score.place(x=200, y=200)

        self.find(entry_name, entry_year, entry_country, entry_films, entry_best_film, entry_best_score, self.tree)

        btn_cancel = ttk.Button(top, text='Закрыть', command=top.destroy)
        btn_cancel.place(x=300, y=240)

        btn_ok = ttk.Button(top, text='Изменить')
        btn_ok.place(x=220, y=240)
        btn_ok.bind('<Button-1>', lambda event: self.change_item(
            entry_name, entry_year, entry_country,
            entry_films, entry_best_film, entry_best_score, self.tree
        ))
        btn_ok = ttk.Button(top, text='Добавить')
        btn_ok.place(x=140, y=240)
        btn_ok.bind('<Button-1>', lambda event: self.add_item(
            entry_name, entry_year, entry_country,
            entry_films, entry_best_film, entry_best_score
        ))

        top.grab_set()
        top.focus_set()

    def delete_item(self):
        item = self.tree.focus()
        print(item)
        work.delete_record(self.tree.index(item))
        self.tree.delete(item)

    def find(self, entry_name, entry_year, entry_country, entry_films, entry_best_film, entry_best_score, tree):
        values = tree.item(tree.focus())["values"]
        print(values)
        entries_list = [entry_name, entry_year, entry_country, entry_films, entry_best_film, entry_best_score]
        for entry, val in zip(entries_list, values):
            # entry.delete(0, tk.END)
            # print(entry.delete(0, tk.END))
            entry.insert(0, val)
        # print(val)

    def change_item(self, entry_name, entry_year, entry_country, entry_films, entry_best_film, entry_best_score, tree):
        try:

            item = tree.focus()
            index = tree.index(item)
            # values = tree.item(item)["values"]
            # print(values)
            # entries_list = [entry_town, entry_federal, entry_founded, entry_population, entry_area]
            # for entry, val in zip(entries_list, values):
            #     entry.delete(0, tk.END)
            #     entry.insert(0, val)

            print(item)
            print(index)

            actor = invalid.invalid_text(entry_name.get())
            print(actor)
            year = invalid.invalid_int(entry_year.get())
            print(year)
            country = invalid.invalid_text(entry_country.get())
            print(country)
            films = invalid.invalid_int(entry_films.get())
            print(films)
            best_film = invalid.invalid_text(entry_best_film.get())
            print(best_film)
            best_score = invalid.invalid_float(entry_best_score.get())
            print(best_score)

            work.insert_record({
                "Actor": actor,
                "year_of_birth": year,
                "country": country,
                "played_films": films,
                "popular_movie": best_film,
                "movie_score": best_score
            })
            # work.update_record(index, (town, federal, founded, population, area))
            tree.item(item, values=(actor, year, country, films, best_film, best_score))

            messagebox.showinfo(title='Успешно', message='Successful!!')
        except ValueError:
            messagebox.showerror("Invalid input", "Input are not valid string or number")

    def add_item(self, entry_name, entry_year, entry_country, entry_films, entry_best_film, entry_best_score):
        try:
            actor = invalid.invalid_text(entry_name.get())
            print(actor)
            year = invalid.invalid_int(entry_year.get())
            print(year)
            country = invalid.invalid_text(entry_country.get())
            print(country)
            films = invalid.invalid_int(entry_films.get())
            print(films)
            best_film = invalid.invalid_text(entry_best_film.get())
            print(best_film)
            best_score = invalid.invalid_float(entry_best_score.get())
            print(best_score)

            work.insert_record({
                "Actor": actor,
                "year_of_birth": year,
                "country": country,
                "played_films": films,
                "popular_movie": best_film,
                "movie_score": best_score
            })
            self.tree.insert("", tk.END, values=(actor, year, country, films, best_film, best_score))

            messagebox.showinfo(title='Успешно', message='Successful!!')
        except ValueError:
            messagebox.showerror("Invalid input", "Input are not valid string or number")

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
    root_window.geometry("950x550+300+150")
    root_window.resizable(False, False)
    root_window.mainloop()


if __name__ == "__main__":
    main()
