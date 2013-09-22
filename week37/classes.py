# -*- coding: utf-8 -*-
import pygame


class UIElement(pygame.sprite.Sprite):
    def __init__(self, font, colors, screensize, rect, text, align):
        pygame.sprite.Sprite.__init__(self)

        # get font values
        font_family = font["family"]
        fontsize = font["size"]

        # distinguish between system fonts and font files
        if font["type"] == "custom":
            self.font = pygame.font.Font(font_family, fontsize)
        elif font["type"] == "system":
            try:
                self.font = pygame.font.SysFont(font_family, fontsize)
            except:
                print "Font not found, default to Arial"
                self.font = pygame.font.Font("Arial", fontsize)

        self.align = align
        self.screensize = screensize

        self.text = text
        self.colors = colors
        self.color = self.colors["text"]
        self.text_image = self.font.render(text, True, self.color)
        size = self.text_image.get_width(), self.text_image.get_height()
        #print size

        # padding and border size
        self.padding = screensize[0]/100
        self.bordersize = screensize[0]/200

        self.rect = rect

        if self.rect.width < size[0]:
            self.rect.width = size[0]+self.padding*2+self.bordersize*2

        if self.rect.height < size[1]:
            self.rect.height = size[1]+self.padding*2+self.bordersize*2

        if self.align[0]:
            self.rect.x = screensize[0]/2-self.rect.width/2
        if self.align[1]:
            self.rect.y = screensize[1]/2-self.rect.height/2

        #print "rect: {0}".format(self.rect)

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.convert()

        # border color
        self.border = pygame.Surface((self.rect.width, self.rect.height))
        self.border.convert()
        self.border.fill(colors["border"])
        self.image.blit(self.border, (0, 0))

        # background color
        self.background = pygame.Surface((
            self.rect.width-self.bordersize*2,
            self.rect.height-self.bordersize*2
        ))
        self.background.convert()
        self.background.fill(colors["background"])
        self.image.blit(self.background, (self.bordersize, self.bordersize))
        imagepos = [self.padding, self.padding]
        if self.align[2]:
            imagepos[0] = (self.rect.width-self.text_image.get_width())/2
        if self.align[3]:
            imagepos[1] = (self.rect.height-self.text_image.get_height())/2
            #print imagepos[1]
        self.image.blit(self.text_image, imagepos)

    def resize(self, width, height):
        width += self.padding*2+self.bordersize*2
        height += self.padding*2+self.bordersize*2
        self.image = pygame.Surface((width, height))
        self.image.convert()
        self.border = pygame.Surface((width, height))
        self.border.convert()
        self.border.fill(self.colors["border"])
        self.image.blit(self.border, (0, 0))

        # background color
        self.background = pygame.Surface((
            width-self.bordersize*2,
            height-self.bordersize*2
        ))
        self.background.convert()
        self.background.fill(self.colors["background"])
        self.image.blit(self.background, (self.bordersize, self.bordersize))
        imagepos = [self.padding, self.padding]
        if self.align[2]:
            imagepos[0] = (self.rect.width-self.text_image.get_width())/2
        if self.align[3]:
            imagepos[1] = (self.rect.height-self.text_image.get_height())/2
            #print imagepos[1]
        self.image.blit(self.text_image, imagepos)

        self.rect.width, self.rect.height = width, height

        if self.align[0]:
            self.rect.x = self.screensize[0]/2-width/2
        if self.align[1]:
            self.rect.y = self.screensize[1]/2-height/2


class ScoreDisplay(UIElement):
    def __init__(self, font, colors, screensize,
                 rect, text, align):
        super(ScoreDisplay, self).__init__(font, colors, screensize,
                                           rect, text, align)

        self.score = -1
        self.update()
        self.resize(self.text_image.get_width(), self.text_image.get_height())

    def update(self):

        self.score += 1
        text = str(self.score)+self.text

        self.image.blit(self.border, (0, 0))
        self.image.blit(self.background, (self.bordersize, self.bordersize))
        self.text_image = self.font.render(text, True, self.color)
        self.image.blit(self.text_image, (self.padding, self.padding))


class Popup(UIElement):
    def __init__(self, font, colors, screensize,
                 rect, text, align, fade=True):
        super(Popup, self).__init__(font, colors, screensize,
                                    rect, text, align)

        self.ready_to_be_removed = False

        self.fade = fade

        self._start = pygame.time.get_ticks()
        self._delay = 300
        self._last_update = 0

        self.alpha = 255
        self.update(pygame.time.get_ticks())

    def update(self, time):

        if time - self._last_update-self._start > self._delay and self.fade:
            if self.alpha > 0:
                self.alpha -= 5
            self.image.set_alpha(self.alpha)


class QuestionDisplay(UIElement):
    def __init__(self, font, colors, screensize, rect, text, align, answer):
        super(QuestionDisplay, self).__init__(font, colors, screensize,
                                              rect, text, align)
        self.answer = answer

        size = self.text_image.get_width(), self.text_image.get_height()
        if size[0] >= font["size"]*18:
            divider = size[0]/(font["size"]*16)+1
            #print divider
            tlist = text.split()
            slist = []

            for i in xrange(0, len(tlist), len(tlist)/divider):
                slist.append(" ".join(tlist[i:i+len(tlist)/divider]))
                #print tlist[i:i+divider]

            size = self.font.size(slist[0])
            for item in slist:
                sz = self.font.size(item)
                if size[0] < sz[0]:
                    size = sz
            self.text_image = pygame.Surface((
                size[0], size[1]*len(slist)+self.padding*(len(slist)-1)
            ))
            self.text_image.fill(colors["background"])
            for i, item in enumerate(slist):
                self.text_image.blit(self.font.render(
                    item, True, self.color),
                    (0, i*size[1]+i*self.padding))
            size = self.text_image.get_width(), self.text_image.get_height()

        self.resize(size[0], size[1])

    def check_answer(self, answer):
        if answer == self.answer:
            return True
        return False


