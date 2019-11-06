from unittest import TestCase
from unittest.mock import Mock
from faker import Faker
faker = Faker()

from auth.hashgenerator import HashGenerator
from auth.hashmatcher import HashMatcher

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
