import numpy as np
import json

def obsDataLoad(file_name):
    # Загрузка данных из файла в словарь
    newDict = dict()
    try:
        newDict = json.load(open(file_name))
    except:
        return 0
    # Перенос данных из словаря в раздельные списки
    newA = newDict['Нормативная матрица']
    newX = newDict['Входной продукт']
    n = int(len(newX))  # Поиск размерности матриц

    # Перенос данных в объекты для работы с матрицами
    A = np.zeros((n, n))
    X = np.zeros(n)
    for i in range(0, n):
        X[i] = newX[i]
        for j in range(0, n):
            A[i][j] = newA[i][j]

    return A, X, n

def synDataLoad(file_name):
    # Загрузка данных из файла в словарь
    newDict = dict()
    try:
        newDict = json.load(open(file_name))
    except:
        return 0
    # Перенос данных из словаря в раздельные списки
    newA = newDict['Нормативная матрица']
    newY = newDict['Выходной продукт']
    n = int(len(newY))  # Поиск размерности матриц

    # Перенос данных в объекты для работы с матрицами
    A = np.zeros((n, n))
    Y = np.zeros(n)
    for i in range(0, n):
        Y[i] = newY[i]
        for j in range(0, n):
            A[i][j] = newA[i][j]

    return A, Y, n

def comDataLoad(file_name):
    # Загрузка данных из файла в словарь
    newDict = dict()
    try:
        newDict = json.load(open(file_name))
    except:
        return 0
    # Перенос данных из словаря в раздельные списки
    newA = newDict['Нормативная матрица']
    newX = newDict['Входной продукт']
    newY = newDict['Выходной продукт']
    n = int(len(newX))  # Поиск размерности матриц

    # Перенос данных в объекты для работы с матрицами
    A = np.zeros((n, n))
    X = np.zeros(n)
    Y = np.zeros(n)
    for i in range(0, n):
        X[i] = newX[i]
        Y[i] = newY[i]
        for j in range(0, n):
            A[i][j] = newA[i][j]

    return A, X, Y, n
