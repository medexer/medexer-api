import re

validation_message = ""
regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")


def validate_donor_signup(data):
    global validation_message

    if not "fullName" in data or data["fullName"] == "":
        validation_message = "Full name is required"
        return False

    if not "email" in data or data["email"] == "":
        validation_message = "Email is required"
        return False

    if "email" in data or data["email"] != "":
        if not re.fullmatch(regex, data["email"].strip()):
            validation_message = "Invalid email address"
            return False

    if not "password" in data or data["password"] == "":
        validation_message = "Password is required"
        return False

    return True


def validate_donor_signin(data):
    global validation_message

    if not "email" in data or data["email"] == "":
        validation_message = "Email is required"
        return False

    if "email" in data or data["email"] != "":
        if not re.fullmatch(regex, data["email"].strip()):
            validation_message = "Invalid email address"
            return False

    if not "password" in data or data["password"] == "":
        validation_message = "Password is required"
        return False

    return True


def validate_donor_forgotpassword(data):
    global validation_message

    if not "email" in data or data["email"] == "":
        validation_message = "Email is required"
        return False

    if "email" in data or data["email"] != "":
        if not re.fullmatch(regex, data["email"].strip()):
            validation_message = "Invalid email address"
            return False

    return True


def validate_donor_resetpassword(data):
    global validation_message

    if not "otp" in data or data["otp"] == "":
        validation_message = "OTP is required"
        return False

    if not "newPassword" in data or data["newPassword"] == "":
        validation_message = "New password is required"
        return False

    return True


def validate_hospital_signup(data):
    global validation_message

    if not "hospitalName" in data or data["hospitalName"] == "":
        validation_message = "Hospital name is required"
        return False
    
    if not "location" in data or data["location"] == "":
        validation_message = "Hospital location is required"
        return False
    
    if not "email" in data or data["email"] == "":
        validation_message = "Hospital email is required"
        return False

    if "email" in data or data["email"] != "":
        if not re.fullmatch(regex, data["email"].strip()):
            validation_message = "Invalid email address"
            return False

    if not "password" in data or data["password"] == "":
        validation_message = "Password is required"
        return False

    return True



def validate_hospital_signin(data):
    global validation_message

    if not "hospitalID" in data or data["hospitalID"] == "":
        validation_message = "Hospital ID is required"
        return False

    if not "email" in data or data["email"] == "":
        validation_message = "Email is required"
        return False

    if "email" in data or data["email"] != "":
        if not re.fullmatch(regex, data["email"].strip()):
            validation_message = "Invalid email address"
            return False

    if not "password" in data or data["password"] == "":
        validation_message = "Password is required"
        return False

    return True
