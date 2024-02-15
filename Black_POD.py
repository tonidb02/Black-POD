#BLACK POD
#Autores: Antonio Dies Beneytez (20095), Mario Montalvo Ramon (20221) y Aníbal Castaño Mijancos (20053)
#Proyecto de la asignatura Programación en Python de 4º curso del Grado de Ingeniería en Tecnologías Industriales (ETSII - UPM)
#Última actualización: 15/02/2024
#Para la correcta ejecución de este código, hay que tener instaladas las siguientes librerías: pandas, tkinter y tkcap.

import pandas as pd

#A continuación se crean Data Frames con los datos de cada curso extraídos del Excel.
datos_primero=pd.read_excel("datos_segundo_semestre.xlsx","primero")
df_primero=pd.DataFrame=datos_primero
datos_segundo=pd.read_excel("datos_segundo_semestre.xlsx","segundo")
df_segundo=pd.DataFrame=datos_segundo
datos_tercero_comunes=pd.read_excel("datos_segundo_semestre.xlsx","tercero_comunes")
df_tercero_comunes=pd.DataFrame=datos_tercero_comunes
datos_tercero_especialidad=pd.read_excel("datos_segundo_semestre.xlsx","tercero_especialidad")
df_tercero_especialidad=pd.DataFrame=datos_tercero_especialidad
datos_cuarto_comunes=pd.read_excel("datos_segundo_semestre.xlsx","cuarto_comunes")
df_cuarto_comunes=pd.DataFrame=datos_cuarto_comunes
datos_cuarto_especialidad=pd.read_excel("datos_segundo_semestre.xlsx","cuarto_especialidad")
df_cuarto_especialidad=pd.DataFrame=datos_cuarto_especialidad
datos_competencias=pd.read_excel("datos_segundo_semestre.xlsx","competencias")
df_competencias=pd.DataFrame=datos_competencias

from tkinter import *

import random

class Ayg: #Aquí defino la clase Ayg
    def __init__(self, nombre, codigo, grupo, sesiones, profesorado):
        self.nombre = nombre #Nombre descriptivo de la asignatura (eg 'Transferencia de Calor')
        self.codigo = codigo #El código de la signatura como string
        self.grupo = grupo #String de 3 dígitos que determina el grupo (eg '4M3')
        self.sesiones = sesiones #Lista de int que son los huecos del horario en los que se imparte (eg [1,2,3,7])
        self.profesorado = profesorado #Listado de strings con los nombres de los profesores (eg ["Francisco Villarreal", "Juana Manuel"])
    def __repr__(self):
        return (self.nombre + '-' + self.grupo)
lista_maestra = []
lista_df = [df_primero, df_segundo, df_tercero_comunes, df_tercero_especialidad,\
            df_cuarto_comunes, df_cuarto_especialidad, df_competencias]
            
for df in lista_df:
    for i in range(len(df)):
        nombre = str(df.loc[i].nombre)
        codigo = str(df.loc[i].codigo)
        grupo = str(df.loc[i].grupo)
        sesiones = list(map(int, df.loc[i].sesiones.split(",")))
        profesorado = str(df.loc[i].profesorado)
        lista_maestra.append(Ayg(nombre,codigo,grupo,sesiones,profesorado))

