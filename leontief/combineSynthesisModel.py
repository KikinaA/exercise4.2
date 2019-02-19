import numpy as np
from copy import deepcopy
from tkinter import *
from tkinter import messagebox

from sens import sensModel


# ИЗМЕНЕНИЕ СТРУКТУРЫ X и Y
def vectorStructureChanges(changes, changedX, changedY, n, k, X1, X2, Y1, Y2):
    helper = 0
    # подготавливаем вектор с изменениями
    for i in range(0, n):
        changes[i] = i

    for i in range(0, k):
        if changedX[i] != -0.0001:
            for j in range(k, n):
                if changedX[j] == -0.0001:
                    # изменение структуры вектора Х
                    helper = changedX[i]
                    changedX[i] = changedX[j]
                    changedX[j] = helper

                    # изменение структуры вектора Y
                    helper = changedY[i]
                    changedY[i] = changedY[j]
                    changedY[j] = helper

                    # сохранение информации об изменениях
                    changes[i] = j
                    changes[j] = i
                    break

    # создание подвекторов
    for i in range(0, k):
        X1[i] = (changedX[i])
        Y1[i] = (changedY[i])
    j = 0
    for i in range(k, n):
        X2[j] = changedX[i]
        Y2[j] = changedY[i]
        j += 1


# ИЗМЕНЕНИЕ СТРУКТУРЫ МАТРИЦЫ А
def matrixStructureChanges(A, changed1A, changed2A, changes, n, k, A11, A12, A21, A22):
    # меняем местами строки
    for i in range(0, n):
        if i != changes[i]:
            num = int(changes[i])
            for j in range(0, n):
                changed1A[i, j] = A[num, j]

    for i in range(0, n):
        for j in range(0, n):
            changed2A[i, j] = changed1A[i, j]

    # меняем местами столбцы
    for j in range(0, n):
        if j != changes[j]:
            num = int(changes[j])
            for i in range(0, n):
                changed2A[i, j] = changed1A[i, num]

    # создание подматриц
    for i in range(0, k):
        for j in range(0, k):
            A11[i, j] = changed2A[i, j]

    for i in range(0, k):
        l = 0
        for j in range(k, n):
            A12[i, l] = changed2A[i, j]
            l += 1

    l = 0
    for i in range(k, n):
        for j in range(0, k):
            A21[l, j] = changed2A[i, j]
        l += 1

    l = 0
    for i in range(k, n):
        m = 0
        for j in range(k, n):
            A22[l, m] = changed2A[i, j]
            m += 1
        l += 1


# ВЫЧИСЛЕНИЯ
# вычисление Х1
def calculationsX(A11, A12, X2, Y1, k):
    # создание матрицы Е
    E = np.zeros((k, k))
    for i in range(0, k):
        for j in range(0, k):
            if i == j:
                E[i, j] = 1

    answer1 = E - A11
    answer1 = np.array(np.matrix(answer1).I)  # обратная матрица

    answer2 = A12.dot(X2)  # умножение матрицы А12 на вектор Х2
    answer2 = answer2 + Y1  # А12*Х2 + Y1
    answer = answer1.dot(answer2)  # (E - A11)^-1 * (A12*X2 + Y1)

    return answer


# вычисление Y2
def calculationsY(A21, A22, X1, X2, k, n):
    # создание матрицы Е
    E = np.zeros((n-k, n-k))
    for i in range(0, n-k):
        for j in range(0, n-k):
            if i == j:
                E[i, j] = 1

    answer1 = E - A22
    answer1 = answer1.dot(X2)  # (E - A22)*X2
    answer2 = A21.dot(X1)  # A21*X1
    answer = answer1 - answer2  # (E - A22)*X2 - A21*X1

    return answer


# ----------------------------------------------------------------------------------------------------------------------

# ВЫЧИСЛЕНИЕ МАТРИЦЫ W

# Проверка матрицы А на продуктивность
def comCheckA(A, n):
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
    return A

# Основные рассчеты
def comCalc(A, X, Y, Yj, n, W, AXY):
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
    if round(Y_sum) != round(Yj_sum):
        messagebox.showinfo('Ошибка', 'Ошибка основного баланса! Y != Yj')
        sys.exit()

    # Проверка баланса B(1-4)
    for i in range(0, n):
        answer = 0
        for j in range(0, n):
            answer += W[i][j]
        AXY[i] = answer + Y[i]

    for i in range(0, n):
        if round(X[i]) != round(AXY[i]):
            messagebox.showinfo('Ошибка', 'Ошибка второстепенного баланса. X != A*X+Y')
            sys.exit()


# Уменьшение элементов матрицы А
def comReduceA(A, n):
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

    A = comCheckA(A, n)
    return A

