# LIGNE 51 POUR MODIFIER TAILLE FONT
import os # REDUNDANT
import json
from random import choice

import pygame

from code.file_paths import save_path, pokemon_path, pokedex_path, font_directory, backgrounds_directory, music_directory, pkmnsprites_directory
from code.pokemon import Pokemon


class Combat:
    # player_pokemon est une instance de la classe Pokemon
    def __init__(self, player_pokemon):
        # `fmt` permet de dire à "black" (programme qui gère le format du code)
        # de ne pas toucher au tuple
        # fmt: off

        # Ce tuple est comme un tableau contenant
        # les facteurs par lesquels le dommage est multiplié
        # Basé sur le tableau Gen 2 de pokemondb.net/type
        self.type_chart = (
            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
            (0,1,1,1,1,1,1,1,1,1,1,1,1,0.5,0,1,1,0.5),
            (0,1,0.5,0.5,1,2,2,1,1,1,1,1,2,0.5,1,0.5,1,2),
            (0,1,2,0.5,1,0.5,1,1,1,2,1,1,1,2,1,0.5,1,1),
            (0,1,1,2,0.5,0.5,1,1,1,0,2,1,1,1,1,0.5,1,1),
            (0,1,0.5,2,1,0.5,1,1,0.5,2,0.5,1,0.5,2,1,0.5,1,0.5),
            (0,1,0.5,0.5,1,2,0.5,1,1,2,2,1,1,1,1,2,1,0.5),
            (0,2,1,1,1,1,2,1,0.5,1,0.5,0.5,0.5,2,0,1,2,2),
            (0,1,1,1,1,2,1,1,0.5,0.5,1,1,1,0.5,0.5,1,1,0),
            (0,1,2,1,2,0.5,1,1,2,1,0,1,0.5,2,1,1,1,2),
            (0,1,1,1,0.5,2,1,2,1,1,1,1,2,0.5,1,1,1,0.5),
            (0,1,1,1,1,1,1,2,2,1,1,0.5,1,1,1,1,0,0.5),
            (0,1,0.5,1,1,2,1,0.5,0.5,1,0.5,2,1,1,0.5,1,2,0.5),
            (0,1,2,1,1,1,2,0.5,1,0.5,2,1,2,1,1,1,1,0.5),
            (0,0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,0.5,0.5),
            (0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,0.5),
            (0,1,1,1,1,1,1,0.5,1,1,1,2,1,1,2,1,0.5,0.5),
            (0,1,0.5,0.5,0.5,1,2,1,1,1,1,1,1,2,1,1,1,0.5)
        )
        # fmt: on

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load(
            os.path.join(backgrounds_directory, "battlebg.png")
        )
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.custom_font_path = os.path.join(font_directory, "pkmn.ttf")
        self.font = pygame.font.Font(self.custom_font_path, 13)

        pygame.mixer.music.load(os.path.join(music_directory, "battle.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.key_pressed = False

        self.player_pokemon = Pokemon(player_pokemon)
        self.enemy_pokemon = self.random_pokemon()

        self.fighting = True
        self.battle()

    # Méthode pour choisir un pokemon adversaire aléatoirement
    def random_pokemon(self):
        with open(pokemon_path, "r") as file:
            pokemons = json.load(file)
            for pokemon in pokemons:
                # Conversion array JSON en tuple Python
                pokemon["types"] = tuple(pokemon["types"])
            enemy_pokemon = choice(pokemons)
        with open(pokedex_path, "r") as file:
            pokedex = json.load(file)
            if not enemy_pokemon in pokedex:
                pokedex.append(enemy_pokemon)
            with open(pokedex_path, "w") as file:
                json.dump(pokedex, file, indent=4)
            enemy_pokemon["level"] = self.player_pokemon.level
        return Pokemon(enemy_pokemon)

    def attack(self, attacker, target):
        multipliers = []
        # Pour obtenir toutes les combinaisons de types
        for attacker_type in attacker.types:
            for target_type in target.types:
                multipliers.append(self.type_chart[attacker_type][target_type])

        # Attaque manqué
        hit_chance = choice(range(0, 4))
        if hit_chance > 0:
            multiplier = max(multipliers)
        else:
            multiplier = 0

        damage = (attacker.attack / target.defense) / 50 + 2 * multiplier
        damage = int(damage)
        target.health -= damage

        attack_message = f"{attacker.name} attacks " f"{target.name}\n"
        messages = {
            2: f"{attack_message}It is very effective!\n{damage} DMG\n",
            1: f"{attack_message}{damage} DMG\n",
            0.5: f"{attack_message}It's not very effective...\n{damage} DMG\n",
            0: f"{attack_message}It missed!\n{damage} DMG\n",
        }
        return (messages[multiplier])

    def capture(self):
        with open(save_path, "r") as file:
            pokemons = json.load(file)
            pokemons.append(self.enemy_pokemon.stat_dict)
            with open(save_path, "w") as file:
                json.dump(pokemons, file, indent=4)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_RETURN:
                self.key_pressed = True

    def turn(self, attacker, defender, fighting=True, message=None):
        if fighting:
            attack_message = self.attack(attacker, defender)
        if message is None:
            message = attack_message
        while True:
            self.handle_input()

            self.screen.blit(self.background, (0, 0))

            player_pokemon_name_surface = self.font.render(
                self.player_pokemon.name,
                True,
                (0, 0 ,0)
            )
            self.screen.blit(player_pokemon_name_surface, (542, 344))
            player_pokemon_health_surface = self.font.render(
                f"{self.player_pokemon.health}/20",
                True,
                (0, 0, 0)
            )
            self.screen.blit(player_pokemon_health_surface, (677, 352))
            player_pokemon_level_surface = self.font.render(
                f"LVL {self.player_pokemon.level}",
                True,
                (0, 0 ,0)
            )
            self.screen.blit(player_pokemon_level_surface, (545, 374))

            enemy_pokemon_name_surface = self.font.render(
                self.enemy_pokemon.name,
                True,
                (0, 0 ,0)
            )
            self.screen.blit(enemy_pokemon_name_surface, (99, 66))
            enemy_pokemon_health_surface = self.font.render(
                f"{self.enemy_pokemon.health}/20",
                True,
                (0, 0, 0)
            )
            self.screen.blit(enemy_pokemon_health_surface, (228, 74))
            enemy_pokemon_level_surface = self.font.render(
                f"LVL {self.enemy_pokemon.level}",
                True,
                (0, 0 ,0)
            )
            self.screen.blit(enemy_pokemon_level_surface, (99, 95))

            for i, line in enumerate(message.split("\n")):
                line_surface = self.font.render(f"{line}", True, (0, 0 ,0))
                self.screen.blit(line_surface, (40, 16*i+486))

            pygame.display.flip()

            if self.key_pressed:
                break
        self.key_pressed = False
             

    def battle(self):
        self.turn(
            self.player_pokemon,
            self.enemy_pokemon,
            False,
            f"A wild {self.enemy_pokemon.name} appears!"
        )
        while self.fighting:
            self.turn(self.player_pokemon, self.enemy_pokemon)
            if self.enemy_pokemon.health <= 0:
                self.fighting = False
                break
            self.turn(self.enemy_pokemon, self.player_pokemon)
            if self.player_pokemon.health <= 0:
                self.fighting = False
                break

        if self.enemy_pokemon.health <= 0:
            self.turn(
                self.player_pokemon,
                self.enemy_pokemon,
                True,
                "The player's Pokemon has won"
            )
            self.player_pokemon.level_up()
            self.turn(
                self.player_pokemon,
                self.enemy_pokemon,
                True,
                f"{self.player_pokemon.name} has leveled up!\n"
                f"It is now level {self.player_pokemon.level}!"
            )
            if self.player_pokemon.check_evolution():
                self.turn(
                    self.player_pokemon,
                    self.enemy_pokemon,
                    True,
                    f"{self.player_pokemon.name} is evolving..."
                )
                self.player_pokemon.evolve()
                self.turn(
                    self.player_pokemon,
                    self.enemy_pokemon,
                    True,
                    f"...into {self.player_pokemon.evolution}!"
                )
            self.capture()
        else:
            self.turn(
                self.player_pokemon,
                self.enemy_pokemon,
                True,
                "The player's Pokemon has lost"
            )