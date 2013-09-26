# -*- coding: utf-8 -*-
import pygame


class GUIElement(pygame.sprite.Sprite):
    def __init__(self, style, screensize, text, align):
        pygame.sprite.Sprite.__init__(self)

        # padding and border size
        self.padding = screensize[0]/100
        self.bordersize = screensize[0]/200
        self.fullpadding = self.padding*2+self.bordersize*2

        self.align = align
        self.screensize = screensize
        self.text = text
        self.style = style
        self.color = style["color_text"]

        # get font values
        font_family = style["font_family"]
        font_size = style["font_size"]

        # distinguish between system fonts and font files
        if style["font_type"] == "custom":
            self.font = pygame.font.Font(font_family, font_size)
        elif style["font_type"] == "system":
            try:
                self.font = pygame.font.SysFont(font_family, font_size)
            except:
                print "Font not found, defaulting to Arial..."
                self.font = pygame.font.Font("Arial", font_size)

        self.text_image = self.font.render(text, True, self.color)
        self.rect = pygame.Rect(
            0, 0,
            self.text_image.get_width()+self.fullpadding,
            self.text_image.get_height()+self.fullpadding
        )

        self.resize(self.rect.width, self.rect.height)

    def resize(self, w, h):

        self.rect.width, self.rect.height = w+self.padding, h+self.padding

        t = self.padding
        l = self.padding
        b = self.screensize[1]-self.rect.height-self.padding
        r = self.screensize[0]-self.rect.width-self.fullpadding-self.padding
        c = self.screensize[0]/2-self.rect.width/2
        m = self.screensize[1]/2-self.rect.height/2

        aligns = {
            "left": (l, m),
            "right": (r, m),
            "top": (c, t),
            "topleft": (l, t),
            "topright": (r, t),
            "bottom": (c, b),
            "bottomleft": (l, b),
            "bottomright": (r, b),
            "center": (c, m)
        }

        self.rect.x, self.rect.y = aligns[self.align]

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.convert()

        # border color
        self.border = pygame.Surface((self.rect.width, self.rect.height))
        self.border.convert()
        self.border.fill(self.style["color_border"])
        self.image.blit(self.border, (0, 0))

        # background color
        self.background = pygame.Surface((
            self.rect.width-self.bordersize*2,
            self.rect.height-self.bordersize*2
        ))
        self.background.convert()
        self.background.fill(self.style["background_default"])
        self.image.blit(self.background, (self.bordersize, self.bordersize))
        w, h = self.text_image.get_size()
        self.image.blit(
            self.text_image,
            (self.rect.width/2-w/2, self.rect.height/2-h/2)
        )


class ScoreDisplay(GUIElement):
    def __init__(self, style, screensize, text, align):
        super(ScoreDisplay, self).__init__(style, screensize, text, align)

        self.score = 0
        h = self.rect.height
        self.resize(screensize[0]-self.bordersize*2, h*2-self.padding*2)
        

        self.scores = [
            0,
            100,
            200,
            300,
            500,
            1000,
            2000,
            4000,
            8000,
            16000,
            32000,
            64000,
            125000,
            250000,
            500000,
            1000000
        ]

        self.update()

    def update(self):

        text = self.text+str(self.scores[self.score])

        self.image.blit(self.border, (0, 0))
        self.image.blit(self.background, (self.bordersize, self.bordersize))
        self.text_image = self.font.render(text, True, self.color)

        w, h = self.text_image.get_size()
        imagepos = (self.rect.width/2-w/2, self.rect.height/2-h/2)

        self.image.blit(self.text_image, imagepos)
        if self.score < len(self.scores):
            self.score += 1

    def getscore(self):
        return self.scores[self.score]

    def prevscore(self):
        return self.scores[self.score-1]

