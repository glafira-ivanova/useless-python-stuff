#!/usr/bin/python3

__author__ = 'Glafira Ivanova'

from random import randint, shuffle

"""
Лото

Правила игры в лото.

Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.
Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. В каждом столбце 2 или 3 числа из соответствующего интервала:
0-10 для первой колонки, 11-20 для второй и т.д. 
Все цифры в карточке уникальны.

В игре 2 игрока: пользователь и компьютер. Каждому в начале игры выдается 
случайная карточка. Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
	
Побеждает тот, кто первый закроет все числа на своей карточке.
"""


class Card(object):

    def __init__(self, name):
        self.name = name
        self.not_crossed = 15
        cells = []
        for i in range(3):
            row = [0] * 4 + [1] * 5
            shuffle(row)
            cells.extend(row)
        for i, v in enumerate(cells):
            if v == 1:
                base = i % 9
                rand = randint(10 * base + 1, 10 * base + 10)
                while rand in cells:
                    rand = randint(10 * base + 1, 10 * base + 10)
                cells[i] = rand
        self.cells = cells

    def __str__(self):
        res = ['{0:-^26}'.format(self.name)]
        for i in range(3):
            res.append(' '.join(str(x).rjust(2) if x else '  ' for x in self.cells[i * 9: i * 9 + 9]))
        res.append('-'*26)
        return '\n'.join(res)

    def cross(self, num):
        try:
            i = self.cells.index(num)
        except ValueError:
            return False
        else:
            self.cells[i] = 'X'
            self.not_crossed -= 1
            return True

    def __contains__(self, item):
        return item in self.cells

    def is_winner(self):
        return self.not_crossed == 0


def gen_barrel():
    barrels = list(range(1, 91))
    shuffle(barrels)
    for barrel in barrels:
        yield barrel


def game():
    player_won = False
    comp_won = False
    player_card = Card('Ваша карточка')
    comp_card = Card('Карточка компьютера')
    barrels = gen_barrel()
    while not player_won and not comp_won:
        print(player_card)
        print(comp_card)
        new_barrel = next(barrels)
        print('Число:', new_barrel)
        resp = input('Зачеркнуть число? (y/n)')
        if resp.lower() == 'y':
            if not player_card.cross(new_barrel):
                comp_won = True
        elif resp.lower() == 'n':
            if new_barrel in player_card:
                comp_won = True
        else:
            comp_won = True
        comp_card.cross(new_barrel)
        if player_card.is_winner():
            player_won = True
        if comp_card.is_winner():
            comp_won = True
    if player_won and comp_won:
        print('Ничья')
    elif player_won:
        print('Гц!')
    elif comp_won:
        print('Вы проиграли')
    else:
        print('Такого не должно было случиться')


if __name__ == '__main__':
    game()
