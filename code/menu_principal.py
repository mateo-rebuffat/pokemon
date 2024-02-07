import pygame
import os
import sys

from code.new_game import NewGame
from code.pokemonadd import PokemonAdd
from code.pokedex import Pokedex
from code.resume import ResumeGame
from code.file_paths import (
    img_directory,
    backgrounds_directory,
    music_directory,
    font_directory,
)


# Constantes pour les dimensions et les positions
WINDOW_SIZE = (800, 600)


class MainMenu:
    def __init__(self):
        pygame.init()
        self.window_size = WINDOW_SIZE
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Main Menu")

        # Logo du jeu
        self.logo = pygame.image.load(os.path.join(img_directory, "logo.png"))
        self.logo = pygame.transform.scale(self.logo, (500, 200))
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (self.window_size[0] // 2, 120)

        # Arrière-plan du menu
        self.background = pygame.image.load(
            os.path.join(backgrounds_directory, "mainmenu.jpg")
        )
        self.background = pygame.transform.scale(self.background, self.window_size)

        # Position de l'arrière-plan
        self.background_position = 0

        # Animation du logo
        self.logo_bounce = 4
        self.bounce_direction = 3

        # Bouton sélectionné
        self.selected_button = 0

        # Chargement de la musique
        pygame.mixer.music.load(os.path.join(music_directory, "mainmenumusic.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Boutons du menu
        self.buttons = [
            {"text": "NEW GAME", "position": (self.window_size[0] // 2, 300)},
            {"text": "CONTINUE", "position": (self.window_size[0] // 2, 330)},
            {
                "text": "POKEDEX",
                "position": (self.window_size[0] // 2, 370),
            },  # New Pokédex button
            {"text": "ADD A POKEMON", "position": (self.window_size[0] // 2, 410)},
            {"text": "QUIT THE GAME", "position": (self.window_size[0] // 2, 450)},
        ]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(self.buttons):
                    if (
                        button["position"][0] - 100
                        < event.pos[0]
                        < button["position"][0] + 100
                        and button["position"][1] - 15
                        < event.pos[1]
                        < button["position"][1] + 15
                    ):
                        self.button_clicked(button["text"])

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_button = (self.selected_button + 1) % len(
                        self.buttons
                    )
                elif event.key == pygame.K_UP:
                    self.selected_button = (self.selected_button - 1) % len(
                        self.buttons
                    )
                elif event.key == pygame.K_RETURN:
                    self.button_clicked(self.buttons[self.selected_button]["text"])

    def button_clicked(self, button_text):
        buttons = {
            "QUIT THE GAME": self.quit,
            "NEW GAME": NewGame,
            "POKEDEX": Pokedex,
            "ADD A POKEMON": PokemonAdd,
            "CONTINUE": ResumeGame
        }
        if button_text in buttons:
            buttons[button_text]()
        else:
            print(f"CE BOUTON NE MARCHE PAS ENCORE: {button_text}")

    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.handle_events()

            # Animation de l'arrière-plan
            self.background_position -= 1
            if self.background_position <= -self.window_size[0]:
                self.background_position = 0

            # Animation du logo
            bounce_speed = 0.2
            max_bounce = 10
            if self.logo_bounce > max_bounce:
                self.bounce_direction = -1
            elif self.logo_bounce < -max_bounce:
                self.bounce_direction = 1

            self.logo_bounce += bounce_speed * self.bounce_direction

            self.logo_rect.centery = 120 + self.logo_bounce

            # Affichage
            self.screen.blit(self.background, (self.background_position, 0))
            self.screen.blit(
                self.background, (self.background_position + self.window_size[0], 0)
            )

            self.screen.blit(self.logo, self.logo_rect)

            custom_font = pygame.font.Font(os.path.join(font_directory, "pkmn.ttf"), 16)
            for i, button in enumerate(self.buttons):
                text = custom_font.render(button["text"], True, (0, 0, 0))
                text_rect = text.get_rect(center=button["position"])
                self.screen.blit(text, text_rect)

                if i == self.selected_button:
                    pygame.draw.rect(
                        self.screen,
                        (0, 0, 0),
                        (
                            text_rect.x - 8,
                            text_rect.y - 8,
                            text_rect.width + 16,
                            text_rect.height + 16,
                        ),
                        4,
                    )

            pygame.display.flip()
            clock.tick(60)

    def quit(self):
        pygame.quit()
        sys.exit()
