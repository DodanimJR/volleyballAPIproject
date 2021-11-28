
from os import access
import re
from flask import Flask,request
from flask.json import jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended.view_decorators import verify_jwt_in_request


from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse
from sqlalchemy.sql.schema import RETAIN_SCHEMA
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/volleyball'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']='secret'
db = SQLAlchemy(app)
api = Api(app)
jwt=JWTManager(app)

PostUser=reqparse.RequestParser()
PostUser.add_argument('Usuario',required=True)
PostUser.add_argument('Password',required=True)

CreateUser=reqparse.RequestParser()
CreateUser.add_argument('Usuario',required=True)
CreateUser.add_argument('Password',required=True)
CreateUser.add_argument('Rol',required=True)

RecoverPass=reqparse.RequestParser()
RecoverPass.add_argument('Usuario',required=True)



PostPlayer=reqparse.RequestParser()
PostPlayer.add_argument('Nombre',required=True)
PostPlayer.add_argument('Equipo_id',required=True)
UpdatePlayer=reqparse.RequestParser()
UpdatePlayer.add_argument('Nombre')
UpdatePlayer.add_argument('Equipo_id')

PostTeam=reqparse.RequestParser()
PostTeam.add_argument('Nombre',required=True)

PUTTeam=reqparse.RequestParser()
PUTTeam.add_argument('Nombre',required=False)

PostTournament=reqparse.RequestParser()
PostTournament.add_argument('Nombre',required=True)
PostTournament.add_argument('ID_Equipo_1',required=True)
PostTournament.add_argument('ID_Equipo_2',required=True)
PostTournament.add_argument('ID_Equipo_3',required=True)
PostTournament.add_argument('ID_Equipo_4',required=True)

PostMatch=reqparse.RequestParser()
PostMatch.add_argument('ID_Torneo',required=True)
PostMatch.add_argument('ID_Equipo_1',required=True)
PostMatch.add_argument('ID_Equipo_2',required=True)
PostMatch.add_argument('Puntos_Equipo_1',required=True)
PostMatch.add_argument('Puntos_Equipo_2',required=True)
PostMatch.add_argument('Sets_Equipo_1',required=True)
PostMatch.add_argument('Sets_Equipo_2',required=True)

PutMatch=reqparse.RequestParser()
PutMatch.add_argument('ID_Torneo')
PutMatch.add_argument('ID_Equipo_1')
PutMatch.add_argument('ID_Equipo_2')
PutMatch.add_argument('Puntos_Equipo_1')
PutMatch.add_argument('Puntos_Equipo_2')
PutMatch.add_argument('Sets_Equipo_1')
PutMatch.add_argument('Sets_Equipo_2')





#Models
class player(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    team_id= db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self) -> str:
        return super().__repr__()

