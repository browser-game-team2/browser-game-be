import json

class RequestFe:
    #We pass a string type parameter to our constructor method, which will take care of returning a useful json
    def __init__(self, strFE):
        self.request = RequestFe.defineBattle(strFE)

    @staticmethod
    def defineBattle(strFE):
        report = json.loads(strFE)
        jsonbattle = {}
        for key, value in report.items():
            if key == 'attacker':
                for value in report[key]:
                    if value == "army":
                        jsonbattle["at"] = dict(report[key][value])
            elif key == 'defender':
                for value in report[key]:
                    if value == "army":
                        jsonbattle["de"] = dict(report[key][value])
        return jsonbattle

    def test(self):
        return self.request


#test
if __name__ == "__main__":
    inputFE = '{"attacker":{"type":"human","name":"player x","mail":"player@mail.com","army":{"B":5,"C":7,"D":9,"F":1},\
    "planet":"Venus"},"defender":{"type":"virtual","name":"computer 1","army":{"B":4,"C":8,"D":9,"F":1},"planet":"Mercury"}}'
    
    request = RequestFe(inputFE)
    print(RequestFe.test(request))
    