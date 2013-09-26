# -*- coding: utf-8 -*-
import pygame
import json
import os
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE, USEREVENT
from GUIElements import ScoreDisplay, QuestionDisplay, Popup, Button


class Game(object):
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        os.environ["SDL_VIDEO_CENTERED"] = '1'

        pygame.display.set_caption("Who Wants To Be A Pythonaire?")

        pygame.key.set_repeat(200, 80)

        info = pygame.display.Info()            # get display info
        screen_height = info.current_h
        screen_width = info.current_w
        self.width, self.height = 700, 700
        if screen_height < 800:
            self.height = 600
            self.width = 600
            if screen_height < 600:
                self.height = screen_height-39
                self.width = screen_width-16

        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            (pygame.RESIZABLE)
        )
        self.mysound = pygame.mixer.Sound("theme.ogg")

        self.failsound = pygame.mixer.Sound("fail.ogg")
        self.successound = pygame.mixer.Sound("success.ogg")

        self.fps = 60
        self.snakeimage = pygame.image.load("snake.png")
        self.snakeimage.convert_alpha()
        self.snakeimage = pygame.transform.smoothscale(
            self.snakeimage,
            (self.height, self.height)
        )
        self.background = pygame.Surface((self.width, self.height))

        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.convert_alpha()
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(130)

        self.show_overlay = False
        self.show_GUI = False

        self.choice_style = {
            "font_type": "custom",
            "font_family": "ArchivoBlack-Regular.otf",
            "font_size": self.width/30,
            "color_text": [30, 30, 31],
            "background_default": [203, 209, 207],  # 2EA736
            "background_right": [38, 153, 38],
            "background_wrong": [191, 48, 48],
            "background_hover": [253, 227, 44],     # 08DE16
            "color_border": [240, 240, 240]          # 03900C
        }

        self.choices = pygame.sprite.Group()

        self.question_style = {
            "font_type": "custom",
            "font_family": "Aleo-Regular.otf",
            "font_size": self.width/20,
            "color_text": [255, 255, 255],
            "background_default": [46, 167, 54],  # 466A58
            "color_border": [112, 239, 120]          # 30493D
        }

        self.question = pygame.sprite.GroupSingle()

        self.score_style = {
            "font_type": "custom",
            "font_family": "ArchivoBlack-Regular.otf",
            "font_size": self.width/30,
            "color_text": [0, 0, 0],
            "background_default": [255, 255, 255],
            "color_border": [240, 240, 240]
        }

        self.scoredisplay = pygame.sprite.GroupSingle()

        self.button_style_play = {
            "font_type": "custom",
            "font_family": "ArchivoBlack-Regular.otf",
            "font_size": self.width/30,
            "color_text": [255, 255, 255],
            "background_default": [38, 153, 38],
            "background_hover": [131, 224, 131],
            "color_border": [0, 133, 0]
        }

        self.button_style_quit = {
            "font_type": "custom",
            "font_family": "ArchivoBlack-Regular.otf",
            "font_size": self.width/30,
            "color_text": [255, 255, 255],
            "background_default": [191, 48, 48],
            "background_hover": [223, 139, 139],
            "color_border": [255, 64, 64]
        }

        self.popup_style_right = {
            "font_type": "custom",
            "font_family": "ArchivoBlack-Regular.otf",
            "font_size": self.width/10,
            "color_text": [255, 255, 255],
            "background_default": [46, 167, 54],  # 2EA736
            "background_hover": [8, 222, 22],     # 08DE16
            "color_border": [3, 144, 12]          # 03900C
        }

        self.popup_style_wrong = {
            "font_type": "custom",
            "font_family": "ArchivoBlack-Regular.otf",
            "font_size": self.width/10,
            "color_text": [255, 255, 255],
            "background_default": [191, 48, 48],
            "background_hover": [223, 139, 139],
            "color_border": [255, 64, 64]
        }

        self.buttons = pygame.sprite.Group()

        self.popup = pygame.sprite.GroupSingle()
        self.topinfo = pygame.sprite.GroupSingle()

        self.title = pygame.sprite.GroupSingle()

        self.mouse = pygame.sprite.GroupSingle()
        self.asking = True
        self.mouse.add(Mouse())

        self.start_game()

    def start_game(self):
        self.background.fill((255, 255, 255))
        self.background.blit(self.snakeimage, (0, 0))
        self.background.convert()

        with open('qa.json') as data_file:
            self.questions_answers = json.load(data_file)["qas"]

        self.scoredisplay.add(ScoreDisplay(
            self.score_style,
            [self.width, self.height],
            u"\u00A3",
            #"/{0}".format(len(self.questions_answers)),
            "bottom"
        ))
        self.scoredisplay.sprite.rect.bottom = self.height
        self.popup.empty()
        self.buttons.empty()
        self.next_question()
        self.show_overlay = False
        self.show_GUI = True

    def quit_game(self):
        return False

    def main(self):
        self.mysound.play(loops=-1, fade_ms=1000)
        while True:
            if self.input() is False:
                return False
            if self.popup.sprite:
                self.popup.update(pygame.time.get_ticks())
            if self.topinfo.sprite:
                self.topinfo.update(pygame.time.get_ticks())
            self.draw()

    def next_question(self):
        if len(self.questions_answers) > 0:
            self.qac = self.questions_answers.pop(0)

            self.question.add(QuestionDisplay(
                self.question_style,
                [self.width, self.height],
                self.qac["question"],
                "top"
            ))

            self.choices.empty()
            for index, choice in enumerate(self.qac["choices"]):
                self.choices.add(Button(
                    self.choice_style,
                    [self.width, self.height],
                    choice,
                    "bottom",
                    "",
                    id=index
                ))

        else:
            self.popup.add(Popup(
                self.score_style,
                [self.width, self.height],
                "Game Over!",
                "top",
                fade=False,
                size=[self.width/2, 0]
            ))

            score = self.scoredisplay.sprite.prevscore()
            self.topinfo.add(Popup(
                self.score_style,
                [self.width, self.height],
                "You made "+u"\u00A3"+str(score)+"!",
                "center",
                fade=False,
                size=[self.width/2, self.height/3]
            ))

            self.show_overlay = True
            self.show_GUI = False

            self.buttons.add(Button(
                self.button_style_play,
                [self.width, self.height],
                "PLAY AGAIN",
                "bottom",
                "start_game",
                id=4
            ))

            self.buttons.add(Button(
                self.button_style_quit,
                [self.width, self.height],
                "QUIT GAME",
                "bottom",
                "quit_game",
                id=5
            ))

    def input(self):
        self.mouse.sprite.move(pygame.mouse.get_pos())
        for event in pygame.event.get():

            if not self.asking:
                if event.type == USEREVENT+1:
                    self.asking = True
                    self.next_question()

            else:
                for choice in self.choices:
                    if pygame.sprite.spritecollide(choice, self.mouse, False):
                        if not self.show_overlay:
                            choice.hover()
                        else:
                            choice.unhover()
                    else:
                        choice.unhover()

                for button in self.buttons:
                    if pygame.sprite.spritecollide(button, self.mouse, False):
                        button.hover()
                    else:
                        button.unhover()

                if event.type == MOUSEBUTTONDOWN:
                    for choice in self.choices:
                        if choice.hovered:
                            self.check_answer(choice.text)
                    for button in self.buttons:
                        if button.hovered:
                            if self.perform_action(button.action) is False:
                                return False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                pass

            if event.type == QUIT:
                return False

    def perform_action(self, name):
        function = getattr(self, name)
        if function() is False:
            return False

    def check_answer(self, text):

        if self.qac["answer"] == text:
            newscore = self.scoredisplay.sprite.getscore()
            oldscore = self.scoredisplay.sprite.prevscore()
            difference = newscore-oldscore

            self.topinfo.add(Popup(
                self.button_style_play,
                [self.width, self.height],
                "+ "u"\u00A3"+str(difference),
                "bottom",
                float=True
            ))
            self.scoredisplay.update()
            self.successound.play()
        else:
            self.failsound.play()

        for choice in self.choices:
            if choice.text == self.qac["answer"]:
                choice.right()
            elif choice.text == text and choice.text != self.qac["answer"]:
                choice.wrong()
            else:
                self.choices.remove(choice)

        self.asking = False
        pygame.time.set_timer(USEREVENT+1, 1000)

    def draw(self):

        if self.show_overlay:
            self.scoredisplay.draw(self.screen)
            self.question.draw(self.screen)
            self.choices.draw(self.screen)
            self.screen.blit(self.overlay, (0, 0))
            self.background.blit(self.screen, (0, 0))
            self.show_overlay = False

        self.screen.blit(self.background, (0, 0))

        if self.show_GUI:
            self.scoredisplay.draw(self.screen)
            self.question.draw(self.screen)
            self.choices.draw(self.screen)

        self.topinfo.draw(self.screen)

        self.popup.draw(self.screen)
        self.buttons.draw(self.screen)
        pygame.display.update()


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 1, 1)

    def move(self, pos):
        self.rect.x, self.rect.y = pos

if __name__ == "__main__":
    game = Game()
    game.main()
