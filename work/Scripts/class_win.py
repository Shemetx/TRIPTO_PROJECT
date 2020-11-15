import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import pickle
from search_win import search_win
from stats_win import stats_win
from info_win import info_win
import time
from find_student_and_analysis import analysis_finding_win
from find_student_and_analysis import analisys_graph
from find_student_and_analysis import analysis_subject_win
from find_student_and_analysis import analisys_subject_graph
import configparser



def class_win(class_name):

    global work_dir
    file2 = open(r"D:\work\workDir.txt","r") 
    work_dir = file2.read()
    file2.close()

    global db_dir
    db_dir = f"{work_dir}/Data/"
    ### Создание окна
    classwin = tk.Toplevel()
    classwin.resizable(False, False)
    classwin.title("Кактус")
    classwin.geometry("870x400")
    classwin.iconbitmap(f"D:/work/Graphics/icon.ico")





    ### Заготовочка
    # students = [
    #     {
    #         "flname": "Александр Пастухов",
    #         "marks": {
    #             "math": 5, 
    #             "physics": 8, 
    #             "history": 5, 
    #             "russian": 3,
    #             "english": 9,
    #             "computer_science": 10,
    #             "literature": 6
    #             }
    #     }]
    optional_subject = {
        "basics_of_csharp": { ###6.5 сделать максимум 10
            "math": 0.300, 
            "physics": 0.150, 
            "history": 0.000, 
            "russian": 0.000,
            "english": 0.050,
            "computer_science": 0.500,
            "literature": 0.000
            },
            
        "history_of_england": { ###4
            "math": 0.000, 
            "physics": 0.000, 
            "history": 0.500, 
            "russian": 0.050,
            "english": 0.300,
            "computer_science": 0.000,
            "literature": 0.150
            }
    }
        

    def scroll_config(event):
        ### ВНУТРЕННЯЯ ФУНКЦИЯ ДЛЯ КАНВАСА
        canvas.configure(scrollregion=canvas.bbox("all"))



    ### Создание канваса для показа и редактирования базы данных
    canvas = tk.Canvas(classwin,bd=0)
    canvas_frame = tk.Frame(canvas)
    #Создание скроллбара, настроенного на прокрутку canvas
    myscrollbar = tk.Scrollbar(classwin,orient="vertical",command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)
    myscrollbar.pack(side="right",fill="y")
    canvas.pack(side="bottom",expand=tk.YES, fill=tk.BOTH)
    canvas.create_window((0,0),window=canvas_frame,anchor="nw")
    canvas_frame.bind("<Configure>",scroll_config)

    """
    Создание массива table_data и btn_list для того чтобы сохранять в нем будущие виджеты
        (это нужно для того чтобы можно было к ним обращаться)
            (а обращаться к ним надо для того чтобы брать из них данные и использовать их для работы с отображением и перезаписи ДБ)  
    """
    table_data = []
    btn_list = []

    global i
    i = 0  
    def show_db(array):
        ### Функция, которая совмещает в себе функции для генерации виджетов для каждого студента
        global i
        for student in array:
            spawn_entry(student)
            spawn_buttons()
            i += 1
    def spawn_entry(student):
        ### Функция, которая отвечает за генерацию ентри, с помощью которых пользователь видит и редактирует базу данных
                global i
                global fl_entry
                global math_entry
                global phy_entry
                global his_entry
                global rus_entry
                global eng_entry
                global cs_entry
                global lit_entry
                ### Тут создаются Entry для имени ученика и предметов
                
                fl_entry = tk.Entry(canvas_frame, width=30)
                fl_entry.grid(row=i+2, column=0)
                fl_entry.insert(0,student["flname"])

                math_entry = tk.Entry(canvas_frame, width=5)
                math_entry.grid(row=i+2, column=1)
                math_entry.insert(0,student["marks"]["math"])

                phy_entry = tk.Entry(canvas_frame, width=5)
                phy_entry.grid(row=i+2, column=2)
                phy_entry.insert(0,student["marks"]["physics"])

                his_entry = tk.Entry(canvas_frame, width=5)
                his_entry.grid(row=i+2, column=3)
                his_entry.insert(0,student["marks"]["history"])

                rus_entry = tk.Entry(canvas_frame, width=5)
                rus_entry.grid(row=i+2, column=4)
                rus_entry.insert(0,student["marks"]["russian"])
            
                eng_entry = tk.Entry(canvas_frame, width=5)
                eng_entry.grid(row=i+2, column=5)
                eng_entry.insert(0,student["marks"]["english"])
    
                cs_entry = tk.Entry(canvas_frame, width=5)
                cs_entry.grid(row=i+2, column=6)
                cs_entry.insert(0,student["marks"]["computer_science"])
    
                lit_entry = tk.Entry(canvas_frame, width=5)
                lit_entry.grid(row=i+2, column=7)
                lit_entry.insert(0,student["marks"]["literature"])
                """
                А вот тут-то вся фишка массива с Entry(которая используется не один раз)
                    В него записывается та же структура, только вместо нормального значения, используется объект Entry
                        чтобы можно было использовать функцию get() и взять с него данные
                """
                table_data.append({
                    "flname": fl_entry,
                    "marks": {
                        "math": math_entry, 
                        "physics": phy_entry, 
                        "history": his_entry, 
                        "russian": rus_entry,
                        "english": eng_entry,
                        "computer_science": cs_entry,
                        "literature": lit_entry
                        }
                    }) 
                

    def on_entry_click(event, entry):
        ### Внутренняя функция бинда нажания на ентри
        entry.config(highlightbackground=None, highlightthickness = 0)
        entry.unbind("<1>")

    def spawn_buttons():
        ### генерация кнопок удаления
        global i
        d_btn = tk.Button(canvas_frame, width=6, text="Удалить")
        d_btn.configure(command=lambda student=table_data[i]: del_student(student))
        btn_list.append(d_btn)
        

    def save_db():
        ### Сейв функция
        #print(db_dir)
        with open(f"{db_dir}{class_name}", 'wb') as f:
            ### Открываем файл в режим записи
            new_data=[]
            new_data = transform_into_readable(table_data)
            pickle.dump(new_data, f)


    def refresh_DB(array):
        ### Функция обновляет отображение базы данных
        global i
        ### Удаляются виджеты перед загрузкой базы данных
        for student in table_data:
            student["flname"].destroy()
            for mark in student["marks"].values():
                mark.destroy()

        for button in btn_list:
            button.destroy()

        ### Обнуление всего перед загрузкой базой данных
        i = 0
        btn_list.clear()
        table_data.clear()
        
        ### Отображаем базу данных
        
        show_db(array)
        


    def open_dic():
        ### Открытие файла .pic
        try:
            global db_dir 
            
            classwin.filename = filedialog.askopenfilename(initialdir = f"{work_dir}/Data/", title="Выберите файл", filetypes=[("pic files","*.pic")])
            db_dir = classwin.filename
            
            with open(db_dir, 'rb') as f:
            ### Читаю pic файл (загружаю ДАТАБАЗУ в ОПЕРАТИВНУЮ ПАМЯТЬ 😎)
                students = pickle.load(f)
                refresh_DB(students)
        except:
            pass

    def addStudent():
        ### Функция создания и добавления нового студента
        global i
        emptyTemplate = {
                    "flname": "",
                    "marks": {
                        "math": 0, 
                        "physics": 0, 
                        "history": 0,
                        "russian": 0,
                        "english": 0,
                        "computer_science": 0,
                        "literature": 0}
                        }
        spawn_entry(emptyTemplate)
        spawn_buttons()
        i += 1


    global are_buttons_visible
    are_buttons_visible  = False

    def del_student(student):
        ### Функция удаления студента с базы данных
        global are_buttons_visible
        student["flname"].destroy()
        for mark in student["marks"].values():
            mark.destroy()
        table_data.remove(student)

        temp = transform_into_readable(table_data)
        refresh_DB(temp)
    
        are_buttons_visible = False


    def show_buttons():
        ### Функция отображения кнопок удаления студента с базы
        global are_buttons_visible
        if not are_buttons_visible:
            count = 0
            for button in btn_list:
                button.grid(row=count+2, column=8)
                count += 1
            are_buttons_visible = not are_buttons_visible
        else:
            for button in btn_list:
                button.grid_remove()
            are_buttons_visible = False

    def find_student():
        ### Функция поиска студента
        text = search_win().lower()
        if text == "":
            pass
        else:
            found = None
            count = 0
            for student in table_data:
                if text == student["flname"].get().lower():
                    found = True
                    count += 1
                    student["flname"].bind("<1>", func=lambda event, entry=student["flname"]: on_entry_click(event, entry))
                    student["flname"].config(highlightbackground="red", highlightthickness = 7)
            if found:
                messagebox.showinfo("Поиск", f"Учеников найдено: {count}")
            else: 
                messagebox.showinfo("Поиск", "Ученик не найден")

    def transform_into_readable(array):
        ### Внутренняя функция, для конвертации данных со словаря с Entry в читаемый формат(который мы используем и при создании рабочего словаря с Entry, и при сохранении)
        new_data = []
        for data in array:
            new_data.append({
                "flname": data["flname"].get(),
                "marks": {
                    "math": data["marks"]["math"].get(), 
                    "physics": data["marks"]["physics"].get(), 
                    "history": data["marks"]["history"].get(),
                    "russian": data["marks"]["russian"].get(),
                    "english": data["marks"]["english"].get(),
                    "computer_science": data["marks"]["computer_science"].get(),
                    "literature": data["marks"]["literature"].get()}
            })
        return new_data

    def analysis_of_subject():
        ### Функция анализа предмета по оценкам
        text = analysis_subject_win().lower()
        if text == "":
            messagebox.showinfo("Анализ","Пустой ввод")
        elif text == "математика":
            graph('math')
        elif text == "физика":
            graph('physics')
        elif text == "история":
            graph('history')
        elif text == "русский":
            graph('russian')
        elif text == "английский":
            graph('english')
        elif text == "информатика":
            graph('computer_science')
        elif text == "литература":
            graph('literature')

    def graph(subject):
        ### Внутреняя функция, функция совмещает две функции и сортирует список
        subj_marks = for_loop_subj(subject)
        temp = sorted(subj_marks)
        analisys_subject_graph(temp)

    def for_loop_subj(subject):
        ### Функция создающая массив из оценок по предмету
        subject_marks = []
        for student in table_data:
            subject_marks.append(int(student["marks"][subject].get()))
        return subject_marks


    def analysis ():
        ### Анализ оценок студента
        global total_csharp
        text = analysis_finding_win().lower()
        if text == "":
            messagebox.showinfo("Анализ","Пустой ввод")
        else:
            student_id = None
            total_csharp = 0
            total_history = 0
            for student in table_data:
                if text == student["flname"].get().lower():
                    student_id = student
            for mark in student_id["marks"]:
                current_csharp = int(student_id["marks"][mark].get()) * float(optional_subject["basics_of_csharp"][mark])
                total_csharp += current_csharp
                current_history = float(optional_subject["history_of_england"][mark]) * int(student_id["marks"][mark].get())
                total_history = current_history + total_history
            analisys_graph(total_csharp, total_history)

        

    global sort_state 
    sort_state = True
    def sort(what):
        ### Функция, сортировки по переменной "what"
        global are_buttons_visible
        global sort_state
        
        reverse = None
        sort_state = not sort_state
        reverse = sort_state
        
        temp = table_data
        if what == "name":
            temp.sort(key=lambda x: x["flname"].get(), reverse=reverse)
        else:
            temp.sort(key=lambda x: int(x["marks"][what].get()), reverse=reverse)
        
        sorted_tableData = transform_into_readable(temp)
        refresh_DB(sorted_tableData)
        are_buttons_visible = False



    ### Кнопочки сортировки ################################################################################################

    sort_name_btn = tk.Button(canvas_frame, width=10, text="Имя/Фамилия", command= lambda: sort("name"))
    sort_name_btn.grid(row=1, column=0)

    sort_math_btn = tk.Button(canvas_frame, width=10, text="Математика", command= lambda: sort("math"))
    sort_math_btn.grid(row=1, column=1)

    sort_phy_btn = tk.Button(canvas_frame, width=10, text="Физика", command= lambda: sort("physics"))
    sort_phy_btn.grid(row=1, column=2)

    sort_his_btn = tk.Button(canvas_frame, width=10, text="История", command= lambda: sort("history"))
    sort_his_btn.grid(row=1, column=3)


    sort_rus_btn = tk.Button(canvas_frame, width=10,text="Русский", command= lambda: sort("russian"))
    sort_rus_btn.grid(row=1, column=4)

    sort_eng_btn = tk.Button(canvas_frame, width=10, text="Английский", command= lambda: sort("english"))
    sort_eng_btn.grid(row=1, column=5)

    sort_cs_btn = tk.Button(canvas_frame, width=10, text="Информатика", command= lambda: sort("computer_science"))
    sort_cs_btn.grid(row=1, column=6)

    sort_lit_btn = tk.Button(canvas_frame, width=10, text="Литература", command= lambda: sort("literature"))
    sort_lit_btn.grid(row=1, column=7)






    ### Меню ########################################################################
    menubar = tk.Menu(classwin)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Открыть", command=open_dic)
    file_menu.add_command(label="Сохранить", command=save_db)
    file_menu.add_separator()
    file_menu.add_command(label="Закрыть", command= classwin.destroy)
    menubar.add_cascade(label="Файл", menu=file_menu)

    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Добавить ученика", command=addStudent)
    edit_menu.add_command(label="Найти учеников", command=find_student)
    edit_menu.add_command(label="Удалить учеников", command=show_buttons)
    edit_menu.add_command(label="Анализ факультатива", command=analysis)
    edit_menu.add_command(label="Анализ оценки", command=analysis_of_subject)
    menubar.add_cascade(label="Редактирование", menu=edit_menu)


    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="Статистика", command=lambda: stats_win(table_data, f"db_dir{class_name}"))
    help_menu.add_command(label="О приложении", command=info_win)
    menubar.add_cascade(label="Помощь", menu=help_menu)

    classwin.config(menu=menubar)
    ################################################################################

    def on_program_start():
        try:
            #print(class_name)
            with open(f"{work_dir}/Data/{class_name}", 'rb') as f:
                ### Функция инициализации .pic файла (загружаю ДАТАБАЗУ в ОПЕРАТИВНУЮ ПАМЯТЬ 😎)
                students = pickle.load(f)
                show_db(students)
                
        except FileNotFoundError:
            open_dic()
            

    def on_program_close():
        classwin.destroy()

    on_program_start()

    classwin.protocol('WM_DELETE_WINDOW', on_program_close)

    classwin.grab_set()
    classwin.focus_set()
    classwin.wait_window()




























