from sqlalchemy import Column, Integer, Enum, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Session

from . import main
from . import category

association_truck_category = Table(
    'association_truck_category', main.Base.metadata,
    Column('category_name', String, ForeignKey(category.Category.name)),
    Column('truck_name', String, ForeignKey('trucks.name'))
)

class Truck(main.Base):
    __tablename__ = 'trucks'

    name = Column(String, primary_key=True)
    nb_seat_min = Column(Integer)
    nb_seat_max = Column(Integer)
    categories = relationship("Category", secondary=association_truck_category)

    def toJson(self):
        return {
            'name': self.name,
            'nb_seat_min': self.nb_seat_min,
            'nb_seat_max': self.nb_seat_max,
            'categories': [category.toJson() for category in self.categories]
        }

def createTrucks():

    fire = category.Category.get('FIRE')
    road_accident = category.Category.get('ROAD_ACCIDENT')
    social = category.Category.get('SOCIAL')
    personnal_assistance = category.Category.get('PERSONNAL_ASSISTANCE')
    high = category.Category.get('HIGH')
    speed = category.Category.get('SPEED')
    multi_purpose = category.Category.get('MULTI_PURPOSE')
    water = category.Category.get('WATER')

    trucks = [
        Truck(name = 'VL',  nb_seat_min = 2,nb_seat_max = 5,categories = [social, speed]),
        Truck(name = 'FPT', nb_seat_min = 4,nb_seat_max = 6,categories = [fire]),
        Truck(name = 'MEA', nb_seat_min = 2,nb_seat_max = 3,categories = [high, fire]),
        Truck(name = 'VSAV',nb_seat_min = 3,nb_seat_max = 4,categories = [speed, personnal_assistance]),
        Truck(name = 'CCF', nb_seat_min = 4,nb_seat_max = 4,categories = [fire, water]),
        Truck(name = 'VTU', nb_seat_min = 2,nb_seat_max = 3,categories = [speed, multi_purpose]),
        Truck(name = 'VSR', nb_seat_min = 2,nb_seat_max = 3,categories = [road_accident]),
    ]

    with Session(main.Engine) as session:
        for truck in trucks:
            if session.query(Truck).filter_by(name=truck.name).first() is None:
                session.add(truck)
                print(f'Added {truck.name}')
        session.commit()
