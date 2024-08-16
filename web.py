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




# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# import time
# from datetime import datetime
# import spacy
# import random

# # Charger le modèle spaCy
# nlp = spacy.load("en_core_web_sm")

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

# # Fonction pour générer des hashtags à partir du texte de l'article
# def generate_hashtags(text, min_hashtags=3, max_hashtags=10):
#     doc = nlp(text)
#     entities = [ent.text for ent in doc.ents]  # Extraire les entités nommées
#     phrases = [chunk.text for chunk in doc.noun_chunks]  # Extraire les groupes nominaux
#     keywords = list(set(entities + phrases))  # Combiner les entités et phrases

#     # Filtrer les mots-clés courts
#     hashtags = [f"#{word.replace(' ', '_')}" for word in keywords if len(word) > 3]

#     # Assurer que le nombre de hashtags à retourner est valide
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




# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# import time
# from datetime import datetime
# import spacy
# import random

# # Charger le modèle spaCy
# nlp = spacy.load("en_core_web_sm")

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

# # Fonction pour générer des hashtags à partir du texte de l'article
# def generate_hashtags(text, min_hashtags=3, max_hashtags=10):
#     doc = nlp(text)
#     entities = [ent.text for ent in doc.ents]  # Extraire les entités nommées
#     phrases = [chunk.text for chunk in doc.noun_chunks]  # Extraire les groupes nominaux
#     keywords = list(set(entities + phrases))  # Combiner les entités et phrases

#     # Filtrer les mots-clés courts
#     hashtags = [f"#{word.replace(' ', '_')}" for word in keywords if len(word) > 3]

#     # Assurer que le nombre de hashtags à retourner est valide
#     num_hashtags = min(max_hashtags, max(min_hashtags, len(hashtags)))

#     # Si le nombre de hashtags demandés est supérieur à ceux disponibles, ajuster
#     if len(hashtags) < num_hashtags:
#         num_hashtags = len(hashtags)

#     return random.sample(hashtags, num_hashtags) if hashtags else []

# # Créer un répertoire principal pour stocker les fichiers
# base_dir = 'articles'
# if not os.path.exists(base_dir):
#     os.makedirs(base_dir)

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

#         # Créer un dossier avec la date du jour
#         date_today = datetime.now().strftime('%Y-%m-%d')
#         date_dir = os.path.join(base_dir, date_today)
#         if not os.path.exists(date_dir):
#             os.makedirs(date_dir)

#         # Nommer les fichiers avec la date et l'heure
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         article_filename = os.path.join(date_dir, f"article_{timestamp}_{index}.txt")
#         image_filename = os.path.join(date_dir, f"article_{timestamp}_{index}.png")

#         # Écrire dans le fichier texte avec la distance, l'ordre demandés et les hashtags
#         with open(article_filename, 'w', encoding='utf-8') as file:
#             file.write(f"{h2_text}\n")  # Titre avec espace
#             file.write(f"------------------------------------------------------\n\n")  # Titre avec espace
#             file.write(f"{content_text}\n")  # Contenu
#             file.write(f"------------------------------------------------------\n\n")  # Titre avec espace
#             file.write(f"{hashtags_str}\n")  # Hashtags
#             file.write(f"------------------------------------------------------\n\n")  # Titre avec espace
#             file.write(f"URL de l'article: {article_url}\n\n")  # URL de l'article avec espace
#             file.write(f"------------------------------------------------------\n\n")  # Titre avec espace
#             file.write(f"Image URL: {image_url}\n\n" if image_url else "Image non disponible\n\n")  # URL de l'image avec espace
#             file.write(f"------------------------------------------------------\n\n")  # Titre avec espace
#             # file.write(f"Titre: {h2_text}\n\n")  # Titre avec espace
#             # file.write(f"URL de l'article: {article_url}\n\n")  # URL de l'article avec espace
#             # file.write(f"Image URL: {image_url}\n\n" if image_url else "Image non disponible\n\n")  # URL de l'image avec espace
#             # file.write(f"Contenu:\n{content_text}\n\n")  # Contenu
#             # file.write(f"Hashtags: {hashtags_str}\n")  # Hashtags
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
# import spacy
# import random
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# # Charger le modèle spaCy
# nlp = spacy.load("en_core_web_sm")

# # URL de la page à analyser
# url = "https://www.lefigaro.fr/sports"

# # Définir les headers, y compris le User-Agent
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# # Clé API Pexels
# PEXELS_API_KEY = '1osRTIRyPIiHgClchOtSXAt27oxTSsDOMOLwbGR5w3M9TKU0cjg9vypU'

# # Informations de l'email
# SENDER_EMAIL = "badour.info@gmail.com"
# SENDER_PASSWORD = "hqzu fcyx yilp cffm"
# RECIPIENT_EMAIL = "mohsinbadour2000@gmail.com"

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

# # Fonction pour générer des hashtags à partir du texte de l'article
# def generate_hashtags(text, min_hashtags=3, max_hashtags=10):
#     doc = nlp(text)
#     entities = [ent.text for ent in doc.ents]  # Extraire les entités nommées
#     phrases = [chunk.text for chunk in doc.noun_chunks]  # Extraire les groupes nominaux
#     keywords = list(set(entities + phrases))  # Combiner les entités et phrases

#     # Filtrer les mots-clés courts
#     hashtags = [f"#{word.replace(' ', '_')}" for word in keywords if len(word) > 3]

#     # Assurer que le nombre de hashtags à retourner est valide
#     num_hashtags = min(max_hashtags, max(min_hashtags, len(hashtags)))

#     # Si le nombre de hashtags demandés est supérieur à ceux disponibles, ajuster
#     if len(hashtags) < num_hashtags:
#         num_hashtags = len(hashtags)

#     return random.sample(hashtags, num_hashtags) if hashtags else []

