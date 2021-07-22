import random


def generate_random_army():  # returns random combinations of troups with a value of 30
    s_price = 5
    c_price = 2
    d_price = 1
    budget = 30
    # type of troups are S,C,D
    # at least one per each type is needed
    s = random.choice([1, 2, 3, 4, 5])
    if s == 5:  # note that maximum s type troups is 5 since 6*2_price = 30 and there would be no budget left
        c = random.choice([1, 2])
    elif s == 4:
        c = random.choice([1, 2, 3, 4])
    elif s == 3:
        c = random.choice([1, 2, 3, 4, 5, 6, 7])
    elif s == 2:
        c = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    elif s == 1:
        c = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    d = budget - (s * s_price + c * c_price)  # the rest of the budget is spent for d type troups

    f = random.choice([1, 2, 3])  # strategy

    army = {"S": s, "C": c, "D": d, "F": f}
    return army


if __name__ == '__main__':
    print(generate_random_army())

