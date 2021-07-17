import json


class Request:
    # We pass a string type parameter to our constructor method,
    # which will take care of returning a useful json
    def __init__(self, request_fe):
        self.challengers_armies = Request.define_challengers(request_fe)

    # The method takes a string parameter and defines a useful json to return to the battle algorithm
    @staticmethod
    def define_challengers(request_fe):
        challengers_dict = request_fe
        challengers_armies = {'attacker': challengers_dict['attacker']['army'],
                              'defender': challengers_dict['defender']['army']}
        return challengers_armies


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
    print(request.challengers_armies)
