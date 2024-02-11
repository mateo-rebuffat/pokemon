# LIGNE 51 POUR MODIFIER TAILLE FONT
import os
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

        self.pkmnsprites_directory = pkmnsprites_directory  # Nouvelle variable pour stocker le répertoire des sprites
        self.load_sprites()  # Charger les sprites des Pokémon

        # Chargez l'image du sprite de Pokémon du joueur
        self.player_pokemon_sprite = pygame.image.load(
            os.path.join(self.pkmnsprites_directory, f"{player_pokemon['name']}-back.png")
            # 3. Utiliser pkmnsprites_directory
        ).convert_alpha()

        # Redimensionner l'image du sprite du Pokémon du joueur
        scaled_width = 300  # Largeur souhaitée
        scaled_height = 300  # Hauteur souhaitée
        self.player_pokemon_sprite = pygame.transform.scale(self.player_pokemon_sprite, (scaled_width, scaled_height))

        # Afficher l'image redimensionnée du Pokémon du joueur
        self.screen.blit(self.player_pokemon_sprite, (55, 290))

        # Charger le sprite du Pokémon ennemi
        self.enemy_pokemon_sprite = pygame.image.load(
            os.path.join(self.pkmnsprites_directory, f"{self.enemy_pokemon.name}.png")
        ).convert_alpha()

        # Redimensionner l'image du sprite du Pokémon ennemi
        scaled_width_enemy = 150
        scaled_height_enemy = 150
        self.enemy_pokemon_sprite = pygame.transform.scale(self.enemy_pokemon_sprite, (scaled_width, scaled_height))

        # Afficher l'image redimensionnée du Pokémon ennemi
        self.screen.blit(self.enemy_pokemon_sprite, (70, 350))  # Positionnez le sprite ennemi selon vos besoins

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

    def load_sprites(self):
        self.pokemon_sprites = {}
        with open(pokemon_path, "r") as file:
            pokemons = json.load(file)
            for pokemon in pokemons:
                player_sprite_path = os.path.join(self.pkmnsprites_directory, f"{pokemon['name']}-back.png")
                enemy_sprite_path = os.path.join(self.pkmnsprites_directory, f"{pokemon['name']}.png")
                if os.path.exists(player_sprite_path):
                    self.pokemon_sprites[pokemon["name"]] = {
                        "player": pygame.image.load(player_sprite_path),
                        "enemy": pygame.image.load(enemy_sprite_path)
                    }

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

            # Afficher le sprite du Pokémon du joueur
            player_pokemon_sprite = self.pokemon_sprites.get(attacker.name, {}).get("player")
            if player_pokemon_sprite is not None:
                scaled_width_player = 300
                scaled_height_player = 300
                player_pokemon_sprite = pygame.transform.scale(player_pokemon_sprite,
                                                               (scaled_width_player, scaled_height_player))
                self.screen.blit(player_pokemon_sprite, (50, 200))

            player_pokemon_name_surface = self.font.render(
                attacker.name,
                True,
                (0, 0, 0)
            )
            self.screen.blit(player_pokemon_name_surface, (542, 344))
            player_pokemon_health_surface = self.font.render(
                f"{attacker.health}/20",
                True,
                (0, 0, 0)
            )
            self.screen.blit(player_pokemon_health_surface, (677, 352))
            player_pokemon_level_surface = self.font.render(
                f"LVL {attacker.level}",
                True,
                (0, 0, 0)
            )
            self.screen.blit(player_pokemon_level_surface, (545, 374))

            # Afficher le sprite du Pokémon ennemi
            enemy_pokemon_sprite = self.pokemon_sprites.get(defender.name, {}).get("enemy")
            if enemy_pokemon_sprite is not None:
                scaled_width_enemy = 150
                scaled_height_enemy = 150
                enemy_pokemon_sprite = pygame.transform.scale(enemy_pokemon_sprite,
                                                              (scaled_width_enemy, scaled_height_enemy))
                self.screen.blit(enemy_pokemon_sprite, (500, 90))

            enemy_pokemon_name_surface = self.font.render(
                defender.name,
                True,
                (0, 0, 0)
            )
            self.screen.blit(enemy_pokemon_name_surface, (99, 66))
            enemy_pokemon_health_surface = self.font.render(
                f"{defender.health}/20",
                True,
                (0, 0, 0)
            )
            self.screen.blit(enemy_pokemon_health_surface, (228, 74))
            enemy_pokemon_level_surface = self.font.render(
                f"LVL {defender.level}",
                True,
                (0, 0, 0)
            )
            self.screen.blit(enemy_pokemon_level_surface, (99, 95))

            for i, line in enumerate(message.split("\n")):
                line_surface = self.font.render(f"{line}", True, (0, 0, 0))
                self.screen.blit(line_surface, (40, 16 * i + 486))

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