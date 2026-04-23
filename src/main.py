# imports
import pygame
from datetime import date

# project imports
from core.logger import setup_logger
from presentation.gui import screen

# constants
log = setup_logger(f"{date.today()}.log")


# functions
def main() -> None:
    pygame.init()
    surface = pygame.display.set_mode((screen.WINDOW_WIDTH, screen.WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    menu = screen.MainMenu(surface, clock)
    if not menu.show():
        pygame.quit()
        return

    game_display = screen.BoardDisplay(surface, clock)
    result = game_display.run()
    log.info(f"GAME_RESULT={result}")
    pygame.quit()



if __name__ == "__main__":
    log.info("STARTING TIC_TAC_TOE")
    try:
        main()
    except Exception as erro:
        log.error(erro)
    finally:
        log.info("ENDING TIC_TAC_TOE")