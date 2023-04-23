from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#n:n between user and team
user_team = db.Table('user_team',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
    )

#n:n between team and tournament
team_tournament = db.Table('team_tournament',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'))
    )

team_tournament_request = db.Table('team_tournament_request',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'))
    )

#n:n between team and match
team_match = db.Table('team_match',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'))
    )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #last_name = db.Column(db.String(150))
    admin = db.Column(db.Boolean, default=False)
    teams = db.relationship('Team', backref='manager')
    tournaments = db.relationship('Tournament', backref='tournament_manager')
    # n : n relationship
    is_in_team = db.relationship('Team',secondary=user_team, backref='members')

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    logo = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    point1 = db.Column(db.Integer)
    point2 = db.Column(db.Integer)
    team1_name = db.Column(db.String(150), db.ForeignKey('team.name'))
    team2_name = db.Column(db.String(150), db.ForeignKey('team.name'))
    round_number = db.Column(db.Integer)
    #foreign keys
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    are_in_match = db.relationship('Team',secondary=team_match, backref='contestant')

class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    date = db.Column(db.Date)
    description = db.Column(db.String(500))
    prize = db.Column(db.String(150))
    max_team_members = db.Column(db.Integer)
    min_team_members = db.Column(db.Integer)
    max_teams = db.Column(db.Integer)
    min_teams = db.Column(db.Integer)
    confirmation = db.Column(db.Boolean, default= False)
    participating = db.relationship('Team',secondary=team_tournament, backref='participators')
    requesting =  db.relationship('Team', secondary=team_tournament_request, backref='requestors')
    match_id = db.relationship('Match', backref='match_id')
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))