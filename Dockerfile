# Utiliser l'image de base Python
FROM python:3.11

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier de requirements
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
# Installer les dépendances
RUN pip install -r requirements.txt

# Copier le reste de l'application
COPY . .

# Exposer le port 5000
EXPOSE 5000

# Commande pour lancer l'application avec Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