# Вывод матрицы в окно пользователя
def comOutput(root, startA, startW, startY, startYj, startAXY, startX, A, n, aText):
    # Создание всех вспомогательных средств, пояснения и обозначения
    wNameLabel = Label(text='Выходная матрица')
    wNameLabel.grid(row=n + 10, column=0)
    nameLabel = Label(text='')
    nameLabel.grid(row=n + 11, column=0)

    # Обозначения по строкам
    for i in range(n + 12, n + n + 12):
        wiNameLabel = Label(text=i - n - 11)
        wiNameLabel.grid(row=i, column=0)
    wiNameLabel = Label(text='Yj')
    wiNameLabel.grid(row=n + n + 13, column=0)

    # Обозначения по столбцам
    for j in range(1, n + 1):
        wjNameLabel = Label(text=j)
        wjNameLabel.grid(row=n + 11, column=j)
    wjNameLabel = Label(text='Y')
    wjNameLabel.grid(row=n + 11, column=n + 1)
    wjNameLabel = Label(text='X')
    wjNameLabel.grid(row=n + 11, column=n + 2)
    wjNameLabel = Label(text='∑W + Y')
    wjNameLabel.grid(row=n + 11, column=n + 3)

    # Вывод значений
    for i in range(n + 12, n + n + 12):
        for j in range(1, n + 1):
            mes = StringVar(root, round(startW[i - n - 12, j - 1], 3))
            wEntry = Entry(root, textvariable=mes)
            wEntry.grid(row=i, column=j)
    for i in range(n + 12, n + n + 12):
        mes = StringVar(root, round(startY[i - n - 12], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=i, column=n + 1)
    mes = StringVar(root, round(startY.sum(), 3))
    wEntry = Entry(root, textvariable=mes)
    wEntry.grid(row=n + n + 13, column=n + 1)
    for i in range(n + 12, n + n + 12):
        mes = StringVar(root, round(startX[i - n - 12], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=i, column=n + 2)
    for i in range(n + 12, n + n + 12):
        mes = StringVar(root, round(startAXY[i - n - 12], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=i, column=n + 3)
    for j in range(1, n + 1):
        mes = StringVar(root, round(startYj[j - 1], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=n + n + 13, column=j)

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
        newALabel.grid(row=n + 12 + i, column=n + 4)

def comProd(root, A, W, Y, Yj, AXY, X, n, prodBtn):
    prodBtn.config(state=DISABLED)

    # Создание вспомогательных средств
    label = Label(text='Изменения\n продуктивности:')
    label.grid(row=n + n + 17, column=0)
    label = Label(text='A = ')
    label.grid(row=n + n + 18, column=0)

    # Матрица А
    label = Label(text='')
    label.grid(row=n + n + 19, column=0)
    for i in range(n + n + 20, n + n + n + 20):
        iNameLabel = Label(text=i - n - n - 19)
        iNameLabel.grid(row=i, column=0)
    for j in range(1, n + 1):
        jNameLabel = Label(text=j)
        jNameLabel.grid(row=n + n + 19, column=j)

    for i in range(n + n + 20, n + n + n + 20):
        for j in range(1, n + 1):
            mes = StringVar(root, round(A[i - n - n - 20][j - 1], 3))
            myEntry = Entry(root, textvariable=mes)
            myEntry.grid(row=i, column=j)

    # Выходная матрица
    # Создание вспомогательных средств
    label = Label(text='')
    label.grid(row=n + n + n + 21, column=0)
    label = Label(text='Выходная матрица')
    label.grid(row=n + n + n + 22, column=0)

    # Обозначения по строкам
    label = Label(text='')
    label.grid(row=n + n + n + 23, column=0)
    for i in range(n + n + n + 24, n + n + n + n + 24):
        wiNameLabel = Label(text=i - n - n - n - 23)
        wiNameLabel.grid(row=i, column=0)
    wiNameLabel = Label(text='Yj')
    wiNameLabel.grid(row=n + n + n + n + 25, column=0)

    # Обозначения по столбцам
    for j in range(1, n + 1):
        wjNameLabel = Label(text=j)
        wjNameLabel.grid(row=n + n + n + 23, column=j)
    wjNameLabel = Label(text='Y')
    wjNameLabel.grid(row=n + n + n + 23, column=n + 1)
    wjNameLabel = Label(text='X')
    wjNameLabel.grid(row=n + n + n + 23, column=n + 2)
    wjNameLabel = Label(text='∑W + Y')
    wjNameLabel.grid(row=n + n + n + 23, column=n + 3)

    # Вывод значений
    for i in range(n + n + n + 24, n + n + n + n + 24):
        for j in range(1, n + 1):
            mes = StringVar(root, round(W[i - n - n - n - 24, j - 1], 3))
            wEntry = Entry(root, textvariable=mes)
            wEntry.grid(row=i, column=j)
    for i in range(n + n + n + 24, n + n + n + n + 24):
        mes = StringVar(root, round(Y[i - n - n - n - 24], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=i, column=n + 1)
    mes = StringVar(root, round(Y.sum(), 3))
    wEntry = Entry(root, textvariable=mes)
    wEntry.grid(row=n + n + n + n + 25, column=n + 1)
    for i in range(n + n + n + 24, n + n + n + n + 24):
        mes = StringVar(root, round(X[i - n - n - n - 24], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=i, column=n + 2)
    for i in range(n + n + n + 24, n + n + n + n + 24):
        mes = StringVar(root, round(AXY[i - n - n - n - 24], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=i, column=n + 3)
    for j in range(1, n + 1):
        mes = StringVar(root, round(Yj[j - 1], 3))
        wEntry = Entry(root, textvariable=mes)
        wEntry.grid(row=n + n + n + n + 25, column=j)

    # расчет оптимального баланса
    sensModel(n, A, X, Y, W)


# ----------------------------------------------------------------------------------------------------------------------

def comModel(root, A, X, Y, n):
    # ПОДГОТОВКА ИСХОДНЫХ ДАННЫХ
    # подготовка переменных
    k = 0  # количество неизвестных данных в векторе X или известных в векторе Y

    changed2A = np.zeros((n, n))
    changes = np.zeros(n)  # вектор с изменениями

    # копии существующих массивов для облегчения рассчетов
    changed1A = deepcopy(A)
    changedX = deepcopy(X)
    changedY = deepcopy(Y)

    # Оригинальные значения матриц
    origX = deepcopy(X)
    origY = deepcopy(Y)

    # получаем значение k
    for i in range(0, n):
        if X[i] == -0.0001:
            k += 1

    # создание подвекторов и подматриц
    X1 = np.zeros(k)
    X2 = np.zeros(n-k)
    Y1 = np.zeros(n-k)
    Y2 = np.zeros(k)

    A11 = np.zeros((k, k))
    A12 = np.zeros((k, n-k))
    A21 = np.zeros((n-k, k))
    A22 = np.zeros((n-k, n-k))

    # решение
    vectorStructureChanges(changes, changedX, changedY, n, k, X1, X2, Y1, Y2)
    matrixStructureChanges(A, changed1A, changed2A, changes, n, k, A11, A12, A21, A22)
    X1 = calculationsX(A11, A12, X2, Y1, k)
    Y2 = calculationsY(A21, A22, X1, X2, k, n)

    # Переворот векторов X, Y и матрицы А
    for i in range(0, k):
        changedX[i] = X1[i]
        changedY[k+i] = Y2[i]

    for i in range(0, n):
        if i != changes[i]:
            X[i] = changedX[int(changes[i])]
            Y[i] = changedY[int(changes[i])]
        else:
            X[i] = changedX[i]
            Y[i] = changedY[i]

    # -------------------

    # Создание необходимых матриц и векторов
    W = np.zeros((n, n))
    AXY = np.zeros(n)
    Yj = np.zeros(n)

    comCalc(A, X, Y, Yj, n, W, AXY)
    # Создание исходных значений
    startA = deepcopy(A)
    startW = deepcopy(W)
    startX = deepcopy(X)
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
            comOutput(root, startA, startW, startY, startYj, startAXY, startX, A, n, aText)

            # Если таблица не продуктивна, создаем кнопку для улучшения продуктивности
            if aText[0] != 'Таблица продуктивна.':
                label = Label(text='')
                label.grid(row=n + n + 14, column=0)
                prodBtn = Button(text='Улучшить\n продуктивность',
                                 command=lambda: comProd(root, A, W, Y, Yj, AXY, X, n, prodBtn))
                prodBtn.grid(row=n + n + 15, column=0)
                label = Label(text='')
                label.grid(row=n + n + 16, column=0)
            else:
                # расчет оптимального баланса
                sensModel(n, A, X, Y, W)
            return 0
        else:
            A = comReduceA(A, n)
            X = deepcopy(origX)
            Y = deepcopy(origY)

            changed2A = np.zeros((n, n))
            changes = np.zeros(n)  # вектор с изменениями

            # копии существующих массивов для облегчения рассчетов
            changed1A = deepcopy(A)
            changedX = deepcopy(X)
            changedY = deepcopy(Y)

            # создание подвекторов и подматриц
            X1 = np.zeros(k)
            X2 = np.zeros(n - k)
            Y1 = np.zeros(k)
            Y2 = np.zeros(n - k)

            A11 = np.zeros((k, k))
            A12 = np.zeros((k, n - k))
            A21 = np.zeros((n - k, k))
            A22 = np.zeros((n - k, n - k))

            vectorStructureChanges(changes, changedX, changedY, n, k, X1, X2, Y1, Y2)
            matrixStructureChanges(A, changed1A, changed2A, changes, n, k, A11, A12, A21, A22)
            X1 = calculationsX(A11, A12, X2, Y1, k)
            Y2 = calculationsY(A21, A22, X1, X2, k, n)

            # Переворот векторов X, Y и матрицы А
            for i in range(0, k):
                changedX[i] = X1[i]
                changedY[k + i] = Y2[i]

            for i in range(0, n):
                if i != changes[i]:
                    X[i] = changedX[int(changes[i])]
                    Y[i] = changedY[int(changes[i])]
                else:
                    X[i] = changedX[i]
                    Y[i] = changedY[i]
            comCalc(A, X, Y, Yj, n, W, AXY)
