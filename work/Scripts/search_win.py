import tkinter as tk

def search_win():
    ### Окно поиска студента по имени
    top = tk.Toplevel()
    top.title("Найти ученика")
    top.resizable(False, False)
    top.geometry("250x50")

    text_var = tk.StringVar()
    text_entry = tk.Entry(top, width=25, textvariable=text_var)
    text_entry.pack()
    
    
    btn = tk.Button(top, width=30, text="Найти", command= lambda: top.destroy())
    btn.pack()

    top.grab_set()
    top.focus_set()
    top.wait_window()
    
    return text_var.get()