# # Fonction pour envoyer un email de notification
# def send_email_notification(title, content, hashtags, image_path):
#     # Créer l'objet MIMEMultipart
#     msg = MIMEMultipart()
#     msg['From'] = SENDER_EMAIL
#     msg['To'] = RECIPIENT_EMAIL
#     msg['Subject'] = f"Nouvel article traité : {title}"

#     # Attacher le corps de l'email
#     body = f"Titre: {title}\n\nContenu:\n{content}\n\nHashtags: {hashtags}\n"
#     msg.attach(MIMEText(body, 'plain'))

#     # Attacher l'image si elle existe
#     if image_path:
#         with open(image_path, "rb") as attachment:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(attachment.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(image_path)}")
#             msg.attach(part)

#     # Envoyer l'email via le serveur SMTP
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         text = msg.as_string()
#         server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
#         server.quit()
#         print(f"Email envoyé à {RECIPIENT_EMAIL}")
#     except Exception as e:
#         print(f"Erreur lors de l'envoi de l'email : {e}")

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
#             file.write(f"URL: {article_url}\n\n")  # URL
#             file.write(f"Contenu:\n{content_text}\n\n")  # Contenu de l'article avec espace
#             file.write(f"Hashtags: {hashtags_str}\n")  # Hashtags

#         # Télécharger et enregistrer l'image
#         if image_url:
#             download_image(image_url, image_filename)

#         # Ajouter le titre au fichier des titres traités
#         add_processed_title(h2_text)

#         # Envoyer la notification par email
#         send_email_notification(h2_text, content_text, hashtags_str, image_filename if image_url else None)

#         print(f"Article '{h2_text}' traité et enregistré sous '{article_filename}'.")

#     else:
#         print(f"Erreur : Pas de lien trouvé pour l'article '{h2_text}'.")

#     # Pause de 5 secondes pour éviter une surcharge du serveur
#     time.sleep(5)

# print("Traitement terminé.")







# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# import time
# from datetime import datetime
# import spacy
# import random
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# # Charger le modèle spaCy
# nlp = spacy.load("en_core_web_sm")

# # URL de la page à analyser
# url = "https://www.lefigaro.fr/sports"

# # Définir les headers, y compris le User-Agent
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# # Clé API Pexels
# PEXELS_API_KEY = '1osRTIRyPIiHgClchOtSXAt27oxTSsDOMOLwbGR5w3M9TKU0cjg9vypU'

# # Informations de l'email
# SENDER_EMAIL = "badour.info@gmail.com"
# SENDER_PASSWORD = "hqzu fcyx yilp cffm"
# RECIPIENT_EMAIL = "mohsinbadour2000@gmail.com"

# # Fichier pour stocker les titres des articles déjà traités
# processed_titles_file = 'processed_titles.txt'

# # Créer un dossier pour les fichiers générés le même jour
# today_date = datetime.now().strftime('%Y-%m-%d')
# daily_folder = f"articles/{today_date}"

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

# # Fonction pour générer des hashtags à partir du texte de l'article
# def generate_hashtags(text, min_hashtags=3, max_hashtags=10):
#     doc = nlp(text)
#     entities = [ent.text for ent in doc.ents]  # Extraire les entités nommées
#     phrases = [chunk.text for chunk in doc.noun_chunks]  # Extraire les groupes nominaux
#     keywords = list(set(entities + phrases))  # Combiner les entités et phrases

#     # Filtrer les mots-clés courts
#     hashtags = [f"#{word.replace(' ', '_')}" for word in keywords if len(word) > 3]

#     # Assurer que le nombre de hashtags à retourner est valide
#     num_hashtags = min(max_hashtags, max(min_hashtags, len(hashtags)))

#     # Si le nombre de hashtags demandés est supérieur à ceux disponibles, ajuster
#     if len(hashtags) < num_hashtags:
#         num_hashtags = len(hashtags)

#     return random.sample(hashtags, num_hashtags) if hashtags else []

# # Fonction pour envoyer un email de notification
# def send_email_notification(title, content, hashtags, image_path):
#     # Créer l'objet MIMEMultipart
#     msg = MIMEMultipart()
#     msg['From'] = SENDER_EMAIL
#     msg['To'] = RECIPIENT_EMAIL
#     msg['Subject'] = f"Nouvel article traité : {title}"

#     # Attacher le corps de l'email
#     body = f"Titre: {title}\n\nContenu:\n{content}\n\nHashtags: {hashtags}\n"
#     msg.attach(MIMEText(body, 'plain'))

#     # Attacher l'image si elle existe
#     if image_path:
#         with open(image_path, "rb") as attachment:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(attachment.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(image_path)}")
#             msg.attach(part)

#     # Envoyer l'email via le serveur SMTP
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         text = msg.as_string()
#         server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
#         server.quit()
#         print(f"Email envoyé à {RECIPIENT_EMAIL}")
#     except Exception as e:
#         print(f"Erreur lors de l'envoi de l'email : {e}")

# # Créer un répertoire pour stocker les fichiers
# if not os.path.exists(daily_folder):
#     os.makedirs(daily_folder)

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
#         article_filename = f"{daily_folder}/article_{timestamp}_{index}.txt"
#         image_filename = f"{daily_folder}/image_{timestamp}_{index}.jpg" if image_url else None

#         # Sauvegarder l'article
#         with open(article_filename, 'w', encoding='utf-8') as file:
#             file.write(f"Titre: {h2_text}\n\nContenu:\n{content_text}\n\nHashtags:\n{hashtags_str}\n")

#         # Télécharger l'image si elle existe
#         if image_url:
#             download_image(image_url, image_filename)

#         # Ajouter le titre à la liste des titres traités
#         add_processed_title(h2_text)

#         # Envoyer un email de notification
#         send_email_notification(h2_text, content_text, hashtags_str, image_filename)


##### MON CODE AU DESSUS


# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# import time
# from datetime import datetime
# import spacy
# import random
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# # Charger le modèle spaCy
# nlp = spacy.load("en_core_web_sm")

# # URL de la page à analyser
# url = "https://www.lefigaro.fr/sports"

# # Définir les headers, y compris le User-Agent
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# # Clé API Pexels
# PEXELS_API_KEY = '1osRTIRyPIiHgClchOtSXAt27oxTSsDOMOLwbGR5w3M9TKU0cjg9vypU'

# # Informations de l'email
# SENDER_EMAIL = "badour.info@gmail.com"
# SENDER_PASSWORD = "hqzu fcyx yilp cffm"
# RECIPIENT_EMAIL = "mohsinbadour2000@gmail.com"

# # ID de la Page Facebook et Access Token
# PAGE_ID = '385436124655444'
# ACCESS_TOKEN = 'EAARrq1nLhkgBOxJ1cVzO2Ki4ieGiH10gY8w2S5uWKWqf6fqiZAFt2NFzZBMXxaUMjHZChS2V1r1OvQ4CgyNZAYRNDZAfrZAldDtEuLvkZBTAdMSSIMGFWR6UnbWhnrLpnuiNObEgbgttPhjLPH11WuZAXZAAuq1V30MMichtGH86cRJ0Td782Uqv0uT3DrMN7oaZB2DKFetgpV5QdQ8Sfr3QZDZD'

# # Fichier pour stocker les titres des articles déjà traités
# processed_titles_file = 'processed_titles.txt'

# # Créer un dossier pour les fichiers générés le même jour
# today_date = datetime.now().strftime('%Y-%m-%d')
# daily_folder = f"articles/{today_date}"

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

# # Fonction pour générer des hashtags à partir du texte de l'article
# def generate_hashtags(text, min_hashtags=3, max_hashtags=10):
#     doc = nlp(text)
#     entities = [ent.text for ent in doc.ents]  # Extraire les entités nommées
#     phrases = [chunk.text for chunk in doc.noun_chunks]  # Extraire les groupes nominaux
#     keywords = list(set(entities + phrases))  # Combiner les entités et phrases

#     # Filtrer les mots-clés courts
#     hashtags = [f"#{word.replace(' ', '_')}" for word in keywords if len(word) > 3]

#     # Assurer que le nombre de hashtags à retourner est valide
#     num_hashtags = min(max_hashtags, max(min_hashtags, len(hashtags)))

#     # Si le nombre de hashtags demandés est supérieur à ceux disponibles, ajuster
#     if len(hashtags) < num_hashtags:
#         num_hashtags = len(hashtags)

#     return random.sample(hashtags, num_hashtags) if hashtags else []

# # Fonction pour envoyer un email de notification
# def send_email_notification(title, content, hashtags, image_path):
#     # Créer l'objet MIMEMultipart
#     msg = MIMEMultipart()
#     msg['From'] = SENDER_EMAIL
#     msg['To'] = RECIPIENT_EMAIL
#     msg['Subject'] = f"Nouvel article traité : {title}"

#     # Attacher le corps de l'email
#     body = f"Titre: {title}\n\nContenu:\n{content}\n\nHashtags: {hashtags}\n"
#     msg.attach(MIMEText(body, 'plain'))

#     # Attacher l'image si elle existe
#     if image_path:
#         with open(image_path, "rb") as attachment:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(attachment.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(image_path)}")
#             msg.attach(part)

#     # Envoyer l'email via le serveur SMTP
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         text = msg.as_string()
#         server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
#         server.quit()
#         print(f"Email envoyé à {RECIPIENT_EMAIL}")
#     except Exception as e:
#         print(f"Erreur lors de l'envoi de l'email : {e}")

# # Fonction pour publier sur Facebook
# def publish_on_facebook(message, image_url=None):
#     if image_url:
#         # Télécharger l'image pour obtenir un ID
#         image_filename = "temp_image.jpg"
#         try:
#             download_image(image_url, image_filename)

#             # Charger l'image sur Facebook
#             upload_url = f"https://graph.facebook.com/{PAGE_ID}/photos"
#             with open(image_filename, 'rb') as img_file:
#                 files = {'file': img_file}
#                 data = {
#                     'caption': message,
#                     'access_token': ACCESS_TOKEN
#                 }
#                 response = requests.post(upload_url, data=data, files=files)
#                 print("Code de statut de la réponse Facebook (image upload):", response.status_code)
#                 if response.status_code == 200:
#                     image_id = response.json().get('id')
#                     if image_id:
#                         data = {
#                             'message': message,
#                             'object_attachment': image_id,
#                             'access_token': ACCESS_TOKEN
#                         }
#                         response = requests.post(f"https://graph.facebook.com/{PAGE_ID}/feed", data=data)
#                         print("Code de statut de la réponse Facebook (post):", response.status_code)
#                 else:
#                     print(f"Erreur lors du téléchargement de l'image sur Facebook: {response.text}")
#         finally:
#             # Toujours essayer de supprimer le fichier, même en cas d'erreur
#             if os.path.exists(image_filename):
#                 os.remove(image_filename)
#     else:
#         # Publier un message sans image
#         data = {
#             'message': message,
#             'access_token': ACCESS_TOKEN
#         }
#         response = requests.post(f"https://graph.facebook.com/{PAGE_ID}/feed", data=data)
#         print("Code de statut de la réponse Facebook (post):", response.status_code)

# # Scraper les articles et traiter les nouveaux articles
# def scrape_and_process_articles():
#     response = requests.get(url, headers=headers)
#     print("Code de statut de la réponse:", response.status_code)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         articles = soup.find_all('article')

#         # Lire les titres déjà traités
#         processed_titles = load_processed_titles()

