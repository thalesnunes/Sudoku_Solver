from time import sleep
import os
from ferramentas import header


class Sudoku:
    
    def __init__(self):
        self.board = [
            [7,8,0,4,0,0,1,2,0],
            [6,0,0,0,7,5,0,0,9],
            [0,0,0,6,0,1,0,7,8],
            [0,0,7,0,4,0,2,6,0],
            [0,0,1,0,5,0,9,3,0],
            [9,0,4,0,6,0,0,0,5],
            [0,7,0,3,0,0,0,1,2],
            [1,2,0,0,0,7,4,0,0],
            [0,4,9,2,0,6,0,0,7]
        ]
        self.sectors = self.create_sectors()
        
    def create_sectors(self):
        sectors = {}
        for i in range(1, 10):
            sectors[f'Sector{i}'] = []
        for row in range(9):
            for col in range(9):
                if not self.board[row][col] == 0:
                    sec = self.sector_identifier((row, col))
                    sectors[f'Sector{sec}'].append(self.board[row][col])
        return sectors
    
    @staticmethod
    def sector_identifier(coord):
        row, col = coord
        if row < 3:
            if col < 3: return 1
            if 3 <= col < 6: return 2
            else: return 3
        if 3 <= row < 6:
            if col < 3: return 4
            if 3 <= col < 6: return 5
            else: return 6
        else:
            if col < 3: return 7
            if 3 <= col < 6: return 8
            else: return 9
                        
        
    def searcher(self):
        for i, row in enumerate(self.board):
            for j, numb in enumerate(row):
                if numb == 0:
                    return (i, j)
                else:
                    continue
        return None
                
    def value_checker(self, coord):
        row, col = coord
        to_check = self.board[row][col]
        for i in range(9):
            if i != col:
                if to_check == self.board[row][i]:
                    return False
            if i != row:
                if to_check == self.board[i][col]:                 
                    return False

        sec = self.sector_identifier(coord)
        if to_check in self.sectors[f'Sector{sec}']:
            return False

        self.sectors[f'Sector{sec}'].append(to_check)        
        return True

    def change_value(self, coord, new):
        
        self.board[coord[0]][coord[1]] = new
    
    def implement(self, coord, prev=False):

        value = self.board[coord[0]][coord[1]]
        if value != 0 and prev:
            sec = self.sector_identifier(coord)
            self.sectors[f'Sector{sec}'].pop()
        for new in range(value+1, 10):
            self.change_value(coord, new)
            # self.display()
            outcome = self.value_checker(coord)
            if outcome:
                break
            else:
                if new == 9:
                    self.change_value(coord, 0)
                continue
        if value == 9 and prev:
            self.change_value(coord, 0)
            outcome = False

        return outcome
    
    def display(self):

        os.system('cls')
        print(self, end='\r', flush=True)
    
    def __str__(self):
        string = ''
        for n, row in enumerate(self.board):
            for ind, numb in enumerate(row):
                if ind == 3 or ind == 6 or ind == 0:
                    string += '| '
                string += f'{str(numb)} '
            string += '|\n'
            if n == 2 or n == 5:
                string += '=' * 25 + '\n'
        return string



if __name__ == "__main__":

    header('SUDOKU SOLVER')
    board = Sudoku()
    sleep(1)
    board.display()
    print("Let's start solving!")
    sleep(4)
    found = False
    coord = 0
    coords = []
    
    while coord != None:
        
        coord = board.searcher()
        if coord == None:
            break

        found = board.implement(coord)
        
        if not coord in coords:
            coords.append(coord)

        place = -2
        while not found:
            
            found = board.implement(coords[place], prev=True)
            coords.pop()
    
    board.display()
    header('CONGRATS! YOUR BOARD IS SOLVED!')
        