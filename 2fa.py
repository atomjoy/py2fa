#!/usr/bin/python

# Install
# sudo apt install python3 python3-pyotp -y

import time, json, os
import pyotp

def main():
        while True:
                rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
                with open(os.path.join(rel,'secrets.json'), 'r') as f:
                        secrets = json.load(f)
                for label, key in sorted(list(secrets.items())):
                        code = pyotp.TOTP(key).now()
                        print("Label {} Secret {} Code {}".format(label, key, code))
                time.sleep(30)

if __name__ == "__main__":
        main()
