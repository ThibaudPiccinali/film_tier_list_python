from PIL import ImageColor

def couleur_en_rgb(nom_couleur):
    nom_couleur = nom_couleur.lower()  # Convertir en minuscules pour la correspondance insensible à la casse
    
    couleurs = {
        'red': ImageColor.getrgb("#FF0000"),
        'orange':ImageColor.getrgb("#FFC000"),
        'yellow': ImageColor.getrgb("#FFFF00"),
        'green': ImageColor.getrgb("#92D050"),
        'dark_green':ImageColor.getrgb("#00B050"),
        'blue': ImageColor.getrgb("#00B0F0"),
        'deep_blue':ImageColor.getrgb("#156082"),
        'purple':ImageColor.getrgb("#7030A0"),
        'grey':ImageColor.getrgb("#AEAEAE"),
        
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        # Ajouter d'autres couleurs selon vos besoins
    }
    
    return couleurs.get(nom_couleur, (0, 0, 0))  # Retourner la valeur RGB correspondante, par défaut (0, 0, 0) si la couleur n'est pas trouvée

# Fonction pour diviser le texte en lignes qui tiennent dans une boîte
def wrap_text(draw,text, box_width, font):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and draw.textlength(line + words[0], font=font) <= box_width:
            line += (words.pop(0) + ' ')
        lines.append(line.strip())
    return lines

# Fonction pour centrer le texte dans un rectangle, avec retour à la ligne si nécessaire
def draw_centered_text(draw, text, box, font, fill):
    lines = wrap_text(draw,text, box[2] - box[0], font)
    total_text_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines)
    
    # Calculer la position y pour centrer le texte
    y = box[1] + (box[3] - box[1] - total_text_height) / 2

    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Calculer la position x pour centrer chaque ligne
        x = box[0] + (box[2] - box[0] - text_width) / 2
        
        draw.text((x, y), line, font=font, fill=fill)
        y += text_height