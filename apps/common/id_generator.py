import random


def donor_id_generator():
    characters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    length = 10

    _id = "MED-DNR-"

    for _ in range(length):
        _id += random.choice(characters)

    return _id


def hospital_id_generator():
    characters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    length = 10

    _id = "MED-HSL-"

    for _ in range(length):
        _id += random.choice(characters)

    return _id


def otp_id_generator():
    characters = list("0123456789")

    length = 6

    otp = ""

    for _ in range(length):
        otp += random.choice(characters)

    return otp


def kyc_document_id_generator():
    characters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    length = 10

    _id = "MED-KYC-"

    for _ in range(length):
        _id += random.choice(characters)

    return _id


def kyb_document_id_generator():
    characters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    length = 10

    _id = "MED-KYB-"

    for _ in range(length):
        _id += random.choice(characters)

    return _id


def complaint_id_generator():
    characters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    length = 8

    _id = "CPT-"

    for _ in range(length):
        _id += random.choice(characters)

    return _id
