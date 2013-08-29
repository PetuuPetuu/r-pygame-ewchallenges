# -*- coding: utf-8 -*-
import pygame


class Title(pygame.sprite.Sprite):
    def __init__(self, font, colors, position, text):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont(font["family"], font["size"])

        size = self.font.size(text)
        self.rect = pygame.Rect((position), (size))
        self.text = text
        self.color = colors["text"]

        self.image = self.font.render(self.text, True, self.color)


