import json
import random
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from authentication.authentication_package.auth_data import UserAuth  # check this import
from .battle_package.request import Request
from .battle_package.response import Response
from .battle_package.algorithm import Battle
from army.army_package.army import Army


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

def creation_input_fe_random(n_army):
    for i in range(n_army):
        army_random_att = Army(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100),
                               random.randint(1, 3))
        army_random_def = Army(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100),
                               random.randint(1, 3))
        input_fe =  '{"attacker":{"type":"human",' \
                    '"name":"player x",' \
                    '"mail":"player@mail.com",' \
                    '"army":{' + f'{army_random_att}' + '},' \
                    '"planet":"Venus"},' \
                    '"defender":{"type":"virtual",' \
                    '"name":"computer 1",' \
                    '"army":{' + f'{army_random_def}' + '},' \
                    '"planet":"Mercury"}}'
        yield input_fe


def index(request):
    message = "Welcome! Go to --> https://browsergameteam2.herokuapp.com/accounts/google/login/"
    return HttpResponse(message, status=200)


# def battle(request):
    # json_str = request.POST.get('data', '')
    # battle_request = Request(input_fe)  # in production replace input_fe with json_str
    # current_battle = Battle(battle_request)  # OBJ type Battle
    # response = Response(current_battle)  # OBJ type Response
    # battle_response = response.battle_final_report
    # return HttpResponse(battle_response, status=200, content_type='application/json')
    # return HttpResponse(TEST_JSON, status=200, content_type='application/json')

def battle(request):
    # json_str = request.POST.get('data', '')
    # create a generator with parameters for statistics and create a list with that values
    armies = list(creation_input_fe_random(1))
    # in production use this armies
    # armies = [json.loads(json_str)]
    battles_responses = []
    val_battles = {'wins_attacker': 0, 'wins_defender': 0}
    for army in armies:
        battle_request = Request(army)
        current_battle = Battle(battle_request)  # OBJ type Battle
        response = Response(current_battle)  # OBJ type Response
        battle_response = response.battle_final_report
        battles_responses.append(battle_response)
    # for statistic see who winner victory
    for battle in battles_responses:
        if 'true' in battle:
            val_battles['wins_attacker'] += 1
        else:
            val_battles['wins_defender'] += 1
    # use this val_response to see the stats and a the actually army value for each player
    # val_response = val_battles.items(), battles_responses
    # default val_response
    val_response = battles_responses
    return HttpResponse(val_response, status=200, content_type='application/json')

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
            'unities': {"S": 6, "C": 15, "D": 30},
            "F": [1, 2, 3],
            "budget": 30}

    data_as_json = json.dumps(data)
    return HttpResponse(data_as_json, status=200, content_type='application/json')


def not_authenticated(request):
    return HttpResponse('not authorized: please sign in', status=401)
