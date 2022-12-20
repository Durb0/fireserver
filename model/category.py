from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session


from . import main



class Category(main.Base):
    """
        Cette classe permet de definir une categorie

        Attributes:
            name (str): le nom de la categorie
            icon (str): l'icone de la categorie
            color (str): la couleur de la categorie
            is_gain (int): si la categorie est un gain
    """

    __tablename__ = 'categories'

    name = Column(String, primary_key=True)
    icon = Column(String)
    color = Column(String)
    is_gain = Column(Integer)

    def get(name : str):
        """
            Cette methode permet de recuperer une categorie en fonction de son nom
        """
        with Session(main.Engine) as session:
            return session.query(Category).filter(Category.name == name).first()

    def toJson(self):
        return {
            'name': self.name,
            'icon': self.icon,
            'color': self.color,
            'is_gain': self.is_gain
        }

    def __repr__(self):
        return f'Category({self.name})'

def createCategories():
    """
        Cette fonction permet de creer les categories par defaut
    """
    categories = [
        Category(name = 'FIRE',                 icon = 'faFire',        color = 'red',          is_gain = 1),
        Category(name = 'ROAD_ACCIDENT',        icon = 'faCarBurst',    color = 'orange',       is_gain = 1),
        Category(name = 'SOCIAL',               icon = 'faThumbsUp',    color = 'deepskyblue',  is_gain = 1),
        Category(name = 'PERSONNAL_ASSISTANCE', icon = 'faPerson',      color = 'green',        is_gain = 1),
        Category(name = 'MULTI_PURPOSE',        icon = 'faWrench',      color = 'grey',         is_gain = 1),
        Category(name = 'SPEED',                icon = 'faGaugeHigh',   color = 'purple',       is_gain = 0),
        Category(name = 'WATER',                icon = 'faDroplet',     color = 'blue',         is_gain = 0),
        Category(name = 'HIGH',                 icon = 'faArrowUp',     color = 'brown',        is_gain = 0)
    ]

    return categories