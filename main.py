import os

from PIL import Image, ImageDraw,ImageFont
import posters_api as poster
import utils as utils
import agenda as agenda

# Chemin vers votre fichier texte
file_path = 'notes.txt'

# On récupère les films de l'agenda
new_films = agenda.get_films_agenda()

# On s'assure que les films dans cette liste ne sont pas déjà traité

with open(file_path, 'r+',encoding='utf-8') as fichier:
    contenu = fichier.read()
    for new_film in new_films:
        if new_film not in contenu:
            print(f'Add new film to tier list:{new_film}')
            # On le rajoute à la fin (dans la partie "Non noté")
            fichier.write(f'\n{new_film}')
            # S'assurer que le contenu est bien écrit
            fichier.flush()

# tier_list = {
#     "tier_1":tier,
#     "tier_2":tier,
# }

# tier = {
#     "name":name,
#     "color":color,
#     "films":[
#         films1,film2
#     ]
# }

first_time = True

tier_list = {}
index_tier = 1

try:
    # Ouvrir le fichier en mode lecture ('r')
    with open(file_path, 'r',encoding='utf-8') as file:
        # Itérer sur chaque ligne du fichier
        for line in file:
            
            if '#' in line:
                
                if first_time:
                    first_time = False
                else:
                    # On cloture le tier précédant:
                    tier_list[f"tier_{index_tier}"] = tier
                    index_tier +=1
                
                tier = {} # On reset tier
                
                name = line.split('#')[1].split('(')[0].strip()
                color = line.split('(')[1].split(')')[0].strip()
                
                tier = {
                    "name":name,
                    "color":color,
                    "films":[]
                    }
            else:
                # On rajoute le film dans le tier
                tier["films"].append(line.replace('\n',''))    
        
        # On cloture le dernier tier
        tier_list[f"tier_{index_tier}"] = tier
        
except IOError:
    print(f"Impossible d'ouvrir le fichier : {file_path}")

# Trouve le tier avec le plus de film (utile pour la taille de l'image)
max = 0
for tier in tier_list: 
    if len(tier_list[tier]["films"])>max:
        max = len(tier_list[tier]["films"])

# Définir la taille de l'image
width, height = 160+108*max, len(tier_list)*160
image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
# Créer un objet de dessin
draw = ImageDraw.Draw(image)

y_axis_previous_tier = 0

for tier in tier_list:                             
    # Dessiner des blocs de couleurs avec des positions différentes
    draw.rectangle([0, y_axis_previous_tier, 160, y_axis_previous_tier+160], fill=utils.couleur_en_rgb(tier_list[tier]["color"]))  # Bleu avec transparence # [x1, y1, x2, y2] [(coin sup gauche, coin sup droit)]
    utils.draw_centered_text(draw, tier_list[tier]["name"], [0, y_axis_previous_tier, 160, y_axis_previous_tier+160], ImageFont.truetype("arial.ttf", 30), "black")

    for i in range(len(tier_list[tier]["films"])):
        # On cherche l'affiche dans une bdd si on ne l'as pas déjà 
        if not os.path.exists(f'posters/{tier_list[tier]["films"][i]}.jpg'):
            poster.save_film_poster(tier_list[tier]["films"][i])

        img_to_add = Image.open(f'posters/{tier_list[tier]["films"][i]}.jpg')  # Remplacez par le chemin de votre image 
        img_to_add = img_to_add.resize((108,160))
        image.paste(img_to_add, (i*108+160, y_axis_previous_tier, 160+(i+1)*108, y_axis_previous_tier + 160))  # Coordonnées du coin supérieur gauche et coin inférieur droit
        
    y_axis_previous_tier +=160









# Sauvegarder l'image
image.save('tier_list.png')

