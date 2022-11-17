class User:
    def __init__(self, username):
        privilege = {"president":3,"ops":2,"weapons":1}
        port = {"president":0,"ops":1,"weapons":2}

        self.username = username
        self.privilege = privilege[username.lower()]
        self.port = port[username.lower()]
        
        
