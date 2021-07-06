import json
import random
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from authentication.authentication_package.auth_data import UserAuth  # check this import
from .battle_package.request import Request
from .battle_package.response import Response
from .battle_package.algorithm import Battle
from army.army_package.army import Army, SpaceShip, SpaceCruiser, SpaceDestroyer


# TEST_JSON = '{"winner":true,"army":{"S":0,"C":1,"D":2},"report":{"1":{"a":3,"d":1},"2":{"a":2,"d":1}}}'
# input_fe = '{"attacker":{"type":"human",' \
#           '"name":"player x",' \
#           '"mail":"player@mail.com",' \
#           '"army":{"S":24,"C":1,"D":1,"F":1},' \
#           '"planet":"Venus"},' \
#           '"defender":{"type":"virtual",' \
#           '"name":"computer 1",' \
#           '"army":{"S":7,"C":8,"D":9,"F":2},' \
#           '"planet":"Mercury"}}'


def battle(request):
    # json_str = request.POST.get('data', '')
    army_attacker = Army()  # random generation (in production remove)
    army_defender = Army()  # random generation (in production remove)
    input_like_fe = Army.creation_input_like_fe(army_attacker, army_defender)  # in production remove
    battle_request = Request(input_like_fe)  # in production replace input_fe with json_str
    current_battle = Battle(battle_request)  # OBJ type Battle
    response = Response(current_battle)  # OBJ type Response
    battle_response = response.battle_final_report
    return HttpResponse(battle_response, status=200, content_type='application/json')
    # return HttpResponse(TEST_JSON, status=200, content_type='application/json')


def index(request):
    message = "Welcome! Go to --> https://browsergameteam2.herokuapp.com/accounts/google/login/"
    return HttpResponse(message, status=200)


# the following (test) code is accessible only if the user is already logged in
# if the user is not logged in, they will be displayed an unauthorized message (401)
@login_required(login_url='/not_authenticated')
def choose(request):

    user_auth = UserAuth(request)
    '''
    # print(request.user)
    user_db = AuthData.get_user(request)  # request.user will be the Google username
    username = AuthData.get_username(user_db)
    # print(username)
    # email = user_db.email
    # print(email)
    # note: the request.user value is always unique! Thus it can be directly used to retrieve token from db
    social_account_db = AuthData.get_social_account(user_db)
    uid = AuthData.get_uid(social_account_db)
    # print(social_account.extra_data)  # here is the mail also among the keys
    social_token_db = AuthData.get_social_token(social_account_db)
    token = AuthData.get_token(social_token_db)
    '''

    data = {'username': user_auth.username,
            'token': user_auth.token,
            'uid': user_auth.uid,
            'prices': {"S": SpaceShip().price, "C": SpaceCruiser().price, "D": SpaceDestroyer().price},
            "F": [1, 2, 3],
            "budget": 30}


    data_as_json = json.dumps(data)
    return HttpResponse(data_as_json, status=200, content_type='application/json')


def not_authenticated(request):
    return HttpResponse('not authorized: please sign in', status=401)
