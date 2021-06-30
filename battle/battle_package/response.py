from .request import Request
from .algorithm import BattleAlgo
import json


class Response:

    def __init__(self, result):
        self.response = Response.define_result(result)
    
    @staticmethod
    def define_result(result):
        json_response = {}
        for i in range(len(result)):
            if i == 0:
                json_response["winner"] = result[i]
            if i == 1:
                json_response["army"] = result[i]
            if i == 2:
                json_response["report"] = result[i]
        json_response = json.dumps(json_response)
        return json_response


# Main program
if __name__ == "__main__":
    inputFE = '{"attacker":{"type":"human",' \
              '"name":"player x",' \
              '"mail":"player@mail.com",' \
              '"army":{"B":5,"C":7,"D":1,"F":1},' \
              '"planet":"Venus"},' \
              '"defender":{"type":"virtual",' \
              '"name":"computer 1",' \
              '"army":{"B":4,"C":8,"D":9,"F":1},' \
              '"planet":"Mercury"}}'

    request = Request(inputFE)
    attacker = BattleAlgo.define_attack(request.request)
    defender = BattleAlgo.define_defender(request.request)
    battle_result = BattleAlgo.battle(attacker, defender)
    print(Response.define_result(battle_result))
