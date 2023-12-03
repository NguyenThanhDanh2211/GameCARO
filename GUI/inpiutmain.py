from pygame.locals import *

class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.font = pygame.font.Font(None, 40)
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color_inactive)
        self.active = False

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        pygame.display.set_caption(render_settings.WINDOW_TITLE)

        bg = pygame.image.load('Asset/bg.jpg')
        bg = pygame.transform.scale(bg, (render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))

        blur_surface = pygame.Surface((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        blur_surface.set_alpha(150)  # Đặt độ trong suốt
        blur_surface.fill((255, 255, 255))

        self.screen.blit(bg, (0, 0))
        self.screen.blit(blur_surface, (0, 0))

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_RETURN:
                    return self.text
                elif event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.txt_surface = self.font.render(self.text, True, self.color_active)  # Cập nhật txt_surface sau khi xóa ký tự
                else:
                    self.text += event.unicode
                    self.txt_surface = self.font.render(self.text, True, self.color_active)  # Cập nhật txt_surface sau khi thêm ký tự
            
        color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(self.screen, color, self.rect, 2)
        self.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(self.screen, color, self.rect, 2)
        pygame.display.update()  # Cập nhật màn hình



    def activate(self):
        self.active = True
        self.txt_surface = self.font.render(self.text, True, self.color_active)

    def deactivate(self):
        self.active = False
        self.txt_surface = self.font.render(self.text, True, self.color_inactive)

    def draw_label(self):
        font = pygame.font.Font(None, 40)
        label = font.render("Enter your name", True, (255, 255, 255))
        label_rect = label.get_rect(center=(self.rect.centerx, self.rect.top - 30))
        self.screen.blit(label, label_rect)

    def get_player_name():
        clock = pygame.time.Clock()
        input_box = InputBox(render_settings.WINDOW_WIDTH//2-70, render_settings.WINDOW_HEIGHT//2, 200, 40)

        input_boxes = [input_box]
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                    sys.exit()
                for box in input_boxes:
                    if event.type == MOUSEBUTTONDOWN:
                        if box.rect.collidepoint(event.pos):
                            box.activate()
                        else:
                            box.deactivate()
                    if event.type == KEYDOWN:
                        if box.active:
                            if event.key == K_RETURN:
                                return box.text
                            box.handle_event(event)

            for box in input_boxes:
                box.handle_event(pygame.event.Event(0)) # Update text surface

            input_box.draw_label()
            pygame.display.flip()
            pygame.display.update()
            clock.tick(30)