import os
from .id_generator import kyc_document_id_generator, kyb_document_id_generator, avatar_id_generator


def avatar_path(model, file):
    class_name = "images"
    code = "profile"
    filename = avatar_id_generator() + "." + file.split(".")[1]
    return os.path.join(class_name, code, filename)

def kyc_document_path(model, file):
    class_name = "images"
    code = "kyc"
    filename = kyc_document_id_generator() + "." + file.split(".")[1]
    return os.path.join(class_name, code, filename)


def kyb_document_path(model, file):
    class_name = "images"
    code = "kyb"
    filename = kyb_document_id_generator() + "." + file.split(".")[1]
    return os.path.join(class_name, code, filename)
