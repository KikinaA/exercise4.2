import numpy as np
from copy import deepcopy
from tkinter import *
from tkinter import messagebox

import matplotlib.pyplot as plt
import pylab

#-------------------------------------------------------------------------
# ИЗМЕНЕНИЕ СТРУКТУРЫ X и Y
def sensVectorStructureChanges(changes, changedX, changedY, n, k, X1, X2, Y1, Y2):
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
def sensMatrixStructureChanges(A, changed1A, changed2A, changes, n, k, A11, A12, A21, A22):
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
def sensCalculationsX(A11, A12, X2, Y1, k):
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
    if k == 1:
        answer2 = np.array([answer2])
    answer = answer1.dot(answer2)  # (E - A11)^-1 * (A12*X2 + Y1)
    if k == 1:
        answer = np.sum(answer)
        answer = np.array([answer])

    return answer


# вычисление Y2
def sensCalculationsY(A21, A22, X1, X2, k, n):
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
def sensComCheckA(A, n):
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
def sensComCalc(A, X, Y, Yj, n, W, AXY):
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

# ----------------------------------------------------------------------------------------------------------------------

def sensComModel(A, X, Y, n):
    # ПОДГОТОВКА ИСХОДНЫХ ДАННЫХ
    # подготовка переменных
    k = 0  # количество неизвестных данных в векторе X или известных в векторе Y

    changed2A = np.zeros((n, n))
    changes = np.zeros(n)  # вектор с изменениями

    # копии существующих массивов для облегчения рассчетов
    changed1A = deepcopy(A)
    changedX = deepcopy(X)
    changedY = deepcopy(Y)

    # получаем значение k
    for i in range(0, n):
        if X[i] == -0.0001:
            k += 1

    # создание подвекторов и подматриц
    X1 = np.zeros(k)
    X2 = np.zeros(n-k)
    Y1 = np.zeros(k)
    Y2 = np.zeros(n-k)

    A11 = np.zeros((k, k))
    A12 = np.zeros((k, n-k))
    A21 = np.zeros((n-k, k))
    A22 = np.zeros((n-k, n-k))

    # решение
    sensVectorStructureChanges(changes, changedX, changedY, n, k, X1, X2, Y1, Y2)
    sensMatrixStructureChanges(A, changed1A, changed2A, changes, n, k, A11, A12, A21, A22)
    X1 = sensCalculationsX(A11, A12, X2, Y1, k)
    Y2 = sensCalculationsY(A21, A22, X1, X2, k, n)

    # Переворот векторов X, Y и матрицы А
    for i in range(0, k):
        changedX[i] = X1[i]
    for i in range(0, n-k):
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

    sensComCalc(A, X, Y, Yj, n, W, AXY)
    print('-----------------------------------')
    print(X)
    print(Y)
    print(W)
    print(sum(Y) / (sum(sum(W))))
    return sum(Y)/(sum(sum(W)))

#-------------------------------------------------------------------------


def sensModel(n, A, X, Y, W):
    R = np.zeros(n)
    delta = np.zeros(n)
    R0 = sum(Y)/(sum(sum(W)))  # Находим изначальное R

    # Находим значения дельта
    for i in range(0, n):
        Xchange = deepcopy(X)  # Переносим значения в переменные, которые можно изменять
        Ychange = deepcopy(Y)
        Achange = deepcopy(A)
        Ychange[i] = Y[i] + 1
        Xchange[i] = -0.0001
        for j in range(0, n):
            if i != j:
                Ychange[j] = -0.0001
        R[i] = sensComModel(Achange, Xchange, Ychange, n)

    for i in range(0, n):
        delta[i] = R[i] - R0

    # Ищем максимальную и минимальную дельты
    maxDelta = np.max(delta)
    minDelta = np.min(delta)

    # Находим положение минимального и максимального y
    maxI = 0
    minI = 0
    for i in range(0, n):
        if delta[i] == maxDelta:
            maxI = i
        if delta[i] == minDelta:
            minI = i

    lastX = deepcopy(X)
    lastY = deepcopy(Y)
    minNum = (lastY[minI]*20)/100  # Ищем изменение минимального и максимального числа(оно же 20% от минимального)
    graphR = np.zeros(int((lastY[minI]/minNum))+1)  # Создаем матрицу со значениями для графика

    # Редактируем X и Y для расчета данных R
    j = 0
    while (lastY[minI]-minNum) > 0:
        for i in range(0, n):
            if i == minI:
                lastY[i] = lastY[i] - minNum
                lastX[i] = -0.0001
            elif i == maxI:
                lastY[i] = lastY[i] + minNum
                lastX[i] = -0.0001
            else:
                lastY[i] = -0.0001

        graphR[j] = sensComModel(A, lastX, lastY, n)
        j += 1

    # Редактируем полученные значения для вывода на график
    yR = []
    yR.append(R0)
    ySize = 1
    for i in range(0, graphR.size):
        if graphR[i] != 0:
            ySize += 1
            yR.append(graphR[i])

    # Нарисуем график
    plt.plot(yR, marker='o')
    plt.grid(True)
    for i in range(0, ySize):
        plt.text(i, yR[i], yR[i])
    plt.show()
