# First Project. Building a simple set of functions that should be able to take in user input and save that information to a file.
# The user should also be able to read the file and see the information that they have saved.



from datetime import datetime
import re
import csv  
import os
import bcrypt


datafile = "data.csv"   # Name of the csv file of which locally will store all the data needed in the program generated by user inputs.               


def firstname ():   # Function that requires user to input their first name with at least 3 characters and make that name case insensitive. Also strips all whitespace.
    
    try:
        while True:
                ask = input ("Please enter your first name: ").strip().lower()
                if len(ask) > 2:
                    return True, ask
                else:
                    print ("Please enter a valid first name. A minimum of 3 characters are required.")
    except Exception as e:
        print (f"An error occurred {e}")
        return False, None    


def lastname ():    # Function that requires user to input their last name with at least 3 characters and make that name case insensitive. Also strips all whitespace.    
    
    try:
        while True:
            ask = input ("Please enter your last name: ").strip().lower()
            if len(ask) > 2:
                return True, ask
            else:
                print ("Please enter a valid last name. A minimum of 3 characters are required.")
    except Exception as e:
        print (f"An error occurred {e}")
        return False, None  


def ValidDoB ():    # Function that requires user to input their date of birth in a specific format. If that condition is not met, the loop continues until True.
    while True:
        try:
            dob = input ("Please enter a valid Date of Birth using the format dd/mm/yyyy: ")
            datetime.strptime(dob,"%d/%m/%Y") 
            day, month, year = dob.split("/")
            day = int(day)
            month = int(month)
            if day < 1 or day > 31:
                print ("Please enter a valid date of birth.")
            if month < 1 or month > 12:
                print ("Please enter a valid date of birth.")
            else:
                return dob
        except ValueError as ve:
            print (f"There has been an error {ve}")


def username(): # Function that requires user to input their desired username however false is returned if there are special characters and the username is more than 15 characters.
    try:
        while True:
            user = input("Please enter a username: ")
            if not user:
                print("Username cannot be empty. Please try again.")
            elif len(user) < 3:
                print ("Your username is less than 3 characters. Please try again.") 
                continue
            elif len(user) > 15:
                print ("Your username is more than 15 characters long. Please try again.")
                continue
            elif re.search(r"[^\w]",user):
                print ("Your username cannot contain any special characters. Please try again.")
                continue
            
            try:
                with open (datafile, "r") as file:
                    reader = csv.reader(file)
    
                    for row in reader:
                        if row:
                            existing_username = row[3]
                            if user.lower() == existing_username.lower():
                                print ("Sorry your username is taken. Please use another.")
                                break
                    else:
                        print ("Your username is valid. It has been added to the record. Thank you.")
                        return True, user
            except FileNotFoundError:
                print (f"New User")
                return True, user
    except Exception as e:
        print ("There seems to be an error {e}")
        return False, None




def password ():    # Function that requires the user to input their desired password from 3 to 10 characters long only.
    try:
        while True:
            salt = bcrypt.gensalt()
            password = input ("Please enter a password: ")
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            if not password:
                print ("You entered an empty password, Please try again.")
            elif len(password) < 3:
                print ("Your password is less than 3 characters. Please try again.")
                continue
            elif len(password) > 10:
                print ("Your password is more than 10 characters. Please try again.")
                continue
            print ("You entered a valid password. Thank you for creating your record.")
            return True, hashed_password
    except Exception as e:
        print (f"There was an error in the password function: {e}")
        return False, None      

def email ():   # Function that takes input from the users email address.
    try:
        while True:
            email = input ("Please enter a valid email address: ")
            if not email:
                print ("Your email is invalid. Please try again")
            elif re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                while True:
                    email2 = input ("Please confirm your email: ")
                    if email2 == email:
                        return True, email
                    else:
                        print ("Emails do not match.")
                else: ("Your email is invalid. Please try again")
    except Exception as e:
        print (f"There was an error in the email function {e}")
        return False, None      

def login_user (username, password):    # Function that checks a username and password against each other to return True.
    try:
        with open(datafile, "r") as file:
            reader = csv.reader(file)

            for row in reader:
                if row:
                    saved_username = row[3]
                    saved_password = row[4]
                    if isinstance(saved_password, str):
                        saved_password = saved_password.encode('utf-8')
                    if isinstance(password, str):
                        password = password.encode('utf-8')    
                    if saved_username.lower() == username.lower() and bcrypt.checkpw(password, saved_password):
                        return True
        return False

    except Exception as e:
        print(f"Error occurred in the valid login function {e}")   

def user_login ():
    login_username = input ("Please enter your username: ")
    login_password = input ("Please enter your password: ")
    login_success = login_user(login_user, login_password)
    if login_success:
        print ("Login Successful")
    else:
        print("Login Failed") 

def user_registration ():    # Function that pieces together the main workflow of the program after the functions before are written.
    valid_fname, first_name = firstname()
    if valid_fname:
        valid_lname, last_name = lastname()
        if valid_lname:
            dob = ValidDoB()
            if dob:
                valid_username, user_name = username()
                if valid_username:
                    valid_password, pass_word = password()
                    if valid_password:
                        valid_email, e_mail = email()
                        if valid_email:
                            WriteToFile(first_name, last_name, dob, user_name, pass_word, e_mail, datafile)
                            print ("User registration successful!")   
                        else:
                            print ("Your email is invalid")    
                    else:
                        print ("Your password is invalid")    
                else:
                    print ("Your username is invalid")
            else:
                print ("Please enter a valid Date of Birth with the correct format YYYY-MM-DD ")
        else:
            print ("Please enter a valid last name. A minimum of 3 characters are required. ")
    else:
        print ("Please enter a valid first name. A minimum of 3 characters are required. ")
                
                
def main ():
    while True:
        action = input ("Choose an action:\n1. Register\n2. Login\n3. Exit")
        if action == "1":
            user_registration()
        elif action == "2":
            user_login()
        elif action == "3":
            print ("Exiting")
            break    
        else:
            print ("Invalid choice. Please try again.")


def WriteToFile(firstname, lastname, dob, username, password, email, datafile):  # 
    try:
        file_exists = os.path.exists(datafile) and os.stat(datafile).st_size > 0
    
        with open(datafile, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                headers = ["First Name", "Last Name", "Date of Birth", "Username", "Password", "Email"]
                writer.writerow(headers)
            writer.writerow([firstname, lastname, dob, username, password.decode('utf-8'), email])
            print("Data written to the Data file successfully.")
    
    except Exception as e:
        print(f"There was an error: {e}")

if __name__ == "__main__":
    main()

  






