class Registry(object):
    def __init__(self):
        self.registry = {}

    def set(self, key, value):
        self.registry[key] = value
        return self

    def get(self, key):
        if key in self.registry:
            return self.registry[key]
        return None
