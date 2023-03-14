
from flask_sqlalchemy import SQLAlchemy
# 6. ✅ Import `SerializerMixin` from `sqlalchemy_serializer`
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()

# 7. ✅ Pass `SerializerMixin` to `Productions`
class Production(db.Model, SerializerMixin):
    __tablename__ = 'productions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    director = db.Column(db.String)
    description = db.Column(db.String)
    ongoing = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    cast_members = db.relationship('CastMember', backref='production')
    #Note:The relationship.backref keyword argument on the relationship() 
    #construct allows the automatic generation of a new relationship() 
    # that will be automatically be added to the ORM mapping for the 
    # related class. It will then be placed into a 
    # relationship.back_populates configuration against the current 
    # relationship() being configured, with both relationship() 
    # constructs referring to each other.

    # 7.1 ✅ Create a serialize rule that will help add our `cast_member` to the response.
    serialize_rules = ('-cast_members.production',)

    def __repr__(self):
        return f'<Production Title:{self.title}, Genre:{self.genre}, Budget:{self.budget}, Image:{self.image}, Director:{self.director},ongoing:{self.ongoing}>'

# 8. ✅ Pass `SerializerMixin` to `CastMember`
class CastMember(db.Model, SerializerMixin):
    __tablename__ = 'cast_members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'))
    
    # 8.1 ✅ Create a serialize rule that will help add our `production` to the response.
    serialize_rules = ('-production.cast_member',)

    def __repr__(self):
        return f'<Production Name:{self.name}, Role:{self.role}'

 # 9. ✅ Navigate back to `app.py` for further steps.