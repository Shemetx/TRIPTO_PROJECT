import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pathlib
import time
import os


def stats_win(array, db_dir):
    ### Окно статистики, которая идет в папку Output
    if array == []:
        messagebox.showinfo("Статистика", "База данных пуста")
    else:
        top = tk.Toplevel()
        top.title("Статистика")
        top.resizable(False, False)
        top.geometry("350x270")

        mark_above = req_int_win()
        
        # Среднее оценки по предметам
        
        list_of_average = {}
        
        count = 0
        math_avr = 0
        phy_avr = 0
        his_avr = 0
        rus_avr = 0
        eng_avr = 0
        cs_avr = 0
        lit_avr = 0
        for data in array:
            math_avr += int(data["marks"]["math"].get())
            phy_avr += int(data["marks"]["physics"].get())
            his_avr += int(data["marks"]["history"].get())
            rus_avr += int(data["marks"]["russian"].get())
            eng_avr += int(data["marks"]["english"].get())
            cs_avr += int(data["marks"]["computer_science"].get())
            lit_avr += int(data["marks"]["literature"].get())
            
            max_value = (int(data["marks"]["math"].get()) + 
                        int(data["marks"]["physics"].get()) + 
                        int(data["marks"]["history"].get()) + 
                        int(data["marks"]["russian"].get()) + 
                        int(data["marks"]["english"].get()) + 
                        int(data["marks"]["computer_science"].get()) + 
                        int(data["marks"]["literature"].get()))/7
            max_flname = data["flname"].get()
            new_index = {f"{max_flname}" : max_value}
            list_of_average.update(new_index)
            count += 1

        best_student = max(list_of_average, key=list_of_average.get)

        students_above_count = 0
        for student in list_of_average:
            if float(mark_above) < float(list_of_average[student]):
                students_above_count += 1   
        
        math_avr = float(math_avr/count)
        phy_avr = float(phy_avr/count)
        his_avr = float(his_avr/count)
        rus_avr = float(rus_avr/count)
        eng_avr = float(eng_avr/count)
        cs_avr = float(cs_avr/count)
        lit_avr = float(lit_avr/count)

        class_avr = float(math_avr + phy_avr + his_avr + rus_avr + eng_avr + cs_avr + lit_avr)/7

        text_list = [
                    f'Количество учеников: {len(array)}',
                    f'Средняя оценка по Математике: {"{:.2f}".format(math_avr)}',
                    f'Средняя оценка по Физике: {"{:.2f}".format(phy_avr)}',
                    f'Средняя оценка по Истории: {"{:.2f}".format(his_avr)}',
                    f'Средняя оценка по Русскому: {"{:.2f}".format(rus_avr)}',
                    f'Средняя оценка по Английскому: {"{:.2f}".format(eng_avr)}',
                    f'Средняя оценка по Информатике: {"{:.2f}".format(cs_avr)}',
                    f'Средняя оценка по Литературе: {"{:.2f}".format(lit_avr)}',
                    f'Средняя оценка класса: {"{:.2f}".format(class_avr)}',
                    f'Лучший ученик: {best_student}, с оценкой: {"{:.2f}".format(list_of_average.get(best_student))}',
                    f'Количество студентов: {students_above_count}, средняя оценка которых выше: {mark_above}'
                    ]
        i = 0
        for text in text_list:
            tk.Label(top,text=text).grid(row=i, column=0, sticky="w")
            i += 1            


        
        
        # work_dir = pathlib.Path(__file__).parent.parent
        work_dir = "D:/work"
        def save_file():
            dir = filedialog.askdirectory(initialdir = f"{work_dir}/Output/", title="Сохранить статистику в...")
            time_now = time.strftime("%Y%m%d-%H%M%S")
            db_name = pathlib.Path(db_dir).stem
            
            with open(f"{dir}/{time_now}_{db_name}_log.txt", 'w', encoding="utf-8") as f:
                for text in text_list:
                    f.write(text+"\n")
                

        tk.Button(top, text="Сохранить статистику", command=save_file).grid(row=12, column=0)
        messagebox.showinfo("Статистика", "Статистика сохранена в папке Output")
    

        top.grab_set()
        top.focus_set()
        top.wait_window()

def req_int_win():
    ### Окно поиска студента по имени
    top = tk.Toplevel()
    top.title("Средняя оценка")
    top.resizable(False, False)
    top.geometry("250x50")

    text_var = tk.IntVar()
    text_entry = tk.Entry(top, width=25, textvariable=text_var)
    text_entry.pack()
    
    
    btn = tk.Button(top, width=30, text="Принять", command= lambda: top.destroy())
    btn.pack()

    top.grab_set()
    top.focus_set()
    top.wait_window()
    
    return text_var.get()