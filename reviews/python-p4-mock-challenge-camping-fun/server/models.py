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


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    # Add relationship
    signups = db.relationship("Signup", backref="activity")

    # Add serialization rules
    serialize_rules = ("-signups.activity",)

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'
    
    # Serializer Adds this method to our class
    # def to_dict(self):
    #     -> everything into dictioniary


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    # Add relationship
    signups = db.relationship("Signup", backref="camper")
    
    # Add serialization rules
    # serialize_only = 
    serialize_rules = ("-signups.camper",)
    
    # Add validation
    @validates("name")
    def validates_name(self, db_column, name):
        if type(name) is str and len(name) > 0:
            return name
        else:
            raise ValueError("Name must be a String")

    @validates("age")
    def validates_age(self, db_column, age):
        if age in range (8,19):
            return age
        else:
            raise ValueError("age must be between 8-18")

    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    # Add relationships
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))

    # activity = ... < this was added by db.relationship
    # camper = ... < this was added by db.relationship

    # Add serialization rules
    serialize_rules = ("-camper.signups", "-activity.signups")
    # Add validation
    @validates("time")
    def validate_time(self, db_column, time):
        if type(time) is int and 0 <= time <= 23:
            return time
        else:
            raise ValueError("time must be between 0 and 23")
        
    @validates("activity_id")
    def validate_activity_id(self, db_column, activity_id):
        activity = Activity.query.get(activity_id)
        if activity:
            return activity_id
        else:
            raise Exception("Activity not found.")
        
    @validates("camper_id")
    def validate_camper_id(self, db_column, camper_id):
        camper = Camper.query.get(camper_id)
        if camper:
            return camper_id
        else:
            raise Exception("Camper not found.")
    
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
