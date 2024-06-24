import requests
from PIL import Image
from io import BytesIO
from PIL import Image, ImageDraw,ImageFont
import utils as utils


with open("credentials/the_movie_db_key.txt", 'r',encoding='utf-8') as fichier:
    key = fichier.read()

def save_film_poster(film:str):
    
    film_format = film.replace(' ','%20')
    film_format = film_format.replace('_','%20')
    url = f"https://api.themoviedb.org/3/search/movie?query={film_format}&include_adult=false&language=fr-FR&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {key}"
    }

    response = requests.get(url, headers=headers)
    if response.json()['total_results'] == 0:
        print(f"Error: poster of {film} has not been found")
        # On enregistre une image de base bidon
        width, height = 108, 160
        image = Image.new('RGB', (width, height), (255, 255, 255, 0))
        # Créer un objet de dessin
        draw = ImageDraw.Draw(image)
        draw.rectangle([0, 0, 108, 160], fill=utils.couleur_en_rgb("black"))  # Bleu avec transparence # [x1, y1, x2, y2] [(coin sup gauche, coin sup droit)]
        utils.draw_centered_text(draw, f"Pas d'affiche trouvé pour {film.replace('_',' ')}", [0, 0, 108, 160], ImageFont.truetype("arial.ttf", 15), "white")
        image.save(f"posters\{film}.jpg")
    
    else:
        url_poster  = f'https://image.tmdb.org/t/p/original/{response.json()["results"][0]["poster_path"]}'
        
        reponse = requests.get(url_poster)
            
        # Vérifier si la requête a réussi (code 200)
        if reponse.status_code == 200:
            # Ouvrir l'image à partir du contenu binaire
            image = Image.open(BytesIO(reponse.content))
            # Enregistrer l'image localement
            image.save(f"posters\{film}.jpg")
            print(f"Poster find of {film} has been found")
    
    