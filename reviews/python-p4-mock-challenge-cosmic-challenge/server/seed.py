from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Planet, Scientist, Mission

fake = Faker()


def create_planets():
    planets = []
    for _ in range(20):
        p = Planet(
            name=fake.first_name(),
            distance_from_earth=str(randint(100000, 10000000000)),
            nearest_star=fake.first_name(),
        )
        planets.append(p)

    return planets


def create_scientists():
    scientists = []
    names = []
    for _ in range(5):
        name = fake.name()
        while name in names:
            name = fake.name()
        names.append(name)

        s = Scientist(
            name=name,
            field_of_study=fake.sentence(),
        )
        scientists.append(s)

    return scientists


def create_missions(planets, scientists):
    missions = []
    for _ in range(20):
        m = Mission(
            name=fake.sentence(nb_words=3),
            planet_id=rc(planets).id,
            scientist_id=rc(scientists).id
        )
        missions.append(m)
    return missions


if __name__ == '__main__':

    with app.app_context():
        print("Clearing db...")
        Planet.query.delete()
        Scientist.query.delete()
        Mission.query.delete()

        print("Seeding planets...")
        planets = create_planets()
        db.session.add_all(planets)
        db.session.commit()

        print("Seeding scientists...")
        scientists = create_scientists()
        db.session.add_all(scientists)
        db.session.commit()

        print("Seeding missions...")
        missions = create_missions(planets, scientists)
        db.session.add_all(missions)
        db.session.commit()

        print("Done seeding!")
