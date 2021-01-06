def removeKey(self, old, key):
    new = dict(old)
    del new[key]
    return new