class Popup(GUIElement):
    def __init__(self, style, screensize, text, align, size=None, fade=True,
                 float=False):
        super(Popup, self).__init__(style, screensize, text, align)

        self.alpha = 255

        self.fade = fade
        self.float = float
        self._start = pygame.time.get_ticks()
        self._delay = 500
        self._fdelay = 100
        self._last_update = 0

        if size is not None:
            if size[0] > self.rect.width:
                self.rect.width = size[0]
            if size[1] > self.rect.height:
                self.rect.height = size[1]
            self.resize(self.rect.width, self.rect.height)

        self.update(pygame.time.get_ticks())

    def update(self, time):

        if self.fade and time - self._last_update-self._start > self._delay:
            if self.alpha > 0:
                self.alpha -= 5
            self.image.set_alpha(self.alpha)
        if self.float and time - self._last_update-self._start > self._fdelay:
            self.rect.y -= 1


class QuestionDisplay(GUIElement):
    def __init__(self, style, screensize, text, align):
        super(QuestionDisplay, self).__init__(style, screensize, text, align)

        size = self.text_image.get_size()
        if size[0] >= screensize[0]-self.fullpadding-self.padding*2:
            divider = size[0]/(screensize[0]-self.fullpadding-self.padding*2)+1
            slist = []

            part = len(text)/divider
            while True:
                t = text[:part]
                if part > len(text):
                    slist.append(text)
                    break
                else:
                    splitter = t.rfind(" ")
                    slist.append(text[:splitter])
                    text = text[splitter:]

            #for i in xrange(0, len(tlist), len(tlist)/divider):
            #    slist.append(" ".join(tlist[i:i+len(tlist)/divider]))

            size = self.font.size(slist[0])
            for item in slist:
                sz = self.font.size(item)
                if size[0] < sz[0]:
                    size = sz
            self.text_image = pygame.Surface((
                size[0]+self.padding*2,
                size[1]*len(slist)+self.padding*(len(slist)-1)
            ))
            self.text_image.fill(style["background_default"])
            for i, item in enumerate(slist):
                self.text_image.blit(self.font.render(
                    item, True, self.color),
                    (self.padding, i*size[1]+i*self.padding))
            size = self.text_image.get_width(), self.text_image.get_height()

        else:
            size = (size[0]+self.padding*2, size[1])

        self.resize(size[0], size[1])


class Button(GUIElement):
    def __init__(self, style, screensize, text, align, action, id=None):
        super(Button, self).__init__(style, screensize, text, align)

        # states
        self.colorchange = None
        self.hovered = False
        self.action = action

        choicesize_x = screensize[0]/2-self.padding*3-self.fullpadding*3
        buttonsize_x = screensize[0]/4

        sizes = [
            [choicesize_x, self.rect.height-self.fullpadding],
            [choicesize_x, self.rect.height-self.fullpadding],
            [choicesize_x, self.rect.height-self.fullpadding],
            [choicesize_x, self.rect.height-self.fullpadding],
            [buttonsize_x, self.rect.height-self.fullpadding],
            [buttonsize_x, self.rect.height-self.fullpadding]
        ]

        self.resize(sizes[id][0], sizes[id][1])

        if id is not None:
            positions = [
                [self.padding,
                 screensize[1]-self.rect.height*2-self.padding*2],
                [self.padding, screensize[1]-self.rect.height-self.padding],
                [screensize[0]-self.rect.width-self.padding,
                 screensize[1]-self.rect.height*2-self.padding*2],
                [screensize[0]-self.rect.width-self.padding,
                 screensize[1]-self.rect.height-self.padding],
                [screensize[0]/2-self.rect.width/2,
                 screensize[1]/2-self.rect.height*2],
                [screensize[0]/2-self.rect.width/2,
                 screensize[1]/2+self.rect.height]
            ]

            self.rect.x, self.rect.y = positions[id]

    def update(self):

        if self.colorchange:
            self.background.fill(self.style[self.colorchange])
            self.colorchange = None

        self.image.blit(self.background, (self.bordersize, self.bordersize))

        w, h = self.text_image.get_size()
        imagepos = (self.rect.width/2-w/2, self.rect.height/2-h/2)
        self.image.blit(self.text_image, imagepos)

    def unhover(self):
        self.colorchange = "background_default"
        self.hovered = False
        self.update()

    def hover(self):
        self.colorchange = "background_hover"
        self.hovered = True
        self.update()

    def right(self):
        self.colorchange = "background_right"
        self.update()

    def wrong(self):
        self.colorchange = "background_wrong"
        self.update()