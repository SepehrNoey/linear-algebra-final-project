import math

import numpy as np
import pygame
import numpy

### Globals ###

pygame.init()

adj = [[0, 0], [0, -1], [-1, 0], [0, 1], [1, 0]]

TILE_HEIGHT = 50
TILE_WIDTH = 50
MARGIN = 2


class Game:
    def __init__(self, cells):
        self.cells = cells
        self.clear()
        self.load_level()

    def clear(self):
        self.grid = [[0 for i in range(len(self.cells))] for j in range(len(self.cells))]

    def load_level(self):
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                self.grid[x][y] = int(self.cells[y][x])

    def draw(self):
        for y in range(len(self.cells)):
            for x in range(len(self.cells)):
                i = x * TILE_WIDTH + MARGIN
                j = y * TILE_HEIGHT + MARGIN
                h = TILE_HEIGHT - (2 * MARGIN)
                w = TILE_WIDTH - (2 * MARGIN)
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, (105, 210, 231), [i, j, w, h])
                else:
                    pygame.draw.rect(screen, (255, 255, 255), [i, j, w, h])

    def get_adjacent(self, x, y):
        adjs = []
        for i, j in adj:
            if (0 <= i + x < len(self.cells)) and (0 <= j + y < len(self.cells)):
                adjs += [[i + x, j + y]]
        return adjs

    def click(self, pos):
        x = int(pos[0] / TILE_WIDTH)
        y = int(pos[1] / TILE_HEIGHT)
        adjs = self.get_adjacent(x, y)
        for i, j in adjs:
            self.grid[j][i] = (self.grid[j][i] + 1) % 2


class Solver:
    def __init__(self, board):
        self.board = board
        self.mat_size = len(board) ** 2
        self.board_vector = numpy.zeros((self.mat_size, 1))
        for i in range(len(board)):
            for j in range(len(board)):
                self.board_vector[i * len(board) + j, 0] = board[i, j]

        self.matrix = numpy.zeros((self.mat_size, self.mat_size + 1))
        for j in range(self.matrix.shape[1] - 1):
            self.matrix[:, j] = self.get_corresponding_vector(self.mat_size, int(j / len(board)),
                                                              j % len(board)).reshape((self.mat_size,))

        self.matrix[:, self.matrix.shape[1] - 1] = self.board_vector.reshape((self.mat_size,))

    def get_corresponding_vector(self, mat_size, i, j):
        sqr = int(math.sqrt(mat_size))
        res_vec = np.zeros((mat_size, 1))
        res_vec[sqr * i + j, 0] = 1
        if 0 < i < sqr:  # so it has upper adjacent
            res_vec[sqr * (i - 1) + j, 0] = 1
        if 0 < j < sqr:  # so it has left adjacent
            res_vec[sqr * i + j - 1, 0] = 1
        if 0 <= j < sqr - 1:  # so it has right adjacent
            res_vec[sqr * i + j + 1, 0] = 1
        if 0 <= i < sqr - 1:  # so it has down adjacent
            res_vec[sqr * (i + 1) + j, 0] = 1

        return res_vec

    def get_solution(self):
        row_reducer = RowReducerInGF2(self.matrix)
        reduced = row_reducer.calculate()
        is_solvable = True
        click_orders = []
        for i in range(reduced.shape[0]):
            if reduced[i, reduced.shape[1] - 1] == 1:
                if reduced[i, i] != 1:
                    is_solvable = False
                    break
                else:
                    click_orders.append(i + 1)

        if not is_solvable:
            print("There is no solution for this board!")
        else:
            print("Order of clicks is :")
            for element in click_orders:
                print(element)


class RowReducerInGF2:
    def __init__(self, augmented_matrix):
        self.augmented_matrix = augmented_matrix

    def calculate(self):
        echelon = self.forward_phase(self.augmented_matrix, 0, 0)
        reduced_echelon = self.backward_phase(echelon)

        return reduced_echelon

    def interchange(self, arr: np.ndarray, row_index1, row_index2):
        temp = np.copy(arr[row_index1])
        arr[row_index1] = arr[row_index2]
        arr[row_index2] = temp

    def replacement(self, arr: np.ndarray, dest_index, src_index,
                    checking_column):  # it's a special replacement (summation is done in Galois Field 2)
        arr[dest_index, checking_column: arr.shape[1]] = (arr[src_index, checking_column: arr.shape[1]] + arr[dest_index,checking_column: arr.shape[1]]) % 2

    def forward_phase(self, arr: np.ndarray, row_index, column_index):
        nonzero_list = []  # it stores indices
        for k in range(row_index, len(arr)):
            if arr[k, column_index] != 0:
                nonzero_list.append(k)

        if arr[row_index, column_index] == 0:  # so , interchange is needed
            if len(nonzero_list) >= 1:
                self.interchange(arr, row_index, nonzero_list[0])
                nonzero_list[0] = row_index

        if len(nonzero_list) >= 2:  # so , replacement is needed
            for each in nonzero_list:
                if each != row_index:
                    self.replacement(arr, each, row_index, column_index)

        column_index += 1
        if len(nonzero_list) != 0:  # so , row must increase too
            row_index += 1
        if row_index <= arr.shape[0] - 1 and column_index <= arr.shape[1] - 1:
            arr = self.forward_phase(arr, row_index, column_index)
            if row_index == arr.shape[0] - 1 or column_index == arr.shape[1] - 1:
                return arr

        return arr

    def backward_phase(self, arr: np.ndarray):
        pivot_positions = self.find_pivot_positions(arr)
        # now we have pivot positions, so we do replacement
        for tpl in pivot_positions:
            nonzero_elements = []
            for row_i in range(tpl[0] - 1, -1, -1):
                if arr[row_i, tpl[1]] != 0:
                    nonzero_elements.append(row_i)

            for row_i in nonzero_elements:
                self.replacement(arr, row_i, tpl[0], tpl[1])

        # now we have reduced echelon form
        return arr

    def find_pivot_positions(self, arr: np.ndarray):
        current_row = 0
        current_column = 0
        pivot_positions = []

        for index in range(max(arr.shape)):  # it must iterate at least max(row , column) to find pivots
            if current_row <= arr.shape[0] - 1 and current_column <= arr.shape[1] - 1:
                if arr[current_row, current_column] != 0:
                    pivot_positions.append((current_row, current_column))
                    current_row += 1
                    current_column += 1
                else:
                    current_column += 1

        return pivot_positions


### Main ###

if __name__ == "__main__":

    cells = numpy.array([[1, 1],
                         [1, 1]])

    screen = pygame.display.set_mode((len(cells) * TILE_WIDTH, len(cells) * TILE_HEIGHT))
    screen.fill((167, 219, 216))
    pygame.display.set_caption("Game")

    game = Game(cells.T)
    game.draw()

    solver = Solver(cells)
    solver.get_solution()

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        game.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.click(pos)
        pygame.display.flip()
    pygame.quit()
