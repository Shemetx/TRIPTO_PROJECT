import tkinter as tk

def info_win():
    ### Окно "О приложении"
    top = tk.Toplevel()
    top.title("О Приложении")
    top.resizable(False, False)
    top.geometry("250x50")

    tk.Label(top,text="Разработчик: ").grid(row=0, column=0)
    tk.Label(top,text="Юрчик Влад").grid(row=1, column=1)


    top.grab_set()
    top.focus_set()
    top.wait_window()
    