def seleccion(ayg_bin, horas_no_bin):
    global lista_maestra
    #Primero procesamos el horas no para que sea un vector con las horas a las que no se puede
    horas_no=[]
    for i in range(len(horas_no_bin)):
        if horas_no_bin[i]: #Si en la posicion x hay un uno añadimos x+1 a horas_no
            horas_no.append(i+1)
            
    #Ahora creamos una lista con solo los ayg elegidos
    l_m_filtrada = []
    for i in range(len(ayg_bin)):
        if ayg_bin[i]:
            l_m_filtrada.append(lista_maestra[i])
    
    #Ahora tenemos que crear la matriz de objetos ayg para el contador
    #Primero vamos a crear una lista con todos los códigos presentes
    lista_codigos = []
    for ayg in l_m_filtrada:
        lista_codigos.append(ayg.codigo)
    lista_codigos = list(set(lista_codigos))
    lista_codigos.sort()
    
    #Ahora creamos la matriz, con una asignatura por fila, utilizando la lista de códigos
    ayg_mat = []
    for codigo in lista_codigos:
        ayg_mat.append(list(filter(lambda obj: obj.codigo == codigo,l_m_filtrada)))
    
    #Utilizamos una especie de contador
    horarios = []
    c = [0]*len(ayg_mat)
    overflow = False
    while not overflow:
       
        h_temp = [] #Inicializamos un horario temporal
        ses_ocupadas = horas_no #Dentro de las sesiones que consideramos ocupadas incluimos las que el alumno no puede utilizar
        for i in range(len(ayg_mat)): #Con este bucle for llenamos el horario temporal con los Ayg que determina el contador
            h_temp.append(ayg_mat[i][c[i]])
            ses_ocupadas = ses_ocupadas + h_temp[i].sesiones #Aquí vamos acumulando las sesiones que quedaran ocupadas
        for i in range(len(ses_ocupadas)): #Con este for loop vemos si algun elemento se repite, si no se repite se ejecuta el else, añadiendo h_temp a horarios
            if ses_ocupadas[i] in ses_ocupadas[i+1:]:
                break
        else:
            horarios.append(h_temp)        

        overflow = True
        for i in range(len(ayg_mat)):
            c[i] = c[i] + overflow
            overflow = False
            if c[i] >= len(ayg_mat[i]):
                c[i] = 0
                overflow = True
    
    n2xy = {1:[1,1], 2:[2,1], 3:[4,1], 4:[5,1], 5:[7,1], 6:[8,1], 7:[10,1], 8:[11,1],\
                   9:[1,2], 10:[2,2], 11:[4,2], 12:[5,2], 13:[7,2], 14:[8,2], 15:[10,2], 16:[11,2],\
                   17:[1,3], 18:[2,3], 19:[4,3], 20:[5,3], 21:[7,3], 22:[8,3], 23:[10,3], 24:[11,3],\
                   25:[1,4], 26:[2,4], 27:[4,4], 28:[5,4], 29:[7,4], 30:[8,4], 31:[10,4], 32:[11,4],\
                   33:[1,5], 34:[2,5], 35:[4,5], 36:[5,5], 37:[7,5], 38:[8,5], 39:[10,5], 40:[11,5]}
    def n2x(n):
        return n2xy[n][1]
    def n2y(n):
        return n2xy[n][0]
    #Con este diccionario y funciones convertimos las coordenadas de la clase Ayg a las de un grid de tkinter

    root=Tk()
    root.geometry("700x500")
    root.resizable(TRUE,TRUE)
    root.iconbitmap("LOGO.ico")
    root.title("Posibles horarios")
    #Lo que viene debajo es para que el horario ocupe toda la ventana
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)
    frame=Frame(root)
    frame.grid(row=0, column=0, sticky="news")
    for row_index in range(13):
        Grid.rowconfigure(frame, row_index, weight=3)
    for col_index in range(6):
        Grid.columnconfigure(frame, col_index, weight=3)
    Grid.rowconfigure(frame, 13, weight=1)


    #Aquí dibujamos los elementos basicos del horario
    lunes = Label(frame, text = "Lunes", borderwidth=1, relief = "solid", font=("Century Gothic",10))
    martes = Label(frame, text = "Martes", borderwidth=1, relief = "solid", font=("Century Gothic",10))
    miercoles = Label(frame, text = "Miércoles", borderwidth=1, relief = "solid", font=("Century Gothic",10))
    jueves = Label(frame, text = "Jueves", borderwidth=1, relief = "solid", font=("Century Gothic",10))
    viernes = Label(frame, text = "Viernes", borderwidth=1, relief = "solid", font=("Century Gothic",10))
    hora1 = Label(frame, text = "8:30 - 9:35", borderwidth=1, relief = "solid", font=("Century Gothic",10))
    hora2 = Label(frame, text = "9:45 - 10:50", borderwidth=1, relief = "solid", font=("Century Gothic",10))
    hora3 = Label(frame, text = "11:10 - 12:15", borderwidth=1, relief = "solid", font=("Century Gothic",10))
    hora4 = Label(frame, text = "12:25 - 13:30", borderwidth=1, relief = "solid", font=("Century Gothic",10))
    hora5 = Label(frame, text = "15:30 - 16:35", borderwidth=1, relief = "solid", font=("Century Gothic",10))
    hora6 = Label(frame, text = "16:45 - 17:50", borderwidth=1, relief = "solid", font=("Century Gothic",10))
    hora7 = Label(frame, text = "18:10 - 19:15", borderwidth=1, relief = "solid", font=("Century Gothic",10))
    hora8 = Label(frame, text = "19:25 - 20:30", borderwidth=1, relief = "solid", font=("Century Gothic",10))

    def hueco_fila(padre, fila, alto): #Esta función es para dejar huecos entra algunas filas
        vacio = Label(padre, height=alto)
        vacio.grid(row = fila, sticky= "news")

    lunes.grid(row =0, column =1, sticky= "news")
    martes.grid(row =0, column =2, sticky= "news")
    miercoles.grid(row =0, column =3, sticky= "news")
    jueves.grid(row =0, column =4, sticky= "news")
    viernes.grid(row =0, column =5, sticky= "news")
    hora1.grid(row =1, column =0, sticky= "news")
    hora2.grid(row =2, column =0, sticky= "news")
    hora3.grid(row =4, column =0, sticky= "news")
    hora4.grid(row =5, column =0, sticky= "news")
    hora5.grid(row =7, column =0, sticky= "news")
    hora6.grid(row =8, column =0, sticky= "news")
    hora7.grid(row =10, column =0, sticky= "news")
    hora8.grid(row =11, column =0, sticky= "news")
    hueco_fila(frame,3,1)
    hueco_fila(frame,6,1)
    hueco_fila(frame,9,1)
    hueco_fila(frame,12,1)

    #A partir de aquí rellenamos el horario

    colores = ["#FFB5E8","#B28DFF","#DCD3FF","#AFF8DB","#BFFCC6","#FFC9DE","#FF9CEE","#C5A3FF",\
               "#A79AFF","#C4FAF8","#DBFFD6","#FFABAB","#FFCCF9","#D5AAFF","#B5B9FF","#85E3FF",\
               "#F3FFE3","#FFBEBC","#FCC2FF","#ECD4FF","#97A2FF","#ACE7FF","#E7FFAC","#FFCBC1",\
               "#F6A6FF","#FBE4FF","#AFCBFF","#6EB5FF","#FFFFDI","#FFF5BA","#77DD77","#99c5c4",\
               "#9adedb","#b2fba5","#bee7a5","#ff6961","#ca9bf7"]
    #Muchos colores para que coja la azar para cada asignatura
    global n_horario #Empezamos en el primer horario posible
    n_horario = 0 #Empezamos en el primer horario posible
    def rellenar_horario(n): #n es cual de los posibles horarios cogemos, de la lista horarios que sale de la función seleccion
        for widget in leyenda.winfo_children(): #Destruye todo lo que hay dentro de la leyenda para volver a ponerlo
            widget.destroy()
        for j in range(1,41): #Con esta parte limpiamos el horario
            slot_limpio = Label(frame, borderwidth=1, relief = "solid")
            slot_limpio.grid(column = n2x(j), row = n2y(j), sticky = "news")
        for ayg in horarios[n]: #Con esta parte tellenamos el horario
            display = ayg.codigo + ' - ' + ayg.grupo #Queremos que aparezca el código y el grupo de la asignatura
            random.seed(ayg.codigo) #Utilizamos una seed que depende del código para que sea siempre igual para una misma asignatura
            color = random.choice(colores)
            entrada = Label(leyenda, text = ayg.nombre + ": " + display, bg = color, font=("Century Gothic",10))
            entrada.pack(fill = X)
            for j in ayg.sesiones:
                slot = Label(frame, text = display, bg = color, borderwidth=1, relief = "solid", font=("Century Gothic",10))
                slot.grid(column = n2x(j), row = n2y(j), sticky = "news")


    try:
        leyenda = Tk()
        leyenda.iconbitmap("LOGO.ico")
        leyenda.title("Leyenda")
        rellenar_horario(n_horario)
    except:
        root.destroy()
        leyenda.destroy()
        ventana_error = Tk()
        ventana_error.title("Error")
        ventana_error.resizable(TRUE,TRUE)
        ventana_error.iconbitmap("LOGO.ico")
        ventana_error.geometry("700x500")
        e_error = Label(ventana_error, text = "No se encontraron combinaciones posibles")
        e_error.pack()
        ventana_error.mainloop()
    
        
    #Lo de abajo son los botones y las cosas que hacen
    def change_n(var):
        global n_horario
        n_new = n_horario + var
        if n_new in range(len(horarios)):
            n_horario = n_new
            rellenar_horario(n_horario)
            muestra = Label(frame, text = str(n_horario+1)+' / '+ str(len(horarios)))
            muestra.grid(row =13, column =3, sticky= "news")
    def screenshot():
        try: #Tenemos que comprobar que tkcap esta instalado para que funcione
            import tkcap
            import time
            int(time.time()*100000)%100000
            cap = tkcap.CAP(root)
            cap.capture("screenshot" + str(int(time.time()*100000)%100000) + ".png")
        except:
            e_imprimir = Label(frame, text="Instala tkcap", bg = "red", fg = "white")
            e_imprimir.grid(row =13, column =5, sticky= "news")
            
    b_anterior = Button(frame, text="Anterior", command = lambda: change_n(-1), font=("Century Gothic",10))
    b_siguiente = Button(frame, text="Siguiente", command = lambda: change_n(1), font=("Century Gothic",10))
    b_imprimir = Button(frame, text="Screenshot", command = screenshot, font=("Century Gothic",10))
    e_contador = Label(frame, text = str(n_horario+1)+' / '+ str(len(horarios)))

    b_anterior.grid(row =13, column =2, sticky= "news")
    b_siguiente.grid(row =13, column =4, sticky= "news")
    b_imprimir.grid(row =13, column =5, sticky= "news")
    e_contador.grid(row =13, column =3, sticky= "news")



    root.mainloop()
    leyenda.mainloop()