#         for article in articles:
#             title_tag = article.find('h2')
#             if title_tag:
#                 title = title_tag.get_text(strip=True)
#                 if title not in processed_titles:
#                     link = article.find('a')['href']
#                     full_url = urljoin(url, link)
#                     article_response = requests.get(full_url, headers=headers)
#                     if article_response.status_code == 200:
#                         article_soup = BeautifulSoup(article_response.content, 'html.parser')
#                         content = article_soup.get_text(strip=True)
#                         content = reformulate_text(content)
#                         hashtags = generate_hashtags(content)

#                         # Télécharger une image
#                         image_url = get_image_url_from_pexels(title)
#                         image_filename = None
#                         if image_url:
#                             image_filename = "image.jpg"
#                             download_image(image_url, image_filename)

#                         # Publier sur Facebook
#                         message = f"{title}\n\n{content}\n\n{' '.join(hashtags)}"
#                         publish_on_facebook(message, image_url=image_url)

#                         # Envoyer un email de notification
#                         send_email_notification(title, content, hashtags, image_filename)

#                         # Ajouter le titre au fichier des titres traités
#                         add_processed_title(title)
#                         print(f"Article traité: {title}")

#                         # Supprimer le fichier image après utilisation
#                         if image_filename and os.path.exists(image_filename):
#                             os.remove(image_filename)
#     else:
#         print(f"Erreur lors de la récupération de la page: {response.status_code}")

# # Créer le dossier pour les fichiers générés le même jour
# os.makedirs(daily_folder, exist_ok=True)

# # Lancer le processus de scraping et de traitement des articles
# scrape_and_process_articles()




# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# import time
# from datetime import datetime
# import spacy
# import random
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# # Charger le modèle spaCy
# nlp = spacy.load("en_core_web_sm")

# # URL de la page à analyser
# url = "https://www.lefigaro.fr/sports"

# # Définir les headers, y compris le User-Agent
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# # Clé API Pexels
# PEXELS_API_KEY = '1osRTIRyPIiHgClchOtSXAt27oxTSsDOMOLwbGR5w3M9TKU0cjg9vypU'

# # Informations de l'email
# SENDER_EMAIL = "badour.info@gmail.com"
# SENDER_PASSWORD = "hqzu fcyx yilp cffm"
# RECIPIENT_EMAIL = "mohsinbadour2000@gmail.com"

# # ID de la Page Facebook et Access Token
# YOUR_APP_ID = '1244283596932680'
# YOUR_REDIRECT_URI = 'https://www.facebook.com/profile.php?id=61564524590305'  # Remplacez par votre URL de redirection

# # Fichier pour stocker les titres des articles déjà traités
# processed_titles_file = 'processed_titles.txt'

# # Créer un dossier pour les fichiers générés le même jour
# today_date = datetime.now().strftime('%Y-%m-%d')
# daily_folder = f"articles/{today_date}"

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

# # Fonction pour générer des hashtags à partir du texte de l'article
# def generate_hashtags(text, min_hashtags=3, max_hashtags=10):
#     doc = nlp(text)
#     entities = [ent.text for ent in doc.ents]  # Extraire les entités nommées
#     phrases = [chunk.text for chunk in doc.noun_chunks]  # Extraire les groupes nominaux
#     keywords = list(set(entities + phrases))  # Combiner les entités et phrases

#     # Filtrer les mots-clés courts
#     hashtags = [f"#{word.replace(' ', '_')}" for word in keywords if len(word) > 3]

#     # Assurer que le nombre de hashtags à retourner est valide
#     num_hashtags = min(max_hashtags, max(min_hashtags, len(hashtags)))

#     # Si le nombre de hashtags demandés est supérieur à ceux disponibles, ajuster
#     if len(hashtags) < num_hashtags:
#         num_hashtags = len(hashtags)

#     return random.sample(hashtags, num_hashtags) if hashtags else []

# # Fonction pour envoyer un email de notification
# def send_email_notification(title, content, hashtags, image_path):
#     # Créer l'objet MIMEMultipart
#     msg = MIMEMultipart()
#     msg['From'] = SENDER_EMAIL
#     msg['To'] = RECIPIENT_EMAIL
#     msg['Subject'] = f"Nouvel article traité : {title}"

#     # Attacher le corps de l'email
#     body = f"Titre: {title}\n\nContenu:\n{content}\n\nHashtags: {hashtags}\n"
#     msg.attach(MIMEText(body, 'plain'))

#     # Attacher l'image si elle existe
#     if image_path:
#         with open(image_path, "rb") as attachment:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(attachment.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(image_path)}")
#             msg.attach(part)

#     # Envoyer l'email via le serveur SMTP
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         text = msg.as_string()
#         server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
#         server.quit()
#         print(f"Email envoyé à {RECIPIENT_EMAIL}")
#     except Exception as e:
#         print(f"Erreur lors de l'envoi de l'email : {e}")

# # Fonction pour générer un lien de partage Facebook
# def generate_facebook_share_link(message, image_url=None):
#     # Encoder le message pour l'URL
#     encoded_message = requests.utils.quote(message)
#     if image_url:
#         # Encoder l'URL de l'image pour l'URL
#         encoded_image_url = requests.utils.quote(image_url)
#         return f"https://www.facebook.com/dialog/share?app_id={YOUR_APP_ID}&display=popup&href={encoded_image_url}&quote={encoded_message}&redirect_uri={YOUR_REDIRECT_URI}"
#     else:
#         return f"https://www.facebook.com/dialog/share?app_id={YOUR_APP_ID}&display=popup&quote={encoded_message}&redirect_uri={YOUR_REDIRECT_URI}"

# # Créer un répertoire pour stocker les fichiers
# if not os.path.exists(daily_folder):
#     os.makedirs(daily_folder)

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
#         article_filename = f"{daily_folder}/article_{timestamp}_{index}.txt"
#         image_filename = f"{daily_folder}/image_{timestamp}_{index}.jpg" if image_url else None

