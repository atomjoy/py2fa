#!/usr/bin/python

# Install
# sudo apt install python3-pyotp -y

import pyotp
import time
import json, os

def main():
        rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(rel,'secrets.json'), 'r') as f:
                secrets = json.load(f)
        for label, key in sorted(list(secrets.items())):
                code = pyotp.TOTP(key).now()
                print("Label {} Secret {} Code {}".format(label, key, code))

if __name__ == "__main__":
    main()