def aceptar(turnos_preferentes, horas_no): #Turnos preferentes no es un vector de ints, he corregido eso
    root.destroy() #Cerramos la ventana inicial
    turnos_preferentes_bin = []
    horas_no_bin = []
    for el in turnos_preferentes:
        turnos_preferentes_bin.append(int(el.get()))
    for elem in horas_no:
        horas_no_bin.append(int(elem.get()))
    turnos_preferentes_bin = turnos_preferentes_bin[:171] #Esto es para cortar el vector, no hara falta cuando corrijamos eso
    seleccion(turnos_preferentes_bin, horas_no_bin)
    
def toggle1(a, variables, btn):
        abrir1(a,variables, btn)

def toggle2(a, variables, btn):
        abrir2(a,variables, btn)

def toggle3(a, variables, btn):
        abrir3(a,variables, btn)

def toggle3_esp(a, variables, btn):
        abrir3_esp(a,variables, btn)

def toggle4(a, variables, btn):
        abrir4(a,variables, btn)

def toggle4_esp(a, variables, btn):
        abrir4_esp(a,variables, btn)
    
def toggle_comp(a, variables, btn):
        abrir_comp(a,variables, btn)
        
def abrir1(a, variables, btn):
    global ventana
    ventana = Toplevel(root)
    ventana.title("Turnos disponibles")
    ventana.config(bg='white')
    ventana.geometry("500x350")
    ventana.resizable(TRUE,TRUE)
    ventana.iconbitmap("LOGO.ico")
    main_frame1 = Frame(ventana)
    main_frame1.pack(fill=BOTH, expand=1)
    main_frame1.config(bg='white')
    my_canvas1 = Canvas(main_frame1)
    my_canvas1.pack(side=LEFT, fill=BOTH, expand=1)
    my_canvas1.config(bg='white')
    my_scrollbar1=Scrollbar(ventana, orient=HORIZONTAL, command=my_canvas1.xview)
    my_scrollbar1.pack(side=BOTTOM, fill=X)
    my_canvas1.configure(xscrollcommand=my_scrollbar1.set)
    my_canvas1.bind('<Configure>', lambda e: my_canvas1.configure(scrollregion=my_canvas1.bbox("all")))
    frame1=Frame(my_canvas1, bg="white", bd=10, cursor="hand2")
    my_canvas1.create_window((0,0), window=frame1, anchor="nw", width=900)
    
    #Función para guardar la selección de casillas
    def guardar_seleccion(z,btnb):
        global seleccion_anterior
        global seleccion_anterior_ind
        seleccion_anterior = [var.get() for var in variables]
        seleccion_anterior_ind[z] = var_ind.get()
        ventana.withdraw()  #Ocultar ventana al guardar selección
        cont = 0
        for j in range(z*6, z*6+6):
            if variables[j].get() == 1:
                cont += 1
        if cont >= 1:
            btnb.config(bg="lightsteelblue")
        else:
            btnb.config(bg="white")
    
    def marcar_desmarcar(a):
        if var_ind.get() == 1:
            for i in range(a*6, a*6+6):
                variables[i].set(1)
    
    def desmarcar(i):
        if not variables[i].get():
            var_ind.set(0)

    #Crear las casillas de los turnos de primero
    aux=0
    if 0<=a<=4: 
        turnos1 = []  
        for i in range(a*6,a*6+6):
            turnos1.append(df_primero.grupo[i] +' ~ '+ df_primero.profesorado[i])
        turnos1.append("Indiferente")
    
    var_ind = IntVar(value=seleccion_anterior_ind[a])
    check_ind = Checkbutton(frame1, text=turnos1[6], variable=var_ind, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=100)
    check_ind.grid(row=8, column=2, sticky="W",padx=20, pady=5)
    var_ind.trace_add("write", lambda *_: marcar_desmarcar(a))
    
    for i in range(a*6, a*6+6):
        var = IntVar(value=seleccion_anterior[i])
        check = Checkbutton(frame1, text=turnos1[aux], variable=var, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=100)
        check.grid(row=2+aux, column=2, sticky="W",padx=20, pady=5)
        variables[i] = var
        variables[i].trace_add("write", lambda *_, i=i: desmarcar(i))
        aux += 1
    
    #Botón para guardar selección
    boton_guardar = Button(frame1, text="Guardar selección", command=lambda: guardar_seleccion(a,btn), font=("Century Gothic",10))
    boton_guardar.grid(row=9, column=2, sticky="w",padx=40, pady=10)