#         # Sauvegarder l'article
#         with open(article_filename, 'w', encoding='utf-8') as file:
#             file.write(f"Titre: {h2_text}\n\nContenu:\n{content_text}\n\nHashtags:\n{hashtags_str}\n")

#         # Télécharger l'image si elle existe
#         if image_url:
#             download_image(image_url, image_filename)

#         # Ajouter le titre à la liste des titres traités
#         add_processed_title(h2_text)

#         # Envoyer un email de notification
#         send_email_notification(h2_text, content_text, hashtags_str, image_filename)

#         # Publier sur Facebook
#         share_link = generate_facebook_share_link(f"{h2_text}\n\n{content_text}\n\n{hashtags_str}", image_url)
#         print("Lien de partage Facebook : ", share_link)






# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# import time
# from datetime import datetime
# import spacy
# import random
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# # Charger le modèle spaCy
# nlp = spacy.load("en_core_web_sm")

# # URL de la page à analyser
# url = "https://www.lefigaro.fr/sports"

# # Définir les headers, y compris le User-Agent
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# # Clé API Pexels
# PEXELS_API_KEY = '1osRTIRyPIiHgClchOtSXAt27oxTSsDOMOLwbGR5w3M9TKU0cjg9vypU'

# # Informations de l'email
# SENDER_EMAIL = "badour.info@gmail.com"
# SENDER_PASSWORD = "hqzu fcyx yilp cffm"
# RECIPIENT_EMAIL = "mohsinbadour2000@gmail.com"

# # ID de la Page Facebook et Access Token
# PAGE_ACCESS_TOKEN = 'EAARrq1nLhkgBOZCgH3GGZBy9808WI091fmtmQWd03gdjVuKIrYhepcud1jl7dU9RzQktOfBTngfimX9CqF95tkJcM2vrdGiiGTYUdbW0D2OIVuui4PzABNyWga2oIhINpZBAApPkcDTxmuMoH0shkFi3mDa9KDMkqsyyNZAJwS3Vvb7PVlhlZCuTDZCQY1A7nN69hqBoXHSu7jMQb5gZBPyuexq'  # Remplacez par votre access token

# # Fichier pour stocker les titres des articles déjà traités
# processed_titles_file = 'processed_titles.txt'

# # Créer un dossier pour les fichiers générés le même jour
# today_date = datetime.now().strftime('%Y-%m-%d')
# daily_folder = f"articles/{today_date}"

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

# # Fonction pour générer des hashtags à partir du texte de l'article
# def generate_hashtags(text, min_hashtags=3, max_hashtags=10):
#     doc = nlp(text)
#     entities = [ent.text for ent in doc.ents]  # Extraire les entités nommées
#     phrases = [chunk.text for chunk in doc.noun_chunks]  # Extraire les groupes nominaux
#     keywords = list(set(entities + phrases))  # Combiner les entités et phrases

#     # Filtrer les mots-clés courts
#     hashtags = [f"#{word.replace(' ', '_')}" for word in keywords if len(word) > 3]

#     # Assurer que le nombre de hashtags à retourner est valide
#     num_hashtags = min(max_hashtags, max(min_hashtags, len(hashtags)))

#     # Si le nombre de hashtags demandés est supérieur à ceux disponibles, ajuster
#     if len(hashtags) < num_hashtags:
#         num_hashtags = len(hashtags)

#     return random.sample(hashtags, num_hashtags) if hashtags else []

# # Fonction pour publier sur Facebook avec texte et image
# def post_to_facebook(message, image_path=None):
#     url = f"https://graph.facebook.com/v16.0/me/feed"
#     payload = {
#         'message': message,
#         'access_token': PAGE_ACCESS_TOKEN
#     }

#     # Ajouter l'image si elle existe
#     if image_path:
#         # Télécharger l'image sur Facebook
#         image_url = upload_image_to_facebook(image_path)
#         payload['link'] = image_url

#     try:
#         response = requests.post(url, data=payload)
#         response.raise_for_status()
#         print(f"Publication réussie sur Facebook : {response.json()}")
#     except requests.RequestException as e:
#         print(f"Erreur lors de la publication sur Facebook : {e}")

# # Fonction pour télécharger une image sur Facebook et obtenir l'URL
# def upload_image_to_facebook(image_path):
#     url = f"https://graph.facebook.com/v16.0/me/photos"
#     payload = {
#         'access_token': PAGE_ACCESS_TOKEN
#     }
#     files = {
#         'source': open(image_path, 'rb')
#     }
#     try:
#         response = requests.post(url, data=payload, files=files)
#         response.raise_for_status()
#         image_id = response.json()['id']
#         image_url = f"https://www.facebook.com/photo.php?fbid={image_id}"
#         return image_url
#     except requests.RequestException as e:
#         print(f"Erreur lors du téléchargement de l'image sur Facebook : {e}")
#         return None

# # Créer un répertoire pour stocker les fichiers
# if not os.path.exists(daily_folder):
#     os.makedirs(daily_folder)

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
#         article_filename = f"{daily_folder}/article_{timestamp}_{index}.txt"
#         image_filename = f"{daily_folder}/image_{timestamp}_{index}.jpg" if image_url else None

#         # Sauvegarder l'article
#         with open(article_filename, 'w', encoding='utf-8') as file:
#             file.write(f"Titre: {h2_text}\n\nContenu:\n{content_text}\n\nHashtags:\n{hashtags_str}\n")

#         # Télécharger l'image si elle existe
#         if image_url:
#             download_image(image_url, image_filename)

#         # Ajouter le titre à la liste des titres traités
#         add_processed_title(h2_text)

#         # Envoyer un email de notification
#         send_email_notification(h2_text, content_text, hashtags_str, image_filename)

#         # Publier sur Facebook
#         if image_filename:
#             post_to_facebook(f"{h2_text}\n\n{content_text}\n\n{hashtags_str}", image_filename)
#         else:
#             post_to_facebook(f"{h2_text}\n\n{content_text}\n\n{hashtags_str}")



# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# import time
# from datetime import datetime
# import spacy
# import random
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# # Charger le modèle spaCy
# nlp = spacy.load("en_core_web_sm")

# # URL de la page à analyser
# url = "https://www.lefigaro.fr/sports"

# # Définir les headers, y compris le User-Agent
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# # Clé API Pexels
# PEXELS_API_KEY = '1osRTIRyPIiHgClchOtSXAt27oxTSsDOMOLwbGR5w3M9TKU0cjg9vypU'

# # Informations de l'email
# SENDER_EMAIL = "badour.info@gmail.com"
# SENDER_PASSWORD = "hqzu fcyx yilp cffm"
# RECIPIENT_EMAIL = "mohsinbadour2000@gmail.com"

# # ID de la Page Facebook et Access Token
# PAGE_ACCESS_TOKEN = 'EAARrq1nLhkgBOZCgH3GGZBy9808WI091fmtmQWd03gdjVuKIrYhepcud1jl7dU9RzQktOfBTngfimX9CqF95tkJcM2vrdGiiGTYUdbW0D2OIVuui4PzABNyWga2oIhINpZBAApPkcDTxmuMoH0shkFi3mDa9KDMkqsyyNZAJwS3Vvb7PVlhlZCuTDZCQY1A7nN69hqBoXHSu7jMQb5gZBPyuexq'  # Remplacez par votre access token

# # Fichier pour stocker les titres des articles déjà traités
# processed_titles_file = 'processed_titles.txt'

# # Créer un dossier pour les fichiers générés le même jour
# today_date = datetime.now().strftime('%Y-%m-%d')
# daily_folder = f"articles/{today_date}"

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

# # Fonction pour générer des hashtags à partir du texte de l'article
# def generate_hashtags(text, min_hashtags=3, max_hashtags=10):
#     doc = nlp(text)
#     entities = [ent.text for ent in doc.ents]  # Extraire les entités nommées
#     phrases = [chunk.text for chunk in doc.noun_chunks]  # Extraire les groupes nominaux
#     keywords = list(set(entities + phrases))  # Combiner les entités et phrases

#     # Filtrer les mots-clés courts
#     hashtags = [f"#{word.replace(' ', '_')}" for word in keywords if len(word) > 3]

#     # Assurer que le nombre de hashtags à retourner est valide
#     num_hashtags = min(max_hashtags, max(min_hashtags, len(hashtags)))

#     # Si le nombre de hashtags demandés est supérieur à ceux disponibles, ajuster
#     if len(hashtags) < num_hashtags:
#         num_hashtags = len(hashtags)

#     return random.sample(hashtags, num_hashtags) if hashtags else []

# # Fonction pour publier sur Facebook avec texte et image
# def post_to_facebook(message, image_path=None):
#     url = f"https://graph.facebook.com/v16.0/me/feed"
#     payload = {
#         'message': message,
#         'access_token': PAGE_ACCESS_TOKEN
#     }

#     # Ajouter l'image si elle existe
#     if image_path:
#         # Télécharger l'image sur Facebook
#         image_url = upload_image_to_facebook(image_path)
#         payload['link'] = image_url

#     try:
#         response = requests.post(url, data=payload)
#         response.raise_for_status()
#         print(f"Publication réussie sur Facebook : {response.json()}")
#     except requests.RequestException as e:
#         print(f"Erreur lors de la publication sur Facebook : {e}")

# # Fonction pour télécharger une image sur Facebook et obtenir l'URL
# def upload_image_to_facebook(image_path):
#     url = f"https://graph.facebook.com/v16.0/me/photos"
#     payload = {
#         'access_token': PAGE_ACCESS_TOKEN
#     }
#     files = {
#         'source': open(image_path, 'rb')
#     }
#     try:
#         response = requests.post(url, data=payload, files=files)
#         response.raise_for_status()
#         image_id = response.json()['id']
#         image_url = f"https://www.facebook.com/photo.php?fbid={image_id}"
#         return image_url
#     except requests.RequestException as e:
#         print(f"Erreur lors du téléchargement de l'image sur Facebook : {e}")
#         return None

# # Fonction pour envoyer une notification par email
# def send_email_notification(title, content, hashtags, image_path=None):
#     try:
#         # Créer un message email
#         message = MIMEMultipart()
#         message['From'] = SENDER_EMAIL
#         message['To'] = RECIPIENT_EMAIL
#         message['Subject'] = f"Nouvel article publié : {title}"

#         # Ajouter le texte du message
#         body = f"Article Titre: {title}\n\nContenu:\n{content}\n\nHashtags:\n{hashtags}"
#         message.attach(MIMEText(body, 'plain'))

#         # Ajouter une image en pièce jointe si elle existe
#         if image_path and os.path.exists(image_path):
#             with open(image_path, 'rb') as img_file:
#                 img_part = MIMEBase('application', 'octet-stream')
#                 img_part.set_payload(img_file.read())
#                 encoders.encode_base64(img_part)
#                 img_part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(image_path)}')
#                 message.attach(img_part)

#         # Se connecter au serveur SMTP et envoyer l'email
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.starttls()
#             server.login(SENDER_EMAIL, SENDER_PASSWORD)
#             server.send_message(message)
#             print("Email envoyé avec succès !")
#     except Exception as e:
#         print(f"Erreur lors de l'envoi de l'email : {e}")

# # Créer un répertoire pour stocker les fichiers
# if not os.path.exists(daily_folder):
#     os.makedirs(daily_folder)

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

# # Traiter chaque article
# for article in articles:
#     title = article.find('h2').get_text(strip=True)
#     if title in processed_titles:
#         continue  # Passer les articles déjà traités

#     content = article.find('p').get_text(strip=True)
#     content = reformulate_text(content)  # Reformuler le texte

