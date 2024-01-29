import pygame
import json
import os
from code.file_paths import (
    font_directory,
    backgrounds_directory,
    music_directory,
    data_directory,
    select_sprites,
)


class Pokedex:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pokedex")
        self.background = pygame.image.load(
            os.path.join(backgrounds_directory, "pokedex.png")
        )
        self.font = pygame.font.Font(os.path.join(font_directory, "pkmn.ttf"), 16)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.HIGHLIGHT_COLOR = (255, 0, 0)  # Color to highlight selected Pokémon
        self.load_data()
        self.selected_index = 0
        self.list_offset = 0  # Offset for scrolling the list
        self.clock = pygame.time.Clock()

        pygame.mixer.music.load(os.path.join(music_directory, "pokedex.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.run()

    def load_data(self):
        with open(os.path.join(data_directory, "pokedex.json"), "r") as file:
            self.pokemon_data = json.load(file)
        self.sprites = {}
        for pokemon in self.pokemon_data:
            sprite_path = select_sprites(pokemon["name"].lower() + ".png")
            if os.path.exists(sprite_path):  # Check if sprite file exists
                self.sprites[pokemon["name"].lower()] = pygame.image.load(sprite_path)

    def handle_mouse_click(self, position):
        list_area_rect = pygame.Rect(30, 100, 140, 380)  # The list area
        if list_area_rect.collidepoint(position):
            # Calculate which index was clicked
            clicked_index = (
                position[1] - list_area_rect.y
            ) // 20 + self.list_offset // 20
            if clicked_index < len(self.pokemon_data):
                self.selected_index = clicked_index

    def render(self):
        # Draw the background
        self.screen.blit(self.background, (0, 0))

        # Draw the list of Pokémon names and the selected Pokémon details
        self.render_pokemon_list()
        self.render_selected_pokemon_info()

        # Update the display
        pygame.display.flip()

    def render_pokemon_list(self):
        list_area_rect = pygame.Rect(30, 100, 140, 380)  # Adjust to fit the left panel
        pygame.draw.rect(
            self.screen, self.WHITE, list_area_rect
        )  # Draw the list background
        # List each Pokémon name
        for i, pokemon in enumerate(self.pokemon_data):
            text_color = (
                self.HIGHLIGHT_COLOR if i == self.selected_index else self.BLACK
            )
            text_surface = self.font.render(pokemon["name"], True, text_color)
            self.screen.blit(
                text_surface, (list_area_rect.x + 5, list_area_rect.y + i * 20)
            )

    def render_selected_pokemon_info(self):
        if self.selected_index < len(self.pokemon_data):
            selected_pokemon = self.pokemon_data[self.selected_index]
            pokemon_name = selected_pokemon["name"].lower()

            # Render the sprite
            sprite = self.sprites.get(pokemon_name, None)
            if sprite:
                sprite_rect = pygame.Rect(460, 90, 300, 300)  # Position for the sprite
                sprite = pygame.transform.scale(
                    sprite, sprite_rect.size
                )  # Scale sprite to fit the designated area
                self.screen.blit(sprite, sprite_rect.topleft)

            # Render the Pokémon information
            info_x = 520  # Horizontal position for text
            info_y_start = 380  # Vertical starting position for text
            info_texts = [
                f"Name: {selected_pokemon['name']}",
                f"Attack: {selected_pokemon['attack_stat']}",
                f"Defense: {selected_pokemon['defense_stat']}",
            ]

            for i, text in enumerate(info_texts):
                text_surface = self.font.render(text, True, self.BLACK)
                self.screen.blit(text_surface, (info_x, info_y_start + i * 20))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
        return True

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.render()
            self.clock.tick(60)  # Cap the frame rate at 60 FPS

        pygame.quit()


# Main execution
if __name__ == "__main__":
    pokedex = Pokedex()
    pokedex.run()