def abrir2(a, variables, btn):
    global ventana
    ventana = Toplevel(root)
    ventana.title("Turnos disponibles")
    ventana.config(bg='white')
    ventana.geometry("500x350")
    ventana.resizable(TRUE,TRUE)
    ventana.iconbitmap("LOGO.ico")
    main_frame1 = Frame(ventana)
    main_frame1.pack(fill=BOTH, expand=1)
    main_frame1.config(bg='white')
    my_canvas1 = Canvas(main_frame1)
    my_canvas1.pack(side=LEFT, fill=BOTH, expand=1)
    my_canvas1.config(bg='white')
    my_scrollbar1=Scrollbar(ventana, orient=HORIZONTAL, command=my_canvas1.xview)
    my_scrollbar1.pack(side=BOTTOM, fill=X)
    my_canvas1.configure(xscrollcommand=my_scrollbar1.set)
    my_canvas1.bind('<Configure>', lambda e: my_canvas1.configure(scrollregion=my_canvas1.bbox("all")))
    frame1=Frame(my_canvas1, bg="white", bd=10, cursor="hand2")
    my_canvas1.create_window((0,0), window=frame1, anchor="nw", width=900)
    
    #Función para guardar la selección de casillas
    def guardar_seleccion(z,btnb):
        global seleccion_anterior
        global seleccion_anterior_ind
        seleccion_anterior = [var.get() for var in variables]
        seleccion_anterior_ind[z] = var_ind.get()
        ventana.withdraw()  #Ocultar ventana al guardar selección
        cont = 0
        for j in range(z*6+30, z*6+36):
            if variables[j].get() == 1:
                cont += 1
        if cont >= 1:
            btnb.config(bg="lightsteelblue")
        else:
            btnb.config(bg="white")
    
    def marcar_desmarcar(a):
        if var_ind.get() == 1:
            for i in range(a*6+30, a*6+36):
                variables[i].set(1)
    
    def desmarcar(i):
        if not variables[i].get():
            var_ind.set(0)

    # Crear las casillas de los turnos de segundo
    aux=0
    if 30<=a<=36:
        turnos2 = []  
        for i in range((a-30)*6,(a-30)*6+6):
            turnos2.append(df_segundo.grupo[i] +' ~ '+ df_segundo.profesorado[i])
        turnos2.append("Indiferente")

    var_ind = IntVar(value=seleccion_anterior_ind[a])
    check_ind = Checkbutton(frame1, text=turnos2[6], variable=var_ind, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=100)
    check_ind.grid(row=8, column=2, sticky="W",padx=20, pady=5)
    var_ind.trace_add("write", lambda *_: marcar_desmarcar(a))
    a -= 30
    for i in range(a*6+30, a*6+36):
        var = IntVar(value=seleccion_anterior[i])
        check = Checkbutton(frame1, text=turnos2[aux], variable=var, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=100)
        check.grid(row=2+aux, column=2, sticky="W",padx=20, pady=5)
        variables[i] = var
        variables[i].trace_add("write", lambda *_, i=i: desmarcar(i))
        aux += 1
    
    #Botón para guardar selección
    boton_guardar = Button(frame1, text="Guardar selección", command=lambda: guardar_seleccion(a,btn), font=("Century Gothic",10))
    boton_guardar.grid(row=9, column=2, sticky="w",padx=40, pady=10)

def abrir3(a, variables, btn):
    global ventana
    ventana = Toplevel(root)
    ventana.title("Turnos disponibles")
    ventana.config(bg='white')
    ventana.geometry("500x300")
    ventana.resizable(TRUE,TRUE)
    ventana.iconbitmap("LOGO.ico")
    main_frame1 = Frame(ventana)
    main_frame1.pack(fill=BOTH, expand=1)
    main_frame1.config(bg='white')
    my_canvas1 = Canvas(main_frame1)
    my_canvas1.pack(side=LEFT, fill=BOTH, expand=1)
    my_canvas1.config(bg='white')
    my_scrollbar1=Scrollbar(ventana, orient=HORIZONTAL, command=my_canvas1.xview)
    my_scrollbar1.pack(side=BOTTOM, fill=X)
    my_canvas1.configure(xscrollcommand=my_scrollbar1.set)
    my_canvas1.bind('<Configure>', lambda e: my_canvas1.configure(scrollregion=my_canvas1.bbox("all")))
    frame1=Frame(my_canvas1, bg="white", bd=10, cursor="hand2")
    my_canvas1.create_window((0,0), window=frame1, anchor="nw", width=900)
    
    #Función para guardar la selección de casillas
    def guardar_seleccion(z,btnb):
        global seleccion_anterior
        global seleccion_anterior_ind
        seleccion_anterior = [var.get() for var in variables]
        seleccion_anterior_ind[z] = var_ind.get()
        ventana.withdraw()  #Ocultar ventana al guardar selección
        cont = 0
        for j in range(z*5+72, z*5+77):
            if variables[j].get() == 1:
                cont += 1
        if cont >= 1:
            btnb.config(bg="lightsteelblue")
        else:
            btnb.config(bg="white")
    
    def marcar_desmarcar(a):
        if var_ind.get() == 1:
            for i in range(a*5+72, a*5+77):
                variables[i].set(1)
    
    def desmarcar(i):
        if not variables[i].get():
            var_ind.set(0)

    #Crear las casillas de los turnos de tercero
    aux=0
    if 72<=a<=76: 
        turnos3 = []  
        for i in range((a-72)*5,(a-72)*5+5):
            turnos3.append(df_tercero_comunes.grupo[i] +' ~ '+ df_tercero_comunes.profesorado[i])
        turnos3.append("Indiferente")

    var_ind = IntVar(value=seleccion_anterior_ind[a])
    check_ind = Checkbutton(frame1, text=turnos3[5], variable=var_ind, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=100)
    check_ind.grid(row=7, column=2, sticky="W",padx=20, pady=5)
    var_ind.trace_add("write", lambda *_: marcar_desmarcar(a))
    a -= 72
    for i in range(a*5+72, a*5+77):
        var = IntVar(value=seleccion_anterior[i])
        check = Checkbutton(frame1, text=turnos3[aux], variable=var, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=100)
        check.grid(row=2+aux, column=2, sticky="W",padx=20, pady=5)
        variables[i] = var
        variables[i].trace_add("write", lambda *_, i=i: desmarcar(i))
        aux += 1
    
    #Botón para guardar selección
    boton_guardar = Button(frame1, text="Guardar selección", command=lambda: guardar_seleccion(a,btn), font=("Century Gothic",10))
    boton_guardar.grid(row=8, column=2, sticky="w",padx=40, pady=10)

