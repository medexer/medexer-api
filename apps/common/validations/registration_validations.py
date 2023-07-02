validation_message = ''

WHITELISTED_IMAGE_TYPES = {
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'png': 'image/png'
}

def validate_donor_kyc_capture(data, files):
    global validation_message
    

    if not "bloodGroup" in data or data["bloodGroup"] == "":
        validation_message = "Blood group is required"
        return False

    if not "genotype" in data or data["genotype"] == "":
        validation_message = "Genotype is required"
        return False

    if not "identificationType" in data or data["identificationType"] == "":
        validation_message = "Identification type is required"
        return False

    if len(files) == 0:
        validation_message = "Document upload files are required (.jpg, jpeg, .png)"
        return False

    if len(files) > 0 and not "documentUploadCover" in files:
        validation_message = "Document cover is required (.jpg, jpeg, .png)"
        return False

    if len(files) > 0 and not "documentUploadRear" in files:
        validation_message = "Document rear is required (.jpg, jpeg, .png)"
        return False

    if len(files) > 0 and "documentUploadCover" in files:
        extension = files['documentUploadCover'].name.split('.')[-1]
        if not extension or extension.lower() not in WHITELISTED_IMAGE_TYPES.keys():
            validation_message = "Invalid document cover upload type, upload (.jpg, .jpeg, .png)"
            return False

    if len(files) > 0 and "documentUploadRear" in files:
        extension = files['documentUploadRear'].name.split('.')[-1]
        if not extension or extension.lower() not in WHITELISTED_IMAGE_TYPES.keys():
            validation_message = "Invalid document rear upload type, upload (.jpg, .jpeg, .png)"
            return False

    return True


def validate_hospital_kyb_capture(data, files):
    global validation_message

    if not "cacRegistrationID" in data or data["cacRegistrationID"] == "":
        validation_message = "CAC registration ID is required"
        return False

    if not "address" in data or data["address"] == "":
        validation_message = "Address is required"
        return False

    if not "description" in data or data["description"] == "":
        validation_message = "Address is required"
        return False
    
    if len(files) == 0:
        validation_message = "Hospital image is required (.jpg, jpeg, .png)"
        return False

    if len(files) > 0 and not "hospitalImage" in files:
        validation_message = "Hospital image is required (.jpg, jpeg, .png)"
        return False

    if len(files) > 0 and "hospitalImage" in files:
        extension = files['hospitalImage'].name.split('.')[-1]
        if not extension or extension.lower() not in WHITELISTED_IMAGE_TYPES.keys():
            validation_message = "Invalid logo upload type, upload (.jpg, .jpeg, .png)"
            return False

    return True
