from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields import DateField, EmailField, TelField, IntegerField
from datetime import datetime

class AddTeamForm(FlaskForm):
    name = StringField("Name (required):", validators=[DataRequired()])
    logo = StringField("Logo:")
    submit = SubmitField("Submit")

class AddTournamentForm(FlaskForm):
    name = StringField("Name (required):", validators=[DataRequired()])
    date = DateField("Date (required):", format="%Y-%m-%d",validators=[DataRequired()])
    description = StringField("Description:")
    prize = StringField("Prize:")
    max_team_members = IntegerField("max_team_members: (required)", validators=[DataRequired()])
    min_team_members = IntegerField("min_team_members: (required)", validators=[DataRequired()])
    max_teams = IntegerField("max_teams: (required)", validators=[DataRequired()])
    min_teams = IntegerField("min_teams: (required)", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateUserForm(FlaskForm):
    first_name = StringField("Name (required):", validators=[DataRequired()])
    email = StringField("Email (required):", validators=[DataRequired()])
    password = StringField("Password (required):", validators=[DataRequired()])
    #password2 = StringField("Reenter Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class MatchPointForm(FlaskForm):
    point1 = IntegerField("point1:")
    point2 = IntegerField("point2:")
    submit = SubmitField("Submit")

class PlaceholderTeams(FlaskForm):
    team_name1= StringField("Team 1 name:")
    team_name2= StringField("Team 2 name:")
    submit = SubmitField("Submit")

class AddMatch(FlaskForm):
    team_name1= StringField("Team 1 name (required):", validators=[DataRequired()])
    team_name2= StringField("Team 2 name (required):", validators=[DataRequired()])
    round_number=IntegerField("Round number:")
    submit = SubmitField("Submit")