class team_tournament(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    team_id=db.Column(db.Integer, db.ForeignKey('team.id'))
    tournament_id=db.Column(db.Integer,db.ForeignKey('tournament.id'))


class team(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    players = db.relationship('player',backref='team')
    # tournaments= db.relationship('tournament', secondary=team_tournament,backref=db.backref('teams',lazy=True))

    def __repr__(self) -> str:
        return super().__repr__()

class tournament(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    

    def __repr__(self) -> str:
        return super().__repr__()

class match(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    tournament_id=db.Column(db.Integer,db.ForeignKey('tournament.id'))
    team1_id=db.Column(db.Integer,db.ForeignKey('team.id'))
    team2_id=db.Column(db.Integer,db.ForeignKey('team.id'))
    points_team1=db.Column(db.Integer)
    points_team2=db.Column(db.Integer)
    sets_team1=db.Column(db.Integer)
    sets_team2=db.Column(db.Integer)
    winner_id=db.Column(db.Integer,db.ForeignKey('team.id'))
    looser_id=db.Column(db.Integer,db.ForeignKey('team.id'))

    def __repr__(self) -> str:
        return super().__repr__()

class user(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user=db.Column(db.String(50))
    password=db.Column(db.String(50))
    rol=db.Column(db.String(20))

db.create_all()



class IndexRoute(Resource):
    def get(self):
        return {'response': 'Este es un api para ser utilizada por equipos de volleyball'},200

class Login(Resource):
    def post(self):
        args=PostUser.parse_args()
        usuario= args['Usuario']
        password=args['Password']
        user1=user.query.filter_by(user=usuario).first()
        contra=user.query.filter_by(password=password).first()
        if user1.password==contra.password:
            access_token=create_access_token(identity=user1.rol)
            
            return {"response":access_token},200
            
        else:
            return {"response":"CREDENCIALES NO VALIDAS"},401

class Sign_up(Resource):
    def post(self):
        args=CreateUser.parse_args()
        new_user=user(user=args['Usuario'],password=args['Password'],rol=args['Rol'])
        db.session.add(new_user)
        db.session.commit()
        return{'response':'USUARIO creado exitosamente'}
    
class Recover_Password(Resource):
    def post(self):
        args=RecoverPass.parse_args()
        usertouptdate=user.query.filter_by(user=args['Usuario']).first()
        if usertouptdate:
            passw=usertouptdate.password
            return{"response":"Su password es: "+ passw}
        else:
            return {'response':"NO EXISTE ESE USUARIO"},404
    
class Refresh_Token(Resource):
    def get(self):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        access_token=create_access_token(identity=identity,fresh=False)
        return{'response':access_token}





class IndexPlayers(Resource):

    def get(self):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        jugadores=player.query.all()
        response=[]
        if jugadores:
            for jugador in jugadores:
                equipo= team.query.filter_by(id=jugador.team_id).first()
                if equipo:
                    equipojugador=equipo.name
                response.append({
                    "Id":jugador.id,
                    "Nombre": jugador.name,
                    "Equipo": equipojugador
                })
            return {"response":response},302
        else:
            return {"response":"NO se encontraron registros"},404
    def post(self):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        args=PostPlayer.parse_args()
        jugador=player(name=args['Nombre'],team_id=args['Equipo_id'])
        db.session.add(jugador)
        db.session.commit()
        return{"response":"Jugador registrado con exito"},201


class IndexPlayerbyID(Resource):
    def get(self,id):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        jugador=player.query.filter_by(id=id).first()
        if jugador:
            response=[]
            equipo=team.query.filter_by(id=jugador.team_id).first()
            response.append({
                "Id":jugador.id,
                "Nombre": jugador.name,
                "Equipo": equipo.name
            })
            return{'response':response},302
        else:
            return{"response":"NO hay ningun jugador con el id: "+str(id)},404
    
    def put(self,id):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        if identity=='admin':
            jugador=player.query.filter_by(id=id)
            if jugador:
                args=UpdatePlayer.parse_args()
                if(args['Nombre']==None and args['Equipo_id']==None):
                    return{"response":"Formato no valido"},400
                if args['Nombre']:
                    jugador.name=args['Nombre']
                elif args['Equipo_id']:
                    jugador.team_id=args['Equipo_id']
                db.session.commit()
                return{'response':"El jugador con id "+str(id)+" ha sido actualizado"}

            else:
                return{"response":"NO hay ningun jugador con el id: "+str(id)},404
        else:
            return{'response':'Solo el admin puede actualizar datos'}
            
  
class indexTeams(Resource):
    def get(self):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        equipos= team.query.all()
        response=[]
        if equipos:
            
            for equipo in equipos:
                jogadores=player.query.filter_by(team_id=equipo.id).all()
                players=[]
                if jogadores:
                    for jogador in jogadores:
                        players.append({
                            "Id":jogador.id,
                            "Nombre": jogador.name,
                        })

                response.append({
                    "id":equipo.id,
                    "Nombre":equipo.name,
                    "Jugadores":players
                })
            
            return {"response":response},302

        else:
            return{'response':'no hay registros de equipos'},404


    def post(self):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        args=PostTeam.parse_args()
        new_equipo=team(name=args['Nombre'])
        db.session.add(new_equipo)
        db.session.commit()
        return{"response":"Equipo registrado con exito"},201
   
class IndexTeambyID(Resource):
    def get(self,id):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        
        equipo=team.query.filter_by(id=id).first()
        if equipo:
            jogadores=player.query.filter_by(team_id=equipo.id).all()
            players=[]
            if jogadores:
                    for jogador in jogadores:
                        players.append({
                            "Id":jogador.id,
                            "Nombre": jogador.name,
                        })
            response=[]
            response.append({
                "Id":equipo.id,
                "Nombre": equipo.name,
                "Jugadores": players
            })
            return{'response':response},302
        else:
            return{"response":"NO hay ningun Equipo con el id: "+str(id)},404
    
    def put(self,id):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        if identity=='admin':
            equipo=team.query.filter_by(id=id)
            if equipo:
                args=PUTTeam.parse_args()
                if(args['Nombre']==None):
                    return{"response":"Formato no valido"},400
                if args['Nombre']:
                    equipo.name=args['Nombre']
                db.session.commit()
                return{'response':"El equipo con id "+str(id)+" ha sido actualizado"}

            else:
                return{"response":"NO hay ningun Equipo con el id: "+str(id)},404
        else:
            return{'response':'Solo el admin puede actualizar datos'}    


class IndexTournaments(Resource):
    def get(self):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        torneos=tournament.query.all()
        if torneos:
            response=[]
            for torneo in torneos:
                torneos_y_equipos=team_tournament.query.filter_by(tournament_id=torneo.id).all()
                teams=[]
                for torneo_y_equipo in torneos_y_equipos:
                    equipo=team.query.filter_by(id=torneo_y_equipo.team_id).first()
    
                    jogadores=player.query.filter_by(team_id=equipo.id).all()
                    players=[]
                    if jogadores:
                        for jogador in jogadores:
                            players.append({
                                "Id":jogador.id,
                                "Nombre": jogador.name,
                            })

                    teams.append({
                        "id":equipo.id,
                        "Nombre":equipo.name,
                        "Jugadores":players
                    })
                    

                response.append({
                    "Id":torneo.id,
                    "Nombre":torneo.name,
                    "Equipos":teams
                })
            return{"response":response},302
        else:
            return{"response":"NO hay torneos registrados"},404
    def post(self):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        args=PostTournament.parse_args()
        new_torneo=tournament(name=args['Nombre'])
        db.session.add(new_torneo)
        db.session.commit()
        print(new_torneo.id)
        new_torneo_equipo1=team_tournament(team_id=args['ID_Equipo_1'],tournament_id=new_torneo.id)
        new_torneo_equipo2=team_tournament(team_id=args['ID_Equipo_2'],tournament_id=new_torneo.id)
        new_torneo_equipo3=team_tournament(team_id=args['ID_Equipo_3'],tournament_id=new_torneo.id)
        new_torneo_equipo4=team_tournament(team_id=args['ID_Equipo_4'],tournament_id=new_torneo.id)
        db.session.add(new_torneo_equipo1)
        db.session.add(new_torneo_equipo2)
        db.session.add(new_torneo_equipo3)
        db.session.add(new_torneo_equipo4)
        db.session.commit()
        return{'response':"TORNEO registrado exitosamente"},201

class IndexTournamentsById(Resource):
    def get(self,id):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        torneo=tournament.query.filter_by(id=id).first()
        if torneo:
            response=[]
            
            torneos_y_equipos=team_tournament.query.filter_by(tournament_id=torneo.id).all()
            teams=[]
            for torneo_y_equipo in torneos_y_equipos:
                equipo=team.query.filter_by(id=torneo_y_equipo.team_id).first()

                jogadores=player.query.filter_by(team_id=equipo.id).all()
                players=[]
                if jogadores:
                    for jogador in jogadores:
                        players.append({
                            "Id":jogador.id,
                            "Nombre": jogador.name,
                        })

                teams.append({
                    "id":equipo.id,
                    "Nombre":equipo.name,
                    "Jugadores":players
                })
                

            response.append({
                "Id":torneo.id,
                "Nombre":torneo.name,
                "Equipos":teams
            })
            return{"response":response},302
        else:
            return{"response":"NO hay torneos registrados con el id: "+str(id)},404

class IndexMatches(Resource):
    def post(self):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        args=PostMatch.parse_args()
        points_team1=args['Puntos_Equipo_1']
        points_team2=args['Puntos_Equipo_2']
        if points_team1>points_team2:
            winner=args['ID_Equipo_1']
            looser=args['ID_Equipo_2']
        else:
            looser=args['ID_Equipo_1']
            winner=args['ID_Equipo_2']
        new_match=match(tournament_id=args['ID_Torneo'],team1_id=args['ID_Equipo_1'],team2_id=args['ID_Equipo_2'],points_team1=args['Puntos_Equipo_1'],points_team2=args['Puntos_Equipo_2'],sets_team1=args['Sets_Equipo_1'],sets_team2=args['Sets_Equipo_2'],winner_id=winner,looser_id=looser)
        db.session.add(new_match)
        db.session.commit()
        return{'response':"PARTIDO creado exitosamente"},201

    def get(self):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)

        partidos=match.query.all()
        if partidos:
            response=[]
            for partido in partidos:
                torneo=tournament.query.filter_by(id=partido.tournament_id).first()
                equipo1=team.query.filter_by(id=partido.team1_id).first()
                equipo2=team.query.filter_by(id=partido.team2_id).first()
                winner=team.query.filter_by(id=partido.winner_id).first()
                looser=team.query.filter_by(id=partido.looser_id).first()

                response.append({
                    "ID":partido.id,
                    "Torneo":torneo.name,
                    "Equipo 1":equipo1.name,
                    "Puntos Totales":partido.points_team1,
                    "Sets Ganados":partido.sets_team1,
                    "Equipo 2": equipo2.name,
                    "Puntos Totales":partido.points_team2,
                    "Sets Ganados":partido.sets_team2,
                    "Ganador":winner.name,
                    "Perdedor":looser.name
                })
            return{'response':response},302

        else:
            return{'response':"NO HAY REGISTROS DE PARTIDOS"},404
        
class IndexMatchesById(Resource):
    def get(self,id):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)

        partido=match.query.filter_by(id=id).first()
        if partido:
            response=[]
            
            torneo=tournament.query.filter_by(id=partido.tournament_id).first()
            equipo1=team.query.filter_by(id=partido.team1_id).first()
            equipo2=team.query.filter_by(id=partido.team2_id).first()
            winner=team.query.filter_by(id=partido.winner_id).first()
            looser=team.query.filter_by(id=partido.looser_id).first()

            response.append({
                "ID":partido.id,
                "Torneo":torneo.name,
                "Equipo 1":equipo1.name,
                "Puntos Totales":partido.points_team1,
                "Sets Ganados":partido.sets_team1,
                "Equipo 2": equipo2.name,
                "Puntos Totales":partido.points_team2,
                "Sets Ganados":partido.sets_team2,
                "Ganador":winner.name,
                "Perdedor":looser.name
            })
            return{'response':response},302
        else:
            return{'response':"NO HAY REGISTROS DE PARTIDOS CON EL ID: "+str(id)},404
    
    def put(self,id):
        verify_jwt_in_request()
        identity=get_jwt_identity()
        print(identity)
        if identity=='admin':
            partido=match.query.filter_by(id=id)
            if partido:
                args=PutMatch.parse_args()
                if(args['ID_Torneo']==None and args['ID_Equipo_1']==None and args['ID_Equipo_2']==None and args['Puntos_Equipo_1']==None and args['Puntos_Equipo_2']==None and args['Sets_Equipo_1']==None and args['Sets_Equipo_2']):
                    return{'response':"FORMATO NO VALIDO"},304
                if(args['ID_Torneo']):
                    partido.tournament_id=args['ID_Torneo']
                if(args['ID_Equipo_1']):
                    partido.team1_id=args['ID_Equipo_1']
                if(args['ID_Equipo_2']):
                    partido.team2_id=args['ID_Equipo_2']
                if(args['Puntos_Equipo_1']):
                    partido.points_team1=args['Puntos_Equipo_1']
                if(args['Puntos_Equipo_2']):
                    partido.points_team2=args['Puntos_Equipo_2']
                if(args['Sets_Equipo_1']):
                    partido.sets_team1=args['Sets_Equipo_1']
                if(args['Sets_Equipo_2']):
                    partido.sets_team2=args['Sets_Equipo_2']
                db.session.commit()
                return{'response':"El equipo con id "+str(id)+" ha sido actualizado"}

            else:
                return{"response":"NO hay ningun Equipo con el id: "+str(id)},404
        else:
            return{'response':'Solo el admin puede actualizar datos'}

api.add_resource(IndexRoute,'/')
api.add_resource(Login,'/login')
api.add_resource(Sign_up,'/sign-up')
api.add_resource(IndexPlayers,'/players')
api.add_resource(IndexPlayerbyID,'/players/<int:id>')
api.add_resource(indexTeams,'/teams')
api.add_resource(IndexTeambyID,'/teams/<int:id>')
api.add_resource(IndexTournaments,'/tournaments')
api.add_resource(IndexTournamentsById,'/tournaments/<int:id>')
api.add_resource(IndexMatches,'/matches')
api.add_resource(Recover_Password,'/recover-password')
api.add_resource(IndexMatchesById,'/matches/<int:id>')
api.add_resource(Refresh_Token,'/refresh-token')