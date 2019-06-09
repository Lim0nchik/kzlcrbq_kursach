import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from Script import config as cg
from Library import work
from Library import invalid

import matplotlib.pyplot as plt


import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.add_img_modify = tk.PhotoImage(file="../Graphics/add2.png")
        self.add_img_cancel = tk.PhotoImage(file="../Graphics/add1.png")
        self.add_img = tk.PhotoImage(file="../Graphics/add.png")
        self.save_img = tk.PhotoImage(file="../Graphics/save.png")
        self.graph_img = tk.PhotoImage(file="../Graphics/graph.png")
        self.search_img = tk.PhotoImage(file="../Graphics/search.png")

        self.set_frame(root).pack(anchor='n')
        self.tree = self.init_main(root)
        self.tree.pack()
        self.fill_on_start()
        # self.find()

    def init_main(self, root):
        tree = ttk.Treeview(root, height=30, show='headings')
        tree['columns'] = ('Actor', 'year_of_birth', 'country', 'played_films', 'popular_movie', 'movie_score')

        tree.column("Actor", width=200, anchor=tk.CENTER)
        tree.column("year_of_birth", width=200, anchor=tk.CENTER)
        tree.column("country", width=175, anchor=tk.CENTER)
        tree.column("played_films", width=200, anchor=tk.CENTER)
        tree.column("popular_movie", width=175, anchor=tk.CENTER)
        tree.column("movie_score", width=175, anchor=tk.CENTER)

        tree.heading("Actor", text='Актёр')
        tree.heading("year_of_birth", text='Год рождение')
        tree.heading("country", text='Страна')
        tree.heading("played_films", text='Число фильмов')
        tree.heading("popular_movie", text='Самый популярный фильм')
        tree.heading("movie_score", text='Оценка самого популярного фильма')

        tree.bind('<Double-Button-1>', lambda event: self.change_actor())

        return tree

    def set_frame(self, root):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_dialog_cancel = tk.Button(toolbar, text='Удалить', command=self.delete_item, bg='#d7d8e0', bd=0,
                                           compound=tk.TOP, image=self.add_img_cancel)

        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', command=self.change_actor, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)

        btn_open_dialog_modify = tk.Button(toolbar, text='Изменить', command=self.change_actor, bg='#d7d8e0', bd=0,
                                           compound=tk.TOP, image=self.add_img_modify)

        btn_open_dialog_save = tk.Button(toolbar, text='Сохранить', bg='#d7d8e0', command=self.save, bd=0,
                                         compound=tk.TOP, image=self.save_img)

        btn_open_dialog_graph = tk.Button(toolbar, text='Графики', bg='#d7d8e0', command=self.graph_selector, bd=0,
                                          compound=tk.TOP, image=self.graph_img)

        btn_open_dialog_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', command=self.graph_selector, bd=0,
                                           compound=tk.TOP, image=self.search_img)

        btn_open_dialog.pack(side=tk.LEFT)

        btn_open_dialog_cancel.pack(side=tk.LEFT)
        btn_open_dialog_modify.pack(side=tk.LEFT)
        btn_open_dialog_save.pack(side=tk.LEFT)
        btn_open_dialog_graph.pack(side=tk.LEFT)
        btn_open_dialog_search.pack(side=tk.LEFT)

        return toolbar

    def save(self):
        work._save_dataframe()

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
        btn_ok.bind('<Button-1>', lambda event: self.change_item(entry_name, entry_year, entry_country,
                                                                 entry_films, entry_best_film, entry_best_score, self.tree))
        btn_ok = ttk.Button(top, text='Добавить')
        btn_ok.place(x=140, y=240)
        btn_ok.bind('<Button-1>', lambda event: self.add_item(entry_name, entry_year, entry_country,
                                                              entry_films, entry_best_film, entry_best_score))

        top.grab_set()
        top.focus_set()

    def fill_on_start(self):
        for row in work.get_records():
            self.tree.insert("", tk.END, values=row)

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

    def graph_selector(self):
        popup = tk.Toplevel()
        popup.title('Выбор типа графика')
        popup.geometry('400x250')
        button_task1 = tk.Button(
            popup,
            text='Кластеризованная столбчатая диаграмма',
            command=lambda: self.graph_task1()
        )
        button_task1.pack()
        button_task2 = tk.Button(
            popup,
            text='Категоризированная гистограмма',
            command=lambda: self.graph_task2()
        )
        button_task2.pack()
        button_task4 = tk.Button(
            popup,
            text='Категоризированная диаграмма рассеивания',
            command=lambda: self.graph_task4()
        )
        button_task4.pack()
        button_not_implemented = tk.Button(
            popup,
            text='Not implemented',
            command=lambda: print('Not implemented')
        )
        button_not_implemented.pack()

    def save_graph(self, graph: plt.Figure):
        filename = tk.filedialog.asksaveasfilename(
            filetypes=[
                ('PDF', '*.pdf'),
                ('PNG', '*.png'),
                ('All files', '*.*')
            ]
        )
        do_continue = True
        if os.path.exists(filename):
            do_continue = tk.messagebox.askokcancel(message='Файл существует, заменить?')
            if not do_continue:
                os.remove(filename)
        if do_continue:
            try:
                graph.savefig(filename)
            except Exception as e:
                tk.messagebox.showerror(message='Exception: {}'.format(e))
            else:
                tk.messagebox.showinfo(message='Plot saved as {}'.format(filename))

    def graph_task4(self):
        graph = tk.Toplevel()
        graph.title('Число фильмов от года рождения')
        graph.geometry('1366x768')
        graph.resizable(False, False)

        f = plt.Figure()
        prev_dx = 0
        for dx in [1970, 9999]:
            data = work.suffer[(prev_dx <= work.suffer['year_of_birth']) & (work.suffer['year_of_birth'] < dx)]
            sub = f.add_subplot(1, 2, dx == 9999 and 2 or 1)
            sub.scatter(
                data['year_of_birth'],
                data['played_films']
            )
            sub.set_ylim(top=500)
            sub.set_yticks(range(0, int(500), int(25)))
            sub.set_yticklabels([])
            sub.yaxis.grid(True)
            prev_dx = dx

        f.get_axes()[0].title.set_text('Рождённые до 1970 г.')
        f.get_axes()[1].title.set_text('Рождённые после 1970 г.')
        f.get_axes()[0].set_yticklabels(range(0, int(500), int(25)))

        canvas = FigureCanvasTkAgg(f, graph)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        save_button = tk.Button(graph, text='Save to file', command=lambda: self.save_graph(f))
        save_button.pack(side='top')

    def graph_task2(self):
        graph = tk.Toplevel()
        graph.title('Число актёров по году рождения с группировкой по лучшему фильму')
        graph.geometry('1366x768')
        graph.resizable(False, False)

        f = plt.Figure()
        films = [
            'Deadpool',
            'The Avengers',
            'The Expendables',
            'Flight Crew'
        ]
        for idx, film in enumerate(films):
            data = work.suffer[work.suffer['popular_movie'] == film]
            sub = f.add_subplot(1, len(films), idx + 1)
            sub.hist(
                data['year_of_birth']
            )
            sub.title.set_text(film)
            sub.set_yticks(range(5))
        # f.get_axes()[0].set_yticklabels(range(0, int(1.3e7), int(5e5)))

        canvas = FigureCanvasTkAgg(f, graph)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        save_button = tk.Button(graph, text='Save to file', command=lambda: self.save_graph(f))
        save_button.pack(side='top')

    def graph_task1(self):
        graph = tk.Toplevel()
        graph.title('Число фильмов с группировкой по году рождения')
        graph.geometry('1366x768')
        graph.resizable(False, False)

        f = plt.Figure()
        sub = f.add_subplot(1, 1, 1)
        prev_dx = 0
        add = {
            1970: 0.05,
            9999: 0.35
        }
        xticks = [], []
        for dx in [1970, 9999]:
            data = work.suffer[(prev_dx <= work.suffer['year_of_birth']) & (work.suffer['year_of_birth'] < dx)]\
                .sort_values('played_films', ascending=False)
            sub.bar(
                [x + add[dx] for x in range(data.index.size)],
                data['played_films'],
                width=0.2,
                label='Рождённые {} 1970 г.'.format(dx == 1970 and 'до' or 'после')
            )
            xticks[0].extend([x + add[dx] for x in range(data.index.size)])
            xticks[1].extend(data['Actor'])
            sub.set_ylim(top=500)
            sub.set_yticks(range(0, int(500), int(25)))
            sub.yaxis.grid(True)
            prev_dx = dx
        sub.set_xticks(xticks[0])
        sub.set_xticklabels(xticks[1], rotation='vertical')
        sub.legend(loc='upper right')
        f.subplots_adjust(bottom=0.2)
        canvas = FigureCanvasTkAgg(f, graph)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        save_button = tk.Button(graph, text='Save to file', command=lambda: self.save_graph(f))
        save_button.pack(side='top')


def main():
    work.load_dataframe(cg.db_plays_path, cg.db_plays_path1)


if __name__ == "__main__":
    main()
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Города России")
    root.geometry("950x550+300+150")
    root.resizable(False, False)
    root.mainloop()
