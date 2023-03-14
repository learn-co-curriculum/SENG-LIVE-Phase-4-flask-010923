#!/usr/bin/env python3
from faker import Faker

from app import app
from models import db, Production, CastMember

db.init_app(app)

fake = Faker()

with app.app_context():   
    Production.query.delete()
    CastMember.query.delete()

    productions = []
 
    p1 = Production(title='Hamlet', genre= 'Drama', director='Bill Shakespeare', description='The Tragedy of Hamlet, Prince of Denmark', budget= 100000.00, image='https://upload.wikimedia.org/wikipedia/commons/6/6a/Edwin_Booth_Hamlet_1870.jpg', ongoing=True)
    
    productions.append(p1)

    p2 = Production(title='Cats', genre='Musical', director='Andrew Lloyd Webber', description=' Jellicles cats sing and dance', budget=200000.00, image='https://upload.wikimedia.org/wikipedia/en/3/3e/CatsMusicalLogo.jpg', ongoing=True)
    
    productions.append(p2)

    p3 = Production(title='Carmen', genre='Opera', director='Georges Bizet', description='Set in southern Spain this is the story of the downfall of Don José, a naïve soldier who is seduced by the wiles of the fiery and beautiful Carmen.', budget=200000.00, image='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Prudent-Louis_Leray_-_Poster_for_the_premi%C3%A8re_of_Georges_Bizet%27s_Carmen.jpg/300px-Prudent-Louis_Leray_-_Poster_for_the_premi%C3%A8re_of_Georges_Bizet%27s_Carmen.jpg', ongoing=False)
    
    productions.append(p3)

    p4 = Production(title= 'Hamilton', genre= 'Musical', director='Lin-Manuel Miranda', description='An American Musical is a sung-and-rapped-through musical by Lin-Manuel Miranda. It tells the story of American Founding Father Alexander Hamilton.', budget= 400000.00, image='https://upload.wikimedia.org/wikipedia/en/thumb/8/83/Hamilton-poster.jpg/220px-Hamilton-poster.jpg',ongoing=False)
    
    productions.append(p4)

    db.session.add_all(productions)
    db.session.commit()

    hamlet_roles = ['Hamlet', 'Ophelia', 'Polonius', 'Laertes', 'Horatio', 'Gertrude', 'Ghost' ]
    hamlet_cast_members = [CastMember(name=fake.name(), role=role, production_id=p1.id) for role in hamlet_roles]
    db.session.add_all(hamlet_cast_members)
    db.session.commit()

    cats_roles = ['Mr. Mistoffelees', 'Bombalurina', 'Rumpletezer', 'Grizabella']
    cats_cast_members = [CastMember(name=fake.name(), role=role, production_id=p2.id) for role in cats_roles]
    db.session.add_all(cats_cast_members)
    db.session.commit()

    carmen_roles = ['Carmen', 'Escamillo', 'Jose', 'Mercedes', 'Dancaire']
    carmen_cast_members = [CastMember(name=fake.name(), role=role, production_id=p3.id) for role in carmen_roles]
    db.session.add_all(carmen_cast_members)
    db.session.commit()

    hamilton_roles = ['Alexander Hamilton', 'King George III', 'Marquis de Lafayett', 'Angelica Schuyler Church', 'Peggy Schuyler', 'Thomas Jefferson']
    hamilton_cast_members = [CastMember(name=fake.name(), role=role, production_id=p4.id) for role in hamilton_roles]
    db.session.add_all(hamilton_cast_members)
    db.session.commit()

