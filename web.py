# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# import time
# from datetime import datetime

# # URL de la page à analyser
# url = "https://www.lefigaro.fr/sports"

# # Définir les headers, y compris le User-Agent
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# # Clé API Pexels
# PEXELS_API_KEY = '1osRTIRyPIiHgClchOtSXAt27oxTSsDOMOLwbGR5w3M9TKU0cjg9vypU'

# # Fichier pour stocker les titres des articles déjà traités
# processed_titles_file = 'articles/processed_titles.txt'

# # Fonction pour reformuler le texte en respectant les règles de SEO
# def reformulate_text(text):
#     return text.replace('contre-la-montre', 'course contre-la-montre').replace('Maillot Jaune', 'le prestigieux Maillot Jaune')

# # Fonction pour récupérer une image depuis Pexels en utilisant le titre de l'article
# def get_image_url_from_pexels(query):
#     api_url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
#     headers = {
#         'Authorization': PEXELS_API_KEY
#     }
#     try:
#         response = requests.get(api_url, headers=headers)
#         print("Code de statut de la réponse Pexels:", response.status_code)
#         if response.status_code == 200:
#             data = response.json()
#             if 'photos' in data and len(data['photos']) > 0:
#                 return data['photos'][0]['src']['original']
#             else:
#                 print("Aucune image trouvée pour la requête:", query)
#         elif response.status_code == 403:
#             print("Limite d'API dépassée. Attente avant la prochaine requête.")
#             time.sleep(60)  # Attendre 60 secondes avant de faire une nouvelle requête
#     except requests.RequestException as e:
#         print(f"Erreur avec l'API Pexels: {e}")
#     return None

# # Fonction pour télécharger une image
# def download_image(image_url, filename):
#     try:
#         image_response = requests.get(image_url, headers=headers)
#         image_response.raise_for_status()
#         with open(filename, 'wb') as img_file:
#             img_file.write(image_response.content)
#         print(f"Image téléchargée et enregistrée sous {filename}")
#     except requests.RequestException as e:
#         print(f"Erreur lors du téléchargement de l'image : {e}")

# # Fonction pour lire les titres déjà traités depuis un fichier
# def load_processed_titles():
#     if os.path.exists(processed_titles_file):
#         with open(processed_titles_file, 'r', encoding='utf-8') as file:
#             return set(line.strip() for line in file)
#     return set()

# # Fonction pour ajouter un titre au fichier des titres traités
# def add_processed_title(title):
#     with open(processed_titles_file, 'a', encoding='utf-8') as file:
#         file.write(title + '\n')

# # Créer un répertoire pour stocker les fichiers
# if not os.path.exists('articles'):
#     os.makedirs('articles')

# # Lire les titres déjà traités
# processed_titles = load_processed_titles()

# # Récupérer le contenu de la page
# try:
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()  # Vérifie les erreurs HTTP
# except requests.RequestException as e:
#     print(f"Erreur lors de la récupération de la page : {e}")
#     exit()

# # Analyser le contenu HTML
# soup = BeautifulSoup(response.text, 'html.parser')

# # Trouver tous les articles
# articles = soup.find_all('article', class_='fig-ranking-profile-container')

# # Parcourir chaque article
# for index, article in enumerate(articles, start=1):
#     # Extraire le titre
#     h2_element = article.find('h2', class_='fig-ranking-profile-headline')
#     h2_text = h2_element.text.strip() if h2_element else "Titre non disponible"
#     h2_text = reformulate_text(h2_text)  # Reformuler le titre

#     # Vérifier si l'article a déjà été traité
#     if h2_text in processed_titles:
#         print(f"Article déjà traité : {h2_text}")
#         continue

#     # Extraire le lien vers l'article complet
#     a_element = article.find('a', class_='fig-ranking-profile-link')
#     if a_element:
#         article_url = urljoin(url, a_element['href'])

#         # Récupérer le contenu de l'article
#         try:
#             article_response = requests.get(article_url, headers=headers)
#             article_response.raise_for_status()
#         except requests.RequestException as e:
#             print(f"Erreur lors de la récupération de l'article : {e}")
#             continue
        
#         # Analyser le contenu de l'article
#         article_soup = BeautifulSoup(article_response.text, 'html.parser')

#         # Extraire le texte de l'article
#         paragraphs = article_soup.find_all('p', class_='fig-paragraph')
#         content_text = "\n".join([reformulate_text(p.get_text(strip=True)) for p in paragraphs]) if paragraphs else "Contenu non disponible"

#         # Obtenir une image correspondante
#         image_url = get_image_url_from_pexels(h2_text)

