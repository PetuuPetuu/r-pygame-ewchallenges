# -*- coding: utf-8 -*-
import pygame
import json
import os
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE
from classes import Popup, Button, QuestionDisplay, ScoreDisplay


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
        self.width, self.height = 800, 800
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
        image = pygame.image.load("snake.png")
        image.convert_alpha()
        image = pygame.transform.smoothscale(image, (self.height, self.height))
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((255, 255, 255))
        self.background.blit(image, (0, 0))
        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.convert_alpha()
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(150)

        self.show_overlay = False
        self.background.convert()

        self.choice_font = {
            "type": "custom",
            "family": "ArchivoBlack-Regular.otf",
            "size": self.width/30
        }

        self.choice_colors = {
            "text": [255, 255, 255],
            "background": [65, 44, 132],
            "hover": [135, 110, 215],
            "border": [32, 7, 114]
        }

        self.choices = pygame.sprite.Group()

        self.question_font = {
            "type": "custom",
            "family": "Aleo-Regular.otf",
            "size": self.width/20
        }

        self.question_colors = {
            "text": [255, 255, 255],
            "background": [65, 44, 132],
            "border": [32, 7, 114]
        }

        self.question = pygame.sprite.GroupSingle()

        self.score_colors = {
            "text": [0, 0, 0],
            "background": [255, 255, 255],
            "border": [240, 240, 240]
        }

        self.popup_font = {
            "type": "custom",
            "family": "ArchivoBlack-Regular.otf",
            "size": self.width/10
        }

        self.popup_colors_right = {
            "text": [255, 255, 255],
            "background": [38, 153, 38],
            "hover": [131, 224, 131],
            "border": [0, 133, 0]
        }

        self.popup_colors_wrong = {
            "text": [255, 255, 255],
            "background": [191, 48, 48],
            "hover": [223, 139, 139],
            "border": [255, 64, 64]
        }

        self.scoredisplay = pygame.sprite.GroupSingle()
        self.buttons = pygame.sprite.Group()

        self.popup = pygame.sprite.GroupSingle()

        self.title = pygame.sprite.GroupSingle()

        self.mouse = pygame.sprite.GroupSingle()
        self.mouse.add(Mouse())

        self.start_game()

    def start_game(self):
        with open('qa.json') as data_file:
            self.questions_answers = json.load(data_file)["qas"]

        self.scoredisplay.add(ScoreDisplay(
            self.question_font,
            self.score_colors,
            [self.width, self.height],
            pygame.Rect(0, 0, 0, 0),
            "/{0}".format(len(self.questions_answers)),
            [False, False, False, False],
        ))
        self.popup.empty()
        self.buttons.empty()
        self.next_question()
        self.show_overlay = False

    def quit_game(self):
        return False

    def main(self):
        self.mysound.play(loops=-1, fade_ms=1000)
        while True:
            if self.input() is False:
                return False
            self.choices.update(pygame.time.get_ticks())
            if self.popup.sprite:
                self.popup.update(pygame.time.get_ticks())
            if self.buttons:
                self.buttons.update(pygame.time.get_ticks())
            #self.spritegroup.update(pygame.time.get_ticks())
            self.draw()

    def show_popup(self, text, colors):
        self.popup.add(Popup(
            self.popup_font,
            colors,
            [self.width, self.height],
            pygame.Rect(0, 0, self.width/2, self.height/2),
            text,
            [True, True, True, True]
        ))

    def next_question(self):
        if len(self.questions_answers) > 0:
            self.qac = self.questions_answers.pop(0)

            print self.qac
            self.question.add(QuestionDisplay(
                self.question_font,
                self.question_colors,
                [self.width, self.height],
                pygame.Rect(0, self.height/10, 0, 0),
                self.qac["question"],
                [True, False, False, False],
                self.qac["answer"]
            ))

            self.choices.empty()
            for index, choice in enumerate(self.qac["choices"]):
                self.choices.add(Button(
                    self.choice_font,
                    self.choice_colors,
                    [self.width, self.height],
                    pygame.Rect(0, 0, 0, 0),
                    choice,
                    [False, False, False, False],
                    "",
                    id=index+1
                ))

        else:
            self.popup.add(Popup(
                self.popup_font,
                self.choice_colors,
                [self.width, self.height],
                pygame.Rect(0, 0, self.width/2, self.height/2),
                "Game Over!",
                [True, True, True, False],
                fade=False
            ))

            self.show_overlay = True
            y = self.popup.sprite.rect.bottom

            self.buttons.add(Button(
                self.choice_font,
                self.popup_colors_right,
                [self.width, self.height],
                pygame.Rect(0, y, 0, 0),
                "PLAY AGAIN",
                [True, False, False, False],
                "start_game",
                id=5
            ))

            self.buttons.add(Button(
                self.choice_font,
                self.popup_colors_wrong,
                [self.width, self.height],
                pygame.Rect(0, y, 0, 0),
                "QUIT GAME",
                [True, False, False, False],
                "quit_game",
                id=6
            ))

    def input(self):
        self.mouse.sprite.move(pygame.mouse.get_pos())
        for event in pygame.event.get():

            for choice in self.choices:
                if pygame.sprite.spritecollide(choice, self.mouse, False):
                    if not self.show_overlay:
                        choice.hover()
                    else:
                        choice.normal()
                else:
                    choice.normal()

            for button in self.buttons:
                if pygame.sprite.spritecollide(button, self.mouse, False):
                    button.hover()
                else:
                    button.normal()

            if event.type == QUIT:
                return False

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

    def perform_action(self, name):
        function = getattr(self, name)
        if function() is False:
            return False

    def check_answer(self, text):
        answer = self.question.sprite.check_answer(text)
        if answer:
            self.show_popup("Correct!", self.popup_colors_right)
            self.scoredisplay.update()
            self.successound.play()
        else:
            self.show_popup("Wrong!", self.popup_colors_wrong)
            self.failsound.play()
        self.next_question()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.scoredisplay.draw(self.screen)
        self.question.draw(self.screen)
        self.choices.draw(self.screen)
        if self.show_overlay:
            self.screen.blit(self.overlay, (0, 0))
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
