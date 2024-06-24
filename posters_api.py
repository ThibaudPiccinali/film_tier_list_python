import requests
from PIL import Image
from io import BytesIO

key = "themoviedb_key"

def save_film_poster(film:str):
    
    film_format = film.replace(' ','%20')
    film_format = film_format.replace('_','%20')
    url = f"https://api.themoviedb.org/3/search/movie?query={film_format}&include_adult=false&language=fr-FR&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {key}"
    }

    response = requests.get(url, headers=headers)
    print(response.json())
    url_poster  = f'https://image.tmdb.org/t/p/original/{response.json()["results"][0]["poster_path"]}'
    
    reponse = requests.get(url_poster)
        
    # Vérifier si la requête a réussi (code 200)
    if reponse.status_code == 200:
        # Ouvrir l'image à partir du contenu binaire
        image = Image.open(BytesIO(reponse.content))
        # Enregistrer l'image localement
        image.save(f"posters\{film}.jpg")
        print(f"Poster find of {film} has been found")
    
    