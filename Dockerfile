# Utilisez une image de base qui prend en charge Python (par exemple Python 3.12)
FROM python:3.12

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le contenu de votre application Flask dans le conteneur
COPY . /app

# Installez les dépendances de l'application
RUN pip install -r requirements.txt

# Exposez le port sur lequel votre application Flask écoute
EXPOSE 5000

CMD ["python", "app.py"]
