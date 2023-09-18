# 📚 Review With Students:
    # Validations and Invalid Data

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

from sqlalchemy.orm import validates

db = SQLAlchemy()

class Production(db.Model, SerializerMixin):
    __tablename__ = 'productions'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    genre = db.Column(db.String)
    budget = db.Column(db.Float, nullable = False)
    image = db.Column(db.String)
    director = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    ongoing = db.Column(db.Boolean, default = True)

    # YOU SHOULD ALWAYS HAVE THESE 2 COLUMNS ON YOUR MODELS!!!! 🫡
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Talk more about how the relationship method works! 🧑‍🏫
    cast_members = db.relationship('CastMember', backref='production')

    @classmethod
    def all ( cls ) :
        return [ prod.to_dict() for prod in Production.query.all() ]
    
    @classmethod
    def find_by_id ( cls, id ) :
        return Production.query.filter_by( id = id ).first()

    # ✅ Create a serialize rule that will help add our `cast_members` to the response.
    # serialize_rules = ('-cast_members.production',)

    def to_dict ( self ) :
        return {
            'id': self.id,
            'title': self.title,
            'budget': self.budget,
            'genre': self.genre,
            'image': self.image,
            'director': self.director,
            'description': self.description,
            'ongoing': self.ongoing
        }
    
    def to_dict_with_cast ( self ) :
        prod = self.to_dict()
        prod[ 'cast' ] = [ cm.to_dict() for cm in self.cast_members ]
        return prod
    
    # ✅ Create validations for the Production model

    validation_errors = []

    @classmethod
    def clear_validation_errors ( cls ) :
        cls.validation_errors = []
    
    @validates( 'title' )
    def validate_title ( self, db_column, new_title ) :
        if type( new_title ) is str and new_title :
            return new_title
        else :
            self.validation_errors.append( 'Title must be a string with at least 1 character.' )

    @validates( 'director' )
    def validate_director ( self, db_column, new_director ) :
        if type( new_director ) is str and new_director :
            return new_director
        else :
            self.validation_errors.append( 'Director must be a string with at least 1 character.' )

    @validates( 'budget' )
    def validate_budget ( self, db_column, new_budget ) :
        if isinstance( new_budget, float ) :
            if new_budget > 1000.00 :
                return new_budget
            else : 
                self.validation_errors.append( 'Budget must be more than $1000.' )
        else :
            self.validation_errors.append( 'Budget must be a float.' )

    def __repr__(self):
        return f'<Production Title:{self.title}, Genre:{self.genre}, Budget:{self.budget}, Image:{self.image}, Director:{self.director},ongoing:{self.ongoing}>'


class CastMember(db.Model, SerializerMixin):
    __tablename__ = 'cast_members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    role = db.Column(db.String, nullable = False)

    # YOU SHOULD ALWAYS HAVE THESE 2 COLUMNS ON YOUR MODELS!!!! 🫡
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'), nullable = False)

    @classmethod
    def all ( cls ) :
        return [ cm.to_dict() for cm in CastMember.query.all() ]
    
    @classmethod
    def find_by_id ( cls, id ) :
        # return CastMember.query.filter( CastMember.id == id ).first()
        return CastMember.query.filter_by( id = id ).first()
    
    # ✅ Create a serialize rule that will help add our `production` to the response.
    # serialize_rules = ('-production.cast_member',)

    def to_dict ( self ) :
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role
        }

    def to_dict_with_prod ( self ) :
        cm = self.to_dict()
        cm[ 'production' ] = self.production.to_dict()
        return cm

    validation_errors = []

    @classmethod
    def clear_validation_errors ( cls ) :
        cls.validation_errors = []
        

    @validates( 'name' )
    def validates_name( self, db_column, new_name ) :
        if type( new_name ) is str and new_name :
            return new_name
        else :
            self.validation_errors.append( 'Name must be a string and cannot be blank' )
    
    @validates( 'role' )
    def validates_role( self, db_column, new_role ) :
        if type( new_role ) is str and new_role :
            return new_role
        else :
            self.validation_errors.append( 'Role must be a string and cannot be blank' )

    @validates( 'production_id' )
    def validates_production ( self, db_column, prod_id ) :
        prod = Production.find_by_id( prod_id )
        if prod :
            return prod_id
        else :
            self.validation_errors.append( 'Production was not found.' )

    def __repr__(self):
        return f'<CastMember Name:{self.name}, Role:{self.role}'