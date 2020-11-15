import tkinter as tk
from tkinter import *
import pickle
import os, glob
import re
from tkinter import messagebox
from PIL import ImageTk, Image

from class_win import class_win


file2 = open(r"D:\work\workDir.txt","r") 
work_dir = file2.read()
file2.close()

### Создание окна
win = tk.Tk()
win.resizable(False, False)
win.title("Кактус")
win.geometry("330x300")
win.iconbitmap(f"D:/work/Graphics/icon.ico")

def scroll_config(event):
    ### ВНУТРЕННЯЯ ФУНКЦИЯ ДЛЯ КАНВАСА
    canvas.configure(scrollregion=canvas.bbox("all"))
 

frame=Frame(win,width=300,height=300)
frame.pack(expand=True, fill=BOTH) 
canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,300,300))
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(width=300,height=300)
canvas.config(yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)


os.chdir(f"{work_dir}/Data")

buttons = []
del_list = []
files = []

def showButtons_menu():

    canvas.delete("all")
    files.clear()
    buttons.clear()
    del_list.clear()
    #print(f"Show buttons menu: {work_dir}")
    button_row = 10
    for file in glob.glob("*.pic"):
        files.append(file)


    files.sort(key=natural_keys)
  
    
    for file in files:
        buttons.append(tk.Button(canvas, width=32,height=2, text=file.rsplit('.',1)[0],activebackground = "#33B5E5", command=lambda class_name=file:class_win(class_name)))
   
    for button in buttons:
        canvas.create_window(10, button_row, anchor="nw", window=button)
        button_row += 42
    canvas.configure(scrollregion=canvas.bbox("all"))
    spawn_buttons_menu(buttons)

def atoi(text):
    return int(text) if text.isdigit() else text
    
def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]



def create_class():
    top = tk.Toplevel()
    top.title("Номер и буква класса")
    top.resizable(False, False)
    top.geometry("250x50")

 

    text_var = tk.StringVar()
    text_entry = tk.Entry(top, width=25, textvariable=text_var)
    text_entry.pack()
    


    btn = tk.Button(top, width=30, text="Принять", command= lambda: class_validate(text_var,top))
    btn.pack()

       
    top.grab_set()
    top.focus_set()
    top.wait_window()

def validate_result(text_var):
    result = re.match(r'\d{1,2} [А-Я]',text_var)
    return result

def class_validate(text_var,top):
    result  = validate_result(text_var.get())
    if result:
        top.destroy()
        with open(f"{work_dir}\Data\{text_var.get()}.pic", 'wb') as f:
            pickle.dump([], f)
        
        for button in buttons:
            button.grid_remove()
        showButtons_menu()
    else:
        text_var = None
        top.destroy()
        messagebox.showinfo("Неверный ввод","Формат ввода: 1 А")
        create_class()

    top.destroy()



def spawn_buttons_menu(buttons):
        ### генерация кнопок удаления
        for button in buttons:
            delete_button = tk.Button(canvas, width=6, text="Удалить")
            delete_button.configure(command=lambda button_name = button["text"]: del_class(button_name))
            del_list.append(delete_button)
            
         
global delete_buttons_visible
delete_buttons_visible  = False

def del_class(class_name):
    ### Функция удаления студента с базы данных
    global delete_buttons_visible
    delete_buttons_visible = True
    show_buttons_menu()
    os.remove(f"{class_name}.pic")
    for button in buttons:
        button.grid_remove()
    showButtons_menu()
    
def unshow_buttons():
    delete_buttons_visible  = True
    show_buttons_menu()
 
def show_buttons_menu():
    global delete_buttons_visible
    if not delete_buttons_visible:
        count = 15
        for button in del_list:
            canvas.create_window(250, count, anchor="nw", window=button)
            count += 42
        delete_buttons_visible = not delete_buttons_visible
    else:
        showButtons_menu()   
        delete_buttons_visible = False

def choose_year(year):
    file2 = open(r"D:\work\workDir.txt","w") 
    global work_dir
    work_dir = "D:/work/year/" + year
    file2.write(work_dir)
    os.chdir(f"{work_dir}/Data")
    file2.close()
    for button in buttons:
        button.grid_remove()
    showButtons_menu()

menubar = tk.Menu(win)
menu = tk.Menu(menubar, tearoff=0)
year = tk.Menu(menubar, tearoff=0)
year.add_command(label="2020",command=lambda: choose_year("2020"))
year.add_command(label="2021",command=lambda: choose_year("2021"))
year.add_command(label="2022",command=lambda: choose_year("2022"))
year.add_command(label="2023",command=lambda: choose_year("2023"))
year.add_command(label="2024",command=lambda: choose_year("2024"))
menu.add_command(label="Открыть")
menu.add_separator()
menu.add_command(label="Добавить класс", command=create_class)
menu.add_command(label="Удалить класс", command=show_buttons_menu)
menu.add_command(label="Отмена удаления", command=unshow_buttons)
menu.add_separator()
menu.add_command(label="Закрыть", command= win.destroy)
menubar.add_cascade(label="Меню", menu=menu)
menubar.add_cascade(label="Год", menu=year)
win.config(menu=menubar)

showButtons_menu()
win.mainloop()