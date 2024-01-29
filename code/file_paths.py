import os


# Répertoire principale
pokemon_directory = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

# Répertoire contenant code
code_directory = os.path.join(pokemon_directory, "code")

# Répertoire contenant données
data_directory = os.path.join(pokemon_directory, "data")
pokemon_path = os.path.join(data_directory, "pokemon.json")
pokedex_path = os.path.join(data_directory, "pokedex.json")
save_path = os.path.join(data_directory, "save.json")

# Répertoire contenant police
font_directory = os.path.join(pokemon_directory, "font")

# Répertoire contenant images
img_directory = os.path.join(pokemon_directory, "img")
backgrounds_directory = os.path.join(img_directory, "backgrounds")
pkmnsprites_directory = os.path.join(img_directory, "pkmnsprites")

# Répertoire contenant musique
music_directory = os.path.join(pokemon_directory, "music")


# Fonction pour obtenir chemin vers image sprite.
def select_sprites(sprite_name):
    if not isinstance(sprite_name, str):
        raise ValueError("Le nom du fichier doit être un string")
    return os.path.join(pkmnsprites_directory, sprite_name)
