import os
import typing
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox

mpl.use("TkAgg")


def save_plot(plot: plt.Figure) -> None:
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
            plot.savefig(filename)
        except Exception as e:
            tk.messagebox.showerror(message='Ошибка: {}'.format(e))
        else:
            tk.messagebox.showinfo(message='Файл сохранён как {}'.format(filename))


def draw_plot(figure: plt.Figure, title: str) -> None:
    frame = tk.Toplevel()
    frame.geometry('1366x768')
    frame.resizable(False, False)
    frame.title(title)

    canvas = FigureCanvasTkAgg(figure, frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    tk.Button(
        frame,
        text='Сохранить как',
        command=lambda: save_plot(figure)
    ).pack(side='top')


def plot_scatter(df: pd.DataFrame) -> typing.Tuple[plt.Figure, str]:
    fig = plt.Figure()
    geometry = (1, 2)

    def draw_subplot(data: pd.DataFrame, idx: int, title: str) -> plt.Subplot:
        sub = fig.add_subplot(*geometry, idx)
        sub.scatter(data['actor_year_of_birth'], data['actor_played_movies'])
        sub.set_ylim(top=500)
        sub.set_yticks(range(0, int(500), int(25)))
        sub.set_yticklabels([])
        sub.yaxis.grid(True)
        sub.title.set_text(title)
        return sub
    
    sub_1 = draw_subplot(
        df[df.actor_year_of_birth < 1970],
        1,
        'Рождённые до 1970 г.'
    )
    draw_subplot(
        df[df.actor_year_of_birth >= 1970],
        2,
        'Рождённые после 1970 г.'
    )
    sub_1.set_yticklabels(range(0, int(500), int(25)))

    return fig, 'Число фильмов / год рождения'


def plot_bar(df: pd.DataFrame) -> typing.Tuple[plt.Figure, str]:
    fig = plt.Figure()
    sub = fig.add_subplot(1, 1, 1)
    add = {
        1: 0.05,
        2: 0.35
    }
    xticks = [], []

    def draw_subplot(data: pd.DataFrame, idx: int, label: str) -> None:
        sub.bar(
            [x + add[idx] for x in range(data.index.size)],
            data['actor_played_movies'],
            width=0.2,
            label=label
        )
        xticks[0].extend([x + add[idx] for x in range(data.index.size)])
        xticks[1].extend(data['actor_name'])
        sub.set_ylim(top=500)
        sub.set_yticks(range(0, int(500), int(25)))
        sub.yaxis.grid(True)
    
    draw_subplot(
        df[df.actor_year_of_birth < 1970],
        1,
        'Рождённые до 1970 г.'
    )
    draw_subplot(
        df[df.actor_year_of_birth >= 1970],
        2,
        'Рождённые после 1970 г.'
    )
    sub.set_xticks(xticks[0])
    sub.set_xticklabels(xticks[1], rotation='vertical')
    sub.legend(loc='upper right')
    fig.subplots_adjust(bottom=0.2)

    return fig, 'Число с группировкой по году рождения'
