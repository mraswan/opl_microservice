class Address(object):

    def __init__(self, street, city, zip5, zip4, state):
        """Return a new Address object"""
        self.street = street
        self.city = city
        self.zip5 = zip5
        self.zip4 = zip4
        self.state = state