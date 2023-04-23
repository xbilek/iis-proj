from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
import math, random
from forms import *
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
views = Blueprint('views',__name__)

@views.route('/') #homepage
@login_required #cant get to home page unless you login
def home():
    return render_template("home.html",user=current_user)


@views.route('/list_of_users') 
def list_of_users():
    all_users = User.query
    return render_template("list_of_users.html",user=current_user, all_users = all_users)

@views.route('/list_of_teams') 
def list_of_teams():
    all_teams = Team.query
    return render_template("list_of_teams.html",user=current_user, all_teams = all_teams)

@views.route('/list_of_tournaments') 
def list_of_tournaments():
    all_tournaments = Tournament.query.order_by(Tournament.id)
    return render_template("list_of_tournaments.html",user=current_user, all_tournaments = all_tournaments)

@views.route('/my_teams', methods = ['GET', 'POST']) 
def my_teams():
    teams = Team.query.filter_by(user_id=current_user.id)
    user_id = current_user.id
    user = User.query.get_or_404(user_id)
    teams_im_in = user.is_in_team
    return render_template("my_teams.html",user=current_user, teams=teams, teams_im_in = teams_im_in)

@views.route('/my_matches', methods = ['GET', 'POST'])
def my_matches():
    
    teams = Team.query.filter_by(user_id=current_user.id) #teams i created
    user_id = current_user.id
    user = User.query.get_or_404(user_id)
    teams_im_in = user.is_in_team
    all_my_matches =[]
    matches = Match.query
    
            
    return render_template('my_matches.html', user=current_user, teams=teams,matches=matches ,all_my_matches=all_my_matches,teams_im_in=teams_im_in)

@views.route('/create_team', methods = ['GET', 'POST']) 
def create_team():
    name = None
    form = AddTeamForm()
    if form.validate_on_submit():
        manager = current_user.id
        team = Team.query.first()
        team = Team(name=form.name.data, logo=form.logo.data, user_id = manager)
        db.session.add(team)
        db.session.commit()
        name = form.name.data
        form.name.data =''
        form.logo.data =''
        flash("Team created!", category='succes')
    our_teams = Team.query
    return render_template("create_team.html",form = form, name = name, our_teams=our_teams, user=current_user)

@views.route('/create_tournament', methods = ['GET', 'POST']) 
def create_tournament():
    name = None
    date = None
    form = AddTournamentForm()
    if form.validate_on_submit():
        manager_id = current_user.id
        participating = None
        requesting = None
        match_id = None
        tournament = Tournament.query.first()
        tournament = Tournament(
            name=form.name.data, 
            date=form.date.data, 
            description=form.description.data,
            prize=form.prize.data,
            max_team_members=form.max_team_members.data,
            min_team_members=form.min_team_members.data,
            max_teams=form.max_teams.data,
            min_teams=form.min_teams.data,
            manager_id = manager_id)
        try:
            db.session.add(tournament)
            db.session.commit()
        except:
            flash('something went wrong',category = 'error')

        name = form.name.data
        date = form.date.data
        form.name.data =''
        form.date.data =''
        form.description.data =''
        form.prize.data =''
        form.max_team_members.data =''
        form.min_team_members.data =''
        form.max_teams.data =''
        form.min_teams.data =''
        flash("Tournament created!", category='succes')
    our_tournaments = Tournament.query
    return render_template("create_tournament.html",form = form, name = name,date=date, our_tournaments=our_tournaments, user=current_user)


@views.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    
    form = AddTeamForm()
    team_to_update = Team.query.get_or_404(id)
    members = team_to_update.members
    if request.method =="POST": #aby to jen nenapsal do URL
        team_to_update.name = request.form['name']
        team_to_update.logo = request.form['logo']
        try:
            db.session.commit()
            flash("User updated succesfully",category = 'succes')
            return redirect('/my_teams')
            #return render_template("update.html", form = form, team_to_update = team_to_update,  user = current_user)
        except:
            return redirect('/my_teams')
    else:
        return render_template("update.html", form = form, team_to_update = team_to_update, members = members, user = current_user)