#     # Télécharger une image pour l'article
#     image_query = f"{title} sports"
#     image_url = get_image_url_from_pexels(image_query)
#     if image_url:
#         image_filename = os.path.join(daily_folder, f"{title.replace('/', '_')}.jpg")
#         download_image(image_url, image_filename)
#     else:
#         image_filename = None

#     # Générer des hashtags
#     hashtags = generate_hashtags(content)

#     # Publier sur Facebook
#     post_to_facebook(content, image_filename)

#     # Envoyer une notification par email
#     send_email_notification(title, content, " ".join(hashtags), image_filename)

#     # Ajouter le titre au fichier des titres traités
#     add_processed_title(title)

#     # Attendre avant de traiter l'article suivant
#     time.sleep(1)










# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# import time
# from datetime import datetime
# import spacy
# import random
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# # Charger le modèle spaCy
# nlp = spacy.load("en_core_web_sm")

# # URL de la page à analyser
# url = "https://www.lefigaro.fr/sports"

# # Définir les headers, y compris le User-Agent
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# # Clé API Pexels
# PEXELS_API_KEY = '1osRTIRyPIiHgClchOtSXAt27oxTSsDOMOLwbGR5w3M9TKU0cjg9vypU'

# # Informations de l'email
# SENDER_EMAIL = "badour.info@gmail.com"
# SENDER_PASSWORD = "hqzu fcyx yilp cffm"
# RECIPIENT_EMAIL = "mohsinbadour2000@gmail.com"

# # Informations de la publication Facebook
# FACEBOOK_PAGE_ACCESS_TOKEN = 'EAARrq1nLhkgBOZCgH3GGZBy9808WI091fmtmQWd03gdjVuKIrYhepcud1jl7dU9RzQktOfBTngfimX9CqF95tkJcM2vrdGiiGTYUdbW0D2OIVuui4PzABNyWga2oIhINpZBAApPkcDTxmuMoH0shkFi3mDa9KDMkqsyyNZAJwS3Vvb7PVlhlZCuTDZCQY1A7nN69hqBoXHSu7jMQb5gZBPyuexq'  # Remplacez par votre jeton d'accès à la page
# FACEBOOK_APP_ID = '1244283596932680'

# # Fichier pour stocker les titres des articles déjà traités
# processed_titles_file = 'processed_titles.txt'

# # Créer un dossier pour les fichiers générés le même jour
# today_date = datetime.now().strftime('%Y-%m-%d')
# daily_folder = f"articles/{today_date}"

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

# # Fonction pour générer des hashtags à partir du texte de l'article
# def generate_hashtags(text, min_hashtags=3, max_hashtags=10):
#     doc = nlp(text)
#     entities = [ent.text for ent in doc.ents]  # Extraire les entités nommées
#     phrases = [chunk.text for chunk in doc.noun_chunks]  # Extraire les groupes nominaux
#     keywords = list(set(entities + phrases))  # Combiner les entités et phrases

#     # Filtrer les mots-clés courts
#     hashtags = [f"#{word.replace(' ', '_')}" for word in keywords if len(word) > 3]

#     # Assurer que le nombre de hashtags à retourner est valide
#     num_hashtags = min(max_hashtags, max(min_hashtags, len(hashtags)))

#     # Si le nombre de hashtags demandés est supérieur à ceux disponibles, ajuster
#     if len(hashtags) < num_hashtags:
#         num_hashtags = len(hashtags)

#     return random.sample(hashtags, num_hashtags) if hashtags else []

# # Fonction pour envoyer un email de notification
# def send_email_notification(title, content, hashtags, image_path):
#     # Créer l'objet MIMEMultipart
#     msg = MIMEMultipart()
#     msg['From'] = SENDER_EMAIL
#     msg['To'] = RECIPIENT_EMAIL
#     msg['Subject'] = f"Nouvel article traité : {title}"

#     # Attacher le corps de l'email
#     body = f"Titre: {title}\n\nContenu:\n{content}\n\nHashtags: {hashtags}\n"
#     msg.attach(MIMEText(body, 'plain'))

#     # Attacher l'image si elle existe
#     if image_path:
#         with open(image_path, "rb") as attachment:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(attachment.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(image_path)}")
#             msg.attach(part)

#     # Envoyer l'email via le serveur SMTP
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         text = msg.as_string()
#         server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
#         server.quit()
#         print(f"Email envoyé à {RECIPIENT_EMAIL}")
#     except Exception as e:
#         print(f"Erreur lors de l'envoi de l'email : {e}")

# # Fonction pour publier sur Facebook
# def post_to_facebook(message, image_path=None):
#     api_url = f"https://graph.facebook.com/v12.0/{FACEBOOK_APP_ID}/feed"
#     payload = {
#         'message': message,
#         'access_token': FACEBOOK_PAGE_ACCESS_TOKEN
#     }
    
#     if image_path:
#         # Upload image
#         image_upload_url = f"https://graph.facebook.com/v12.0/{FACEBOOK_APP_ID}/photos"
#         files = {'file': open(image_path, 'rb')}
#         image_payload = {
#             'access_token': FACEBOOK_PAGE_ACCESS_TOKEN
#         }
#         image_response = requests.post(image_upload_url, data=image_payload, files=files)
#         if image_response.status_code == 200:
#             image_id = image_response.json()['id']
#             payload['object_attachment'] = image_id
#         else:
#             print(f"Erreur lors du téléchargement de l'image sur Facebook : {image_response.status_code}")

#     response = requests.post(api_url, data=payload)
#     if response.status_code == 200:
#         print("Publication réussie sur Facebook")
#     else:
#         print(f"Erreur lors de la publication sur Facebook : {response.status_code}")

# # Créer un répertoire pour stocker les fichiers
# if not os.path.exists(daily_folder):
#     os.makedirs(daily_folder)

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
#         article_filename = f"{daily_folder}/article_{timestamp}_{index}.txt"
#         image_filename = f"{daily_folder}/image_{timestamp}_{index}.jpg" if image_url else None

