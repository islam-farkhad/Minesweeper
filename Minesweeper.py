import collections
import math
import time
from enum import Enum
from random import shuffle


class GameStatus(Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    VICTORY = 3
    DEFEAT = 4


class Cell:
    def __init__(self, x=1, y=1):
        self.x = x - 1
        self.y = y - 1
        self.flag = False
        self.is_mine = False
        self.is_opened = False
        self.mines_qty_nearby = 0


class Minesweeper:
    def __init__(self, field_height, field_width, mines):
        self.field_height = field_height
        self.field_width = field_width
        self.game_status = GameStatus.NOT_STARTED
        self.game_start_time = 0
        self.game_end_time = 0
        self.field = [[Cell(i + 1, j + 1) for j in range(field_width)] for i in range(field_height)]
        self.count_opened_cells = 0
        if isinstance(mines, list):
            self.non_mines_total = field_height * field_width - len(mines)
            for mine_cell in mines:
                self.field[mine_cell.x][mine_cell.y].is_mine = True
                self.update_mines_qty_nearby_for_neighbours(mine_cell)
        else:  # mines is a number
            self.non_mines_total = field_height * field_width - mines
            id_list = list(range(field_width * field_height))
            shuffle(id_list)
            for i in range(mines):
                x = math.ceil((id_list[i]) / field_width)
                y = (id_list[i]) % field_width
                self.field[x - 1][y - 1].is_mine = True
                self.update_mines_qty_nearby_for_neighbours(self.field[x - 1][y - 1])

    def open_cell(self, i, j):
        cell = self.field[i - 1][j - 1]

        if self.game_status is GameStatus.NOT_STARTED:
            self.game_start_time = time.time()
            self.game_status = GameStatus.IN_PROGRESS

        if self.game_status is GameStatus.IN_PROGRESS:

            if cell.is_mine:
                self.game_status = GameStatus.DEFEAT
                self.game_end_time = time.time()
                for i in range(self.field_height):
                    for j in range(self.field_width):
                        self.field[i][j].is_opened = True
                        self.count_opened_cells += 1

            elif not cell.is_opened:
                self.bfs(cell)
                if self.count_opened_cells == self.non_mines_total:
                    self.game_status = GameStatus.VICTORY
                    self.game_end_time = time.time()

    def mark_cell(self, i, j):
        cell = self.field[i - 1][j - 1]

        if self.game_status is GameStatus.NOT_STARTED:
            self.game_start_time = time.time()
            self.game_status = GameStatus.IN_PROGRESS

        if self.game_status is GameStatus.IN_PROGRESS:
            cell.flag = not cell.flag

    def get_game_status(self):
        return self.game_status.name

    def get_game_time(self):
        if self.game_status is GameStatus.IN_PROGRESS:
            return round(time.time() - self.game_start_time)

        elif self.game_status is GameStatus.NOT_STARTED:
            return 0

        else:
            return round(self.game_end_time - self.game_start_time)

    def render_field(self):
        list_of_rows = []
        for i in self.field:
            row = ""
            for j in i:
                if j.is_opened:
                    if j.is_mine:
                        row += '* '
                    else:
                        if j.mines_qty_nearby > 0:
                            row += str(j.mines_qty_nearby) + ' '
                        else:
                            row += '. '
                elif j.flag:
                    row += '? '
                else:
                    row += '- '
            list_of_rows.append(row)

        return list_of_rows

    def get_neighbours(self, cell):
        i = cell.x
        j = cell.y
        list_of_neighbours = []

        if i > 0 and j > 0:
            list_of_neighbours.append(self.field[i - 1][j - 1])

        if i > 0:
            list_of_neighbours.append(self.field[i - 1][j])

        if i > 0 and j + 1 < self.field_width:
            list_of_neighbours.append(self.field[i - 1][j + 1])

        if j + 1 < self.field_width:
            list_of_neighbours.append(self.field[i][j + 1])

        if i + 1 < self.field_height and j + 1 < self.field_width:
            list_of_neighbours.append(self.field[i + 1][j + 1])

        if i + 1 < self.field_height:
            list_of_neighbours.append(self.field[i + 1][j])

        if i + 1 < self.field_height and j > 0:
            list_of_neighbours.append(self.field[i + 1][j - 1])

        if j > 0:
            list_of_neighbours.append(self.field[i][j - 1])

        return list_of_neighbours

    def update_mines_qty_nearby_for_neighbours(self, mine_cell):
        list_of_neighbours = self.get_neighbours(mine_cell)

        for cell in list_of_neighbours:
            cell.mines_qty_nearby += 1

    def bfs(self, cell):

        queue = collections.deque([cell])
        while queue:
            vertex = queue.popleft()
            if vertex.flag:
                continue

            if vertex.mines_qty_nearby > 0:
                if not vertex.is_opened:
                    vertex.is_opened = True
                    self.count_opened_cells += 1
                continue

            list_of_neighbours = self.get_neighbours(vertex)

            for neighbour in list_of_neighbours:

                if neighbour.is_opened or neighbour.flag:
                    continue

                queue.append(neighbour)
                neighbour.is_opened = True
                self.count_opened_cells += 1


# Using example
game = Minesweeper(16, 30, 99)


while (game.game_status is not GameStatus.DEFEAT) and (game.game_status is not GameStatus.VICTORY):
    i, j = list(map(int, input("Enter cell coordinates: ").split()))
    button = input("Press F to mark cell, press any character to open cell: ")

    if button == "F":
        game.mark_cell(i, j)
    else:
        game.open_cell(i, j)

    lst = game.render_field()
    for i in lst:
        print(i)
    print("Time:", game.get_game_time())

    if game.game_status is GameStatus.VICTORY:
        print("You win!")

    if game.game_status is GameStatus.DEFEAT:
        print("Ooops... Try again")
