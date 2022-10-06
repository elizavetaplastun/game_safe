import pygame
import random
from tkinter import *
import tkinter
import json
from tkinter.ttk import Combobox


def matrix_generator(n):
    matrix = [[0 for i in range(n)] for i in range(n)]
    if n % 2 == 0:
        for i in range(n):
            for j in range(n):
                matrix[i][j] = random.randint(0, 1)
    else:
        hah = random.randint(5, 20)
        for i in range(hah):
            r = random.randint(0, n - 1)
            c = random.randint(1, n - 1)
            matrix = click(r, c, matrix)
    if check(matrix):
        matrix = matrix_generator(n)
    return matrix


def check(matrix):
    n = len(matrix[0])
    for i in range(n):
        if len(set(matrix[i])) > 1:
            return False
        if i == n - 1:
            return True


def click(column, row, matrix):
    n = len(matrix[0])
    for i in range(n):
        if matrix[i][row]:
            matrix[i][row] = 0
        else:
            matrix[i][row] = 1
        if matrix[column][i] and i != row:
            matrix[column][i] = 0
        elif i != row:
            matrix[column][i] = 1
    return matrix


def start_page():
    def clicked():
        n = int(inf.get())
        matrix = matrix_generator(n)
        window.destroy()
        game(matrix)

    def clicked_old():
        window.destroy()
        old_game()

    window = Tk()
    window.title("")
    window.geometry('700x300')
    text = Label(window, text="укажите размер поля")
    text.pack(expand=True)
    inf = Entry(window, width=20)
    inf.pack(expand=True)
    btn = tkinter.Button(text="начать игру", command=clicked)
    btn.pack(expand=True)
    btn1 = tkinter.Button(text="продолжить игру", command=clicked_old)
    btn1.pack(expand=True)

    window.mainloop()


def old_game():
    def clicked():
        with open('package.json') as f:
            data = json.load(f)
            n = combo1.get()
            matrix = data[n]
        with open('package.json', 'w') as f:
            f.write(json.dumps(data))
        window.destroy()
        game(matrix)

    def new_game():
        window.destroy()
        start_page()

    def delite_game():
        with open('package.json') as f:
            data = json.load(f)
            n = combo1.get()
            data.pop(n)
        with open('package.json', 'w') as f:
            f.write(json.dumps(data))
        window.destroy()
        old_game()

    with open('package.json') as f:
        data = json.load(f)

    window = Tk()
    window.title("")
    window.geometry('700x300')
    btn3 = tkinter.Button(text="начать новую игру", command=new_game)
    btn3.pack(expand=True)
    text = Label(window, text="выберите файл")
    text.pack(expand=True)

    combo1 = Combobox(window)
    combo1.pack(expand=True)
    combo1['values'] = list(data.keys())

    text1 = Label(window, text="выберите действие")
    text1.pack(expand=True)

    btn1 = tkinter.Button(text="продолжить игру", command=clicked)
    btn1.pack(expand=True)

    btn2 = tkinter.Button(text="удалить файл игры", command=delite_game)
    btn2.pack(expand=True)

    window.mainloop()


def winn_page():
    def clicked():
        window2.destroy()

    def clicked_again():
        window2.destroy()
        start_page()

    window2 = Tk()
    window2.title("")
    window2.geometry('700x100')
    text = Label(window2, text="ты решил головоломку братьев пилотов!")
    text.pack(expand=True)
    btn1 = tkinter.Button(text="выйти", command=clicked)
    btn1.pack(expand=True)
    btn2 = tkinter.Button(text="новая игра", command=clicked_again)
    btn2.pack(expand=True)
    window2.mainloop()


def exit(matrix):
    def clicked():
        window2.destroy()

    def clicked_again():
        window2.destroy()
        start_page()

    def clicked_save():
        with open('package.json') as f:
            data = json.load(f)
            name = name_.get()
            data[name] = matrix
        with open('package.json', 'w') as f:
            f.write(json.dumps(data))

    window2 = Tk()
    window2.title("")
    window2.geometry('700x200')
    text = Label(window2, text="сохранить игру?")
    text.pack(expand=True)
    name = Label(window2, text="введите название файла")
    name.pack(expand=True)
    name_ = Entry(window2, width=20)
    name_.pack(expand=True)
    btn1 = tkinter.Button(text="сохранить игру", command=clicked_save)
    btn1.pack(expand=True)
    btn1 = tkinter.Button(text="выйти", command=clicked)
    btn1.pack(expand=True)
    btn2 = tkinter.Button(text="попробовать снова", command=clicked_again)
    btn2.pack(expand=True)
    window2.mainloop()


def game(matrix):
    n = len(matrix[0])
    pygame.init()
    margin = 1
    size = (800, 800)
    block_size = (800 - (n + 1) * margin) / n
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption("сейф братьев пилотов")
    bg = pygame.image.load("img/bg.png")
    bg = pygame.transform.scale(bg, (800, 800))
    bg_rect = bg.get_rect()
    gor = pygame.image.load("img/1.png")
    gor = pygame.transform.scale(gor, (block_size, block_size))
    ver = pygame.image.load("img/0.png")
    ver = pygame.transform.scale(ver, (block_size, block_size))
    while True:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(matrix)
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                column = int(x_mouse // (margin + block_size))
                row = int(y_mouse // (margin + block_size))
                matrix = click(column, row, matrix)
        winn = check(matrix)
        if winn:
            pygame.quit()
            winn_page()
        screen.blit(bg, bg_rect)
        for col in range(n):
            for row in range(n):
                x = col * block_size + margin * (col + 1)
                y = row * block_size + margin * (row + 1)
                if matrix[col][row]:
                    screen.blit(gor, (x, y))
                else:
                    screen.blit(ver, (x, y))
        pygame.display.flip()


start_page()
