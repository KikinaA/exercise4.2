import numpy as np
from copy import deepcopy
from tkinter import *
from tkinter import messagebox

# Проверка матрицы А на продуктивность
def obsCheckA(A, n):
    for j in range(0, n):
        sumNum = 0
        for i in range(0, n):
            sumNum += A[i][j]
        # Если сумма значений столбца больше или равна единице
        if sumNum > 1.0 or sumNum == 1.0:
            # Поиск максимального числа в столбце
            maxNum = A[0, 0]
            for l in range(0, n):
                if maxNum < A[l][j]:
                    maxNum = A[l][j]

            # Уменьшаем значение максимального числа так, чтобы сумма элементов столбца была меньше 1
            for i in range(0, n):
                if maxNum == A[i, j]:
                    sumNum = sumNum - 1
                    A[i, j] = A[i, j] - sumNum - 0.1

# Основные рассчеты
def obsCalc(A, X, Y, Yj, E, n, W, AXY):
    c = E - A
    # Рассчет Y = (E - A)*X
    for i in range(0, n):
        y = c[i] * X
        y = sum(y)
        Y[i] = y

    # Рассчет W[i][j] = A[i][j]*X[j]
    for i in range(0, n):
        for j in range(0, n):
            W[i, j] = A[i][j] * X[j]

    # Рассчет Yj
    for j in range(0, n):
        num = 0
        for i in range(0, n):
            num += W[i][j]
        Yj[j] = X[j] - num

    # Проверка баланса B0
    Y_sum = 0
    Yj_sum = 0
    for i in range(0, n):
        Y_sum += Y[i]
        Yj_sum += Yj[i]
    if Y_sum != Yj_sum:
        messagebox.showinfo('Ошибка', 'Ошибка основного баланса! Y != Yj')
        sys.exit()

    # Проверка баланса B(1-4)
    for i in range(0, n):
        answer = 0
        for j in range(0, n):
            answer += W[i][j]
        AXY[i] = answer + Y[i]

    for i in range(0, n):
        if X[i] != AXY[i]:
            messagebox.showinfo('Ошибка', 'Ошибка второстепенного баланса. X != A*X+Y')
            sys.exit()


# Уменьшение элементов матрицы А
def obsReduceA(A, n):
    row = 0
    column = 0
    answer = 0
    maxNum = np.zeros(n)

    # Вычисление суммы столбцов матрицы А
    for j in range(0, n):
        num = 0
        for i in range(0, n):
            num += A[i][j]
        maxNum[j] = num

    # Вычисление столбца с максимальной суммой.
    # Заполнение матрицы с максимальными значениями значениями данного столбца
    for j in range(0, n):
        if maxNum[j] == max(maxNum):
            column = j
            for i in range(0, n):
                maxNum[i] = A[i][j]

    # Вычисление максимального элемента в максимальном столбце
    for i in range(0, n):
        if maxNum[i] == max(maxNum):
            row = i
            answer = maxNum[i]

    # Уменьшение максимального элемента
    answer = answer - 0.1
    A[row][column] = answer

    obsCheckA(A, n)

