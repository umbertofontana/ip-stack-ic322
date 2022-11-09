class User:
    def __init__(self, username):
        privilege = {"president":3,"ops":2,"weapons":1}

        self.username = username
        self.privilege = privilege[username.lower()]
        
        