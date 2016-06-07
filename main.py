import sqlite3
import random
import threading
import os
import dbActions
import Settings


def finish_game(name, level):
    """
    inserts player's name and score, and finishes the game.
    :param name: player's name
    :param level: player's score
    """
    con = raise_database()
    dbActions.insert_new_score(name, level, con, Settings.db_table_name)
    print "game over"
    os._exit(1)


def calculate_result(first_num, second_num, operation):
    """
    calculates equation result
    :param first_num
    :param second_num
    :param operation
    :return: math result
    """
    if operation == '/':
        return first_num / second_num
    elif operation == '*':
        return first_num * second_num
    elif operation == '+':
        return first_num + second_num
    elif operation == '-':
        return first_num - second_num


def check_no_zero(operation, second_num, level):
    """
    ensures that we would not divide by zero
    :param operation
    :param second_num
    :param level: in case we need to generate new number
    :return: original number or a new one
    """
    if operation == '/':
        while second_num == 0:
            second_num = get_random_num(level)
    return second_num


def lottery_numbers(level):
    """
    generates 2 numbers and sing and calculates result of the equation
    :param level: by the level it will be generated
    :return: equation to print to the user and its result
    """
    first_num = get_random_num(level)
    second_num = get_random_num(level)
    mathematical_sign = ['+', '-', '*', '/']
    operation = random.choice(mathematical_sign)
    second_num = check_no_zero(operation, second_num, level)
    equation = str(first_num),operation.replace("'", ""),str(second_num)
    result = calculate_result(first_num, second_num, operation)
    return equation, result


def get_random_num(level):
    """
    generates random number by the level
    :param level
    :return: generated number
    """
    range_start = 10 ** (level - 1)
    range_end = (10 ** level) - 1
    return random.randint(range_start, range_end)


def raise_database():
    """
    connect to the database of scores
    :return: con
    """
    con = sqlite3.connect(Settings.db_path)
    dbActions.create_table(con)
    return con


def main():
    """
    the main function which active the game
    """
    print "hello! please enter your name"
    name = raw_input()
    level = 1;
    answer = True;
    while answer:
        t = threading.Timer(5.0, finish_game, args=[name, level])
        equation, result = lottery_numbers(level)
        t.start()
        print "please enter next equation:", ''.join(equation)
        equation_answer = raw_input()
        t.cancel()
        if int(equation_answer) == result:
            print "your answer was good! next level!"
            level += 1
        else:
            finish_game(name, level)


if __name__ == "__main__":
    main()
