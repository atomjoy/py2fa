# Py2FA Google Authenticator in Python

Google Authenticator desktop GUI and script application in Python with JSON secrets.

## How to

Install python3 and modules

```sh
# Check
which python3

# Install
sudo apt install python3 python3-pyotp python3-tk -y
```

### Add secrets

First add your 2FA secrets to the **secrets.json** file (when enabling github two factor auth get secret key).

```json
{
  "atomjoy_github": "JBSWY3DPEHPK3PXP",
  "moovspace_github": "JBSWY3DPEHPK3PXD"
}
```

### Run script

The script generates 2fa codes for secrets.

```sh
# Gui desktop app tkinter
python3 main.py

# Console script
python3 auth.py

# Console script (30 seconds loop)
python3 2fa.py
```

### Output

```sh
Label atomjoy_github Secret JBSWY3DPEHPK3PXP Code 280070
Label moovspace_github Secret JBSWY3DPEHPK3PXD Code 304997
```

## Random secret base32

```py
#!/usr/bin/python3

import pyotp
import time

# Base32 secret
secret = pyotp.random_base32()

# Code from secret
x = pyotp.TOTP(secret)
code = x.now()

# Show
print(secret)
print(code)

# Code verified for current time
print(x.verify(code)) # True

# time.sleep(35)
# print(x.verify(code))
```

## Edit and copy PyF2A activator

For Linux Debian 12 Gnome 43+

```sh
# Edit this line change main.py file location
Exec=/bin/python3 /home/username/Dokumenty/github/py2fa-gui/main.py %u

# And copy app activator file to
cp py2fa.desktop /home/username/.local/share/applications
```

## Links

- <https://pyauth.github.io/pyotp/>
- <https://medium.com/@olutomilayodolapo/how-to-retrieve-otp-from-authy-google-authenticator-with-python-53544575bcef>
- <https://github.com/grahammitchell/google-authenticator/blob/master/google-authenticator.py>
- <https://www.geeksforgeeks.org/two-factor-authentication-using-google-authenticator-in-python>
- <https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html>
- <https://www.pythontutorial.net/tkinter/tkinter-treeview>
