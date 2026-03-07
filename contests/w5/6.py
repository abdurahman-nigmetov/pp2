import re

txt = input()
email = re.search('\S+@+\S+[.]+\S+', txt)
if email:
    print(txt[email.start():email.end()])
else:
    print("No email")