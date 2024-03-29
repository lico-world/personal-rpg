from settings import *
from level import Level
from keys_config import *
from debug import DevTool


class Game:
    def __init__(self):
        key_config = KeyConfig()
        key_config.init_keymaps()  # Import the saved config
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('RPG')
        # pygame.display.set_icon(INSERT ICON)

        self.level = Level()

    def run(self):
        dev_tool = DevTool()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:
                        dev_tool.switch_on_off()

            self.screen.fill('black')
            self.level.run()
            self.clock.tick(FPS)

            dev_tool.update_info('FPS', round(self.clock.get_fps(), 1))
            if dev_tool.display_info:
                dev_tool.display()

            # ------------------------- End of the loop /!\ ----------------------------
            pygame.display.update()

    def quit_game(self):
        self.level.save()  # Save player and level relative information

        key_config = KeyConfig()
        key_config.save_keymaps()  # Export the current config

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
