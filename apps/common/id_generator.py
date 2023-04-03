import random


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
