import pytest

from app import app
from models import db, Scientist, Planet, Mission
from faker import Faker


class TestModels:
    '''SQLAlchemy models in models.py'''

    def test_validates_scientist_name(self):
        '''require scientist to have names.'''

        with app.app_context():

            with pytest.raises(ValueError):
                Scientist(name=None, field_of_study='time travel')

            with pytest.raises(ValueError):
                Scientist(name='', field_of_study='time travel')

    def test_validates_scientist_field_of_study(self):
        '''require scientist to have fields of study.'''

        with app.app_context():

            with pytest.raises(ValueError):
                Scientist(name=Faker().name(), field_of_study=None)

            with pytest.raises(ValueError):
                Scientist(name=Faker().name(), field_of_study='')

    def test_validates_mission_name(self):
        '''require missions to have names.'''

        with app.app_context():

            with pytest.raises(ValueError):
                Mission(name=None, scientist_id=1, planet_id=1)

            with pytest.raises(ValueError):
                Mission(name='', scientist_id=1, planet_id=1)

    def test_validates_mission_scientist(self):
        '''require missions to have scientist_id.'''

        with app.app_context():

            with pytest.raises(ValueError):
                Mission(name=Faker().name(), planet_id=1, scientist_id=None)

    def test_validates_mission_planet(self):
        '''require missions to have planet_id.'''

        with app.app_context():

            with pytest.raises(ValueError):
                Mission(name=Faker().name(), scientist_id=1, planet_id=None)
