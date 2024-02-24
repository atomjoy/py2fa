#!/usr/bin/python3

import pyotp, time, json, os, shutil, base64, sys


class JsonFile:
    data = []
    data_code = []
    filename = ""

    def __init__(self, filename="secrets.json"):
        self.data = []
        self.data_code = []
        self.filename = filename
        self.__loadJson()
        self.__updateCode()
        self.scriptPath()

    def scriptPath(self):
        print(os.path.dirname(os.path.realpath(sys.argv[0])))

    def getAll(self):
        return self.data_code

    def getAllData(self):
        return self.data

    def loadJson(self):
        try:
            rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            with open(os.path.join(rel, self.filename), "r") as f:
                secrets = json.load(f)
                self.data = list(secrets.items())
                print("Loaded", self.data)
        except (ImportError, Exception):
            print("Load error")

    def addItem(self, name, secret):
        if len(name) >= 3:
            if len(secret) >= 16:
                if self.isBase32(secret):
                    item = tuple([name, secret])
                    self.data.append(item)
                    self.__updateCode()
                    self.saveJson()
                    # print("Appended", self.data)

    def updateCode(self):
        self.data_code = []
        for tuple_val in self.data:
            item = list(tuple_val)
            item.append(self.otpCode(str(item[1])))
            self.data_code.append(tuple(item))

    def otpCode(self, secret):
        try:
            return pyotp.TOTP(secret).now()
        except Exception:
            print("Otp code error")
        return "000000"

    def saveJson(self):
        json_obj = {}
        for key, secret in self.data:
            json_obj[key] = secret
        try:
            self.backupFile()
            rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            with open(os.path.join(rel, self.filename), "w") as outfile:
                json.dump(json_obj, outfile)
                # print("Saved json", json_obj)
        except (ImportError, Exception):
            print("Save error")

    def backupFile(self):
        tm = str(time.time()).replace(".", "_")
        shutil.copy(self.filename, "backup/secrets_copy_" + tm + ".json")

    def isBase32(self, str):
        try:
            base64.b32decode(str)
            return True
        except Exception:
            print("Invalid base32:", str)
            return False

    def removeItem(self, name):
        if len(name) >= 3:
            res = [i for i in self.data if i[0] != name]
            self.data = res
            self.saveJson()
            # print(res)

    def showPaths(self):
        print(sys.path[0])
        print(os.path.realpath(__file__))
        print(os.path.dirname(__file__))
        print(os.getcwd())
        print(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        print(os.path.dirname(os.path.realpath(__file__)))
        print(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))))

    __loadJson = loadJson  # private copy of original update() method
    __updateCode = updateCode  # private copy of original update() method