def abrir3_esp(a, variables, btn):
    global ventana
    ventana = Toplevel(root)
    ventana.title("Turnos disponibles")
    ventana.config(bg='white')
    ventana.geometry("500x300")
    ventana.resizable(TRUE,TRUE)
    ventana.iconbitmap("LOGO.ico")
    main_frame1 = Frame(ventana)
    main_frame1.pack(fill=BOTH, expand=1)
    main_frame1.config(bg='white')
    my_canvas1 = Canvas(main_frame1)
    my_canvas1.pack(side=LEFT, fill=BOTH, expand=1)
    my_canvas1.config(bg='white')
    my_scrollbar1=Scrollbar(ventana, orient=HORIZONTAL, command=my_canvas1.xview)
    my_scrollbar1.pack(side=BOTTOM, fill=X)
    my_canvas1.configure(xscrollcommand=my_scrollbar1.set)
    my_canvas1.bind('<Configure>', lambda e: my_canvas1.configure(scrollregion=my_canvas1.bbox("all")))
    frame1=Frame(my_canvas1, bg="white", bd=10, cursor="hand2")
    my_canvas1.create_window((0,0), window=frame1, anchor="nw", width=1600)
    
    #Función para guardar la selección de casillas
    def guardar_seleccion(z,btnb):
        global seleccion_anterior
        global seleccion_anterior_ind
        seleccion_anterior = [var.get() for var in variables]
        seleccion_anterior_ind[z] = var_ind.get()
        ventana.withdraw()  #Ocultar ventana al guardar selección
        cont = 0
        for j in range(z, z+1):
            if variables[j].get() == 1:
                cont += 1
        if cont >= 1:
            btnb.config(bg="lightsteelblue")
        else:
            btnb.config(bg="white")
    
    def marcar_desmarcar(a):
        if var_ind.get() == 1:
            for i in range(a, a+1):
                variables[i].set(1)
    
    def desmarcar(i):
        if not variables[i].get():
            var_ind.set(0)

    #Crear las casillas de los turnos de tercero esp
    aux=0
    if 97<=a<=115: 
        turnos3_esp = []  
        turnos3_esp.append(df_tercero_especialidad.grupo[a-97] +' ~ '+ df_tercero_especialidad.profesorado[a-97])
        turnos3_esp.append("Indiferente")

    var_ind = IntVar(value=seleccion_anterior_ind[a])
    check_ind = Checkbutton(frame1, text=turnos3_esp[1], variable=var_ind, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=100)
    check_ind.grid(row=3, column=2, sticky="W",padx=20, pady=5)
    var_ind.trace_add("write", lambda *_: marcar_desmarcar(a))
    a
    for i in range(a, a+1):
        var = IntVar(value=seleccion_anterior[i])
        check = Checkbutton(frame1, text=turnos3_esp[aux], variable=var, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=800)
        check.grid(row=2+aux, column=2, sticky="W",padx=20, pady=5)
        variables[i] = var
        variables[i].trace_add("write", lambda *_, i=i: desmarcar(i))
        aux += 1
    
    #Botón para guardar selección
    boton_guardar = Button(frame1, text="Guardar selección", command=lambda: guardar_seleccion(a,btn), font=("Century Gothic",10))
    boton_guardar.grid(row=4, column=2, sticky="w",padx=40, pady=10)

def abrir4(a, variables, btn):
    global ventana
    ventana = Toplevel(root)
    ventana.title("Turnos disponibles")
    ventana.config(bg='white')
    ventana.geometry("500x300")
    ventana.resizable(TRUE,TRUE)
    ventana.iconbitmap("LOGO.ico")
    main_frame1 = Frame(ventana)
    main_frame1.pack(fill=BOTH, expand=1)
    main_frame1.config(bg='white')
    my_canvas1 = Canvas(main_frame1)
    my_canvas1.pack(side=LEFT, fill=BOTH, expand=1)
    my_canvas1.config(bg='white')
    my_scrollbar1=Scrollbar(ventana, orient=HORIZONTAL, command=my_canvas1.xview)
    my_scrollbar1.pack(side=BOTTOM, fill=X)
    my_canvas1.configure(xscrollcommand=my_scrollbar1.set)
    my_canvas1.bind('<Configure>', lambda e: my_canvas1.configure(scrollregion=my_canvas1.bbox("all")))
    frame1=Frame(my_canvas1, bg="white", bd=10, cursor="hand2")
    my_canvas1.create_window((0,0), window=frame1, anchor="nw", width=900)
    
    #Función para guardar la selección de casillas
    def guardar_seleccion(z,btnb):
        global seleccion_anterior
        global seleccion_anterior_ind
        seleccion_anterior = [var.get() for var in variables]
        seleccion_anterior_ind[z] = var_ind.get()
        ventana.withdraw()  #Ocultar ventana al guardar selección
        cont = 0
        for j in range(z*5+116, z*5+121):
            if variables[j].get() == 1:
                cont += 1
        if cont >= 1:
            btnb.config(bg="lightsteelblue")
        else:
            btnb.config(bg="white")
    
    def marcar_desmarcar(a):
        if var_ind.get() == 1:
            for i in range(a*5+116, a*5+121):
                variables[i].set(1)
    
    def desmarcar(i):
        if not variables[i].get():
            var_ind.set(0)

    # Crear las casillas de los turnos de cuarto
    aux=0
    if a==116: 
        turnos4 = []  
        for i in range(0,5):
            turnos4.append(df_cuarto_comunes.grupo[i] +' ~ '+ df_cuarto_comunes.profesorado[i])
        turnos4.append("Indiferente")

    var_ind = IntVar(value=seleccion_anterior_ind[a])
    check_ind = Checkbutton(frame1, text=turnos4[5], variable=var_ind, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=100)
    check_ind.grid(row=7, column=2, sticky="W",padx=20, pady=5)
    var_ind.trace_add("write", lambda *_: marcar_desmarcar(a))
    a -= 116
    for i in range(a*5+116, a*5+121):
        var = IntVar(value=seleccion_anterior[i])
        check = Checkbutton(frame1, text=turnos4[aux], variable=var, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=100)
        check.grid(row=2+aux, column=2, sticky="W",padx=20, pady=5)
        variables[i] = var
        variables[i].trace_add("write", lambda *_, i=i: desmarcar(i))
        aux += 1
    
    #Botón para guardar selección
    boton_guardar = Button(frame1, text="Guardar selección", command=lambda: guardar_seleccion(a,btn), font=("Century Gothic",10))
    boton_guardar.grid(row=8, column=2, sticky="w",padx=40, pady=10)

