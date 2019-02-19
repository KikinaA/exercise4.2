from dataLoad import *
from observabilityModel import obsModel
from synthesisModel import synModel
from combineSynthesisModel import comModel

import numpy as np
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd

# Нажатие кнопок
def click_btn1():
    global calcModel, message
    calcModel = 'obs'
    nChangies()
    btn1.config(state=DISABLED, bg='white')
    btn2.config(state=DISABLED)
    btn3.config(state=DISABLED)

def click_btn2():
    global calcModel
    calcModel = 'syn'
    nChangies()
    btn1.config(state=DISABLED)
    btn2.config(state=DISABLED, bg='white')
    btn3.config(state=DISABLED)

def click_btn3():
    global calcModel
    calcModel = 'com'
    nChangies()
    btn1.config(state=DISABLED)
    btn2.config(state=DISABLED)
    btn3.config(state=DISABLED, bg='white')

# Если любая из кнопок выбора модели нажата
def nChangies():
    global strN, nBtn, loadBtn
    label = Label(text='')
    label.grid(row=1, column=0)

    # Создание лейбла "Количество строк матрицы А"
    nLabel = Label(text='В матрице строк')
    nLabel.grid(row=2, column=0)

    # Создание поля для ввода количества строк
    strN = StringVar()
    nEntry = Entry(textvariable=strN)
    nEntry.grid(row=2, column=1)

    # Создание кнопки "количество строк"
    nBtn = Button(text='Ввести', command=click_nBtn)
    nBtn.grid(row=2, column=2)

    # Создание кнопки загрузки
    loadBtn = Button(text='Загрузить из БД', command=click_loadBtn)
    loadBtn.grid(row=2, column=3)

# Если кнопка "количество строк" нажата
def click_nBtn():
    global n, calcBtn, helpA, helpX, helpY, loadBtn, calcModel
    try: n = int(strN.get())
    except:
        messagebox.showinfo('Ошибка', 'Необходимо ввести число.')
        return
    nBtn.config(state=DISABLED)
    loadBtn.config(state=DISABLED)
    label = Label(text='')
    label.grid(row=3, column=0)

    # Создание всех вспомогательных средств, пояснения и обозначения
    aNameLabel = Label(text='A =')
    aNameLabel.grid(row=4, column=0)
    nameLabel = Label(text='')
    nameLabel.grid(row=5, column=0)

    # МАТРИЦА А
    for i in range(6, n+6):
        iNameLabel = Label(text=i-5)
        iNameLabel.grid(row=i, column=0)

    for j in range(1, n+1):
        jNameLabel = Label(text=j)
        jNameLabel.grid(row=5, column=j)

    # Создание таблицы для ввода
    for i in range(n):
        helpA.append([])
    for i in range(6, n+6):
        for j in range(1, n+1):
            message = StringVar()
            aEntry = Entry(root, textvariable=message)
            helpA[i-6].append(message)
            aEntry.grid(row=i, column=j)

    if calcModel == 'obs':
        # ВЕКТОР X
        xNameLabel = Label(text='X =')
        xNameLabel.grid(row=4, column=n + 1)

        for i in range(6, n + 6):
            message = StringVar()
            xEntry = Entry(root, textvariable=message)
            helpX.append(message)
            xEntry.grid(row=i, column=n + 2)
    elif calcModel == 'syn':
        xNameLabel = Label(text='Y =')
        xNameLabel.grid(row=4, column=n + 1)

        # ВЕКТОР Y
        for i in range(6, n + 6):
            message = StringVar()
            yEntry = Entry(root, textvariable=message)
            helpY.append(message)
            yEntry.grid(row=i, column=n + 2)
    elif calcModel == 'com':
        xNameLabel = Label(text='X =')
        xNameLabel.grid(row=4, column=n + 1)
        xNameLabel = Label(text='Y =')
        xNameLabel.grid(row=4, column=n + 3)

        # ВЕКТОР X
        for i in range(6, n + 6):
            message = StringVar()
            xEntry = Entry(root, textvariable=message)
            helpX.append(message)
            xEntry.grid(row=i, column=n + 2)
        # ВЕКТОР Y
        for i in range(6, n + 6):
            message = StringVar()
            yEntry = Entry(root, textvariable=message)
            helpY.append(message)
            yEntry.grid(row=i, column=n + 4)

    label = Label(text='')
    label.grid(row=n+7, column=0)
    # Кнопка "рассчет"
    calcBtn = Button(text='Рассчитать', padx='10', command=click_calcBtn)
    calcBtn.grid(row=n+8, column=0)

# Если кнопка "рассчитать" нажата
def click_calcBtn():
    global n, helpA, helpX, helpY, calcBtn, calcModel, root

    calcBtn.config(state=DISABLED)
    label = Label(text='')
    label.grid(row=n+9, column=0)

    # Выбор модуля с рассчетами в зависимости от модели
    if calcModel == 'obs':
        A = np.zeros((n, n))
        X = np.zeros(n)

        # Переводим полученные из окна значения в матрицу А и вектор Х
        for i in range(0, n):
            for j in range(0, n):
                A[i, j] = float(helpA[i][j].get())
        for i in range(0, n):
            X[i] = float(helpX[i].get())

        obsModel(root, A, X, n)
    elif calcModel == 'syn':
        A = np.zeros((n, n))
        Y = np.zeros(n)

        # Переводим полученные из окна значения в матрицу А и вектор Х
        for i in range(0, n):
            for j in range(0, n):
                A[i, j] = float(helpA[i][j].get())
        for i in range(0, n):
            Y[i] = float(helpY[i].get())

        synModel(root, A, Y, n)
    elif calcModel == 'com':
        A = np.zeros((n, n))
        X = np.zeros(n)
        Y = np.zeros(n)

        # Переводим полученные из окна значения в матрицу А и вектор Х
        for i in range(0, n):
            for j in range(0, n):
                A[i, j] = float(helpA[i][j].get())


        for i in range(0, n):
            try:
                X[i] = float(helpX[i].get())
            except:
                X[i] = -0.0001
            try:
                Y[i] = float(helpY[i].get())
            except:
                Y[i] = -0.0001

        comModel(root, A, X, Y, n)
    else:
        messagebox.showinfo('Ошибка', 'Не выбрана модель.')

