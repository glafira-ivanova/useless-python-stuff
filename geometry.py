# -*- coding: utf-8 -*-

__author__ = 'Glafira Ivanova'

"""
Это пример небольшой программы для рисования кругов и квадратов.
Вам нужно на основе этой программы сделать небольшую "танцевальную" сценку с
использованием кругов, квардратов и треугольников. Сделать всё это нужно в
объектно ориентированном стиле.

Какие классы нужно реализовать:

-Многоугольник(на его основе сделать квадрат и правильный треугольник)
--класс должне уметь отрисовывать себя
--премещаться в некоторм направлении заданом координатами x, y
--увеличивать(необязательно)
--поворачивать(необязательно)

-Квардрат(наследуется от многоугольника)
--метод __init__ принимает координаты середины, ширину и цвет

-Треугольник(наследуется от многоугольника)
--метод __init__ принимает координаты середины, длинну грани и цвет

-Круг
--метод __init__ принимает координаты середины, радиус и цвет
--класс должне уметь отрисовывать себя
--премещаться в некоторм направлении заданом координатами x, y
--увеличивать(необязательно)

Также рекомендую создать вспомогательный сласс Vector для представления
точек на плоскости и различных операций с ними - сложение, умножение на число,
вычитаные.


Из получившихся классов нужно составить какую-нибудь динамическую сцену.
Смотрите пример example.gif
"""

import turtle
import time
import random
from math import sqrt, sin, cos, pi


# def draw_rect(ttl):
#     x = random.randint(-200, 200) #получаем случайные координаты
#     y = random.randint(-200, 200)
#
#     ttl.color('red') #устанавливаем цвет линии
#     ttl.penup() # убираем "ручку" от холста, чтобы переместить в нужное место
#     ttl.setpos(x, y) # перемещаем на первую вершину
#     ttl.pendown() #опускаем ручку обратно
#     ttl.goto(x + 50, y) #проводим линии для сторон четырёхугольника
#     ttl.goto(x + 50, y + 50)
#     ttl.goto(x, y + 50)
#     ttl.goto(x, y)
#
# def draw_circle(ttl):
#     x = random.randint(-200, 200) #получаем случайные координаты
#     y = random.randint(-200, 200)
#
#     ttl.color('violet') #устанавливаем цвет линии
#     ttl.penup() # убираем "ручку" от холста, чтобы переместить в нужное место
#     ttl.setpos(x, y) # перемещаем в "основание" - это будет самая низкая точка
#     ttl.pendown() #опускаем ручку обратно
#
#     ttl.circle(25) #рисуем круг радиуса 25


class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self * (1 / other)

    def __repr__(self):
        return 'Vector({0}, {1})'.format(self.x, self.y)

    def __iter__(self):
        for coord in [self.x, self.y]:
            yield coord

    def move(self, x, y):
        self.x += x
        self.y += y

    def enlarge(self, times):
        self.x *= times
        self.y *= times

    def rotate(self, angle):
        new_x = self.x * cos(angle) + self.y * sin(angle)
        new_y = -self.x * sin(angle) + self.y * cos(angle)
        self.x = new_x
        self.y = new_y

class Figure(object):
    def __init__(self, x, y, color='black'):
        self.center = Vector(x, y)
        self.color = color

    def move(self, x, y):
        self.center.move(x, y)


class Poligon(Figure):
    def __init__(self, x, y, vertices, color='red'):
        """
        :param vertices: list of (x, y) pairs relative to center
        """
        Figure.__init__(self, x, y, color)
        self.vertices = [Vector(ver[0], ver[1]) for ver in vertices]

    def draw(self, ttl):
        ttl.color(self.color)
        ttl.penup()
        last_ver = self.vertices[-1] + self.center
        ttl.setpos(*last_ver)
        ttl.pendown()
        for ver in self.vertices:
            ver = ver + self.center
            ttl.goto(*ver)

    def enlarge(self, times):
        for v in self.vertices:
            v.enlarge(times)

    def rotate(self, angle):
        for v in self.vertices:
            v.rotate(angle)


    def __repr__(self):
        return '{0}: {1}'.format(self.__class__.__name__, ', '.join(repr(v) for v in self.vertices))

class Square(Poligon):
    def __init__(self, x, y, width, color='red'):
        hw = width / 2
        vertices = [(-hw, hw), (hw, hw), (hw, -hw), (-hw, -hw)]
        Poligon.__init__(self, x, y, vertices, color)


class Triangle(Poligon):
    def __init__(self, x, y, side, color='blue'):
        h = sqrt(3) * side / 2
        vertices = [(0, 2 * h / 3 ), (side / 2, -h / 3), (-side / 2, -h / 3)]
        Poligon.__init__(self, x, y, vertices, color)


class Circle(Figure):
    def __init__(self, x, y, radius, color='yellow'):
        Figure.__init__(self, x, y, color)
        self.radius = radius

    def draw(self, ttl):
        ttl.color(self.color)
        ttl.penup()
        pos = self.center + Vector(0, -self.radius)
        ttl.setpos(*pos)
        ttl.pendown()
        ttl.circle(self.radius)

    def enlarge(self, times):
        self.radius *= times


def main():
    turtle.tracer(0, 0)
    turtle.hideturtle()
    ttl = turtle.Turtle()
    ttl.hideturtle()
    ttl.clear()

    ss = 15
    star = Poligon(0, 0, [(-ss * 5, 0), (-ss, ss), (0, ss * 5), (ss, ss), (ss * 5, 0), (ss, -ss), (0, -ss * 5), (-ss, -ss) ], 'green')
    circle = Circle(0, 0, 100)
    triangles = [
        Triangle(-200, 200, 50),
        Triangle(200, 200, 50),
        Triangle(200, -200, 50),
        Triangle(-200, -200, 50)
    ]
    square = Square(-200, 200, 50)
    figs = [star, circle, square] + triangles

    while True:
        for square_direction in [(1, 0), (0, -1), (-1, 0), (0, 1)]:

            for step in range(20):
                time.sleep(0.2)
                ttl.clear()

                star.rotate(pi / 18)
                for tr in triangles:
                    tr.rotate((-1) ** step * pi / 4)
                if step // 10 == 0:
                    circle.radius -= 10
                else:
                    circle.radius += 10
                square.rotate(pi / 6)
                square.move(20 * square_direction[0], 20 * square_direction[1])

                for fig in figs:
                    fig.draw(ttl)
                turtle.update()


if __name__ == '__main__':
    main()
