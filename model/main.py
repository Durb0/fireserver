from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine


Base = declarative_base() # Crée une classe de base pour les classes de modèle
Engine = create_engine('sqlite:///db.sqlite3') # Crée un moteur de base de données