class Button(UIElement):
    def __init__(self, font, colors, screensize, rect, text, align,
                 action, id=0):
        super(Button, self).__init__(font, colors, screensize,
                                     rect, text, align)

        # states
        self.hovered = False
        self.selected = False
        self.error = False

        self.action = action

        fontsize = font["size"]

        offset = self.padding*3+self.bordersize*2
        off = fontsize+self.padding*2+self.bordersize*2

        ids = [
            [self.padding, screensize[1]-off*2-offset*2],
            [self.padding, screensize[1]-off-offset],
            [screensize[0]-self.padding*4, screensize[1]-off*2-offset*2],
            [screensize[0]-self.padding*4, screensize[1]-off-offset]
        ]

        passed = self.rect.y
        #print passed

        if id != 0:
            self.rect.width = screensize[0]/2-self.padding*5
            self.rect.height = fontsize+self.padding*2+self.bordersize*2
            y = self.rect.height
            if id == 1 or id == 2:
                pos = ids[id-1]
                self.rect.topleft = pos
            elif id == 3 or id == 4:
                pos = ids[id-1]
                self.rect.topright = pos
            elif id == 5:
                #print y
                self.rect.y = self.rect.x-y*2-self.padding*2-self.bordersize
            elif id == 6:
                self.rect.y = self.rect.x-y-self.padding

        # border color
        self.background = pygame.Surface((self.rect.width, self.rect.height))
        self.background.convert_alpha()
        self.background.fill(colors["border"])
        self.image.blit(self.background, (0, 0))

        # background color
        self.background = pygame.Surface((
            self.rect.width-self.bordersize*2,
            self.rect.height-self.bordersize*2
        ))
        self.background.convert_alpha()
        self.background.fill(colors["background"])
        self.image.blit(self.background, (self.bordersize, self.bordersize))

        # background color when hovered
        self.background_hover = pygame.Surface((
            self.rect.width-self.bordersize*2,
            self.rect.height-self.bordersize*2
        ))
        self.background_hover.convert_alpha()
        self.background_hover.fill(colors["hover"])

        self.resize(self.rect.width, self.rect.height)

        # set vertical bar ticking rate
        self._start = pygame.time.get_ticks()
        self._delay = 20000 / 60
        self._errordelay = 10000 / 60
        self._last_update = 0
        self._frame = 0

        #print self.rect

        self.update(pygame.time.get_ticks())
        y = self.rect.height
        if id == 5:
            self.rect.top = passed-y*2-self.padding*2-self.bordersize
            #print passed-y*2-self.padding*2-self.bordersize
            #print "s"
        elif id == 6:
            self.rect.top = passed-y-self.padding-self.bordersize

    def resize(self, width, height):

        width += self.padding*2+self.bordersize*2
        height += self.padding*2+self.bordersize*2

        self.image = pygame.Surface((width, height))
        self.image.convert()
        self.border = pygame.Surface((width, height))
        self.border.convert()
        self.border.fill(self.colors["border"])
        self.image.blit(self.border, (0, 0))

        # background color
        self.background = pygame.Surface((
            width-self.bordersize*2,
            height-self.bordersize*2
        ))
        self.background.convert_alpha()
        self.background.fill(self.colors["background"])
        self.image.blit(self.background, (self.bordersize, self.bordersize))

        # background color when hovered
        self.background_hover = pygame.Surface((
            width-self.bordersize*2,
            height-self.bordersize*2
        ))
        self.background_hover.convert_alpha()
        self.background_hover.fill(self.colors["hover"])

        # background color
        self.background = pygame.Surface((
            width-self.bordersize*2,
            height-self.bordersize*2
        ))
        self.background.convert()
        self.background.fill(self.colors["background"])
        self.image.blit(self.background, (self.bordersize, self.bordersize))

        imagepos = [+self.bordersize, self.padding+self.bordersize]
        if self.align[2]:
            imagepos[0] = (self.rect.width-self.text_image.get_width())/2
        if self.align[3]:
            imagepos[1] = (self.rect.height-self.text_image.get_height())/2
        self.rect.width, self.rect.height = width, height

        if self.align[0]:
            self.rect.x = self.screensize[0]/2-width/2
        if self.align[1]:
            self.rect.y = self.screensize[1]/2-height/2

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

        elif self.hovered:
            self.image.blit(self.background_hover, (
                self.bordersize,
                self.bordersize
            ))
        else:
            self.image.blit(self.background, (
                self.bordersize,
                self.bordersize
            ))

        imagepos = [
            self.padding+self.bordersize,
            self.padding+self.bordersize
        ]
        if self.align[2]:
            imagepos[0] = (self.rect.width-self.text_image.get_width())/2
        if self.align[3]:
            imagepos[1] = (self.rect.height-self.text_image.get_height())/2
            #print imagepos[1]
        self.image.blit(self.text_image, imagepos)

    def normal(self):
        self.hovered = False

    def hover(self):
        self.hovered = True
