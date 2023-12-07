from random import randrange


def generate_pin():
    return randrange(1000, 10000)


def is_otp_the_same(otp, compared):
    if otp == compared:
        return True;

    return False
