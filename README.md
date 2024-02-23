# Google Authenticator in Python
Desktop Python Google Authenticator script with json secrets.

## How to
Install python3 and module

```sh
# Check
which python3

# Install
sudo apt install python3 python3-pyotp -y
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

# Show
print(code)

# Code verified for current time
print(x.verify(code)) # True

# time.sleep(35)
# print(x.verify(code))
```

## Links
- https://pyauth.github.io/pyotp/
- https://medium.com/@olutomilayodolapo/how-to-retrieve-otp-from-authy-google-authenticator-with-python-53544575bcef
- https://github.com/grahammitchell/google-authenticator/blob/master/google-authenticator.py
- https://www.geeksforgeeks.org/two-factor-authentication-using-google-authenticator-in-python/
