from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session


from . import main
#import main

class Category(main.Base):
    __tablename__ = 'categories'

    name = Column(String, primary_key=True)
    icon = Column(String)
    color = Column(String)
    is_gain = Column(Integer)

    def get(name : str):
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

if __name__ == "__main__":
    main.Base.metadata.create_all(main.Engine)

    with Session(main.Engine) as session:
        categories = createCategories()
        for category in categories:
            if session.query(Category).filter_by(name=category.name).first() is None:
                session.add(category)
                print(f'Added {category.name}')
        session.commit()