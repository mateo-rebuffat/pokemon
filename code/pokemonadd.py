import pygame
import os
import json
import shutil
from tkinter import filedialog
from tkinter import Tk
from code.file_paths import (
    backgrounds_directory,
    music_directory,
    font_directory,
    pkmnsprites_directory,
    pokemon_path,
    select_sprites,
)

# Constants for the dimensions and positions
WINDOW_SIZE = (800, 600)
INPUT_BOX_WIDTH = 140
INPUT_BOX_HEIGHT = 32
FONT_SIZE = 24
BUTTON_SIZE = (300, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class PokemonAdd:
    def __init__(self):
        pygame.init()
        self.window_size = WINDOW_SIZE
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Add A Pokemon")

        # Load the background
        self.background = pygame.image.load(
            os.path.join(backgrounds_directory, "addpokemon.jpg")
        )
        self.background = pygame.transform.scale(self.background, self.window_size)

        # Font for the input boxes and buttons
        self.font = pygame.font.Font(
            os.path.join(font_directory, "pkmn.ttf"), FONT_SIZE
        )

        # Define the positions for input boxes and buttons
        self.name_box_pos = (self.window_size[0] * 0.3, self.window_size[1] * 0.43)
        self.type_box_pos = (self.window_size[0] * 0.3, self.window_size[1] * 0.5)
        self.atk_box_pos = (self.window_size[0] * 0.7, self.window_size[1] * 0.43)
        self.def_box_pos = (self.window_size[0] * 0.7, self.window_size[1] * 0.5)
        self.select_sprite_button_pos = (
            self.window_size[0] * 0.4,
            self.window_size[1] * 0.6,
        )
        self.save_button_pos = (self.window_size[0] * 0.4, self.window_size[1] * 0.7)

        # Create input boxes
        self.input_boxes = {
            "name": pygame.Rect(self.name_box_pos, (INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)),
            "type": pygame.Rect(self.type_box_pos, (INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)),
            "atk": pygame.Rect(self.atk_box_pos, (INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)),
            "def": pygame.Rect(self.def_box_pos, (INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)),
        }

        # Create buttons
        self.buttons = {
            "select_sprite": pygame.Rect(self.select_sprite_button_pos, BUTTON_SIZE),
            "save": pygame.Rect(self.save_button_pos, BUTTON_SIZE),
        }

        # Input data
        self.input_data = {"name": "", "type": "", "atk": "", "def": "", "sprite": None}

        self.active_input = None

        # Load and play background music
        pygame.mixer.music.load(os.path.join(music_directory, "pokeadd.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.running = True
        self.run()

    def render_labels(self):
        labels = {"name": "NAME :", "type": "TYPE :", "atk": "ATK :", "def": "DEF :"}
        for key, label in labels.items():
            label_surface = self.font.render(label, True, BLACK)
            label_rect = label_surface.get_rect()
            label_rect.topleft = (
                self.input_boxes[key].x - label_surface.get_width() - 10,
                self.input_boxes[key].y,
            )
            self.screen.blit(label_surface, label_rect)

    def handle_events(self):
        MAX_NAME_LENGTH = 10  # Set the maximum length for the name input

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 is the mouse left button
                    self.handle_click(event.pos)
                    # Set the active input box
                    for input_name, input_box in self.input_boxes.items():
                        if input_box.collidepoint(event.pos):
                            self.active_input = input_name
                            break
                    else:
                        self.active_input = None  # Clicked outside any box, so deselect
            elif event.type == pygame.KEYDOWN:
                if self.active_input:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_data[self.active_input] = self.input_data[
                            self.active_input
                        ][:-1]
                    elif event.key == pygame.K_RETURN:
                        self.active_input = (
                            None  # Deselect input box when enter is pressed
                        )
                    else:
                        if (
                            self.active_input == "name"
                            and len(self.input_data["name"]) >= MAX_NAME_LENGTH
                        ):
                            # If the maximum length is reached, don't add more characters
                            continue
                        self.input_data[self.active_input] += event.unicode
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        return True

    def handle_click(self, position):
        # Check if any of the buttons were clicked
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(position):
                if button_name == "select_sprite":
                    self.select_sprite()
                elif button_name == "save":
                    self.save_pokemon()
                break  # If a button was clicked, no need to check the others

    # Placeholder methods for select_sprite and save_pokemon
    def select_sprite(self):
        # Open a file dialog to select a sprite
        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        sprite_path = (
            filedialog.askopenfilename()
        )  # show an "Open" dialog box and return the path to the selected file
        if sprite_path:
            self.input_data["sprite"] = sprite_path

    def save_pokemon(self):
        print("Attempting to save the pokemon...")  # Debug print
        # Check if all fields are filled
        if not all(self.input_data.values()):
            print("Some fields are missing.")
            return

        # Move the sprite image to the pkmnsprites directory
        try:
            if self.input_data["sprite"]:
                sprite_filename = os.path.basename(self.input_data["sprite"])
                sprite_destination = os.path.join(
                    pkmnsprites_directory, sprite_filename
                )
                shutil.move(self.input_data["sprite"], sprite_destination)
                print(f"Sprite moved to {sprite_destination}")
        except Exception as e:
            print(f"An error occurred while moving the sprite: {e}")
            return

        # Save the data to pokemon.json
        try:
            with open(pokemon_path, "r") as file:
                pokemon_list = json.load(file)

            new_pokemon = {
                "name": self.input_data["name"],
                "types": self.input_data["type"],
                "attack_stat": int(self.input_data["atk"]),
                "defense_stat": int(self.input_data["def"]),
            }

            pokemon_list.append(new_pokemon)

            with open(pokemon_path, "w") as file:
                json.dump(pokemon_list, file, indent=4)

            print("Pokemon saved successfully.")
        except Exception as e:
            print(f"An error occurred while saving the Pokemon: {e}")

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()

            # Clear the screen and draw the background
            self.screen.blit(self.background, (0, 0))

            # Render labels for input boxes
            self.render_labels()

            # Draw input boxes and text within them
            for key, box in self.input_boxes.items():
                text_surface = self.font.render(self.input_data[key], True, BLACK)
                # Adjust the width of the box if the text is too long
                box.w = max(INPUT_BOX_WIDTH, text_surface.get_width() + 10)
                # Draw the input box
                pygame.draw.rect(self.screen, WHITE, box)
                pygame.draw.rect(self.screen, BLACK, box, 2)  # Border for the box
                # Blit the text surface onto the screen at the position of the input box
                self.screen.blit(text_surface, (box.x + 5, box.y + 5))

            # Draw buttons
            for button_name, button_rect in self.buttons.items():
                button_text = self.font.render(
                    button_name.replace("_", " ").title(), True, BLACK
                )
                pygame.draw.rect(self.screen, WHITE, button_rect)
                pygame.draw.rect(
                    self.screen, BLACK, button_rect, 2
                )  # Border for the button
                # Center the text on the button
                self.screen.blit(
                    button_text,
                    (
                        button_rect.x
                        + (button_rect.width - button_text.get_width()) // 2,
                        button_rect.y
                        + (button_rect.height - button_text.get_height()) // 2,
                    ),
                )

            pygame.display.flip()  # Update the full display Surface to the screen
            clock.tick(60)  # Cap the frame rate at 60 frames per second


if __name__ == "__main__":
    pokemon_add_app = PokemonAdd()
    pokemon_add_app.run()
