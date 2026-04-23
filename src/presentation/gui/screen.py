# imports
import os
import pygame
from core.game import gameSession

# constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)


class MainMenu:
    def __init__(self, surface: pygame.Surface, clock: pygame.time.Clock) -> None:
        self.screen = surface
        self.clock = clock
        pygame.display.set_caption("Tic Tac Toe - Menu")
        self.font_title = pygame.font.SysFont(None, 72)
        self.font_option = pygame.font.SysFont(None, 36)

        # define o ícone da janela / barra de tarefas
        base_dir = os.path.dirname(os.path.dirname(__file__))  # ...\presentation
        assets_dir = os.path.join(base_dir, "assets")
        icon_path = os.path.join(assets_dir, "icon.png")
        try:
            icon_surface = pygame.image.load(icon_path).convert_alpha()
            pygame.display.set_icon(icon_surface)
        except pygame.error:
            # Se o ícone não puder ser carregado, apenas segue sem quebrar o jogo
            pass

    def show(self) -> bool:
        """Mostra o menu. Retorna True se o jogador quiser começar o jogo."""
        running = True
        start_game = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        start_game = True
                        running = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            self._draw()
            self.clock.tick(60)

        return start_game

    def _draw(self) -> None:
        self.screen.fill(BG_COLOR)

        title_surf = self.font_title.render("Tic Tac Toe", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.screen.blit(title_surf, title_rect)

        option_surf = self.font_option.render(
            "ENTER/SPACE: Jogar | ESC: Sair", True, TEXT_COLOR
        )
        option_rect = option_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 * 2))
        self.screen.blit(option_surf, option_rect)

        pygame.display.flip()


