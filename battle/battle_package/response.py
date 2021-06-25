from request import Request
from algorithm import BattleAlgo

import json

class Response:
    def __int__(self, result):
        self.response = Response.defineResult(result)
    
    @staticmethod
    def defineResult(result):
        jsonresponse = {}
        for i in range(len(result)):
            if i == 0:
                jsonresponse["winner"] = result[i]
            if i == 1:
                army = result[i]
                jsonresponse["army"] = result[i]
            if i == 2:
                jsonresponse["report"] = result[i]
        jsonresponse = json.dumps(jsonresponse)
        return jsonresponse


if __name__ == "__main__":
    inputFE = '{"attacker":{"type":"human","name":"player x","mail":"player@mail.com","army":{"B":5,"C":7,"D":1,"F":1},\
    	    "planet":"Venus"},"defender":{"type":"virtual","name":"computer 1","army":{"B":4,"C":8,"D":9,"F":1},"planet":"Mercury"}}'

    request = Request.defineBattle(inputFE)
    at = BattleAlgo.defineAttack(request)
    de = BattleAlgo.defineDefender(request)
    result = BattleAlgo.battle(at, de)
    print(Response.defineResult(result))