# Вывод матрицы в окно пользователя
def obsOutput(root, startA, startW, startY, startYj, startAXY, X, A, n, aText):
    # Создание всех вспомогательных средств, пояснения и обозначения
    wNameLabel = Label(text='Выходная матрица')
    wNameLabel.grid(row=n+10, column=0)
    nameLabel = Label(text='')
    nameLabel.grid(row=n+11, column=0)

    # Обозначения по строкам
    for i in range(n+12, n+n+12):
        wiNameLabel = Label(text=i-n-11)
        wiNameLabel.grid(row=i, column=0)
    wiNameLabel = Label(text='Yj')
    wiNameLabel.grid(row=n+n+13, column=0)

    # Обозначения по столбцам
    for j in range(1, n+1):
        wjNameLabel = Label(text=j)
        wjNameLabel.grid(row=n+11, column=j)
    wjNameLabel = Label(text='Y')
    wjNameLabel.grid(row=n+11, column=n+1)
    wjNameLabel = Label(text='X')
    wjNameLabel.grid(row=n+11, column=n+2)
    wjNameLabel = Label(text='∑W + Y')
    wjNameLabel.grid(row=n+11, column=n+3)

    # Вывод значений
    for i in range(n+12, n+n+12):
        for j in range(1, n+1):
            mes = StringVar(root, round(startW[i-n-12, j-1], 3))
            wEntry = Entry(root, textvariable=mes)
            wEntry.grid(row=i, column=j)
    for i in range(n+12, n+n+12):
        mes = StringVar(root, round(startY[i-n-12], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=i, column=n+1)
    mes = StringVar(root, round(startY.sum(), 3))
    wEntry = Entry(root, textvariable=mes)
    wEntry.grid(row=n+n+13, column=n+1)
    for i in range(n+12, n+n+12):
        mes = StringVar(root, round(X[i-n-12], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=i, column=n+2)
    for i in range(n+12, n+n+12):
        mes = StringVar(root, round(startAXY[i-n-12], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=i, column=n+3)
    for j in range(1, n+1):
        mes = StringVar(root, round(startYj[j - 1], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=n+n+13, column=j)

    # Вывод информации об изменении А
    myCheck = 1
    for i in range(0, n):
        for j in range(0, n):
            if A[i, j] != startA[i, j]:
                aText.append('Необходимо уменьшить A[{0}][{1}], на {2}.'.format(i + 1, j + 1, startA[i, j] - A[i, j]))
                myCheck += 1
    if not aText:
        aText.append('Таблица продуктивна.')
    for i in range(0, len(aText)):
        newALabel = Label(root, text=aText[i])
        newALabel.grid(row=n+12+i, column=n+4)

# Вывод измененной продуктивности
def obsProd(root, A, W, Y, Yj, AXY, X, n, prodBtn):
    prodBtn.config(state=DISABLED)

    # Создание вспомогательных средств
    label = Label(text='Изменения\n продуктивности:')
    label.grid(row=n+n+17, column=0)
    label = Label(text='A = ')
    label.grid(row=n+n+18, column=0)

    # Матрица А
    label = Label(text='')
    label.grid(row=n+n+19, column=0)
    for i in range(n+n+20, n+n+n+20):
        iNameLabel = Label(text=i-n-n-19)
        iNameLabel.grid(row=i, column=0)
    for j in range(1, n+1):
        jNameLabel = Label(text=j)
        jNameLabel.grid(row=n+n+19, column=j)

    for i in range(n+n+20, n+n+n+20):
        for j in range(1, n+1):
            mes = StringVar(root, round(A[i-n-n-20][j-1], 3))
            myEntry = Entry(root, textvariable=mes)
            myEntry.grid(row=i, column=j)

    # Выходная матрица
    # Создание вспомогательных средств
    label = Label(text='')
    label.grid(row=n+n+n+21, column=0)
    label = Label(text='Выходная матрица')
    label.grid(row=n+n+n+22, column=0)

    # Обозначения по строкам
    label = Label(text='')
    label.grid(row=n+n+n+23, column=0)
    for i in range(n+n+n+24, n+n+n+n+24):
        wiNameLabel = Label(text=i-n-n-n-23)
        wiNameLabel.grid(row=i, column=0)
    wiNameLabel = Label(text='Yj')
    wiNameLabel.grid(row=n+n+n+n+25, column=0)

    # Обозначения по столбцам
    for j in range(1, n+1):
        wjNameLabel = Label(text=j)
        wjNameLabel.grid(row=n+n+n+23, column=j)
    wjNameLabel = Label(text='Y')
    wjNameLabel.grid(row=n+n+n+23, column=n+1)
    wjNameLabel = Label(text='X')
    wjNameLabel.grid(row=n+n+n+23, column=n+2)
    wjNameLabel = Label(text='∑W + Y')
    wjNameLabel.grid(row=n+n+n+23, column=n+3)

    # Вывод значений
    for i in range(n+n+n+24, n+n+n+n+24):
        for j in range(1, n+1):
            mes = StringVar(root, round(W[i-n-n-n-24, j-1], 3))
            wEntry = Entry(root, textvariable=mes)
            wEntry.grid(row=i, column=j)
    for i in range(n+n+n+24, n+n+n+n+24):
        mes = StringVar(root, round(Y[i-n-n-n-24], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=i, column=n+1)
    mes = StringVar(root, round(Y.sum(), 3))
    wEntry = Entry(root, textvariable=mes)
    wEntry.grid(row=n+n+n+n+25, column=n+1)
    for i in range(n+n+n+24, n+n+n+n+24):
        mes = StringVar(root, round(X[i-n-n-n-24], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=i, column=n+2)
    for i in range(n+n+n+24, n+n+n+n+24):
        mes = StringVar(root, round(AXY[i-n-n-n-24], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=i, column=n+3)
    for j in range(1, n+1):
        mes = StringVar(root, round(Yj[j-1], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=n+n+n+n+25, column=j)

# Основной модуль рассчетов
def obsModel(root, A, X, n):
    # Создание необходимых матриц и векторов
    W = np.zeros((n, n))
    AXY = np.zeros(n)
    Y = np.zeros(n)
    Yj = np.zeros(n)
    E = np.eye(n, n)

    obsCalc(A, X, Y, Yj, E, n, W, AXY)
    # СОздание исходных значений
    startA = deepcopy(A)
    startW = deepcopy(W)
    startY = deepcopy(Y)
    startYj = deepcopy(Yj)
    startAXY = deepcopy(AXY)

    # Проверка продуктивности
    while 1:
        myCheck = 0
        for i in range(0, n):
            if Y[i] <= 0 or Yj[i] <= 0:
                myCheck = 1
        if myCheck == 0:
            # Вывод полученных значений
            aText = []
            obsOutput(root, startA, startW, startY, startYj, startAXY, X, A, n, aText)

            # Если таблица не продуктивна, создаем кнопку для улучшения продуктивности
            if aText[0] != 'Таблица продуктивна.':
                label = Label(text='')
                label.grid(row=n+n+14, column=0)
                prodBtn = Button(text='Улучшить\n продуктивность',
                                 command=lambda:obsProd(root, A, W, Y, Yj, AXY, X, n, prodBtn))
                prodBtn.grid(row=n+n+15, column=0)
                label = Label(text='')
                label.grid(row=n+n+16, column=0)
            return 0
        else:
            obsReduceA(A, n)
            obsCalc(A, X, Y, Yj, E, n, W, AXY)