#                                                                                      `.inWWx*.                   
#                                                                                   `izW@MxnnnxMn;                 
#                                                                                 `*WWxnnnnnnnnnnxx*`              
#                                                                                :MWnnnznnnnnnnnnnnxxi`            
#                                                                              `#@xnn#***+#+nnnnnnnnnxn,           
#                                                                             ,MWnnnn******+nnnnnnnnnnnx+          
#                                                                            :WMnnnn+*****znnnnnnnnnnnnnnn.        
#                                                                           ;@xnnnz+***+#znnnzznnnnnnnnnnnx,       
#                                                                          :@xnnnnz+*+znnnzzzzzzzznnnnnnnnnx:      
#                                                                         ,WMnnnnnnnMMxxMxnzzzzzzznnnnnnnnnnx,     
#                                                                        `MMnnnnnnnM*,,,,:*nMnzzzzznnnnnnnnnnx.    
#                                                                        zWnnnnnnnM:,,,,,,,,:+Mnzzzznnnnnnnnnnz    
#                                                                       i@nnnnnnnnxxxMMxxz+:,,,zxzzznnnnnnnnnnni   
#                                                                      .Wxnnnnnnnnzz#zz#zznMxi,,*Mzznnnnnnnnnnnx`  
#                                                                      zWnnnnnnnnzzzzzzzzzzzzxn:,iMzznnnnnnnnnnn+  
#                                                                     ;@nnnnnnnnzzzzzzzzzzzzzzzM;,ixznnnnnnnnnnnx` 
#                                                                    `MMnnnnnxMMMnzzzzzzzzzzzzzzM:,#nnnnnnnnnnnnni 
#                                                                    *@nnnnnM#,..ixxzzzzzzzzzzzzzx,,xznnnnnnnnnnn# 
#                                                                   `WxnnnnM:``````iMzzzzzzzzzzzzx*,*xnnnnnnnnnnnx`
#                                                                   +WnnnnM:.`````.`,xzzzzzzzzzzzzx,,Mnnnnnnnnnnnx.
#                                                                  .@xnnnx*.````````.,Mzzzzzzzzzzzx*,xnnnnnnnnnnnx;
#                                                                  #WnnnnM.```..``````*nzzzzzzzzzzzM:xnnnnnnnnnnnn*
#                                                                 ,@nnnnnn````zn`````.,Mzz#zzzzzzzzzxxnnnnnnnnnnnn+
#                                                                 zMnnnnnz````.,``````.MzMxnnxMnzzzzznnnnnnnnnnnnnz
#                                                                ,@nnnnnnz````````````,W#.````.ixnzzznnnnnnnnnnnnnn
#                                                                nMnnnnnnx```````````.*+````````.#xzznnnnnnnnnnnnnz
#                                                               :@nnnnnnzM.``````````.x`````````.`nzznnnnnnnnnnnnnn
#                                                              `MxnnnnnzMn#`.````````#;```````````,Mnnnnnnnnnnnnnnn
#                                                              *Wnnnnnzzxnx+.``````.*W`.```````````xnnnnnnnnnnnnnnz
#                                                             .WxnnnnzzzzM#xn,````.#xn`.````##`````znnnnnnnnnnnnnnn
#                                                             zMnnnxMMMxznxzzMxz#zxnzz`.````z+`````#nnnnnnnnnnnnnnn
#                                                            :@nnnMMzzznMxnMnzzzMnzzzx`.```````````nnnnnnnnnnnnnnn#
#                                                           `MxnnMxzxWWMznMzxxzxxzzzzM,```````````.Mnnnnnnnnnnnnnn+
#                                                           +WnnxMzW@@@@WzzzzzzMzzzzzzn..```````..+xnnnnnnnnnnnnnx;
#                                                          .@xnnWnM@@@@@:xzzzzMzzzzx#zn#`.```````:MnnnnnnnnnnnnnnM.
#                                                          zMnnnWz@@@@@@W@MzzzMzzzMnzzzxz.``````:Mnnnnnnnnnnnnnnnx 
#                                                         :@nnnnWz@@@@@@@#,MzzxznMzzzz#zzM#;..:zMnnnnnnnnnnnnnnnnz 
#                                                        `MxnnnnMz@@@@@@@z:nMzMMxzzzzzxnz#zxMMMnnnnnnnnnnnnnnnnnxi 
#                                                        iWnnnnnWz@@@@@@@@@x;MzzzzzzzzzxxzzzzznnnnnnnnnnnnnnnnnnM, 
#                                                       .WxnnnnnMzW@@@@@@@@;`+MnzzzzzzzznWxnnxWnnnnnnnnnnnnnnnnnM  
#                                                       #Mnnnnnnxnx@@@@@@@@z+W.zM#xMMxzzzznxxnnnnnnnnnnnnnnnnnnn#  
#                                                      ,@nnnnnnnzMz@@@@@@@@@@M:Mn`n#`n@xnzzzzznnnnnnnnnnnnnnnnnM:  
#                                                      nMnnnnnnzzxnM#@@@@@@@@@@@@n@@n@@z@WzzxnnnnnnnnnnnnnnnnnnM`  
#                                                     :@nnnnnnnzzzMzzz@@@@@@@@@@@@@@@@@@@@@nzWnnnnnnnnnnnnnnnnnz   
#                                                    `MxnznnnnnzzznMxMzx@@@@@@@@@@@@@@@@@@@@nMxnnnnnnnnnnnnnnnM;   
#                                                    iWzxMMnnnnzzzznxM:zWM@@@@@@WnnxW@@@@@@@WnMnnnnnnnnnnnnnnnM`   
#                                                   `WnxMMxnnnnzzzzzxxxM,:@@@@@@@WnnnM@@@@@@@nWnnnnnnnnnnnnnnnz    
#                                                   +WzMMMnnnnnzzzzzzxnxz;@*M@@@@@@xnnM@@@@@@nWnnnnnnnnnnnnnnM;    
#                                                  .WnzxMxnnnnnzzzzzzzzzzW#`#@@@@@@@nnn@@@@@@nWnnnnnnnnnnnnnnM     
#                                                  #MnnnMnnnnnzzzzzzzzzzzzx#n+,@@@@@xnn@@@@@WnMnnnnnnnnnnnnnx+     
#                                                 .@nnnnnnnnnnzzzzzzzzzzzzzzM*`@+.@@WnnW@@@@xMxnnnnnnnnnnnnnW,     
#                                                 zMnnnnnnnnnnzzzzzzzzzzzzzzznMW,`x:MnnW@@@MnWnnnnnnnnnnnnnnx      
#                                                ,@nnnnnnnnnnnzzzzzzzzzzzzzzzzzzMxM*xMM@@WxnWnnnnnnnnnnnnnnM*      
#                                                nMnnnnnnnnnnzzzzzzzzzzzzzzzzzzzzzznnMxxnnMWnnnnnnnnnnnnnnnM`      
#                                               :@nnnnnnnnnnnzzzzzzzzzzzzzzzzzzzzzzzxMMMWWxnnnnnnnnnnnnnnnx#       
#                                              `xxnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzzzzznxxxnnnnnnnnnnnnnnnnnnW.       
#                                              ;@nnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnxz        
#                                              MxnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnM,        
#                                             iWnnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnn         
#                                            `WnnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnM;         
#                                            *MnnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnM          
#                                           .Wnnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnx*          
#                                           #MnnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnW.          
#                                          ,@nnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnx#           
#                                          nxnnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnM,           
#                                         ;Wnnnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnx            
#                                        `MnnnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnMi            
#                                        +MnnnnnnnnnnnnnzzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnM`            
#                                       ,Wnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnx*             
#                                      `xxnnnnnnnnnnnnnzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnW`             
#                                      *Mnnnnnnnnnnnnnzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnx+              
#                                     .WnnnnnnnnnnnnnzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnW.              
#                                     xxnnnnnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnx+               
#                                    *MnnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnM`               
#                                   ,Wnnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnx+                
#                                  `xxnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW`                
#                                  +Mnnnnnnnnnnnnnzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnx#                 
#                                 :WnznnnnnnnnnnnzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnM.                 
#                                `MnnxMxnnnnnnnnzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnz                  
#                                #xnzMMxnnnnnnnnzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnM:                  
#                               ;WnnzxMnnnnnnnnzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnx                   
#                              .Wnnnnnnnnnnnnnzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnxnnnnnnnnnxi                   
#                             `xxnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnxMnnnnnnnnnx`                   
#                             +MnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnxMMnnnnnnnnx*                    
#                            :WnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnMMMnnnnnnnnM`                    
#                           .MnnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnxMMMznnnnnnx#                     
#                          `xnnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnznnnnnnnM.                     
#                          #xnnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnx#                      
#                         *MnnnnnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW.                      
#                        ;MnnnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnM#                       
#                       ,MnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW`                       
#                      ,MnnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnMi                        
#                     .xnnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnx                         
#                    .xnnnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW:                         
#                   .xnnnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxz                          
#                  `nnnnnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW.                          
#                  nxnnnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnM*                           
#                 #xnnnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnM`                           
#                *MnnnnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW;                            
#               :Wnnnnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxn                             
#              .MnnnnnnnnnnnnzznnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW,                             
#             `xxnnnnnnnnnnnzxxxzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnx#                              
#             #MnnnnnnnnnnnzxMMMzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnM`                              
#            ;WnnnnnnnnnnnnzMMMnzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnM;                               
#           .MnnzznnnnnnnnnzxMnzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxn                                
#           nxzxMMnnnnnnnnnnnnzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW.                                
#          *MzxMMMxnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnM+                                 
#         ,WnzMMMMnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnM`                                 
#        `xnnzxMMxnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW;                                  
#        +Mnnnzxxnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxn                                   
#       ,WnnnnnznnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW.                                   
#      `xxnnnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnMi                                    
#      iMnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxx                                     
#     `MnnnnnnnnnnnnnnzzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW.                                     
#     *MnnnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnWi                                      
#    `WnnnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW#                                       
#    iMnnnnnnnnnnnnnzzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnMn`                                       
#    MnnnnnnnnnnnnnnzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnMM`                                        
#   :WnnnnnnnnnnnnnzzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxW.                                         
#   zxnnnnnnnnnnnnnzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxW,                                          
#  `Wnnnnnnnnnnnnnzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn@:                                           
#  :WnnnnnnnnnnnnnzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW;                                            
#  +MnnnnnnnnnnnnzzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW*                                             
#  xxnnnnnnnnnnnnzzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnxxnnnnnnnnnnnnnnW*                                              
# `WnnnnnnnnnnnnnzzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnMMMnnnnnnnnnnnnnW#                                               
# ,@nnnnnnnnnnnnnzzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnMMMMxnnnnnnnnnnnMz`                                               
# :WnnnnnnnnnnnnnzzzzzzzzzznnnnnnnnnnnnnnnnnnnnnxMMMMnnnnnnnnnnnMn                                                 
# *MnnnnnnnnnnnnnnzzzzzzznnnnnnnnnnnnnnnnnnnnnnnxMMMMznnnnnnnnnMx`                                                 
# +Mnnnnnnnnnnnnnnnzzznnnnnnnnnnnnnnnnnnnnnnnnnnzxxxznnnnnnnnnxx`                                                  
# zMnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnznnnnnnnnnnxM`                                                   
# zxnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxM.                                                    
# #xnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxM.                                                     
# #MnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxM.                                                      
# #MnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxM.                                                       
# iMnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxM.                                                        
# ;WnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxM.                                                         
# .@nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxM.                                                          
#  MxnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxM.                                                           
#  *MnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnMx`                                                            
#  .WnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnMn`                                                             
#   *WnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW#`                                                              
#   `nMnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnW*                                                                
#    `xMnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnMM:                                                                 
#     `zWnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnxWz.                                                     `            
#       *Wxnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnx@x;                                                      `.            
#        .#WxnnnnnnnnnnnnnnnnnnnnnnnnnnnnM@x:`                                                                     
#          .#WMnnnnnnnnnnnnnnnnnnnnnnnxWW#,                                                                        
#            `ixWMxnnnnnnnnnnnnnnnnxW@ni`                                                                          
#               .izMWWMxxxxxxxMMW@M#;`                                                                             
#                  `.;+#nxxxzz+*;.`                                                                                