#         # Nommer les fichiers avec la date et l'heure
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         article_filename = f"articles/article_{timestamp}_{index}.txt"
#         image_filename = f"articles/article_{timestamp}_{index}.png"

#         # Écrire dans le fichier texte avec la distance et l'ordre demandés
#         with open(article_filename, 'w', encoding='utf-8') as file:
#             file.write(f"Titre: {h2_text}\n\n")  # Titre avec espace
#             file.write(f"URL de l'article: {article_url}\n\n")  # URL de l'article avec espace
#             file.write(f"Image URL: {image_url}\n\n" if image_url else "Image non disponible\n\n")  # URL de l'image avec espace
#             file.write(f"Contenu:\n{content_text}\n")  # Contenu

#         # Télécharger et enregistrer l'image
#         if image_url:
#             download_image(image_url, image_filename)

#         # Ajouter le titre au fichier des titres traités
#         add_processed_title(h2_text)

# print("Le contenu de tous les nouveaux articles a été extrait et enregistré dans des fichiers texte et images.")




# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# import time
# from datetime import datetime
# from collections import Counter
# import re
# import random

# # URL de la page à analyser
# url = "https://www.lefigaro.fr/sports"

# # Définir les headers, y compris le User-Agent
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# # Clé API Pexels
# PEXELS_API_KEY = '1osRTIRyPIiHgClchOtSXAt27oxTSsDOMOLwbGR5w3M9TKU0cjg9vypU'

# # Fichier pour stocker les titres des articles déjà traités
# processed_titles_file = 'articles/processed_titles.txt'

# # Fonction pour reformuler le texte en respectant les règles de SEO
# def reformulate_text(text):
#     return text.replace('contre-la-montre', 'course contre-la-montre').replace('Maillot Jaune', 'le prestigieux Maillot Jaune')

# # Fonction pour récupérer une image depuis Pexels en utilisant le titre de l'article
# def get_image_url_from_pexels(query):
#     api_url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
#     headers = {
#         'Authorization': PEXELS_API_KEY
#     }
#     try:
#         response = requests.get(api_url, headers=headers)
#         print("Code de statut de la réponse Pexels:", response.status_code)
#         if response.status_code == 200:
#             data = response.json()
#             if 'photos' in data and len(data['photos']) > 0:
#                 return data['photos'][0]['src']['original']
#             else:
#                 print("Aucune image trouvée pour la requête:", query)
#         elif response.status_code == 403:
#             print("Limite d'API dépassée. Attente avant la prochaine requête.")
#             time.sleep(60)  # Attendre 60 secondes avant de faire une nouvelle requête
#     except requests.RequestException as e:
#         print(f"Erreur avec l'API Pexels: {e}")
#     return None

# # Fonction pour télécharger une image
# def download_image(image_url, filename):
#     try:
#         image_response = requests.get(image_url, headers=headers)
#         image_response.raise_for_status()
#         with open(filename, 'wb') as img_file:
#             img_file.write(image_response.content)
#         print(f"Image téléchargée et enregistrée sous {filename}")
#     except requests.RequestException as e:
#         print(f"Erreur lors du téléchargement de l'image : {e}")

# # Fonction pour lire les titres déjà traités depuis un fichier
# def load_processed_titles():
#     if os.path.exists(processed_titles_file):
#         with open(processed_titles_file, 'r', encoding='utf-8') as file:
#             return set(line.strip() for line in file)
#     return set()

# # Fonction pour ajouter un titre au fichier des titres traités
# def add_processed_title(title):
#     with open(processed_titles_file, 'a', encoding='utf-8') as file:
#         file.write(title + '\n')

# # Fonction pour générer des hashtags à partir du contenu de l'article
# def generate_hashtags(text, min_hashtags=3, max_hashtags=10):
#     words = re.findall(r'\b\w+\b', text.lower())
#     word_freq = Counter(words)
#     common_words = [word for word, _ in word_freq.most_common(max_hashtags)]
#     hashtags = [f"#{word}" for word in common_words if len(word) > 3]  # Exclure les mots trop courts
    
#     # Assurez-vous que le nombre de hashtags à retourner est valide
#     num_hashtags = min(max_hashtags, max(min_hashtags, len(hashtags)))
    
#     # Si le nombre de hashtags demandés est supérieur à ceux disponibles, ajuster
#     if len(hashtags) < num_hashtags:
#         num_hashtags = len(hashtags)
    
#     return random.sample(hashtags, num_hashtags) if hashtags else []

# # Créer un répertoire pour stocker les fichiers
# if not os.path.exists('articles'):
#     os.makedirs('articles')

# # Lire les titres déjà traités
# processed_titles = load_processed_titles()

