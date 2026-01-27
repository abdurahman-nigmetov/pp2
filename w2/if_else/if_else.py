a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

number = 7

if number % 2 == 0:
  print("The number is even")
else:
  print("The number is odd")

username = "Emil"

if len(username) > 0:
  print(f"Welcome, {username}!")
else:
  print("Error: Username cannot be empty")

username = "Tobias"
password = "secret123"
is_verified = True

if username and password and is_verified:
  print("Login successful")
else:
  print("Login failed")

score = 85

if score >= 0 and score <= 100:
  print("Valid score")
else:
  print("Invalid score")