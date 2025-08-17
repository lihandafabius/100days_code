import time


def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        #  do something before
        function()
        function()
        #  do something after
    return wrapper_function


@delay_decorator
def say_hello():
    print("hello")


@delay_decorator
def say_bye():
    print("bye")


def say_greeting():
    print("good bye")


# say_bye()
say_greeting()
say_hello()

decorated_function = delay_decorator(say_greeting)
decorated_function()
