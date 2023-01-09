# Access-Control-System
A Web App, which allow admins to manage the access of apps/services on user's side.

Controls/Features provided based on profile:
  The Administrator can control the access of applications of all the users. He can
give/revoke access to applications, and add/remove the users.

The User can access all the applications approved by the admin specifically for them.

If users want access to any other applications that they are not granted access to, they can
request their admin for access. After the admin approval, the user can access those
applications

This webapp runs on flask-based server...

You can access the project using it's live link: http://smtbhd32.pythonanywhere.com/

# You can run the server on your computer by following below steps:
1. Download the main folder as zip
2. Extract the zip
3. Install the dependencies... Python from it's website... Then flask using pip...
4. Open the cmd as Administrator
5. Change the directory to project directory using cd
6. Run the server using command: flask run

# Passwords for default accounts:
Admin = {
    "admin@gmail.com": "1234admin",
    }

User = {
    "aa@gmail.com": ["aa@gmail.com","aa"],
    "bb@gmail.com": ["bb@gmail.com","bb"],
    "cc@gmail.com": ["cc@gmail.com","cc"],
    }
