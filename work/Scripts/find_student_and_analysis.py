import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import time
from PIL import Image, ImageDraw

def analysis_finding_win():
    ### Окно поиска студента по имени
    top = tk.Toplevel()
    top.title("Анализ факультатива ученика")
    top.resizable(False, False)
    top.geometry("250x50")

    text_var = tk.StringVar()
    text_entry = tk.Entry(top, width=25, textvariable=text_var)
    text_entry.pack()
    
    
    btn = tk.Button(top, width=30, text="Начать анализ", command= lambda: top.destroy())
    btn.pack()

    top.grab_set()
    top.focus_set()
    top.wait_window()
    
    return text_var.get()

def analysis_subject_win():
    ### Окно поиска студента по имени
    top = tk.Toplevel()
    top.title("Анализ средней оценки по предмету")
    top.resizable(False, False)
    top.geometry("250x50")
    options = ["Математика","Физика","История","Русский","Английский","Информатика","Литература"]
    

    text_var = tk.StringVar()
    text_entry = ttk.Combobox(top, width=25,value = options, textvariable=text_var)
    text_entry.pack()
    
    
    btn = tk.Button(top, width=30, text="Начать анализ", command= lambda: top.destroy())
    btn.pack()

    top.grab_set()
    top.focus_set()
    top.wait_window()
    
    return text_var.get()

def analisys_graph(total_csharp, total_history):
    data = [total_csharp, total_history]

    root = tk.Toplevel()
    root.title("Процент факультатива")
    white = (255, 255, 255)

    bar_width = 400 
    bar_height = 200
    bar = tk.Canvas(root, width=bar_width, height=bar_height, bg='white')
    bar.pack()

    image1 = Image.new("RGB", (bar_width, bar_height), white)
    draw = ImageDraw.Draw(image1)

    y_stretch = 15  
    y_gap = 20  
    x_stretch = 150  
    x_width = 20  
    x_gap = 100  

    for x, y in enumerate(data):


        x0 = x * x_stretch + x * x_width + x_gap

        y0 = bar_height - (y * y_stretch + y_gap)

        x1 = x * x_stretch + x * x_width + x_width + x_gap

        y1 = bar_height - y_gap

        bar.create_rectangle(x0, y0, x1, y1, fill="red")
        draw.rectangle([(x0, y0), (x1, y1)], fill="red")
        bar.create_text(x0 + 2, y0, anchor=tk.SW, text=str(y*10))
        draw.text((x0,y0-10),fill="black",anchor=tk.SW,text=str(y*10))

    messagebox.showinfo("Факультатив","Левый процент отвечает за факультатив basics of C# второй - history of England")
    time_now = time.strftime("%Y%m%d-%H%M%S")
    name  = f"D:/work/Graphics/{time_now}_optional_subject.jpg"
    image1.save(name)
    messagebox.showinfo("Анализ", "Анализ сохранен в папке Graphics")
    root.mainloop() 

def analisys_subject_graph(subject_array):
    data = subject_array
    

    root = tk.Toplevel()
    root.title("Оценки студентов")

    bar_width = len(data) * 70 +50
    bar_height = 200
    bar = tk.Canvas(root, width=bar_width, height=bar_height, bg='white')
    bar.pack()
    white = (255, 255, 255)

    image1 = Image.new("RGB", (bar_width, bar_height), white)
    draw = ImageDraw.Draw(image1)

    y_stretch = 15  
    y_gap = 20  
    x_stretch = 50  
    x_width = 20  
    x_gap = 50  
    
    for x, y in enumerate(data):


        x0 = x * x_stretch + x * x_width + x_gap

        y0 = bar_height - (y * y_stretch + y_gap)

        x1 = x * x_stretch + x * x_width + x_width + x_gap

        y1 = bar_height - y_gap

        bar.create_rectangle(x0, y0, x1, y1, fill="red")
        draw.rectangle([(x0, y0), (x1, y1)], fill="red")
        bar.create_text(x0 + 2, y0, anchor=tk.SW, text=str(y))
        draw.text((x0+2,y0-10),fill="black",anchor=tk.SW,text=str(y))
 
    time_now = time.strftime("%Y%m%d-%H%M%S")
    name  = f"D:/work/Graphics/{time_now}_mark.jpg"
    image1.save(name)
    messagebox.showinfo("Анализ", "Анализ сохранен в папке Graphics")
    root.mainloop() 