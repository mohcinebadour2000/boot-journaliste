
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
PAGE_ACCESS_TOKEN = 'EAARrq1nLhkgBO8tjTZBb7SPQpGhZBGeu2GV2ReGqXjsJBqcVGrHbZBiUFZCTRSJRohOAh4nNCVyoFdFZATOHydjSZCwxCEGvwV7reOLeRbC5bZBlYJOtCG6op4LXC9ZAlIUZCv3Gn4a8VWNGUVSPDr6ggApetkRXtTfXiZC7HENtLigoXZB8vcuFUNVCYyJ2hAB07IFga7XmiLHIQBp0ZBIr1j5Y7NvHCQZDZD'

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
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver les articles
    articles = soup.find_all('article')

    for article in articles:
        title_tag = article.find('h2')  # Modifier si nécessaire selon la structure HTML
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)

        # Vérifier si l'article a déjà été traité
        if title in processed_titles:
            print(f"Article déjà traité : {title}")
            continue

        # URL de l'article
        article_url = urljoin(url, article.find('a')['href'])

        # Télécharger le contenu de l'article
        article_response = requests.get(article_url, headers=headers)
        article_response.raise_for_status()
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        content = article_soup.get_text(strip=True)

        # Récupérer une image pour l'article
        image_url = get_image_url_from_pexels(title)
        if image_url:
            # Nommer l'image et le fichier texte
            current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            image_filename = f"{daily_folder}/image_{current_time}.png"
            text_filename = f"{daily_folder}/article_{current_time}.txt"
            
            # Télécharger et enregistrer l'image
            download_and_convert_image(image_url, image_filename)
            
            # Sauvegarder les informations dans le fichier texte
            with open(text_filename, 'w', encoding='utf-8') as file:
                file.write(f"Titre: {title}\n")
                file.write(f"URL de l'article: {article_url}\n")
                file.write(f"Image URL: {image_url}\n")
                file.write(f"Contenu:\n{content}\n")
            
            # Ajouter le titre au fichier des titres traités
            add_processed_title(title)
            
            # Générer des hashtags
            hashtags = generate_hashtags(content)
            
            # Envoyer une notification par email
            send_email_notification(title, content, ', '.join(hashtags), image_filename)
            
            # Publier sur Facebook
            post_to_facebook(title, image_filename)

except requests.RequestException as e:
    print(f"Erreur lors de la récupération de la page principale : {e}")
