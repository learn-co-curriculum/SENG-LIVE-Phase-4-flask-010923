from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship
    missions = db.relationship( 'Mission', backref = 'planet' )
    scientists = association_proxy( 'missions', 'scientist' )

    @classmethod
    def all ( cls ) :
        return [ planet.to_dict() for planet in Planet.query.all() ]

    @classmethod
    def find_by_id ( cls, id ) :
        return Planet.query.filter( Planet.id == id ).first()

    # Add serialization rules
    def to_dict( self ) :
        return {
            'id': self.id,
            'name': self.name,
            'distance_from_earth': self.distance_from_earth,
            'nearest_star': self.nearest_star
        }


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    # Add relationship
    missions = db.relationship( 'Mission', backref = 'scientist' )
    planets = association_proxy( 'missions', 'planet' )

    @classmethod
    def all ( cls ) :
        return [ scientist.to_dict() for scientist in Scientist.query.all() ]

    @classmethod
    def find_by_id ( cls, id ) :
        return Scientist.query.filter( Scientist.id == id ).first()

    # Add serialization rules
    def to_dict ( self ) :
        return {
            'id': self.id,
            'name': self.name,
            'field_of_study': self.field_of_study
        }

    # Add validation
    validation_errors = []

    @classmethod
    def clear_validation_errors ( cls ) :
        cls.validation_errors = []

    @validates( 'name' )
    def validate_name ( self, key, name ) :
        if type( name ) is str and name :
            return name
        else :
            self.validation_errors.append( 'Name must be a string with at least 1 character.' )


    @validates( 'field_of_study' )
    def validate_fos ( self, key, fos ) :
        if type( fos ) is str and fos :
            return fos
        else :
            self.validation_errors.append( 'Field of Study must be a string with at least 1 character.' )


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationships
    planet_id = db.Column( db.Integer, db.ForeignKey( 'planets.id' ) )
    scientist_id = db.Column( db.Integer, db.ForeignKey( 'scientists.id' ) )

    # Add serialization rules
    def to_dict( self ) :
        return {
            'id': self.id,
            'name': self.name,
            'planet_id': self.planet_id,
            'scientist_id': self.scientist_id,
            'planet': self.planet.to_dict()
        }
    
    def to_dict_with_ps ( self ) :
        return {
            'id': self.id,
            'name': self.name,
            'planet_id': self.planet_id,
            'scientist_id': self.scientist_id,
            'planet': self.planet.to_dict(),
            'scientist': self.scientist.to_dict()
        }


    # Add validation
    validation_errors = []

    @classmethod
    def clear_validation_errors ( cls ) :
        cls.validation_errors = []

    @validates( 'name' )
    def validate_name ( self, key, name ) :
        if type( name ) is str and name :
            return name
        else :
            self.validation_errors.append( 'Name must be a string with at least 1 character.' )

    @validates( 'planet_id' )
    def validate_planet ( self, key, planet_id ) :
        planet = Planet.find_by_id( planet_id )
        if planet :
            return planet_id
        else :
            self.validation_errors.append( 'Planet not found.' )

    @validates( 'scientist_id' )
    def validate_scientist ( self, key, scientist_id ) :
        scientist = Scientist.find_by_id( scientist_id )
        if scientist :
            return scientist_id
        else :
            self.validation_errors.append( 'Scientist not found.' )

# add any models you may need.