@views.route('/delete/<int:id>')
def delete(id):
    team_to_delete = Team.query.get_or_404(id)
    try:
        db.session.delete(team_to_delete)
        db.session.commit()
        flash('Team deleted succesfully!', category='succes')
        return redirect('/my_teams')
    except:
        return "there was a problem"

@views.route('/add_member/<int:id>')
def add_member(id):
    all_users = User.query
    team_id = id
    return render_template("add_member.html",user=current_user, all_users = all_users, team_id = team_id)

@views.route('/add_member_to_team/<int:user_id>/<int:team_id>')
def add_member_to_team(user_id, team_id):
    user_id = user_id
    teams = Team.query.filter_by(user_id=current_user.id)
    team = Team.query.get_or_404(team_id)
    user = User.query.get_or_404(user_id)
    user.is_in_team.append(team)
    db.session.commit()
    #return render_template("my_teams.html",user=current_user, teams=teams, teams_im_in=team.members)
    return redirect('/my_teams')

@views.route('/show_members/<int:id>', methods = ['GET', 'POST'])
def show_members(id):
    team = Team.query.get_or_404(id)
    members = team.members
    founder_id =team.user_id
    founder = User.query.get_or_404(founder_id) 
    return render_template("show_members.html",  team = team, members = members, user = current_user, founder=founder)

@views.route('/tournament_detail/<int:id>', methods = ['GET', 'POST'])
def tournament_detail(id):
    tournament = Tournament.query.get_or_404(id)
    try:
        teams_you_can_register = Team.query.filter_by(user_id = current_user.id)
    except:
        teams_you_can_register = "42"
    manager_id = tournament.manager_id
    manager = User.query.get_or_404(manager_id)
    teams_that_requested = tournament.requesting
    teams_registered = tournament.participating
    registered_teams_count = len(teams_registered)
    flag = True
    if registered_teams_count == tournament.max_teams:
        flag = False
        
    return render_template("tournament_detail.html",flag=flag, manager=manager,teams_registered = teams_registered, teams_that_requested=teams_that_requested,teams_you_can_register=teams_you_can_register,tournament = tournament, user = current_user)   

