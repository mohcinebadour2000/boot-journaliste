import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk import download

# Assure-toi d'avoir téléchargé les données nécessaires pour NLTK
download('punkt')
download('wordnet')

# Fonction pour reformuler un texte en remplaçant des mots par leurs synonymes
def reformulate_text(text):
    words = word_tokenize(text)
    reformulated_words = []
    for word in words:
        synonyms = wordnet.synsets(word)
        if synonyms:
            # Prendre le premier synonyme de la liste des synonymes
            synonym = synonyms[0].lemmas()[0].name()
            reformulated_words.append(synonym if synonym != word else word)
        else:
            reformulated_words.append(word)
    return ' '.join(reformulated_words)

# URL de la sous-catégorie Sports
url = 'https://www.france24.com/fr/sports/'

# Faire une requête HTTP pour obtenir le contenu du site
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Affiche le contenu HTML pour débogage
print(soup.prettify())

# Trouver les articles de sport
articles = soup.find_all('div', class_='m-item-list-article')

# Affiche les éléments extraits pour débogage
print("Nombre d'articles trouvés:", len(articles))
news_items = []
for article in articles:
    title_tag = article.find('h2')
    link_tag = article.find('a', href=True)
    if title_tag and link_tag:
        title = title_tag.get_text(strip=True)
        link = link_tag['href']
        news_items.append(f"{title} - {url.split('/')[0]}/{link}")

# Affiche les titres pour débogage
print("Articles extraits:")
for item in news_items:
    print(item)

# Reformuler les titres des nouvelles
reformulated_news = [reformulate_text(item) for item in news_items]

# Sauvegarder les nouvelles reformulées dans un fichier texte
with open('actualites_sport_reformulees.txt', 'w', encoding='utf-8') as file:
    for item in reformulated_news:
        file.write(item + '\n')

print("Les actualités sportives ont été extraites, reformulées et sauvegardées avec succès.")
