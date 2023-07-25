from datetime import datetime

class utils ():
    def __init__(self) -> None:
        pass
    
    def emailCheck(email):
        # Checks if the email is an @
        # and checks if it has a .
        # if not, return invalid
        # otherwise return good

        validations = (
            (lambda s: "@" in s, "Email is invalid"),
            (lambda s: "." in s, "Email is invalid"),
        )

        for valid, message in validations:
            if not valid(email):
                return message

        return "good"
    
    def nameCheck(fname, lname):
        if len(fname) == 0 or len(lname) == 0:
            return "Name was not entered"

        return "good"
    
    def IDCheck(user_id):
        if len(user_id) <= 2:
            return "PID was not entered"
        return "good"
    
    def IDVet(id_check):
        for c in id_check:
            if c == "+":
                return "bad"

        if "\r" in id_check:
            return "bad"

        if len(id_check) > 0:
            if id_check[0] == "?":
                return "bad"

        if id_check.isalpha():
            return "bad"

        return "good"
    
    def getDatetime():
        return datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")