@views.route('/tournament_request/<int:team_id>/<int:tournament_id>', methods = ['GET', 'POST'])
def tournament_request(team_id, tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    team = Team.query.get_or_404(team_id)
    tournament.requesting.append(team)
    db.session.commit()
    flash("team requested succesfully",category='succes')


    return redirect(url_for('.tournament_detail', id=tournament_id))
    
@views.route('/tournament_unrequest/<int:team_id>/<int:tournament_id>', methods = ['GET', 'POST'])
def tournament_unrequest(team_id, tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    team = Team.query.get_or_404(team_id)
    tournament.requesting.remove(team)
    db.session.commit()
    flash("team unrequested succesfully")


    return redirect(url_for('.tournament_detail', id=tournament_id))
    
@views.route('/tournament_unregister/<int:team_id>/<int:tournament_id>', methods = ['GET', 'POST'])
def tournament_unregister(team_id, tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    team = Team.query.get_or_404(team_id)
    tournament.participating.remove(team)
    db.session.commit()
    flash("team unregistered succesfully")


    return redirect(url_for('.tournament_detail', id=tournament_id))
    
#current user
@views.route('/my_tournaments', methods = ['GET', 'POST'])
def my_tournaments():
    
    tournaments_created = Tournament.query.filter_by(manager_id=current_user.id)            
    
    return render_template("my_tournaments.html", user=current_user,tournaments_created=tournaments_created)

@views.route('/tournament_detail_manager/<int:tournament_id>', methods = ['GET', 'POST'])
def tournament_detail_manager(tournament_id):
    form = AddTournamentForm()
    tournament = Tournament.query.get_or_404(tournament_id)
    teams_that_requested = tournament.requesting
    teams_participating = tournament.participating
    
    registered_teams_count = len(teams_participating)
    flag=True
    if registered_teams_count == tournament.max_teams:
        flag = False
    
    if request.method =="POST": #aby to jen nenapsal do URL
        tournament.name = request.form['name']
        tournament.date = request.form['date']
        tournament.description = request.form['description']
        tournament.prize = request.form['prize']
        tournament.max_team_members = request.form['max_team_members']
        tournament.min_team_members = request.form['min_team_members']
        tournament.max_teams = request.form['max_teams']
        tournament.min_teams = request.form['min_teams']
        try:
            db.session.commit()
            flash("Tournament updated succesfully",category = 'succes')
            return redirect('/my_tournaments')
        except:
            flash("Tournament update failed",category = 'error')
            return redirect(url_for('.tournament_detail_manager', id=tournament_id))
    else:
        return render_template("tournament_detail_manager.html", flag=flag,form = form, tournament = tournament, user = current_user,teams_that_requested=teams_that_requested,teams_participating=teams_participating)

@views.route('/confirm_team/<int:team_id>/<int:tournament_id>', methods = ['GET', 'POST'])
def confirm_team(team_id, tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    team_to_confirm = Team.query.get_or_404(team_id)
    tournament.participating.append(team_to_confirm)
    tournament.requesting.remove(team_to_confirm)
    teams_participating= tournament.participating
    try:
        db.session.commit()
        flash('Team registered to tournament!', category='succes')
    except:
        flash('Something went wrong', category='error')
    return redirect(url_for('.tournament_detail_manager', tournament_id = tournament_id))

@views.route('/remove_team_tournament/<int:team_id>/<int:tournament_id>', methods = ['GET', 'POST'])
def remove_team_tournament(team_id, tournament_id):
    team_to_delete=Team.query.get_or_404(team_id)
    tournament = Tournament.query.get_or_404(tournament_id)

    tournament.participating.remove(team_to_delete)
    try:
        db.session.commit()
        flash('Team removed from tournament!',category='succes')
    except:
        flash('Something went wrong!', category='error')

    return redirect(url_for('.tournament_detail_manager', tournament_id = tournament_id))

@views.route('/confirm_tournament/<int:tournament_id>', methods = ['GET', 'POST'])
def confirm_tournament(tournament_id):
    tournament= Tournament.query.get_or_404(tournament_id)
    tournament.confirmation=True
    try:
        db.session.commit()
        flash('Tournament confirmed!',category='succes')
    except:
        flash('Something went wrong!', category='error')
    return redirect('/list_of_tournaments')

@views.route('/delete_user/<int:user_id>', methods = ['GET', 'POST'])
def delete_user(user_id):

    user_to_delete = User.query.get_or_404(user_id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User deleted succesfully!', category='succes')
        return redirect('/list_of_users')
    except:
        return flash('Something went wrong!', category='error')

@views.route('/delete_team/<int:team_id>', methods = ['GET', 'POST'])
def delete_team(team_id):

    team_to_delete = Team.query.get_or_404(team_id)
    try:
        db.session.delete(team_to_delete)
        db.session.commit()
        flash('Team "'+ str(team_to_delete.name) +'" deleted succesfully!', category='succes')
        return redirect('/list_of_teams')
    except:
        return flash('Something went wrong!', category='error')   

@views.route('/settings', methods = ['GET', 'POST'])
def settings():

    user_to_update = User.query.get_or_404(current_user.id)
    form = UpdateUserForm()
    if request.method =="POST":
        user_to_update.first_name=request.form['first_name']
        user_to_update.email=request.form['email']
        user_to_update.password=generate_password_hash(request.form['password'], method='sha256')##bez overovani hesla
        try:
            db.session.commit()
            flash("updated succesfully", category='success')
            return redirect('/settings')
        except:
            flash("update failed",category='error')
            return redirect('/settings')
    else:
        return render_template("settings.html",form = form, user=current_user)   

def get_range(number_of_teams):
    i = 0
    j = 0
    for i in range(100):
        range_1 = j
        j = 2**i
        if j>number_of_teams:
            return range_1

def preliminaries(tournament, team_count, rounds_count):
    a = get_range(team_count)
    prelims_count = (team_count-a)*2
    


def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]
    
def convert_list_to_dictionary(list_1,list_2):
    res = {list_1[i]: list_2[i] for i in range(len(list_1))}
    return res

def fill_list(match_count, list_to_fill):
    a = match_count/2
    for i in range(int(match_count)):
        list_to_fill.append(int(a))
        a = int(a/2)

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

@views.route('/harmonogram/<int:tournament_id>', methods = ['GET', 'POST'])
def harmonogram(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    team_list = tournament.participating
    match_list=[]
    teams_in_match_list=[]
    #random.shuffle(team_list)
    team_count = len(team_list)
        #8
    #print (team_list)
    B = team_list[:len(team_list)//2]
    C = team_list[len(team_list)//2:]
    matches_dictionary = {B[i]: C[i] for i in range(len(B))}
    match_list.append(B)
    match_list.append(C)
    #print (matches_dictionary)
    
    list_of_rounds=[]
    list_of_winners=[]
    half_team_count = team_count

    generate_list = []
    fill_list(team_count, generate_list)
    
    for team1,team2  in matches_dictionary.items():
        try: 
            match = Match.query.filter_by(team1_name = team1.name, team2_name = team2.name, round_number = 1, tournament_id = tournament_id).first()
            if match == None:
                a = 1/0
        except:
            match = Match(team1_name = team1.name, team2_name = team2.name, round_number = 1, tournament_id = tournament_id)
        
            db.session.add(match)
            db.session.commit()
    list_of_matches = Match.query.filter_by(tournament_id=tournament.id).order_by(Match.id)

    n = team_count
    if (n & (n-1) == 0) and n != 0:
        return render_template("harmonogram.html", number_of_rounds = int(team_count**(1/2)), list_of_matches=list_of_matches,half_team_count = int(team_count/2),generate_list = generate_list, matches_dictionary=matches_dictionary, list_of_rounds=list_of_rounds ,team_list = team_list, tournament = tournament, team_count = team_count, user = current_user)
    else:
        flash("For this number of teams, you must create you own scheme!", category = 'error')
        return redirect(url_for('.tournament_detail_manager', tournament_id = tournament_id))

@views.route('/own_harmonogram/<int:tournament_id>', methods = ['GET', 'POST'])
def own_harmonogram(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    team_list = tournament.participating
    match_list=[]
    teams_in_match_list=[]
    #random.shuffle(team_list)
    team_count = len(team_list)
        #8
    #print (team_list)
    B = team_list[:len(team_list)//2]
    C = team_list[len(team_list)//2:]
    matches_dictionary = {B[i]: C[i] for i in range(len(B))}
    match_list.append(B)
    match_list.append(C)
    
    participators = tournament.participating
    participators_count = len(participators) 
    
    
    # for team1,team2  in matches_dictionary.items():
    #     match = Match(team1_name = team1.name, team2_name = team2.name, round_number = 1)
    #     db.session.commit()
    # generate_list = []
    # fill_list(participators_count, generate_list)
    # flash(generate_list)
    list_of_matches = Match.query.filter_by(tournament_id=tournament.id).order_by(Match.id)
    
    #list_of_matches.order_by(match.id)
    return render_template("own_harmonogram.html", number_of_rounds = int(team_count**(1/2)),participators=participators ,list_of_matches=list_of_matches,team_list = team_list, tournament = tournament, user = current_user,participators_count=participators_count)



@views.route('/match_detail/<team1_name>/<team2_name>/<int:tournament_id>', methods = ['GET', 'POST'])
def match_detail(team1_name, team2_name,tournament_id):   
    team1 = Team.query.filter_by(name=team1_name).first()
    team2 = Team.query.filter_by(name=team2_name).first()

    form = MatchPointForm()
    try:
        match = Match.query.filter_by(team1_name=team1_name,team2_name=team2_name,tournament_id=tournament_id).first()
    except:
        match=Match(
        team1_name = team1_name,
        team2_name = team2_name,
        tournament_id = tournament_id,
        round_number = 1)

    if form.validate_on_submit():
        match.point1 = form.point1.data
        match.point2 = form.point2.data

        try:
            #db.session.add(match)
            db.session.commit()
        
            flash('Points set succesfuly!',category='succes')
        except:
            flash('Somethinng went wrong!', category="error")
        
    return render_template("match_detail.html",match=match ,user=current_user, team1=team1,team2=team2,form=form)

@views.route('/own_match_detail/<team1_name>/<team2_name>/<int:tournament_id>', methods = ['GET', 'POST'])
def own_match_detail(team1_name, team2_name,tournament_id):   
    team1 = Team.query.filter_by(name=team1_name).first()
    team2 = Team.query.filter_by(name=team2_name).first()

    form = MatchPointForm()
    try:
        match = Match.query.filter_by(team1_name=team1_name,team2_name=team2_name,tournament_id=tournament_id).first()
    except:
        match=Match(
        team1_name = team1_name,
        team2_name = team2_name,
        tournament_id = tournament_id,
        round_number = 1)

    if form.validate_on_submit():
        match.point1 = form.point1.data
        match.point2 = form.point2.data

        try:
            db.session.add(match)
            db.session.commit()
        
            flash('Points set succesfuly!',category='succes')
        except:
            flash('Somethinng went wrong!', category="error")
        
    return render_template("own_match_detail.html",match=match ,user=current_user, team1=team1,team2=team2,form=form)


# @views.route('/placeholder_match_detail/<int:tournament_id>', methods = ['GET', 'POST'])
# def placeholder_match_detail(tournament_id):  

#     form = PlaceholderTeams()
#     tournament = Tournament.query.get_or_404(tournament_id)
#     team1=None
#     team2=None

#     if form.validate_on_submit():
#         team_name1= form.team_name1.data
#         team_name2= form.team_name2.data
        
    
#     try:
#         flash(team_name1)
#         team1 = Team.query.filter_by(name=team_name1).first()
#         team2 = Team.query.filter_by(name=team_name2).first()
#         try:
#             if team1 in tournament.participating and team2 in tournament.participating:
#                 flash('its ok')
#         except:
#             flash('at least one of the teams is not in tournament',category='error')
#     except:
#         flash('at least one of the teams is not in tournament',category='error')

#     return render_template("placeholder_match_detail.html",form=form,user=current_user, team1=team1, team2=team2, tournament=tournament)


# @views.route('/add_match/<int:tournament_id>', methods = ['GET', 'POST'])
# def add_match(tournament_id):  
#     form = AddMatch()
#     match=Match.query.first()
#     tournament = Tournament.query.get_or_404(tournament_id)
#     team1=None
#     team2=None
#     participators = tournament.participating
#     list_of_matches = Match.query.filter_by(tournament_id=tournament.id)
#     if form.validate_on_submit():
#         match=Match.query.first()
#         team_name1= form.team_name1.data
#         team_name2= form.team_name2.data
#         team1 = Team.query.filter_by(name=team_name1).first()
#         team2 = Team.query.filter_by(name=team_name2).first()
#         match=Match(
#             round_number=form.round_number.data, 
#             team1_name=team_name1, 
#             team2_name=team_name2,
#             tournament_id = tournament_id
#             )
#         try:
#             if team1 in participators and team2 in participators:
#                 db.session.add(match)
#                 db.session.commit()
#                 flash('Match succesfully added!', category='succes')
#             else:
#                 flash('At least one of the teams is not in this tournament',category='error')
#         except:
#             pass
#         return redirect(url_for('.harmonogram', tournament_id = tournament_id))
#     print(list_of_matches.first())
#     list_of_all_matches = Match.query
#     return render_template('add_match.html',list_of_all_matches=list_of_all_matches,list_of_matches=list_of_matches,team2=team2,team1=team1,form=form,tournament_id=tournament_id, user=current_user)

@views.route('/own_add_match/<int:tournament_id>/<int:round_number>', methods = ['GET', 'POST'])
def own_add_match(tournament_id,round_number):  
    form = AddMatch()
    match=Match.query.first()
    tournament = Tournament.query.get_or_404(tournament_id)
    team1=None
    team2=None
    list_of_matches = Match.query.filter_by(tournament_id=tournament.id)
    participators = tournament.participating
    if form.validate_on_submit():
        match=Match.query.first()
        team_name1= form.team_name1.data
        team_name2= form.team_name2.data
        team1 = Team.query.filter_by(name=team_name1).first()
        team2 = Team.query.filter_by(name=team_name2).first()
        match=Match(
            round_number=round_number, 
            team1_name=team_name1, 
            team2_name=team_name2,
            tournament_id = tournament_id
            )
        if team1 in participators and team2 in participators:
            try:
                db.session.add(match)
                db.session.commit()
                flash('Match succesfully added!', category='succes')
            except:
                pass
        else:
            flash('At least one of the teams is not in this tournament',category='error')
        return redirect(url_for('.own_harmonogram', tournament_id = tournament_id))
    print(list_of_matches.first())
    list_of_all_matches = Match.query
    return render_template('own_add_match.html',participators=participators,tounament= tournament, list_of_all_matches=list_of_all_matches,list_of_matches=list_of_matches,team2=team2,team1=team1,form=form,tournament_id=tournament_id, user=current_user)

@views.route('/delete_match/<int:match_id>', methods = ['GET', 'POST'])
def delete_match(match_id):
    match_to_delete = Match.query.get_or_404(match_id)
    tournament_id= match_to_delete.tournament_id
    try:
        db.session.delete(match_to_delete)
        db.session.commit()
        flash("Match deleted succesfully", category = 'succes')
        return redirect(url_for('.harmonogram', tournament_id = tournament_id))
    except:
        return flash('Something went wrong!', category = 'error')

@views.route('/own_delete_match/<int:match_id>', methods = ['GET', 'POST'])
def own_delete_match(match_id):
    match_to_delete = Match.query.get_or_404(match_id)
    tournament_id= match_to_delete.tournament_id
    try:
        db.session.delete(match_to_delete)
        db.session.commit()
        flash("Match deleted succesfully", category = 'succes')
        return redirect(url_for('.own_harmonogram', tournament_id = tournament_id))
    except:
        return flash('Something went wrong!', category = 'error')

@views.route('/leave_team/<int:team_id>', methods = ['GET', 'POST'])
def leave_team(team_id):  
    team = Team.query.get_or_404(team_id)
    user = current_user
    user.is_in_team.remove(team)
    db.session.commit()
    flash('You left the team succesfully',category='succes')
    return redirect('/my_teams')

@views.route('/kick_from_team/<int:user_id>/<int:team_id>', methods = ['GET', 'POST'])
def kick_from_team(user_id,team_id):  
    team = Team.query.get_or_404(team_id)
    user = User.query.get_or_404(user_id)
    user.is_in_team.remove(team)
    db.session.commit()
    flash('User: "'+ str(user.first_name) +'" was kicked kicked from team!',category='succes')
    return redirect(url_for('.update', id = team_id))

@views.route('/delete_tournament/<int:tournament_id>', methods = ['GET', 'POST'])
def delete_tournament(tournament_id): 
    tournament_to_delete = Tournament.query.get_or_404(tournament_id)
    try:
        db.session.delete(tournament_to_delete)
        db.session.commit()
        flash('Tournament deleted succesfully!', category='succes')
        return redirect('/my_tournaments')
    except:
        return flash('Something went wrong!', category='error')