# ----------------------------------------------------------------------------------------------------------------------
# Если кнопка "загрузить" нажата
def click_loadBtn():
    global n, calcModel
    # Открытие файла
    file_name = fd.askopenfilename()
    if calcModel == 'obs':
        try: fileA, fileX, n = obsDataLoad(file_name)
        except:
            messagebox.showinfo('Ошибка', 'Файл не выбран.')
            return 0
        fileY = np.zeros((n, n))
        dataInput(fileA, fileX, fileY)

    elif calcModel == 'syn':
        try: fileA, fileY, n = synDataLoad(file_name)
        except:
            messagebox.showinfo('Ошибка', 'Файл не выбран.')
            return 0
        fileX = np.zeros((n, n))
        dataInput(fileA, fileX, fileY)

    elif calcModel == 'com':
        try: fileA, fileX, fileY, n = comDataLoad(file_name)
        except:
            messagebox.showinfo('Ошибка', 'Файл не выбран.')
            return 0
        dataInput(fileA, fileX, fileY)

def dataInput(fileA, fileX, fileY):
    global n, calcBtn, helpA, helpX, helpY, loadBtn, calcModel
    nBtn.config(state=DISABLED)
    loadBtn.config(state=DISABLED)
    label = Label(text='')
    label.grid(row=3, column=0)

    # Создание всех вспомогательных средств, пояснения и обозначения
    aNameLabel = Label(text='A =')
    aNameLabel.grid(row=4, column=0)
    nameLabel = Label(text='')
    nameLabel.grid(row=5, column=0)

    # МАТРИЦА А
    for i in range(6, n + 6):
        iNameLabel = Label(text=i - 5)
        iNameLabel.grid(row=i, column=0)

    for j in range(1, n + 1):
        jNameLabel = Label(text=j)
        jNameLabel.grid(row=5, column=j)

    # Создание таблицы для ввода
    for i in range(n):
        helpA.append([])
    for i in range(6, n + 6):
        for j in range(1, n + 1):
            message = StringVar(root, fileA[i-6][j-1])
            aEntry = Entry(root, textvariable=message)
            helpA[i - 6].append(message)
            aEntry.grid(row=i, column=j)

    if calcModel == 'obs':
        # ВЕКТОР X
        xNameLabel = Label(text='X =')
        xNameLabel.grid(row=4, column=n + 1)

        for i in range(6, n + 6):
            message = StringVar(root, fileX[i-6])
            xEntry = Entry(root, textvariable=message)
            helpX.append(message)
            xEntry.grid(row=i, column=n + 2)
    elif calcModel == 'syn':
        xNameLabel = Label(text='Y =')
        xNameLabel.grid(row=4, column=n + 1)

        # ВЕКТОР Y
        for i in range(6, n + 6):
            message = StringVar(root, fileY[i-6])
            yEntry = Entry(root, textvariable=message)
            helpY.append(message)
            yEntry.grid(row=i, column=n + 2)
    elif calcModel == 'com':
        xNameLabel = Label(text='X =')
        xNameLabel.grid(row=4, column=n + 1)
        xNameLabel = Label(text='Y =')
        xNameLabel.grid(row=4, column=n + 3)

        # ВЕКТОР X
        for i in range(6, n + 6):
            message = StringVar(root, fileX[i-6])
            xEntry = Entry(root, textvariable=message)
            helpX.append(message)
            xEntry.grid(row=i, column=n + 2)
        # ВЕКТОР Y
        for i in range(6, n + 6):
            message = StringVar(root, fileY[i-6])
            yEntry = Entry(root, textvariable=message)
            helpY.append(message)
            yEntry.grid(row=i, column=n + 4)

    label = Label(text='')
    label.grid(row=n + 7, column=0)
    # Кнопка "рассчет"
    calcBtn = Button(text='Рассчитать', padx='10', command=click_calcBtn)
    calcBtn.grid(row=n + 8, column=0)

if __name__ == '__main__':
    n = 0
    calcModel = 'None'
    helpA = []
    helpX = []
    helpY = []

    # Создание окна
    root = Tk()
    root.title('Модели Леонтьева')
    root.geometry('1600x900')

    # Создание кнопок выбора модели
    btn1 = Button(text='Модель\n наблюдаемости', command=click_btn1, padx='10', pady='9')
    btn1.grid(row=0, column=0)
    btn2 = Button(text='Модель\n синтеза', command=click_btn2, padx='35', pady='9')
    btn2.grid(row=0, column=1)
    btn3 = Button(text='Модель\n комбинированного\n синтеза', command=click_btn3, padx='5', pady='1.5')
    btn3.grid(row=0, column=2)

    root.mainloop()