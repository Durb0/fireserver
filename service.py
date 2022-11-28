from model.main import Engine
from sqlalchemy.orm import Session

def getCategories():
    from model.category import Category
    list = []
    with Session(Engine) as session:
        categories = session.query(Category).all()
        for category in categories:
            list.append(category.toJson())
    return list


def getTruck(str):
    from model.truck import Truck

    with Session(Engine) as session:
        truck = session.query(Truck).filter(Truck.name == str).first()
        return truck.toJson()


if __name__ == "__main__":
    print(getCategories())