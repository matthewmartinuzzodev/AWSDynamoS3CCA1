import json

data = []

email = "s3850470@student.rmit.edu.au"
user_name = "Matthew Martinuzzo0"
password = "012345"

for i in range(10):
    entry = {
        "email": email,
        "user_name": user_name,
        "password": password
    }
    data.append(entry)
    
    # Increment email, user_name, and password for the next entry
    email = email.replace(email[:8], "s" + str(int(email[1:8]) + 1))
    user_name = user_name.replace(user_name[-1], str(int(user_name[-1]) + 1))
    if (int(password[-1]) + 1 == 10):
        password = password[1:] + '0'
    
    else:
        password = password[1:] + str(int(password[-1]) + 1)
    

json_data = json.dumps(data, indent=4)

with open("login_data.json", "w") as file:
    file.write(json_data)