# # Récupérer le contenu de la page
# try:
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()  # Vérifie les erreurs HTTP
# except requests.RequestException as e:
#     print(f"Erreur lors de la récupération de la page : {e}")
#     exit()

# # Analyser le contenu HTML
# soup = BeautifulSoup(response.text, 'html.parser')

# # Trouver tous les articles
# articles = soup.find_all('article', class_='fig-ranking-profile-container')

# # Parcourir chaque article
# for index, article in enumerate(articles, start=1):
#     # Extraire le titre
#     h2_element = article.find('h2', class_='fig-ranking-profile-headline')
#     h2_text = h2_element.text.strip() if h2_element else "Titre non disponible"
#     h2_text = reformulate_text(h2_text)  # Reformuler le titre

#     # Vérifier si l'article a déjà été traité
#     if h2_text in processed_titles:
#         print(f"Article déjà traité : {h2_text}")
#         continue

#     # Extraire le lien vers l'article complet
#     a_element = article.find('a', class_='fig-ranking-profile-link')
#     if a_element:
#         article_url = urljoin(url, a_element['href'])

#         # Récupérer le contenu de l'article
#         try:
#             article_response = requests.get(article_url, headers=headers)
#             article_response.raise_for_status()
#         except requests.RequestException as e:
#             print(f"Erreur lors de la récupération de l'article : {e}")
#             continue
        
#         # Analyser le contenu de l'article
#         article_soup = BeautifulSoup(article_response.text, 'html.parser')

#         # Extraire le texte de l'article
#         paragraphs = article_soup.find_all('p', class_='fig-paragraph')
#         content_text = "\n".join([reformulate_text(p.get_text(strip=True)) for p in paragraphs]) if paragraphs else "Contenu non disponible"

#         # Obtenir une image correspondante
#         image_url = get_image_url_from_pexels(h2_text)

#         # Générer des hashtags
#         hashtags = generate_hashtags(content_text)
#         hashtags_str = ' '.join(hashtags)

#         # Nommer les fichiers avec la date et l'heure
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         article_filename = f"articles/article_{timestamp}_{index}.txt"
#         image_filename = f"articles/article_{timestamp}_{index}.png"

#         # Écrire dans le fichier texte avec la distance, l'ordre demandés et les hashtags
#         with open(article_filename, 'w', encoding='utf-8') as file:
#             file.write(f"Titre: {h2_text}\n\n")  # Titre avec espace
#             file.write(f"URL de l'article: {article_url}\n\n")  # URL de l'article avec espace
#             file.write(f"Image URL: {image_url}\n\n" if image_url else "Image non disponible\n\n")  # URL de l'image avec espace
#             file.write(f"Contenu:\n{content_text}\n\n")  # Contenu
#             file.write(f"Hashtags: {hashtags_str}\n")  # Hashtags

#         # Télécharger et enregistrer l'image
#         if image_url:
#             download_image(image_url, image_filename)

#         # Ajouter le titre au fichier des titres traités
#         add_processed_title(h2_text)

# print("Le contenu de tous les nouveaux articles a été extrait et enregistré dans des fichiers texte et images.")




import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import time
from datetime import datetime
import spacy
import random

# Charger le modèle spaCy
nlp = spacy.load("en_core_web_sm")

# URL de la page à analyser
url = "https://www.lefigaro.fr/sports"

# Définir les headers, y compris le User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Clé API Pexels
PEXELS_API_KEY = '1osRTIRyPIiHgClchOtSXAt27oxTSsDOMOLwbGR5w3M9TKU0cjg9vypU'

# Fichier pour stocker les titres des articles déjà traités
processed_titles_file = 'articles/processed_titles.txt'

# Fonction pour reformuler le texte en respectant les règles de SEO
def reformulate_text(text):
    return text.replace('contre-la-montre', 'course contre-la-montre').replace('Maillot Jaune', 'le prestigieux Maillot Jaune')

