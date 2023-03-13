# 📚 Review With Students:
    # Validations and Invalid Data

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


# 1.✅ Import validates from sqlalchemy.orm

from sqlalchemy.orm import validates

db = SQLAlchemy()
# nullable and unique
class Production(db.Model, SerializerMixin):
    __tablename__ = 'productions'
    #CheckConstraint is not working
    __table_args__ = (
        db.CheckConstraint('budget < 100'),
    )

    id = db.Column(db.Integer, primary_key=True)

# 2.✅ Add Constraints to the Columns      
    
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    director = db.Column(db.String)
    description = db.Column(db.String)
    ongoing = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    crew_members = db.relationship('CrewMember', backref='production')
        
    serialize_rules = ('-crew_members.production',)


# 3.✅ Use the "validates" decorator to create a validation for images
    # 3.1 Pass the decorator 'image'
    # 3.2 Define a validate_image method, pass it self, key and image_path
    # 3.3 If .jpg is not in the image passed, raise the ValueError exceptions 
    # else return the image_path  
    
    @validates('image')
    def validate_image(self, key, image_path):
        if '.jpg' not in image_path:
            raise ValueError("Image file type must be a jpg")
        return image_path


    def __repr__(self):
        return f'<Production Title:{self.title}, Genre:{self.genre}, Budget:{self.budget}, Image:{self.image}, Director:{self.director},ongoing:{self.ongoing}>'

class CrewMember(db.Model, SerializerMixin):
    __tablename__ = 'crew_members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'))
    
    serialize_rules = ('-production.crew_members',)

    def __repr__(self):
        return f'<Production Name:{self.name}, Role:{self.role}'

