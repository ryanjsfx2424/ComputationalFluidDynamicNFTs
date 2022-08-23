import pyotp
import qrcode
key = pyotp.random_base32()
totp = pyotp.TOTP(key)

auth_str = totp.provisioning_uri(name="discid1234", issuer_name="Dauthy")

img = qrcode.make(auth_str)
img.save("Test.png")
