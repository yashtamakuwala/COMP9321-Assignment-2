from unittest import TestCase
from faker import Faker
faker = Faker()

from tahelka.auth.hash_generator import HashGenerator
from tahelka.auth.hash_matcher import HashMatcher

class TestHashing(TestCase):
    def test_matched(self):
        plaintext = faker.sentence()

        generator = HashGenerator(plaintext)
        hash = generator.generate()

        matcher = HashMatcher(plaintext, hash)
        self.assertTrue(matcher.is_matched())

    def test_not_matched(self):
        plaintext = faker.sentence()

        generator = HashGenerator(plaintext)
        hash = generator.generate()

        matcher = HashMatcher(f'{plaintext}{faker.word()}', hash)
        self.assertFalse(matcher.is_matched())
