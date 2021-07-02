from .request import Request
from .algorithm import Battle
import json


class Response:

    def __init__(self, current_battle):
        self.battle_final_report = Response.json_response(current_battle.final_report)
    
    @staticmethod
    def json_response(final_report):
        """
        json_response = {}
        for i in range(len(result)):
            print(i)
            if i == 0:
                json_response["winner"] = result[i]
            if i == 1:
                json_response["army"] = result[i]
            if i == 2:
                json_response["report"] = result[i]
            print(json_response)
        """
        return json.dumps(final_report)


# Main program
if __name__ == "__main__":
    inputFE = '{"attacker":{"type":"human",' \
              '"name":"player x",' \
              '"mail":"player@mail.com",' \
              '"army":{"S":5,"C":7,"D":1,"F":1},' \
              '"planet":"Venus"},' \
              '"defender":{"type":"virtual",' \
              '"name":"computer 1",' \
              '"army":{"S":4,"C":8,"D":9,"F":1},' \
              '"planet":"Mercury"}}'

    request = Request(inputFE)
    battle = Battle(request)
    battle_result = battle.final_report
    print(battle_result)
