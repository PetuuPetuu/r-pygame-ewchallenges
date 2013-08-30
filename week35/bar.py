# -*- coding: utf-8 -*-
import pygame


class Bar(pygame.sprite.Sprite):
    def __init__(self, caption, value, maxvalue, maxheight, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", 12)
        self.caption = caption

        # truncate long strings on the chart
        if len(caption) > 10:
            caption = caption[:6]+"..."

        self.text = self.font.render(caption, True, (155, 155, 155))

        self.value = value
        self.maxvalue = maxvalue
        self.maxheight = maxheight
        # height is scaled according to the biggest value among bars
        self.height = int(1.0*value/maxvalue*maxheight)

        self.rect = pygame.Rect(x, y, width, maxheight)

        # drawn from the bottom
        self.rect.bottom = y

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill((255, 255, 255))
        self.image.convert_alpha()

        self.hovered = False
        self.selected = False

        self.bar = pygame.Surface((self.rect.width, self.height))
        self.bar.convert_alpha()
        self.bar.fill((205, 205, 205))

        self.bar_selected = pygame.Surface((self.rect.width, self.height))
        self.bar_selected.convert_alpha()
        self.bar_selected.fill((205, 205, 150))

        self.bar_hover = pygame.Surface((self.rect.width, self.height))
        self.bar_hover.convert_alpha()
        self.bar_hover.fill((150, 200, 150))

        self.image.blit(self.bar, (0, self.rect.height-self.height-30))

        twidth, theight = self.text.get_size()
        self.image.blit(self.text, (1, self.rect.height-theight))

    def set_size(self, maxvalue):
        self.height = int(1.0*self.value/maxvalue*self.maxheight)

        self.bar = pygame.Surface((self.rect.width, self.height))
        self.bar.convert_alpha()
        self.bar.fill((205, 205, 205))

        self.bar_selected = pygame.Surface((self.rect.width, self.height))
        self.bar_selected.convert_alpha()
        self.bar_selected.fill((200, 200, 150))

        self.bar_hover = pygame.Surface((self.rect.width, self.height))
        self.bar_hover.convert_alpha()
        self.bar_hover.fill((150, 200, 150))

    def move(self, x):
        self.rect.x += x

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def normal(self):
        self.hovered = False

    def hover(self):
        self.hovered = True

    def update(self):
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill((255, 255, 255))
        self.image.convert_alpha()

        if self.selected:
            self.image.blit(self.bar_selected,
                           (0, self.rect.height-self.height-30))
        elif self.hovered:
            self.image.blit(self.bar_hover,
                           (0, self.rect.height-self.height-30))
        else:
            self.image.blit(self.bar, (0, self.rect.height-self.height-30))

        twidth, theight = self.text.get_size()

        self.image.blit(self.text, (5, self.rect.height-theight))
