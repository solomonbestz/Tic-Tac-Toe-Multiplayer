import sys 

import pygame


class TicTacToe:
    def __init__(self) ->None:
        self.null_char: str = 'n'
        self.board: list = [self.null_char] * 9

        self.turn: int = 0

        pygame.init()

        self.screen: pygame.display = pygame.display.set_mode((800, 850))
        self.clock: pygame.time = pygame.time.Clock()

        self.space_size: int = 250
        self.board_center: tuple = (self.screen.get_width() / 2, self.screen.get_height() - self.screen.get_width() / 2)
        self.winner = None
        self.teams = ['x', 'o']

        self.clicked = False
        self.font = pygame.font.Font(size=34)

    def draw_letter(self, letter: str, pos: tuple) -> None:
        if letter == self.teams[0]:
            pygame.draw.line(
                self.screen, 
                (0, 0, 255),
                (pos[0] - self.space_size * 0.4, pos[1] - self.space_size * 0.4),
                (pos[0] + self.space_size * 0.4, pos[1] + self.space_size * 0.4),
                10
            )
            pygame.draw.line(
                self.screen,
                (0, 0, 255),
                (pos[0] + self.space_size * 0.4, pos[1] - self.space_size * 0.4),
                (pos[0] - self.space_size * 0.4, pos[1] + self.space_size * 0.4),
                10
            )
        if letter == self.teams[1]:
            pygame.draw.circle(
                self.screen, 
                (255, 0, 0), 
                pos, 
                self.space_size * 0.4,
                10 
            )

    def draw_board(self) -> None:
        pygame.draw.line(
            self.screen,
            (0, 0, 0),
            (self.board_center[0] - self.space_size / 2, self.board_center[1] - self.space_size * 1.5),
            (self.board_center[0] - self.space_size / 2, self.board_center[1] + self.space_size * 1.5)
        )
        pygame.draw.line(
            self.screen,
            (0, 0, 0),
            (self.board_center[0] + self.space_size / 2, self.board_center[1] - self.space_size * 1.5),
            (self.board_center[0] + self.space_size / 2, self.board_center[1] + self.space_size * 1.5)
        )
        pygame.draw.line(
            self.screen,
            (0, 0, 0),
            (self.board_center[0] - self.space_size * 1.5, self.board_center[1] - self.space_size / 2),
            (self.board_center[0] + self.space_size * 1.5, self.board_center[1] - self.space_size / 2)
        )
        pygame.draw.line(
            self.screen,
            (0, 0, 0),
            (self.board_center[0] - self.space_size * 1.5, self.board_center[1] + self.space_size / 2),
            (self.board_center[0] + self.space_size * 1.5, self.board_center[1] + self.space_size / 2)
        )
    
    def place(self, space_index: int) -> None:
        if 0 <= space_index < len(self.board):
            if self.board[space_index] == self.null_char:
                self.board[space_index] = self.teams[self.turn % 2]
                self.turn += 1

    def get_space(self, pos: tuple) -> str:
        space_index = pos[0] + pos[1] * 3
        if (0 <= pos[0] < 3) and (0 <= pos[1] < 3):
            return self.board[space_index]

    def check_win(self) -> str:
        for i, letter in enumerate(self.board):
            if letter != self.null_char:
                space_id = (i % 3, i // 3)
                for angle in [(1, 0), (1, 1), (0, 1), (-1, 1)]:
                    for j in range(3):
                        if self.get_space((space_id[0] + angle[0] * j, space_id[1] + angle[1] * j)) != letter:
                            break
                        if j == 2:
                            return letter
    
    def update(self) -> None:
        self.screen.fill((255, 255, 255))

        self.clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True
        
        mouse_pos = pygame.mouse.get_pos()

        game_text = f'{self.teams[self.turn % 2]}\'s turn'
        if self.winner:
            game_text = f'{self.winner} wins!'
        self.screen.blit(self.font.render(game_text, True, (0, 0, 0)), (10, 10))

        self.draw_board()
        for i, letter in enumerate(self.board):
            space_id = (i % 3, i // 3)
            space_center = ((space_id[0] - 1) * self.space_size + self.board_center[0], (space_id[1] - 1) * self.space_size + self.board_center[1])
            space_r = pygame.Rect(space_center[0] - self.space_size / 2, space_center[1] - self.space_size / 2, self.space_size, self.space_size)
            if letter != self.null_char:
                self.draw_letter(letter, space_center)
            if not self.winner:
                if space_r.collidepoint(mouse_pos):
                    if self.clicked:
                        self.place(i)
        
        self.winner = self.check_win()
            
        pygame.display.update()

        self.clock.tick()

    def run(self):
        while True:
            self.update()


if __name__=='__main__':
    game = TicTacToe()
    game.run()