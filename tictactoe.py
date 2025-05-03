import sys
import pygame
import numpy as np
import random
import copy

from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Aaloo Cross')
screen.fill(BG_COLOR)

class Board():
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.marked_squares = 0
    
    def final_state(self):
        '''
            return 0 if there is no win yet
            return 1 if player 1 wins 
            return 2 if player 2 wins 
        '''
        #vertical wins 
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
            
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
    
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[0][0]
        
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]
        
        #no win yet
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    def isFull(self):
        return self.marked_squares == 9
    
    def isEmpty(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_sqr(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

class AI:
    def __init__(self, level = 1, player = 2):
        self.level = level
        self.player = player 
    
    def random_ai(self, board):
        empty_squares = board.get_empty_sqr()
        idx = random.randrange(0, len(empty_squares))

        return empty_squares[idx]
    
    def minimax(self, board, maximizing):
        #terminal case 
        case = board.final_state()
        if case == 1:
            return 1, None 
        
        #player 2 wins
        elif case == 2:
            return -1, None

        #draw 
        elif board.isFull():
            return 0, None 
        
        if maximizing:
            max_eval = -100
            best_move = None 
            empty_squares = board.get_empty_sqr()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None 
            empty_squares = board.get_empty_sqr()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            eval = "random"
            move = self.random_ai(main_board)
        else: 
            #minimax algo
            eval, move = self.minimax(main_board, False)
        
        print(f'AI has chosen to mark the square in pos{move} with an eval of {eval}')

        return move

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'
        self.running = True
        self.show_lines()

    def show_lines(self):
        #vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH- SQSIZE, HEIGHT), LINE_WIDTH)

        #horizontal 
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)
    
    def draw_fig(self, row, col):
        if self.player == 1:
            #draw cross
            #desc line
            start_desc = (col * SQSIZE + OFFSET, row *  SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            #ascending line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)

            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1

def main():
    #create game object
    game = Game()
    board = game.board
    Ai = game.ai

    #mainloop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                if board.empty_sqr(row, col):
                    board.mark_square(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_turn()

        if game.gamemode == 'ai' and game.player == Ai.player:
            #update the screen
            pygame.display.update()
            #ai methods
            row, col = Ai.eval(board)

            board.mark_square(row, col, Ai.player)
            game.draw_fig(row, col)
            game.next_turn()

        pygame.display.update()

main()