def abrir4_esp(a, variables, btn):
    global ventana
    ventana = Toplevel(root)
    ventana.title("Turnos disponibles")
    ventana.config(bg='white')
    ventana.geometry("500x300")
    ventana.resizable(TRUE,TRUE)
    ventana.iconbitmap("LOGO.ico")
    main_frame1 = Frame(ventana)
    main_frame1.pack(fill=BOTH, expand=1)
    main_frame1.config(bg='white')
    my_canvas1 = Canvas(main_frame1)
    my_canvas1.pack(side=LEFT, fill=BOTH, expand=1)
    my_canvas1.config(bg='white')
    my_scrollbar1=Scrollbar(ventana, orient=HORIZONTAL, command=my_canvas1.xview)
    my_scrollbar1.pack(side=BOTTOM, fill=X)
    my_canvas1.configure(xscrollcommand=my_scrollbar1.set)
    my_canvas1.bind('<Configure>', lambda e: my_canvas1.configure(scrollregion=my_canvas1.bbox("all")))
    frame1=Frame(my_canvas1, bg="white", bd=10, cursor="hand2")
    my_canvas1.create_window((0,0), window=frame1, anchor="nw", width=1500)
    
    #Función para guardar la selección de casillas
    def guardar_seleccion(z,btnb):
        global seleccion_anterior
        global seleccion_anterior_ind
        seleccion_anterior = [var.get() for var in variables]
        seleccion_anterior_ind[z] = var_ind.get()
        ventana.withdraw()  #Ocultar ventana al guardar selección
        cont = 0
        for j in range(z, z+1):
            if variables[j].get() == 1:
                cont += 1
        if cont >= 1:
            btnb.config(bg="lightsteelblue")
        else:
            btnb.config(bg="white")
    
    def marcar_desmarcar(a):
        if var_ind.get() == 1:
            for i in range(a, a+1):
                variables[i].set(1)
    
    def desmarcar(i):
        if not variables[i].get():
            var_ind.set(0)

    #Crear las casillas de los turnos de cuarto esp 
    aux=0
    if 121<=a<=156: 
        turnos4_esp = []  
        turnos4_esp.append(df_cuarto_especialidad.grupo[a-121] +' ~ '+ df_cuarto_especialidad.profesorado[a-121])
        turnos4_esp.append("Indiferente")

    var_ind = IntVar(value=seleccion_anterior_ind[a])
    check_ind = Checkbutton(frame1, text=turnos4_esp[1], variable=var_ind, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=100)
    check_ind.grid(row=3, column=2, sticky="W",padx=20, pady=5)
    var_ind.trace_add("write", lambda *_: marcar_desmarcar(a))
    
    for i in range(a, a+1):
        var = IntVar(value=seleccion_anterior[i])
        check = Checkbutton(frame1, text=turnos4_esp[aux], variable=var, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=900)
        check.grid(row=2+aux, column=2, sticky="W",padx=20, pady=5)
        variables[i] = var
        variables[i].trace_add("write", lambda *_, i=i: desmarcar(i))
        aux += 1
    
    #Botón para guardar selección
    boton_guardar = Button(frame1, text="Guardar selección", command=lambda: guardar_seleccion(a,btn), font=("Century Gothic",10))
    boton_guardar.grid(row=4, column=2, sticky="w",padx=40, pady=10)

def abrir_comp(a, variables, btn):
    global ventana
    ventana = Toplevel(root)
    ventana.title("Turnos disponibles")
    ventana.config(bg='white')
    ventana.geometry("500x300")
    ventana.resizable(TRUE,TRUE)
    ventana.iconbitmap("LOGO.ico")
    main_frame1 = Frame(ventana)
    main_frame1.pack(fill=BOTH, expand=1)
    main_frame1.config(bg='white')
    my_canvas1 = Canvas(main_frame1)
    my_canvas1.pack(side=LEFT, fill=BOTH, expand=1)
    my_canvas1.config(bg='white')
    my_scrollbar1=Scrollbar(ventana, orient=HORIZONTAL, command=my_canvas1.xview)
    my_scrollbar1.pack(side=BOTTOM, fill=X)
    my_canvas1.configure(xscrollcommand=my_scrollbar1.set)
    my_canvas1.bind('<Configure>', lambda e: my_canvas1.configure(scrollregion=my_canvas1.bbox("all")))
    frame1=Frame(my_canvas1, bg="white", bd=10, cursor="hand2")
    my_canvas1.create_window((0,0), window=frame1, anchor="nw", width=1200)
    
    #Función para guardar la selección de casillas
    def guardar_seleccion(z,btnb):
        global seleccion_anterior
        global seleccion_anterior_ind
        seleccion_anterior = [var.get() for var in variables]
        seleccion_anterior_ind[z] = var_ind.get()
        ventana.withdraw()  #Ocultar ventana al guardar selección
        cont = 0
        for j in range(z, z+1):
            if variables[j].get() == 1:
                cont += 1
        if cont >= 1:
            btnb.config(bg="lightsteelblue")
        else:
            btnb.config(bg="white")
    
    def marcar_desmarcar(a):
        if var_ind.get() == 1:
            for i in range(a, a+1):
                variables[i].set(1)
    
    def desmarcar(i):
        if not variables[i].get():
            var_ind.set(0)

    #Crear las casillas de los turnos de competencias 
    aux=0
    if 157<=a<=170: 
        turnos_comp = []  
        turnos_comp.append(df_competencias.grupo[a-157] +' ~ '+ df_competencias.profesorado[a-157])
        turnos_comp.append("Indiferente")

    var_ind = IntVar(value=seleccion_anterior_ind[a])
    check_ind = Checkbutton(frame1, text=turnos_comp[1], variable=var_ind, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=100)
    check_ind.grid(row=3, column=2, sticky="W",padx=20, pady=5)
    var_ind.trace_add("write", lambda *_: marcar_desmarcar(a))
    
    for i in range(a, a+1):
        var = IntVar(value=seleccion_anterior[i])
        check = Checkbutton(frame1, text=turnos_comp[aux], variable=var, fg="black", font=("Century Gothic",10), anchor="w", justify="left", bg="white", width=700)
        check.grid(row=2+aux, column=2, sticky="W",padx=20, pady=5)
        variables[i] = var
        variables[i].trace_add("write", lambda *_, i=i: desmarcar(i))
        aux += 1
    
    #Botón para guardar selección
    boton_guardar = Button(frame1, text="Guardar selección", command=lambda: guardar_seleccion(a,btn), font=("Century Gothic",10))
    boton_guardar.grid(row=4, column=2, sticky="w",padx=40, pady=10)

