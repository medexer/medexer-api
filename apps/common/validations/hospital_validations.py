validation_message = ""


def validate_generate_complaint(data):
    global validation_message

    if not "title" in data or data["title"] == "":
        validation_message = "Title is required"
        return False

    if not "message" in data or data["message"] == "":
        validation_message = "Message is required"
        return False


    return True
