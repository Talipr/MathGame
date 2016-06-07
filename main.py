import sqlite3
import random
import threading
import sys
import dbactions
import settings


def finish_game(name, level):
    """
    inserts player's name and score, and finishes the game.
    :param name: player's name
    :param level: player's score
    """
    db_connection = raise_database()
    dbactions.insert_new_score(name, level, db_connection)
    dbactions.show_high_scores(db_connection)
    resume_game = raw_input("Do you want to play again? press 1 for yes: ")
    if int(resume_game) == 1:
        main()
    else:
        print "game over"
        sys.exit(0)


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


def check_no_divide_problems(operation, first_num, second_num, level):
    """
    ensures that we would not divide by zero
    :param operation : our mathematical operation
    :param first_num : first random number
    :param second_num : second random number
    :param level: in case we need to generate new number
    :return: original number or a new one
    """
    if operation == '/':
        print "divide:", first_num % second_num
        print first_num
        print second_num
        while second_num == 0 or first_num % second_num != 0:
            first_num, second_num = get_random_numbers(level)
    return first_num, second_num


def lottery_numbers(level):
    """
    generates 2 numbers and sing and calculates result of the equation
    :param level: by the level it will be generated
    :return: equation to print to the user and its result
    """
    first_num, second_num = get_random_numbers(level)
    mathematical_sign = ['+', '-', '*', '/']
    operation = random.choice(mathematical_sign)
    first_num, second_num = check_no_divide_problems(operation, first_num, second_num, level)
    equation = str(first_num),operation.replace("'", ""),str(second_num)
    result = calculate_result(first_num, second_num, operation)
    return equation, result


def get_random_numbers(level):
    """
    generates random numbers by the level
    :param level
    :return: 2 generated numbers
    """
    range_start = 10 ** (level - 1)
    range_end = (10 ** level) - 1
    first_num = random.randint(range_start, range_end)
    second_num = random.randint(range_start, range_end)
    return first_num, second_num


def raise_database():
    """
    connect to the database of scores
    :return: db_connection
    """
    db_connection = sqlite3.connect(settings.db_path)
    dbactions.create_table(db_connection)
    return db_connection


def main():
    """
    the main function which active the game
    """
    name = raw_input("hello! please enter your name")
    level = 1
    answer = True
    while answer:
        t = threading.Timer(settings.timer_sec, finish_game, args=[name, level])
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