# Fonction pour récupérer une image depuis Pexels en utilisant le titre de l'article
def get_image_url_from_pexels(query):
    api_url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    headers = {
        'Authorization': PEXELS_API_KEY
    }
    try:
        response = requests.get(api_url, headers=headers)
        print("Code de statut de la réponse Pexels:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            if 'photos' in data and len(data['photos']) > 0:
                return data['photos'][0]['src']['original']
            else:
                print("Aucune image trouvée pour la requête:", query)
        elif response.status_code == 403:
            print("Limite d'API dépassée. Attente avant la prochaine requête.")
            time.sleep(60)  # Attendre 60 secondes avant de faire une nouvelle requête
    except requests.RequestException as e:
        print(f"Erreur avec l'API Pexels: {e}")
    return None

# Fonction pour télécharger une image
def download_image(image_url, filename):
    try:
        image_response = requests.get(image_url, headers=headers)
        image_response.raise_for_status()
        with open(filename, 'wb') as img_file:
            img_file.write(image_response.content)
        print(f"Image téléchargée et enregistrée sous {filename}")
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")

# Fonction pour lire les titres déjà traités depuis un fichier
def load_processed_titles():
    if os.path.exists(processed_titles_file):
        with open(processed_titles_file, 'r', encoding='utf-8') as file:
            return set(line.strip() for line in file)
    return set()

# Fonction pour ajouter un titre au fichier des titres traités
def add_processed_title(title):
    with open(processed_titles_file, 'a', encoding='utf-8') as file:
        file.write(title + '\n')

# Fonction pour générer des hashtags à partir du texte de l'article
def generate_hashtags(text, min_hashtags=3, max_hashtags=10):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]  # Extraire les entités nommées
    phrases = [chunk.text for chunk in doc.noun_chunks]  # Extraire les groupes nominaux
    keywords = list(set(entities + phrases))  # Combiner les entités et phrases

    # Filtrer les mots-clés courts
    hashtags = [f"#{word.replace(' ', '_')}" for word in keywords if len(word) > 3]

    # Assurer que le nombre de hashtags à retourner est valide
    num_hashtags = min(max_hashtags, max(min_hashtags, len(hashtags)))

    # Si le nombre de hashtags demandés est supérieur à ceux disponibles, ajuster
    if len(hashtags) < num_hashtags:
        num_hashtags = len(hashtags)

    return random.sample(hashtags, num_hashtags) if hashtags else []

# Créer un répertoire pour stocker les fichiers
if not os.path.exists('articles'):
    os.makedirs('articles')

# Lire les titres déjà traités
processed_titles = load_processed_titles()

# Récupérer le contenu de la page
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Vérifie les erreurs HTTP
except requests.RequestException as e:
    print(f"Erreur lors de la récupération de la page : {e}")
    exit()

# Analyser le contenu HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Trouver tous les articles
articles = soup.find_all('article', class_='fig-ranking-profile-container')

# Parcourir chaque article
for index, article in enumerate(articles, start=1):
    # Extraire le titre
    h2_element = article.find('h2', class_='fig-ranking-profile-headline')
    h2_text = h2_element.text.strip() if h2_element else "Titre non disponible"
    h2_text = reformulate_text(h2_text)  # Reformuler le titre

    # Vérifier si l'article a déjà été traité
    if h2_text in processed_titles:
        print(f"Article déjà traité : {h2_text}")
        continue

    # Extraire le lien vers l'article complet
    a_element = article.find('a', class_='fig-ranking-profile-link')
    if a_element:
        article_url = urljoin(url, a_element['href'])

        # Récupérer le contenu de l'article
        try:
            article_response = requests.get(article_url, headers=headers)
            article_response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération de l'article : {e}")
            continue
        
        # Analyser le contenu de l'article
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        # Extraire le texte de l'article
        paragraphs = article_soup.find_all('p', class_='fig-paragraph')
        content_text = "\n".join([reformulate_text(p.get_text(strip=True)) for p in paragraphs]) if paragraphs else "Contenu non disponible"

        # Obtenir une image correspondante
        image_url = get_image_url_from_pexels(h2_text)

        # Générer des hashtags
        hashtags = generate_hashtags(content_text)
        hashtags_str = ' '.join(hashtags)

        # Nommer les fichiers avec la date et l'heure
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        article_filename = f"articles/article_{timestamp}_{index}.txt"
        image_filename = f"articles/article_{timestamp}_{index}.png"

        # Écrire dans le fichier texte avec la distance, l'ordre demandés et les hashtags
        with open(article_filename, 'w', encoding='utf-8') as file:
            file.write(f"Titre: {h2_text}\n\n")  # Titre avec espace
            file.write(f"URL de l'article: {article_url}\n\n")  # URL de l'article avec espace
            file.write(f"Image URL: {image_url}\n\n" if image_url else "Image non disponible\n\n")  # URL de l'image avec espace
            file.write(f"Contenu:\n{content_text}\n\n")  # Contenu
            file.write(f"Hashtags: {hashtags_str}\n")  # Hashtags

        # Télécharger et enregistrer l'image
        if image_url:
            download_image(image_url, image_filename)

        # Ajouter le titre au fichier des titres traités
        add_processed_title(h2_text)

print("Le contenu de tous les nouveaux articles a été extrait et enregistré dans des fichiers texte et images.")