#         # Sauvegarder l'article
#         with open(article_filename, 'w', encoding='utf-8') as file:
#             file.write(f"Titre: {h2_text}\n\nContenu:\n{content_text}\n\nHashtags:\n{hashtags_str}\n")

#         # Télécharger l'image si elle existe
#         if image_url:
#             download_image(image_url, image_filename)

#         # Ajouter le titre à la liste des titres traités
#         add_processed_title(h2_text)

#         # Envoyer un email de notification
#         send_email_notification(h2_text, content_text, hashtags_str, image_filename)

#         # Publier sur Facebook
#         post_to_facebook(f"{h2_text}\n\n{content_text}\n\n{hashtags_str}", image_filename)







import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import time
from datetime import datetime
import spacy
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PIL import Image
from io import BytesIO

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

# Informations de l'email
SENDER_EMAIL = "badour.info@gmail.com"
SENDER_PASSWORD = "hqzu fcyx yilp cffm"
RECIPIENT_EMAIL = "mohsinbadour2000@gmail.com"

# ID de la Page Facebook et Access Token
PAGE_ACCESS_TOKEN = 'EAARrq1nLhkgBO5dGpfZCZB6i6693E8zHVkUCDsD4cDWjIQmDAFMq6aZB5y3ZAQvS2rkwO8cMXpwtmv9kAFegMWQyaJ3MhYRVaZCG0Nmj6msRLebbrWi7ZC561GcfyX9BiK7MRc8sZBJmnkRqhoFDQEWokxh3ZANJ9VGCyd8kZAdw1PtbMet4ldB3X8bHrERSZAcWigSKgIkRxUdEZBYD0hl5xjFiHcU'

# Fichier pour stocker les titres des articles déjà traités
processed_titles_file = 'processed_titles.txt'

# Créer un dossier pour les fichiers générés le même jour
today_date = datetime.now().strftime('%Y-%m-%d')
daily_folder = f"articles/{today_date}"

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

# Fonction pour télécharger une image et la convertir en PNG
def download_and_convert_image(image_url, filename):
    try:
        image_response = requests.get(image_url, headers=headers)
        image_response.raise_for_status()
        with Image.open(BytesIO(image_response.content)) as img:
            img.save(filename, format='PNG')
        print(f"Image téléchargée et enregistrée sous {filename}")
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")
    except Exception as e:
        print(f"Erreur lors de la conversion de l'image : {e}")

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

# Fonction pour publier sur Facebook avec texte et image
def post_to_facebook(message, image_path=None):
    url = f"https://graph.facebook.com/v16.0/me/feed"
    payload = {
        'message': message,
        'access_token': PAGE_ACCESS_TOKEN
    }

    # Ajouter l'image si elle existe
    if image_path:
        # Télécharger l'image sur Facebook
        image_url = upload_image_to_facebook(image_path)
        payload['link'] = image_url

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print(f"Publication réussie sur Facebook : {response.json()}")
    except requests.RequestException as e:
        print(f"Erreur lors de la publication sur Facebook : {e}")

# Fonction pour télécharger une image sur Facebook et obtenir l'URL
def upload_image_to_facebook(image_path):
    url = f"https://graph.facebook.com/v16.0/me/photos"
    payload = {
        'access_token': PAGE_ACCESS_TOKEN
    }
    files = {
        'source': open(image_path, 'rb')
    }
    try:
        response = requests.post(url, data=payload, files=files)
        response.raise_for_status()
        image_id = response.json()['id']
        image_url = f"https://www.facebook.com/photo.php?fbid={image_id}"
        return image_url
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image sur Facebook : {e}")
        return None

# Fonction pour envoyer une notification par email
def send_email_notification(title, content, hashtags, image_path=None):
    try:
        # Créer un message email
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = RECIPIENT_EMAIL
        message['Subject'] = f"Nouvel article publié : {title}"

        # Ajouter le texte du message
        body = f"Article Titre: {title}\n\nContenu:\n{content}\n\nHashtags:\n{hashtags}"
        message.attach(MIMEText(body, 'plain'))

        # Ajouter une image en pièce jointe si elle existe
        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                img_part = MIMEBase('application', 'octet-stream')
                img_part.set_payload(img_file.read())
                encoders.encode_base64(img_part)
                img_part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(image_path)}')
                message.attach(img_part)

        # Se connecter au serveur SMTP et envoyer l'email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
            print("Email envoyé avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

# Créer un répertoire pour stocker les fichiers
if not os.path.exists(daily_folder):
    os.makedirs(daily_folder)

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

# Traiter chaque article
for article in articles:
    title = article.find('h2').get_text(strip=True)
    
    # Vérifier si l'article est déjà traité
    if title in processed_titles:
        print(f"L'article '{title}' a déjà été traité. Passer au suivant.")
        continue

    content = article.find('p').get_text(strip=True)
    content = reformulate_text(content)  # Reformuler le texte

    # Enregistrer le contenu de l'article dans un fichier texte
    txt_filename = os.path.join(daily_folder, f"{title.replace('/', '_')}.txt")
    with open(txt_filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(content)

    # Télécharger une image pour l'article
    image_query = f"{title} sports"
    image_url = get_image_url_from_pexels(image_query)
    if image_url:
        image_filename = os.path.join(daily_folder, f"{title.replace('/', '_')}.png")
        download_and_convert_image(image_url, image_filename)
    else:
        image_filename = None

    # Générer des hashtags
    hashtags = generate_hashtags(content)

    # Publier sur Facebook
    post_to_facebook(content, image_filename)

    # Envoyer une notification par email
    send_email_notification(title, content, " ".join(hashtags), image_filename)

    # Ajouter le titre au fichier des titres traités
    add_processed_title(title)

    # Attendre avant de traiter l'article suivant
    time.sleep(1)
