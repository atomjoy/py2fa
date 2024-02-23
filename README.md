# Google Authenticator in Python
Desktop Python Google Authenticator script with json secrets.

## How to
Install python3 and module

```sh
sudo apt install python3
sudo apt install python3-pyotp -y
```

### Run script
First add your 2FA secrets to the secrets.json file (when enabling github two factor auth get secret hash). The script generates 2fa codes for secrets.

```sh
python3 auth.py
```

### Output

```sh
Label atomjoy_github Secret JBSWY3DPEHPK3PXP Code 280070
Label moovspace_github Secret JBSWY3DPEHPK3PXD Code 304997
```

## Random secret base32

```py
import pyotp
import time

# Base32 secret
secret = pyotp.random_base32()

# Code from secret
x = pyotp.TOTP(secret)
code = x.now()

print(secret)
print(code)
```

## Links
- https://pyauth.github.io/pyotp/
- https://medium.com/@olutomilayodolapo/how-to-retrieve-otp-from-authy-google-authenticator-with-python-53544575bcef
- https://github.com/grahammitchell/google-authenticator/blob/master/google-authenticator.py
- https://www.geeksforgeeks.org/two-factor-authentication-using-google-authenticator-in-python/
