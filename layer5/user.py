import hashlib
import user

class User:
    def __init__(self, username):
        privilege = {"president":3,"ops":2,"weapons":1}
        port = {"president":0,"ops":1,"weapons":2}

        self.username = username
        self.privilege = privilege[username.lower()]
        self.port = port[username.lower()]
    
    def passCheck(self, password):
        #president = password
        #ops = gonavy
        #weapons = italy
        hashPass = hashlib.md5(password.encode())
        hashPass = hashPass.hexdigest()
        PasswordDict = {"president":"5f4dcc3b5aa765d61d8327deb882cf99","ops":"3281691b3f4309c331c1e2e44e83e965","weapons":"bab4ac375adad13f5693f24fceab7903"}
        print(hashPass)
        print(PasswordDict["president"])
        return (PassowrdDict[self.username] == hashPass)


    def main():
        test = user.User('president')
        password = "password"
        print("password = " + password)
        print(test.passCheck(password))

    if __name__ == "__main__":
        main()
