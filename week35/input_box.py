# -*- coding: utf-8 -*-
import pygame


class InputBox(pygame.sprite.Sprite):
    def __init__(self, font, colors, rect, fps, buttonid, action="", limit=25):
        pygame.sprite.Sprite.__init__(self)

        self.id = buttonid

        # get font values
        font_family = font["family"]
        fontsize = font["size"]
        self.font = pygame.font.SysFont(font_family, fontsize)
        self.color = colors["text"]

        # states
        self.hovered = False
        self.selected = False
        self.error = False

        # character limit. default is 10
        self.limit = limit-1

        # action
        self.action = action

        # holds data from the user
        self.data = ""
        self.vbar_show = False

        # position, width and height of the input box
        self.rect = rect

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.convert_alpha()

        # background color
        self.background = pygame.Surface((self.rect.width, self.rect.height))
        self.background.convert_alpha()
        self.background.fill(colors["background"])
        self.image.blit(self.background, (0, 0))

        # background color when hovered
        self.background_hover = pygame.Surface((
            self.rect.width,
            self.rect.height
        ))
        self.background_hover.convert_alpha()
        self.background_hover.fill(colors["hover"])

        # background color when selected
        self.background_selected = pygame.Surface((
            self.rect.width,
            self.rect.height)
        )
        self.background_selected.convert_alpha()
        self.background_selected.fill(colors["selected"])

        # background color when an error occurs
        self.background_error = pygame.Surface((
            self.rect.width,
            self.rect.height
        ))
        self.background_error.convert_alpha()
        self.background_error.fill(colors["error"])

        # set vertical bar ticking rate
        self._start = pygame.time.get_ticks()
        self._delay = 20000 / fps
        self._errordelay = 10000 / fps
        self._last_update = 0
        self._frame = 0

        self.update(pygame.time.get_ticks())

    def update(self, time):

        # don't use self.data directly
        data = self.data
        if time - self._last_update > self._delay:
            if self.selected:
                if self._frame == 0:
                    # append vertical bar to the end
                    self.vbar_show = True
                    self._frame += 1
                else:
                    self._frame -= 1
                    self.vbar_show = False

                if self.error:
                    self.error = False

            self._last_update = time

        if self.vbar_show:
            data += "|"

        text = self.font.render(data, True, self.color)

        if self.error:
            self.image.blit(self.background_error, (0, 0))
        elif self.selected:
            self.image.blit(self.background_selected, (0, 0))
        elif self.hovered:
            self.image.blit(self.background_hover, (0, 0))
        else:
            self.image.blit(self.background, (0, 0))

        self.image.blit(text, (5, 5))

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False
        self.vbar_show = False

    def normal(self):
        self.hovered = False

    def hover(self):
        self.hovered = True

    def update_data(self, data):

        if data == u"\u0008":
            self.data = self.data[:-1]
        elif data.isalnum() and len(self.data) < self.limit:
            if self.id == 0:
                self.data += data
            if self.id == 1:
                if data.isdigit():
                    self.data += data
                else:
                    self.error = True
        else:
            self.error = True
