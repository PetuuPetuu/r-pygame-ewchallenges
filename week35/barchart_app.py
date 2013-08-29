# -*- coding: utf-8 -*-
import pygame
import datetime
import os

from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_RETURN, K_DELETE,
                          MOUSEBUTTONDOWN, KMOD_LSHIFT, KMOD_RSHIFT, KMOD_CAPS)
from input_box import InputBox
from button import Button
from title import Title
from bar import Bar


class BarchartApp(object):
    def __init__(self):
        pygame.init()
        os.environ["SDL_VIDEO_CENTERED"] = '1'          # Center the game window
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("BarchartApp")       # Set app name
        pygame.key.set_repeat(200, 80)

        self.fps = 60
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((255, 255, 255))
        self.background.convert()

        self.bottombar = pygame.Surface((800, 100))
        self.bottombar.fill((240, 240, 240))

        self.menu = pygame.sprite.OrderedUpdates()
        self.barmenu = pygame.sprite.Group()
        self.bartitles = pygame.sprite.Group()
        self.mouse = pygame.sprite.GroupSingle()
        self.mouse.add(Mouse())

        self.bars = pygame.sprite.OrderedUpdates()

        self.titles = pygame.sprite.Group()

    def main(self):
        self.main_menu()

        while True:
            if self.input() is False:
                return False
            self.menu.update(pygame.time.get_ticks())
            self.bars.update()
            self.draw()

    def input(self):
        self.mouse.sprite.move(pygame.mouse.get_pos())
        for event in pygame.event.get():

            for button in self.menu:
                if pygame.sprite.spritecollide(button, self.mouse, False):
                    button.hover()
                else:
                    button.normal()

            for bar in self.bars:
                if pygame.sprite.spritecollide(bar, self.mouse, False):
                    bar.hover()
                else:
                    bar.normal()

            if event.type == QUIT:
                return False

            if event.type == MOUSEBUTTONDOWN:
                for button in self.menu:
                    if pygame.sprite.spritecollide(button, self.mouse, False):
                        if button.action:
                            self.perform_action(button.action)
                        if not button.error:
                            button.select()
                    else:
                        button.deselect()

                for bar in self.bars:
                    if pygame.sprite.spritecollide(bar, self.mouse, False):
                        if bar.selected:
                            bar.deselect()
                        else:
                            bar.select()
                    else:
                        bar.deselect()
                self.bar_menu()


            if event.type == KEYDOWN:
                if event.key == K_DELETE:
                    for bar in self.bars:
                        if bar.selected:
                            self.delete_bar()
                if event.key == K_ESCAPE:
                    return False
                for box in self.menu:
                    if box.selected and box.id in [0, 1]:
                        if event.key not in [K_RETURN, K_ESCAPE]:
                            mods = pygame.key.get_mods()

                            # Caps Lock ON 
                            if (mods & KMOD_CAPS):

                                # Caps Lock ON & Shift ON
                                if (mods & KMOD_LSHIFT) or (mods & KMOD_RSHIFT):
                                    box.update_data(event.key, False)

                                # Caps Lock ON & Shift OFF
                                else:
                                    box.update_data(event.key, True)

                            # Caps Lock OFF & Shift ON
                            elif (mods & KMOD_LSHIFT) or (mods & KMOD_RSHIFT):
                                box.update_data(event.key, True)

                            else:
                                box.update_data(event.key, False)

    def bar_menu(self):
        self.barmenu.empty()
        self.bartitles.empty()

        font = {"family":"Arial", "size":14}

        colors = {
            "background":(205, 205, 205),
            "selected":(200, 200, 150),
            "hover":(150, 200, 150),
            "error":(200, 150, 150),
            "text":(25, 25, 25)
        }

        colors_text = {
            "background":(225, 225, 225),
            "selected":(250, 250, 200),
            "hover":(200, 250, 200),
            "error":(250, 200, 200),
            "text":(75, 75, 75)
        }

        bar_selected  = ""
        for bar in self.bars:
            if bar.selected:
                bar_selected = bar

        if bar_selected:

            self.bartitles.add(Title(font, colors, (580, 700), "Name:"))
            self.bartitles.add(Title(font, colors, (580, 716), "Value:"))
            self.bartitles.add(Title(font, colors, (580, 732),"% of max:"))

            self.bartitles.add(Title(font, colors_text, (635, 700),
                                     bar_selected.caption))
            self.bartitles.add(Title(font, colors_text, (635, 716),
                                     str(bar_selected.value)))
            percentage = 1.0*bar_selected.value/bar_selected.maxvalue*100
            rounded = str(int(round(percentage)))+"%"
            self.bartitles.add(Title(font, colors_text, (635, 732), rounded))

            button_delete_rect = pygame.Rect(580, self.height-40-10, 130, 40)

            font["size"] = 20
            self.menu.add(Button(font, colors, button_delete_rect, "Delete",
                                 "delete_bar"))

    def save_image(self):
        for bar in self.bars:
            if bar.selected:
                bar.deselect()
                bar.update()
        self.draw()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        surface = self.screen.subsurface(pygame.Rect(0, 0, 800, 700))
        filename = str(date)+".png"
        pygame.image.save(surface, filename)
        print "Saved image as "+filename

    def delete_bar(self):
        x = 0
        for bar in self.bars:
            if bar.selected:
                x = bar.rect.x
                self.bars.remove(bar)
                break
        for bar in self.bars:
            if bar.rect.x > x:
                bar.move(-70)
        self.bar_menu()
        self.main_menu()


    def main_menu(self):
        self.menu.empty()
        self.titles.empty()
        font = {"family":"Arial", "size":20}
        colors = {
            "background":(225, 225, 225),
            "selected":(250, 250, 200),
            "hover":(200, 250, 200),
            "error":(250, 200, 200),
            "text":(75, 75, 75)
        }
        input_caption_rect = pygame.Rect(10, self.height-40-10, 300, 40)
        input_caption = InputBox(font, colors, input_caption_rect, self.fps, 0)

        input_value_rect = pygame.Rect(320, self.height-40-10, 65, 40)
        input_value = InputBox(font, colors, input_value_rect, self.fps, 1)

        button_colors = {
            "background":(205, 205, 205),
            "selected":(200, 200, 150),
            "hover":(150, 200, 150),
            "error":(200, 150, 150),
            "text":(25, 25, 25)
        }

        button_submit_rect = pygame.Rect(395, self.height-40-10, 65, 40)
        button_submit = Button(font, button_colors, button_submit_rect,
                               "Add", "submit_values")

        button_save_rect = pygame.Rect(470, self.height-40-10, 100, 40)
        button_save = Button(font, button_colors, button_save_rect,
                               "Save image", "save_image")

        self.menu.add(input_caption)
        self.menu.add(input_value)
        self.menu.add(button_submit)
        self.menu.add(button_save)

        self.titles.add(Title(font, colors, (10, 710), "Caption:"))
        self.titles.add(Title(font, colors, (320, 710), "Value:"))

    def submit_values(self):
        caption = ""
        value = 0
        for button in self.menu:
            if button.id == 0:
                caption = str(button.data)
            elif button.id == 1:
                try:
                    value = int(button.data)
                except:
                    print "Incorrect input!"

        if caption == "" or value == 0:
            for button in self.menu:
                if button.id == 2:
                    button.throw_error()

        else:
            maxvalue = value

            if self.bars:
                maxvalue = max(bar.value for bar in self.bars)
                if value > maxvalue:
                    maxvalue = value
                    for bar in self.bars:
                        bar.set_size(maxvalue)

            x = 10+len(self.bars)*70

            if x+70 > self.width:
                for button in self.menu:
                    if button.id == 2:
                        button.throw_error()
            else:
                self.bars.add(Bar(caption, value, maxvalue,
                                  600, x, self.height-160))


    def perform_action(self, name):
        function = getattr(self, name)
        if function() is False:
            return False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.bottombar, (0, 700))
        self.menu.draw(self.screen)
        self.titles.draw(self.screen)
        self.bars.draw(self.screen)
        self.barmenu.draw(self.screen)
        self.bartitles.draw(self.screen)
        pygame.display.update()


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 1, 1)

    def move(self, pos):
        self.rect.x, self.rect.y = pos

if __name__ == "__main__":
    app = BarchartApp()
    app.main()