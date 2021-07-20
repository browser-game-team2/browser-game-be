import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from authentication.authentication_package.auth_data import UserAuth  # check this import
from .battle_package.request import Request
from .battle_package.response import Response
from .battle_package.algorithm import Battle
from army.army_package.army import SpaceShip, SpaceCruiser, SpaceDestroyer
from army.army_package.army_for_test import generate_random_army
from django.views.decorators.csrf import csrf_exempt
import copy


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


def index(request):
    message = "Welcome! Go to --> https://browsergameteam2.herokuapp.com/accounts/google/login/"
    return HttpResponse(message, status=200)


# if the user is not logged in, they will be displayed an unauthorized message (401)
# @csrf_exempt
#@login_required(login_url='/not_authenticated')
def battle(request):
    """
    # in case FE temporarily does not send us the JSON (test code)
    army_attacker = Army()  # random generation (in production remove)
    army_defender = Army()  # random generation (in production remove)
    input_like_fe = Army.creation_input_like_fe(army_attacker, army_defender)  # in production remove
    battle_request = Request(input_like_fe)  # in production replace input_fe with json_str
    current_battle = Battle(battle_request)  # OBJ type Battle
   """
    if not (request.method == 'POST'):
        return HttpResponseBadRequest("Bad request")
    json_request = json.loads(request.body)
    #print(json_request)  # incoming request for the battle
    #print()
    if json_request["defender"]["army"] and json_request["attacker"]["army"]:
        # temporarily overwriting sent defender's army !
        random_defender_army = generate_random_army()
        initial_d_army = copy.deepcopy(random_defender_army)  # copied because it will be added to thi final json
        initial_a_army = copy.deepcopy(json_request["attacker"]["army"])
        json_request["defender"]["army"] = random_defender_army  # an army with an overall value of 30 is returned
        ##############################################
        print(json_request)  # updated battle request (the defender army is overwritten by BE)
        battle_request = Request(json_request)  # a dictionary is passed to the Request
        current_battle = Battle(battle_request)
        response = Response(current_battle)  # OBJ type Response
        battle_response = response.battle_final_report
        # temporarily adding the initial defender army inside the battle response
        battle_response_as_json = json.loads(battle_response)
        battle_response_as_json["init_d_army"] = initial_d_army  # initial defender army
        battle_response_as_json["init_a_army"] = initial_a_army  # initial attacker army
        battle_response_final = json.dumps(battle_response_as_json)
        print()
        print(battle_response)
        ##########################################################################
        return HttpResponse(battle_response_final, status=200, content_type='application/json')
    else:
        return HttpResponseBadRequest("Bad request")


def battle_temp(request):  # does not require login (useful for FE tests)
    """
    request = {"attacker":
              {"type":"Human",
              "username":"fake user",
              "army":
              {"S":1,"C":1,"D":1,"F":1},
              "planet":"Earth"},
              "defender":{"type":"virtual",
              "username":"Computer1",
              "army":{"S":3,"C":5,"D":5,"F":2},
              "planet":"Venus"},
              "token":"abcd.FAKETOKENnafk48598258gnfmn43849gnfureufjjurjru383574n3jkf"}

    request = '{"attacker":' \
              '{"type":"Human",' \
              '"username":"fake user",' \
              '"army":' \
              '{"S":1,"C":1,"D":1,"F":1},' \
              '"planet":"Earth"},' \
              '"defender":{"type":"virtual",' \
              '"username":"Computer1",' \
              '"army":{"S":3,"C":5,"D":5,"F":2},' \
              '"planet":"Venus"},' \
              '"token":"abcd.FAKETOKENnafk48598258gnfmn43849gnfureufjjurjru383574n3jkf"}'
    """

    if not (request.method == 'POST'):
        return HttpResponseBadRequest("Bad request")

    json_request = json.loads(request.body)
    battle_request = Request(json_request)
    current_battle = Battle(battle_request)
    response = Response(current_battle)  # OBJ type Response
    battle_response = response.battle_final_report
    return HttpResponse(battle_response, status=200, content_type='application/json')


# if the user is not logged in, they will be displayed an unauthorized message (401)
#@login_required(login_url='/not_authenticated')
def choose(request):
    print(request.headers)
    if not request.method == 'GET':
        return HttpResponseBadRequest("Bad request")
    ### test code ###
    data = {'username': 'fake user',
            'token': 'fake_142524523515fjgnjdgn',
            'prices': {'S': 5, 'C': 2, 'D': 1},
            "F": [1, 2, 3],
            'budget': 30,
            'planets': ['Earth', 'Jupiter', 'Mars', 'Mercury', 'Neptune', 'Saturn', 'Uranus', 'Venus']}
            #################
    data_as_json = json.dumps(data)
    return HttpResponse(data_as_json, status=200, content_type='application/json')

    user_auth = UserAuth(request)
    '''
    # print(request.user)
    # note: the request.user value is always unique! Thus it can be directly used to retrieve token from db
    '''
    data = {'username': user_auth.username,
            'token': user_auth.token,
            'uid': user_auth.uid,
            'prices': {"S": SpaceShip().price, "C": SpaceCruiser().price, "D": SpaceDestroyer().price},
            "F": [1, 2, 3],
            'budget': 30,
            'planets': ['Earth', 'Jupiter', 'Mars', 'Mercury', 'Neptune', 'Saturn', 'Uranus', 'Venus']
            }
    data_as_json = json.dumps(data)
    return HttpResponse(data_as_json, status=200, content_type='application/json')


def choose_temp(request):  # does not require login (useful for FE tests)
    data = {'username': "fake user",
            'token': "abcd.FAKETOKENnafk48598258gnfmn43849gnfureufjjurjru383574n3jkf",
            'prices': {"S": SpaceShip().price, "C": SpaceCruiser().price, "D": SpaceDestroyer().price},
            "F": [1, 2, 3],
            'budget': 30,
            'planets': ['Earth', 'Jupiter', 'Mars', 'Mercury', 'Neptune', 'Saturn', 'Uranus', 'Venus']
            }

    data_as_json = json.dumps(data)
    return HttpResponse(data_as_json, status=200, content_type='application/json')


def not_authenticated(request):
    return HttpResponse('not authorized: please sign in', status=401)
