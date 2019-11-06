import bycrpt

class HashMatcher:
    def __init__(self, plaintext, hash):
        self.plaintext = plaintext
        self.hash = hash

    def is_matched(self):
        plaintext_bytes = self.plaintext.encode()
        return bcrypt.checkpw(plaintext_bytes, self.hash)
