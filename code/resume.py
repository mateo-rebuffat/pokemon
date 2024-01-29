import os
import pygame
import json
from code.file_paths import save_path, pkmnsprites_directory, backgrounds_directory, font_directory, music_directory
from code.combat import Combat

class ResumeGame:
    def __init__(self):
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            pygame.display.set_caption("Resume Game - Pokemon La Plateforme")

            self.custom_font_path = os.path.join(font_directory, "pkmn.ttf")
            self.font = pygame.font.Font(self.custom_font_path, 16)

            self.load_data()
            self.load_sprites()

            self.current_selection = 0
            self.running = True

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
            }

            self.run()
        except Exception as e:
            print(f"Error in ResumeGame __init__: {e}")


    def load_data(self):
        with open(save_path, "r") as file:
            self.saved_pokemons = json.load(file)
        self.pokemon_names = [pokemon["name"] for pokemon in self.saved_pokemons]

    def load_sprites(self):
        self.pokemon_sprites = {}
        for pokemon in self.saved_pokemons:
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

    def draw_buttons(self):
        for button_text, button_rect in self.buttons.items():
            pygame.draw.rect(self.screen, (180, 180, 180), button_rect)
            text_surf = self.font.render(button_text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=button_rect.center)
            self.screen.blit(text_surf, text_rect)

    def handle_button_click(self, pos):
        for button_text, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                return button_text
        return None

    def start_combat(self, pokemon_index):
        Combat(self.saved_pokemons[pokemon_index])


    def run(self):
        try:
            title_text = self.font.render("SELECT YOUR POKEMON !", True, (0, 0, 0))
            title_rect = title_text.get_rect(center=(800 // 2, 100))

            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        clicked_button = self.handle_button_click(event.pos)
                        if clicked_button == "PREVIOUS":
                            self.current_selection = (self.current_selection - 1) % len(self.pokemon_names)
                        elif clicked_button == "NEXT":
                            self.current_selection = (self.current_selection + 1) % len(self.pokemon_names)
                        elif clicked_button == "CONFIRM":
                            self.start_combat(self.current_selection)

                self.screen.blit(self.background, (0, 0))
                self.screen.blit(title_text, title_rect)
                self.draw_pokemon_sprites()
                self.draw_buttons()
                pygame.display.flip()
        except Exception as e:
            print(f"Error in ResumeGame run method: {e}")
            self.running = False

        pygame.quit()
