import os
import pygame
import json
from os.path import exists
from code.file_paths import (
    pokedex_path,
    pokemon_path,
    save_path,
    pkmnsprites_directory,
    backgrounds_directory,
    font_directory,
    music_directory,
)
from code.combat import Combat


class NewGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("New Game - Pokemon La Plateforme")

        self.custom_font_path = os.path.join(font_directory, "pkmn.ttf")
        self.font = pygame.font.Font(self.custom_font_path, 16)
        self.button_font = pygame.font.Font(self.custom_font_path, 11)

        self.load_data()
        self.load_sprites()

        self.current_selection = 0
        self.running = True
        self.show_popup = False

        self.background = pygame.image.load(
            os.path.join(backgrounds_directory, "newgame.jpg")
        )
        self.background = pygame.transform.scale(self.background, (800, 600))

        pygame.mixer.music.load(os.path.join(music_directory, "newgamemusic.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.buttons = {
            "PREVIOUS": pygame.Rect(220 - 10, 230 - 10, 120, 60),
            "NEXT": pygame.Rect(480 - 10, 230 - 10, 120, 60),
            "CONFIRM": pygame.Rect(350 - 10, 300 - 10, 120, 60),
            "YES": pygame.Rect(250 - 10, 300 - 10, 120, 60),
            "NO": pygame.Rect(450 - 10, 300 - 10, 120, 60),
        }

        self.run()

    def load_data(self):
        with open(pokemon_path, "r") as file:
            self.pokemons = json.load(file)
        self.pokemon_names = [pokemon["name"] for pokemon in self.pokemons]

    def load_sprites(self):
        self.pokemon_sprites = {}
        for pokemon in self.pokemons:
            sprite_path = os.path.join(pkmnsprites_directory, f"{pokemon['name']}.png")
            if os.path.exists(sprite_path):
                self.pokemon_sprites[pokemon["name"]] = pygame.image.load(sprite_path)

    def draw_pokemon_sprites(self):
        sprite = self.pokemon_sprites.get(self.pokemon_names[self.current_selection])
        if sprite:
            sprite_width = sprite.get_width()
            sprite_height = sprite.get_height()
            x_position = (self.screen.get_width() - sprite_width) // 2
            y_position = (self.screen.get_height() - sprite_height) // 2 - 100
            self.screen.blit(sprite, (x_position, y_position))
            name_text = self.font.render(
                self.pokemon_names[self.current_selection], True, (0, 0, 0)
            )
            name_text_width = name_text.get_width()
            name_x_position = (self.screen.get_width() - name_text_width) // 2
            name_y_position = y_position + sprite_height + 10
            self.screen.blit(name_text, (name_x_position, name_y_position))

    def draw_popup(self):
        if self.show_popup:
            popup_rect = pygame.Rect(200, 200, 400, 200)
            pygame.draw.rect(self.screen, (200, 200, 200), popup_rect)
            message_text = self.font.render("Overwrite current save?", True, (0, 0, 0))
            message_rect = message_text.get_rect(center=(400, 250))
            self.screen.blit(message_text, message_rect)
            for button_text in ["YES", "NO"]:
                button_rect = self.buttons[button_text]
                pygame.draw.rect(self.screen, (180, 180, 180), button_rect)
                text_surf = self.button_font.render(button_text, True, (0, 0, 0))
                text_rect = text_surf.get_rect(center=button_rect.center)
                self.screen.blit(text_surf, text_rect)

    def draw_buttons(self):
        for button_text, button_rect in self.buttons.items():
            if self.show_popup and button_text in ["YES", "NO"]:
                pygame.draw.rect(self.screen, (180, 180, 180), button_rect)
                text_surf = self.font.render(button_text, True, (0, 0, 0))
                text_rect = text_surf.get_rect(center=button_rect.center)
                self.screen.blit(text_surf, text_rect)
            elif not self.show_popup and button_text in ["PREVIOUS", "NEXT", "CONFIRM"]:
                pygame.draw.rect(self.screen, (180, 180, 180), button_rect)
                text_surf = self.button_font.render(button_text, True, (0, 0, 0))
                text_rect = text_surf.get_rect(center=button_rect.center)
                self.screen.blit(text_surf, text_rect)

    def handle_button_click(self, pos):
        for button_text, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                return button_text
        return None

    def create_save(self, pokemon_index):
        new_save = [self.pokemons[pokemon_index]]
        with open(pokedex_path, "w") as file:
            json.dump(new_save, file, indent=4)
        new_save[0]["level"] = 5
        with open(save_path, "w") as file:
            json.dump(new_save, file, indent=4)

    def start_combat(self):
        with open(save_path, "r") as file:
            pokemons = json.load(file)
        Combat(pokemons[0])

    def is_save_file_non_empty(self):
        return exists(save_path) and os.path.getsize(save_path) > 0

    def run(self):
        title_text = self.font.render("CHOOSE YOUR POKEMON !", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))

        while self.running:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(title_text, title_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_button = self.handle_button_click(event.pos)
                    if clicked_button == "PREVIOUS":
                        self.current_selection = (self.current_selection - 1) % len(
                            self.pokemon_names
                        )
                    elif clicked_button == "NEXT":
                        self.current_selection = (self.current_selection + 1) % len(
                            self.pokemon_names
                        )
                    elif clicked_button == "CONFIRM":
                        if self.is_save_file_non_empty():
                            self.show_popup = True
                        else:
                            self.create_save(self.current_selection)
                            self.start_combat()
                    elif clicked_button == "YES":
                        self.show_popup = False
                        self.create_save(self.current_selection)
                        self.start_combat()
                    elif clicked_button == "NO":
                        self.show_popup = False

            self.draw_pokemon_sprites()
            self.draw_buttons()
            self.draw_popup()
            pygame.display.flip()

        pygame.quit()
