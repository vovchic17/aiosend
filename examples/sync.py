from aiosend import CryptoPay

cp = CryptoPay("TOKEN")
app = cp.get_me()
print(app.name)  # Your App Name
