# 📚 Review With Students:
   # The dangers of plain text passwords 
   # What Hashing is
     # Hashing vs encryption 
     # How to Hash a string   
   # Salting 
     #Rainbow Tables
   # Bcrypt


# Let's move our flask_sqlalchemy import and the db line into our config file first to help clean up our code!
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# We should grab some imports from our config file, like db and bcrypt!


# Time to work on creating a user model so we can have users login and use our app!
    # What are the other attributes we think a user should have?
    # Which validations should there be?
    # How do we use bcrypt to help secure our user's information?
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # ✅ Add a column _password_hash
        # Note: When an underscore is used, it's a sign that the variable or method is for internal use.
    
    # ✅ Create a hybrid_property that will protect the hash from being viewed

    # ✅ Create a setter method called password_hash that takes self and a password.
        # Use bcyrpt to generate the password hash with bcrypt.generate_password_hash
        # Set the _password_hash to the hashed password

    # ✅ Create an authenticate method that uses bcyrpt to verify the password against the hash in the DB with bcrypt.check_password_hash 

    # ✅ Navigate to app

    def __repr__(self):
        return f'< username:{self.name}'


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

    cast_members = db.relationship('CastMember', backref='production')

    @classmethod
    def all ( cls ) :
        return [ prod.to_dict() for prod in Production.query.all() ]
    
    @classmethod
    def find_by_id ( cls, id ) :
        return Production.query.filter_by( id = id ).first()

    serialize_rules = ('-cast_members.production',)
    
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
        return CastMember.query.filter_by( id = id ).first()

    serialize_rules = ('-production.cast_member',)

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


# Password stuff for user model!
    # @hybrid_property
    # def password_hash ( self ) :
    #     return self._password_hash
    
    # @password_hash.setter
    # def password_hash ( self, password ) :
    #     if type( password ) is str and len( password ) in range( 6, 17 ) :
    #         password_hash = bcrypt.generate_password_hash( password.encode( 'utf-8' ) )
    #         self._password_hash = password_hash.decode( 'utf-8' )
    #     else :
    #         self.validation_errors.append( "Password validation error goes here!" )

    # def authenticate ( self, password ) :
    #     return bcrypt.check_password_hash( self._password_hash, password.encode( 'utf-8' ) )