#CREAMOS LA VENTANA PRINCIPAL
root=Tk()
root.title("Black Pod")
root.config(bg='white')
root.geometry("850x500")
root.resizable(True,True)
root.iconbitmap("LOGO.ico")

#CREAMOS UN FRAME
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)
main_frame.config(bg='white')

#CREAMOS UN CANVAS
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
my_canvas.config(bg='white')

#BARRA DE SCROLL VERTICAL
my_scrollbarv=Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbarv.pack(side=RIGHT, fill=Y)

#BARRA DE SCROLL HORIZONTAL
my_scrollbarh=Scrollbar(root, orient=HORIZONTAL, command=my_canvas.xview)
my_scrollbarh.pack(side=BOTTOM, fill=X)

#CONFIGURAMOS EL CANVAS
my_canvas.configure(yscrollcommand=my_scrollbarv.set)
my_canvas.configure(xscrollcommand=my_scrollbarh.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

#VENTANA BLANCA
Frame1=Frame(my_canvas, bg="white", bd=10, cursor="hand2")
my_canvas.create_window((0,50), window=Frame1, anchor="nw", width=900)

#FRANJA AZUL SUPERIOR
Frame_superior=Frame(my_canvas, height=50, bg='navy')
my_canvas.create_window((0,0), window=Frame_superior, anchor="nw", width=2000)

#TITULO
titulo = Label(Frame_superior, text="BLACK POD", fg='white', bg='navy', font=("BankGothic Md BT", 30))
titulo.grid(row=0, column=2, sticky="n",padx=300, pady=10)

#BOTON ACEPTAR
boton_aceptar = Button(root, text="Aceptar", fg="black", font=("Century Gothic", 10), bg="white", command=lambda: aceptar(variables,variables_horas))
boton_aceptar.pack(pady=10, side=BOTTOM, padx=10, anchor="s")

#LABEL CURSOS
Label1=Label(Frame1, text="1º GITI", fg="navy", font=("BankGothic Lt BT", 18), bg="white")
Label1.grid(row=2, column=2, columnspan=3, sticky="sw",padx=10, pady=10)
Label2=Label(Frame1, text="2º GITI", fg="navy", font=("BankGothic Lt BT", 18), bg="white")
Label2.grid(row=12, column=2, columnspan=3, sticky="w",padx=10, pady=10)
Label3=Label(Frame1, text="3º GITI", fg="navy", font=("BankGothic Lt BT", 18), bg="white")
Label3.grid(row=20, column=2, columnspan=3, sticky="w",padx=10, pady=10)
Label3esp=Label(Frame1, text="3º GITI - ESPECIALIDAD", fg="navy", font=("BankGothic Lt BT", 18), bg="white")
Label3esp.grid(row=26, column=2, columnspan=3, sticky="w",padx=10, pady=10)
Label4=Label(Frame1, text="4º GITI", fg="navy", font=("BankGothic Lt BT", 18), bg="white")
Label4.grid(row=46, column=2, columnspan=3, sticky="w",padx=10, pady=10)
Label4esp=Label(Frame1, text="4º GITI - ESPECIALIDAD", fg="navy", font=("BankGothic Lt BT", 18), bg="white")
Label4esp.grid(row=48, column=2, columnspan=3, sticky="w",padx=10, pady=10)
Labelcomp=Label(Frame1, text="ASIGNATURAS DE COMPETENCIAS", fg="navy", font=("BankGothic Lt BT", 18), bg="white")
Labelcomp.grid(row=85, column=2, columnspan=3, sticky="w",padx=10, pady=10)

#LISTAS DE VARIABLES
variables_boton = [IntVar() for _ in range(90)] #Lista para almacenar las variables boton
seleccion_anterior_ind = [0] * 171 #Lista para las variables "indiferente"
variables = [IntVar() for _ in range(171)] #Lista para almacenar las variables de los 190 turnos
seleccion_anterior = [0] * 171  #Almacena la selección de las casillas de los turnos

#BOTONES ASIGNATURAS 1º
clases1 = []
for i in range(0,30,6):
    clases1.append(df_primero.nombre[i])
for x, clase in enumerate(clases1):
    Boton_1 = Button(Frame1, text=clase, fg="black", font=("Century Gothic", 10), anchor="w", justify="left", bg="white", width=27,relief="ridge")
    Boton_1.grid(row=6+x, column=2, columnspan=4, sticky="w",padx=5, pady=5)
    Boton_1.config(command=lambda x=x, btn=Boton_1: toggle1(x, variables, btn))

#BOTONES ASIGNATURAS 2º
clases2 = []
for i in range(0,41,6):
    clases2.append(df_segundo.nombre[i])
for x, clase in enumerate(clases2):
    Boton_2 = Button(Frame1, text=clase, fg="black", font=("Century Gothic", 10), anchor="w", justify="left", bg="white", width=40,relief="ridge")
    Boton_2.grid(row=13+x, column=2, columnspan=4, sticky="w", padx=5, pady=5)
    Boton_2.config(command=lambda x=x+30, btn=Boton_2: toggle2(x, variables, btn))

#BOTONES ASIGNATURAS 3º
clases3 = []
for i in range(0,24,5):
    clases3.append(df_tercero_comunes.nombre[i])
for x, clase in enumerate(clases3):
    Boton_3 = Button(Frame1, text=clase, fg="black", font=("Century Gothic", 10), anchor="w", justify="left", bg="white", width=35,relief="ridge")
    Boton_3.grid(row=21+x, column=2, columnspan=4, sticky="w", padx=5, pady=5)
    Boton_3.config(command=lambda x=x+72, btn=Boton_3: toggle3(x, variables, btn))

#BOTONES ESPECIALIDAD 3º
clases3esp = df_tercero_especialidad.nombre 
for x, clase in enumerate(clases3esp):
    Boton_3esp = Button(Frame1, text=clase, fg="black", font=("Century Gothic", 10), anchor="w", justify="left", bg="white", width=55,relief="ridge")
    Boton_3esp.grid(row=27+x, column=2, columnspan=4, sticky="w", padx=5, pady=5)
    Boton_3esp.config(command=lambda x=x+97, btn=Boton_3esp: toggle3_esp(x, variables, btn))

#BOTONES ASIGNATURAS 4º
clases4 = []
clases4.append(df_cuarto_comunes.nombre[0])
for x, clase in enumerate(clases4):
    Boton_4 = Button(Frame1, text=clase, fg="black", font=("Century Gothic", 10), anchor="w", justify="left", bg="white", width=45,relief="ridge")
    Boton_4.grid(row=47+x, column=2, columnspan=4, sticky="w", padx=5, pady=5)
    Boton_4.config(command=lambda x=x+116, btn=Boton_4: toggle4(x, variables, btn))

#BOTONES ESPECIALIDAD 4º
clases4esp = df_cuarto_especialidad.nombre
for x, clase in enumerate(clases4esp):
    Boton_4esp = Button(Frame1, text=clase, fg="black", font=("Century Gothic", 10), anchor="w", justify="left", bg="white", width=65,relief="ridge")
    Boton_4esp.grid(row=49+x, column=2, columnspan=4, sticky="w", padx=5, pady=5)
    Boton_4esp.config(command=lambda x=x+121, btn=Boton_4esp: toggle4_esp(x, variables, btn))
    
#BOTONES COMPETENCIAS
clasescomp = df_competencias.nombre
for x, clase in enumerate(clasescomp):
    Boton_comp = Button(Frame1, text=clase, fg="black", font=("Century Gothic", 10), anchor="w", justify="left", bg="white", width=63,relief="ridge")
    Boton_comp.grid(row=86+x, column=2, columnspan=4, sticky="w", padx=5, pady=5)
    Boton_comp.config(command=lambda x=x+157, btn=Boton_comp: toggle_comp(x, variables, btn))
 
#LABEL DE HORAS OCUPADAS
Labelhoras=Label(Frame1, text="Horas ocupadas", fg="navy", font=("BankGothic Lt BT", 25), bg="white")
Labelhoras.grid(row=114, column=2, columnspan=3, sticky="w",padx=0, pady=10)
Labelhoras2=Label(Frame1, text="Introduce las horas que tienes ocupadas:", fg="black", font=("Century Gothic", 10), bg="white")
Labelhoras2.grid(row=115, column=2, columnspan=3, sticky="w",padx=0, pady=0)
Labellunes=Label(Frame1, text="LUNES", fg="royalblue", font=("BankGothic Lt BT", 15), bg="white")
Labellunes.grid(row=116, column=2, sticky="n",padx=0, pady=10)
Labelmartes=Label(Frame1, text="MARTES", fg="royalblue", font=("BankGothic Lt BT", 15), bg="white")
Labelmartes.grid(row=116, column=3, sticky="n",padx=0, pady=10)
Labelmiercoles=Label(Frame1, text="MIÉRCOLES", fg="royalblue", font=("BankGothic Lt BT", 15), bg="white")
Labelmiercoles.grid(row=116, column=4, sticky="n",padx=0, pady=10)
Labeljueves=Label(Frame1, text="JUEVES", fg="royalblue", font=("BankGothic Lt BT", 15), bg="white")
Labeljueves.grid(row=116, column=5, sticky="n",padx=0, pady=10)
Labelviernes=Label(Frame1, text="VIERNES", fg="royalblue", font=("BankGothic Lt BT", 15), bg="white")
Labelviernes.grid(row=116, column=6, sticky="n",padx=0, pady=10)

#LISTA DE VARIABLES
variables_horas = [IntVar() for _ in range(40)]
horario = ["08:30 - 09:35", "09:45 - 10:50", "11:10 - 12:15", "12:25 - 13:30", "15:30 - 16:35", "16:45 - 17:50", "18:10 - 19:15", "19:25 - 20:30"]

#BOTONES DE HORAS
for h, hora in enumerate(horario):
    Boton_lunes = Checkbutton(Frame1, text=hora, variable=variables_horas[h], fg="black", font=("Century Gothic", 10), anchor="n", justify="left", bg="white", width=15)
    Boton_lunes.grid(row=117+h, column=2, sticky="n", padx=5, pady=5)

for h, hora in enumerate(horario):
    Boton_martes = Checkbutton(Frame1, text=hora, variable=variables_horas[h+8], fg="black", font=("Century Gothic", 10), anchor="n", justify="left", bg="white", width=15)
    Boton_martes.grid(row=117+h, column=3, sticky="w", padx=5, pady=5)

for h, hora in enumerate(horario):
    Boton_miercoles = Checkbutton(Frame1, text=hora, variable=variables_horas[h+16], fg="black", font=("Century Gothic", 10), anchor="n", justify="left", bg="white", width=15)
    Boton_miercoles.grid(row=117+h, column=4, sticky="w", padx=5, pady=5)

for h, hora in enumerate(horario):
    Boton_jueves = Checkbutton(Frame1, text=hora, variable=variables_horas[h+24], fg="black", font=("Century Gothic", 10), anchor="n", justify="left", bg="white", width=15)
    Boton_jueves.grid(row=117+h, column=5, sticky="w", padx=5, pady=5)

for h, hora in enumerate(horario):
    Boton_viernes = Checkbutton(Frame1, text=hora, variable=variables_horas[h+32], fg="black", font=("Century Gothic", 10), anchor="n", justify="left", bg="white", width=15)
    Boton_viernes.grid(row=117+h, column=6, sticky="w", padx=5, pady=5)

root.mainloop()