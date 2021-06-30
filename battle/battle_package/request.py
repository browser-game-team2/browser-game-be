import json


class Request:
    # We pass a string type parameter to our constructor method,
    # which will take care of returning a useful json
    def __init__(self, str_fe):
        self.request = Request.define_battle(str_fe)

    # The method takes a string parameter and defines a useful json to return to the battle algorithm
    @staticmethod
    def define_battle(str_fe):
        report = json.loads(str_fe)
        # print(type(report))
        json_battle = {}
        for key in report:          # check: during refactoring removed items method
            if key == 'attacker':
                for value in report[key]:
                    if value == "army":
                        json_battle["attacker"] = dict(report[key][value])
            elif key == 'defender':
                for value in report[key]:
                    if value == "army":
                        json_battle["defender"] = dict(report[key][value])
        return json_battle

    def test(self):
        return self.request


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
    print(Request.test(request))
