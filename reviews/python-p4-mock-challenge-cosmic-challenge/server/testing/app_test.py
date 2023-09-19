from models import Scientist, Planet, Mission
from app import app, db
from faker import Faker
from random import randint


class TestApp:
    '''Flask application in app.py'''

    def test_gets_scientists(self):
        '''retrieves scientists with GET requests to /scientists.'''

        with app.app_context():
            scientist1 = Scientist(name=Faker().name(),
                                   field_of_study=Faker().sentence())
            scientist2 = Scientist(name=Faker().name(),
                                   field_of_study=Faker().sentence())
            db.session.add_all([scientist1, scientist2])
            db.session.commit()

            response = app.test_client().get('/scientists')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json
            scientists = Scientist.query.all()
            assert [scientist['id'] for scientist in response] == [
                scientist.id for scientist in scientists]
            assert [scientist['name'] for scientist in response] == [
                scientist.name for scientist in scientists]
            assert [scientist['field_of_study'] for scientist in response] == [
                scientist.field_of_study for scientist in scientists]
            for scientist in response:
                assert 'missions' not in scientist

    def test_gets_scientist_by_id(self):
        '''retrieves one scientist using its ID with GET request to /scientists/<int:id>.'''

        with app.app_context():
            fake = Faker()
            scientist = Scientist(
                name=fake.name(), field_of_study=fake.sentence())
            planet = Planet(name=fake.name(),
                            distance_from_earth=randint(1000, 10000), nearest_star=fake.name())

            db.session.add_all([scientist, planet])
            db.session.commit()

            mission = Mission(scientist_id=scientist.id,
                              planet_id=planet.id, name=fake.sentence())
            db.session.add(mission)
            db.session.commit()

            response = app.test_client().get(f'/scientists/{scientist.id}')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json

            assert response['name'] == scientist.name
            assert response['field_of_study'] == scientist.field_of_study
            assert response['missions']

    def test_returns_404_if_no_scientist(self):
        '''returns an error message and 404 status code when a scientist is searched by a non-existent ID.'''

        with app.app_context():

            response = app.test_client().get('/scientists/0')
            assert response.json.get('error') == "Scientist not found"
            assert response.status_code == 404

    def test_creates_scientist(self):
        '''creates one scientist using a name and field of study with a POST request to /campers.'''

        with app.app_context():
            fake = Faker()
            name = fake.name()
            field_of_study = fake.sentence()
            response = app.test_client().post(
                '/scientists',
                json={
                    'name': name,
                    'field_of_study': field_of_study
                }
            ).json

            assert response['id']
            assert response['name'] == name
            assert response['field_of_study'] == field_of_study

            scientist = Scientist.query.filter(
                Scientist.name == name, Scientist.field_of_study == field_of_study).one_or_none()
            assert scientist

    def test_400_for_scientist_validation_error(self):
        '''returns a 400 status code and error message if a POST request to /scientists fails.'''

        with app.app_context():

            response = app.test_client().post(
                '/scientists',
                json={
                    'name': Faker().name(),
                    'field_of_study': ''
                }
            )

            assert response.status_code == 400
            assert response.json['errors'] == ["validation errors"]

            response = app.test_client().post(
                'scientists',
                json={
                    'name': '',
                    'field_of_study': ''
                }
            )

            assert response.status_code == 400
            assert response.json['errors'] == ["validation errors"]

    def test_patch_campers_by_id(self):
        '''updates scientist with PATCH request to /scientists/<int:id>.'''

        with app.app_context():
            fake = Faker()
            scientist = Scientist(
                name=fake.name(), field_of_study=fake.sentence())
            db.session.add(scientist)
            db.session.commit()

            response = app.test_client().patch(
                f'/scientists/{scientist.id}',
                json={
                    'name': scientist.name + '(updated)',
                    'field_of_study': scientist.field_of_study + '(updated)'
                })

            assert response.status_code == 202
            assert response.content_type == 'application/json'
            response = response.json

            scientist_updated = Scientist.query.filter(
                Scientist.id == scientist.id).one_or_none()

            assert response['id'] == scientist.id
            assert response['name'] == scientist_updated.name
            assert '(updated)' in scientist_updated.name
            assert response['field_of_study'] == scientist_updated.field_of_study
            assert '(updated)' in scientist_updated.field_of_study

    def test_validates_scientist_update(self):
        '''returns an error message if a PATCH request to /scientists/<int:id>  is invalid.'''

        with app.app_context():
            fake = Faker()
            scientist = Scientist(
                name=fake.name(), field_of_study=fake.sentence())
            db.session.add(scientist)
            db.session.commit()

            response = app.test_client().patch(
                f'/scientists/{scientist.id}',
                json={
                    'name': '',
                    'field_of_study': scientist.field_of_study
                })

            assert response.status_code == 400
            assert response.content_type == 'application/json'
            assert response.json['errors'] == ["validation errors"]

            response = app.test_client().patch(
                f'/scientists/{scientist.id}',
                json={
                    'name': scientist.name,
                    'field_of_study': ''
                })

            assert response.status_code == 400
            assert response.content_type == 'application/json'
            assert response.json['errors'] == ["validation errors"]

    def test_404_no_scientist_to_patch(self):
        '''returns an error message if a PATCH request to /scientists/<int:id> references a non-existent camper'''

        with app.app_context():

            response = app.test_client().patch(
                f'/scientists/0',
                json={
                    'name': 'some name',
                    'field_of_study': 'time travel'
                })
            assert response.status_code == 404
            assert response.content_type == 'application/json'
            assert response.json.get('error')
            assert response.status_code == 404

    def test_deletes_scientist_by_id(self):
        '''deletes scientist with DELETE request to /scientists/<int:id>.'''

        with app.app_context():
            fake = Faker()
            scientist = Scientist(
                name=fake.name(), field_of_study=fake.sentence())
            planet = Planet(name=fake.name(),
                            distance_from_earth=randint(1000, 10000), nearest_star=fake.name())

            db.session.add_all([scientist, planet])
            db.session.commit()

            mission = Mission(scientist_id=scientist.id,
                              planet_id=planet.id, name=fake.sentence())
            db.session.add(mission)
            db.session.commit()

            response = app.test_client().delete(f'/scientists/{scientist.id}')

            assert response.status_code == 204
            assert response.content_type == 'application/json'

            scientist = Scientist.query.filter(
                Scientist.id == scientist.id).one_or_none()
            assert not scientist

    def test_returns_404_if_no_scientist(self):
        '''returns 404 status code with DELETE request to /scientist/<int:id> if activity does not exist.'''

        with app.app_context():
            response = app.test_client().delete('/scientists/0')
            assert response.status_code == 404
            assert response.content_type == 'application/json'
            assert response.json.get('error') == 'Scientist not found'

    def test_gets_planets(self):
        '''retrieves planets with GET requests to /planets.'''

        with app.app_context():
            planet1 = Planet(name=Faker().name(), distance_from_earth=randint(10000, 100000),
                             nearest_star=Faker().name())
            planet2 = Planet(name=Faker().name(), distance_from_earth=randint(10000, 100000),
                             nearest_star=Faker().name())
            db.session.add_all([planet1, planet2])
            db.session.commit()

            response = app.test_client().get('/planets')
            assert response.status_code == 200
            assert response.content_type == 'application/json'

            response = response.json
            planets = Planet.query.all()

            assert [planet['id'] for planet in response] == [
                planet.id for planet in planets]
            assert [planet['name'] for planet in response] == [
                planet.name for planet in planets]
            assert [planet['distance_from_earth'] for planet in response] == [
                planet.distance_from_earth for planet in planets]
            assert [planet['nearest_star'] for planet in response] == [
                planet.nearest_star for planet in planets]
            for planet in response:
                assert 'missions' not in planet

    def test_creates_missions(self):
        '''creates mission with POST request to /missions'''

        with app.app_context():
            fake = Faker()
            scientist = Scientist(
                name=fake.name(), field_of_study=fake.sentence())
            planet = Planet(name=fake.name(),
                            distance_from_earth=randint(1000, 10000), nearest_star=fake.name())

            db.session.add_all([scientist, planet])
            db.session.commit()

            name = fake.sentence()
            response = app.test_client().post(
                '/missions',
                json={
                    'name': name,
                    'scientist_id': scientist.id,
                    'planet_id': planet.id
                }
            )

            assert response.status_code == 201
            assert response.content_type == 'application/json'
            response = response.json

            assert response['id']
            assert response['scientist_id'] == scientist.id
            assert response['planet_id'] == planet.id
            assert response['name'] == name
            assert response['planet']
            assert response['scientist']

            mission = Mission.query.filter(
                Mission.scientist_id == scientist.id, Mission.planet_id == planet.id).one_or_none()

            assert mission.name == name

    def test_400_for_mission_validation_error(self):
        '''returns a 400 status code and error message if a POST request to /mission fails.'''

        with app.app_context():
            fake = Faker()
            scientist = Scientist(
                name=fake.name(), field_of_study=fake.sentence())
            planet = Planet(name=fake.name(),
                            distance_from_earth=randint(1000, 10000), nearest_star=fake.name())

            db.session.add_all([scientist, planet])
            db.session.commit()

            response = app.test_client().post(
                '/missions',
                json={
                    'name': '',
                    'scientist_id': scientist.id,
                    'planet_id': planet.id
                }
            )

            assert response.status_code == 400
            assert response.content_type == 'application/json'
            assert response.json['errors'] == ["validation errors"]

            response = app.test_client().post(
                '/missions',
                json={
                    'name': Faker().sentence(),
                    'planet_id': planet.id,
                    'scientist_id': None
                }
            )

            assert response.status_code == 400
            assert response.content_type == 'application/json'
            assert response.json['errors'] == ["validation errors"]

            response = app.test_client().post(
                '/missions',
                json={
                    'name': Faker().sentence(),
                    'scientist_id': scientist.id,
                    'planet_id': None
                }
            )

            assert response.status_code == 400
            assert response.content_type == 'application/json'
            assert response.json['errors'] == ["validation errors"]
