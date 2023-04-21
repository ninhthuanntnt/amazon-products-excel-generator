import random
import string
import uuid

class RandomUtil:
    @classmethod
    def random_digits(self, number_of_digits):
        return str(uuid.uuid4().int)[0:number_of_digits]

    @classmethod
    def random_string(self, number_of_characters):
        letters = string.ascii_uppercase
        return ''.join(random.choice(letters) for i in range(number_of_characters))