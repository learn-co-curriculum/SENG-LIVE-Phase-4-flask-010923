# 📚 Review With Students:
    # Review models
    # Review MVC
#SQLAlchemy import
from flask_sqlalchemy import SQLAlchemy

# 📚 Review With Students:
    # What SQLAlchemy() is replacing from SQLAlchemy in phase 3
     
db = SQLAlchemy()
# 1. ✅ Create a Production Model
	# tablename = 'Productions'
	# Columns:
        # title: string, genre: string, budget:float, image:string,director: string, description:string, ongoing:boolean, created_at:date time, updated_at: date time 
# 2. ✅ navigate to app.py
class Production(db.Model):
    __tablename__ = 'Productions'

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

    def __repr__(self):
        return f'<Production Title:{self.title}, Genre:{self.genre}, Budget:{self.budget}, Image:{self.image}, Director:{self.director},ongoing:{self.ongoing}>'