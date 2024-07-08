import random
import string


class HelperRandom:
    @classmethod
    def get_str(cls):
        return ''.join(random.choices(string.ascii_lowercase, k=5))

    @classmethod
    def get_full_name(cls):
        return f'{cls.get_str()} {cls.get_str()}'

    @classmethod
    def get_email_address(cls):
        return f'{cls.get_str()}@{cls.get_str()}.com'
