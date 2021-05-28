from django.shortcuts import render
import json
from django.http import HttpResponse

TEST_JSON = '{"winner":True,"army":{"S":0,"C":1,"D":2},"report":{1:{"a":3,"d":1},2:{"a":2,"d":1}}}'


def battle(request):
    #json_str = request.POST.get('data', '')
    return HttpResponse(TEST_JSON, status=200, content_type='application/json')



