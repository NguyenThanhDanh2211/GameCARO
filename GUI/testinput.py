import pygame as pg
import pygame
class InputBox:
    # def __init__(self, screen, font, x, y, width, height):
    #     self.screen = screen
    #     self.font = font
    #     self.rect = pg.Rect(x, y, width, height)
    #     self.color_inactive = pg.Color('lightskyblue3')
    #     self.color_active = pg.Color('dodgerblue2')
    #     self.color = self.color_inactive
    #     self.active = False
    #     self.text = ''

    # def handle_event(self, event):
    #     if event.type == pg.MOUSEBUTTONDOWN:
    #         self.active = self.rect.collidepoint(event.pos)
    #         self.color = self.color_active if self.active else self.color_inactive
    #     if event.type == pg.KEYDOWN and self.active:
    #         if event.key == pg.K_RETURN:
    #             print(self.text)
    #             self.text = ''
    #         elif event.key == pg.K_BACKSPACE:
    #             self.text = self.text[:-1]
    #         else:
    #             self.text += event.unicode

    # def update(self):
    #     txt_surface = self.font.render(self.text, True, self.color)
    #     width = max(200, txt_surface.get_width() + 10)
    #     self.rect.w = width
    #     self.screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
    #     pg.draw.rect(self.screen, self.color, self.rect, 2)

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)#
        self.color_inactive = pygame.Color('lightskyblue3')#
        self.color_active = pygame.Color('dodgerblue2')#
        self.font = pygame.font.Font(None, 40) #
        self.color = self.color_inactive #
        self.text = ''#
        
        self.active = False#

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(500,500) #


       

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode



    def update(self):
        txt_surface = self.font.render(self.text, True, self.color)
        width = max(200, txt_surface.get_width() + 10)
        self.rect.w = width
        self.screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

    def draw_label(self):
        font = pygame.font.Font(None, 40)
        label = font.render("Enter your name", True, (255, 255, 255))
        label_rect = label.get_rect(center=(self.rect.centerx, self.rect.top - 30))
        self.screen.blit(label, label_rect)

    def get_player_name():
        clock = pygame.time.Clock()
        input_box = InputBox(500//2-70, 500//2, 200, 40)

        input_boxes = [input_box]
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pg.QUIT:
                    done = True
                   
                for box in input_boxes:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if box.rect.collidepoint(event.pos):
                            True
                        else:
                            False
                    if event.type == pg.KEYDOWN:
                        if box.active:
                            if event.key == pg.K_RETURN:
                                return box.text
                            box.handle_event(event)

            for box in input_boxes:
                box.handle_event(pygame.event.Event(0)) # Update text surface

            input_box.draw_label()
            pygame.display.flip()
            pygame.display.update()
            clock.tick(30)


def main():
    pg.init()
    # screen_width, screen_height = 640, 480
    screen = pg.display.set_mode((500, 500))
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()

    input_box = InputBox((500 - 140) // 2 - 50, (500 - 32) // 2, 140, 32)

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            input_box.handle_event(event)

        screen.fill((30, 30, 30))
        input_box.update()

        pg.display.flip()
        clock.tick(30)

    pg.quit()


if __name__ == '__main__':
    main()


