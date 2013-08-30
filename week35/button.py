# -*- coding: utf-8 -*-
import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, font, colors, rect, text, action, id=2):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        # get font values
        font_family = font["family"]
        fontsize = font["size"]
        self.font = pygame.font.SysFont(font_family, fontsize)
        self.color = colors["text"]
        self.text = self.font.render(text, True, self.color)

        # states
        self.hovered = False
        self.selected = False
        self.error = False

        # action
        self.action = action

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

        # background color when encountering an error
        self.background_error = pygame.Surface((
            self.rect.width,
            self.rect.height)
        )
        self.background_error.convert_alpha()
        self.background_error.fill(colors["error"])

        # set vertical bar ticking rate
        self._start = pygame.time.get_ticks()
        self._delay = 20000 / 60
        self._errordelay = 10000 / 60
        self._last_update = 0
        self._frame = 0

        self.update(pygame.time.get_ticks())

    def update(self, time):

        if time - self._last_update > self._delay:
            if self.selected:
                if self._frame == 0:
                    self._frame += 1
                    self.selected = False
                else:
                    self._frame -= 1

            if self.error:
                self.error = False

            self._last_update = time

        if self.error:
            self.image.blit(self.background_error, (0, 0))
        elif self.selected:
            self.image.blit(self.background_selected, (0, 0))
        elif self.hovered:
            self.image.blit(self.background_hover, (0, 0))
        else:
            self.image.blit(self.background, (0, 0))

        self.image.blit(self.text, (5, 5))

    def throw_error(self):
        self.error = True

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def normal(self):
        self.hovered = False

    def hover(self):
        self.hovered = True
