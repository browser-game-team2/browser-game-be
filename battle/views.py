from django.shortcuts import render
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

TEST_JSON = '{"winner":True,"army":{"S":0,"C":1,"D":2},"report":{1:{"a":3,"d":1},2:{"a":2,"d":1}}}'


def battle(request):
    #json_str = request.POST.get('data', '')
    return HttpResponse(TEST_JSON, status=200, content_type='application/json')


# the following (test) code is accessible only if the user is already logged in
# if the user is not logged in, they will be displayed an unauthorized message (401)
@login_required(login_url='/not_authenticated')
def choose(request):
    #print(request.user)  # getting the user in order to retrieve data from database

    # note: we can add code to retrieve token here
    # there will be a json instead of the following message
    return HttpResponse('I can see this because I am logged in', status=200)


def not_authenticated(request):
    return HttpResponse('not authorized: please sign in', status=401)