class BoardDisplay:
    def __init__(self, surface: pygame.Surface, clock: pygame.time.Clock) -> None:
        self.screen = surface
        self.clock = clock
        pygame.display.set_caption("Tic Tac Toe - Game")
        self.font_status = pygame.font.SysFont(None, 36)

        # lógica do jogo
        self._restart_game()

        # layout
        self.board_size = min(WINDOW_WIDTH, WINDOW_HEIGHT) - 40
        self.cell_size = self.board_size // 3
        self.board_x = (WINDOW_WIDTH - self.board_size) // 2
        self.board_y = (WINDOW_HEIGHT - self.board_size) // 2

        # caminhos de imagens (somente X e O)
        base_dir = os.path.dirname(os.path.dirname(__file__))  # ...\presentation
        assets_dir = os.path.join(base_dir, "assets")

        icon_path = os.path.join(assets_dir, "icon.png")
        x_path = os.path.join(assets_dir, "x.png")
        o_path = os.path.join(assets_dir, "o.png")

        # garante o ícone também na janela do jogo (caso chegue direto aqui)
        try:
            icon_surface = pygame.image.load(icon_path).convert_alpha()
            pygame.display.set_icon(icon_surface)
        except pygame.error:
            pass

        symbol_size = int(self.cell_size * 0.7)
        self.x_img = pygame.image.load(x_path).convert_alpha()
        self.x_img = pygame.transform.smoothscale(
            self.x_img, (symbol_size, symbol_size)
        )

        self.o_img = pygame.image.load(o_path).convert_alpha()
        self.o_img = pygame.transform.smoothscale(
            self.o_img, (symbol_size, symbol_size)
        )

    def run(self) -> str:
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif self.game.result:
                        if event.key == pygame.K_RETURN:
                            running = False
                        elif event.key == pygame.K_SPACE:
                            # Reinicia o jogo após finalizar
                            self._restart_game()

            self._draw()
            self.clock.tick(60)

        return self.game.result

    def _handle_click(self, pos) -> None:
        mx, my = pos
        if not (
            self.board_x <= mx < self.board_x + self.board_size
            and self.board_y <= my < self.board_y + self.board_size
        ):
            return

        col = (mx - self.board_x) // self.cell_size
        row = (my - self.board_y) // self.cell_size

        self.game.play_move(row, col)

    def _restart_game(self) -> None:
        """Cria um novo jogo e tenta usar start_game() sem alterar a função."""
        self.game = gameSession.Game()
        try:
            # Usa a função start_game definida em Game, mas protege
            # contra possíveis loops/erros internos (_on_turn, etc.).
            self.game.start_game()
        except Exception:
            # Se start_game não estiver compatível com a interface gráfica,
            # ignoramos o erro e seguimos apenas com o novo estado do jogo.
            pass

    def _draw(self) -> None:
        self.screen.fill(BG_COLOR)

        # desenha o grid
        rect = pygame.Rect(self.board_x, self.board_y, self.board_size, self.board_size)
        pygame.draw.rect(self.screen, TEXT_COLOR, rect, width=2)

        # linhas verticais
        for i in range(1, 3):
            x = self.board_x + i * self.cell_size
            pygame.draw.line(
                self.screen,
                TEXT_COLOR,
                (x, self.board_y),
                (x, self.board_y + self.board_size),
                width=2,
            )

        # linhas horizontais
        for i in range(1, 3):
            y = self.board_y + i * self.cell_size
            pygame.draw.line(
                self.screen,
                TEXT_COLOR,
                (self.board_x, y),
                (self.board_x + self.board_size, y),
                width=2,
            )

        # símbolos
        for row in range(3):
            for col in range(3):
                symbol = self.game.board[row][col]
                if symbol:
                    img = self.o_img if symbol == "o" else self.x_img
                    cx = self.board_x + col * self.cell_size + self.cell_size // 2
                    cy = self.board_y + row * self.cell_size + self.cell_size // 2
                    rect = img.get_rect(center=(cx, cy))
                    self.screen.blit(img, rect)

        # linha destacando a jogada vencedora
        winning_line = self._get_winning_line()
        if winning_line is not None:
            start_pos, end_pos = winning_line
            pygame.draw.line(
                self.screen,
                (0, 255, 0),  # cor da linha vencedora
                start_pos,
                end_pos,
                width=6,
            )

        # status
        if not self.game.result:
            text = f"Vez: {'Jogador 1 (O)' if self.game.turn == 'o' else 'Jogador 2 (X)'}"
        else:
            if self.game.result == "draw":
                text = "Empate! SPACE para jogar novamente"
            elif self.game.result == "o":
                text = "Jogador 1 (O) venceu!"
            elif self.game.result == "x":
                text = "Jogador 2 (X) venceu!"
            else:
                text = "Fim de jogo"

        text_surf = self.font_status.render(text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 10))
        self.screen.blit(text_surf, text_rect)

        pygame.display.flip()

    def _get_winning_line(self):
        """Retorna os pontos (inicio, fim) da linha vencedora em coordenadas de tela.

        Caso não haja vencedor, retorna None.
        """
        result = self.game.result
        board = self.game.board

        if result not in ("o", "x"):
            return None

        padding = 10  # margem para a linha não encostar na borda

        # verifica linhas
        for row in range(3):
            if (
                board[row][0] == board[row][1] == board[row][2] == result
            ):
                y = self.board_y + row * self.cell_size + self.cell_size // 2
                x1 = self.board_x + padding
                x2 = self.board_x + self.board_size - padding
                return (x1, y), (x2, y)

        # verifica colunas
        for col in range(3):
            if (
                board[0][col] == board[1][col] == board[2][col] == result
            ):
                x = self.board_x + col * self.cell_size + self.cell_size // 2
                y1 = self.board_y + padding
                y2 = self.board_y + self.board_size - padding
                return (x, y1), (x, y2)

        # verifica diagonal principal
        if board[0][0] == board[1][1] == board[2][2] == result:
            x1 = self.board_x + padding
            y1 = self.board_y + padding
            x2 = self.board_x + self.board_size - padding
            y2 = self.board_y + self.board_size - padding
            return (x1, y1), (x2, y2)

        # verifica diagonal secundária
        if board[0][2] == board[1][1] == board[2][0] == result:
            x1 = self.board_x + self.board_size - padding
            y1 = self.board_y + padding
            x2 = self.board_x + padding
            y2 = self.board_y + self.board_size - padding
            return (x1, y1), (x2, y2)

        return None