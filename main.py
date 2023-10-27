import pygame
import GUI.menu_render as menu_render
import Settings.render_settings as render_settings
from GUI.aboutme_render import Aboutme
from GUI.menu_playwFriend_render import playwFriend
from GUI.menu_playwAI_render import MenuPlaywithAI

pygame.init()

if __name__ == '__main__':
    # current_match = State()
    menu = menu_render.Menu()
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(render_settings.FPS)
        pygame.display.update()
        
        menu.loop()
        if menu.MenuPlaywAI:
            menu.init_btn()
            MenuPlaywAI = MenuPlaywithAI()
            MenuPlaywAI.loop()
            menu.running = True

        if menu.playwFriend:
            menu.init_btn()
            pwFriend = playwFriend()
            pwFriend.loop()
            menu.running = True

        if menu.rank:
            menu.init_btn()

        if menu.aboutme:
            menu.init_btn()
            aboutme = Aboutme()
            aboutme.loop()
            # if aboutme: del aboutme
            # aboutme = None
            menu.running = True

        if menu.quit:
            menu.init_btn()

        for event in pygame.event.get():

            #exit
            if event.type == pygame.QUIT:
                running = False
                exit()