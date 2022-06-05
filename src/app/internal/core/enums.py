from enum import Enum


class ServiceEnum(Enum):
    CODE_NOT_EXIST = "Code isn't exist"
    CODE_IS_USED = "Code is used"
    CATEGORY_NOT_EXIST = "Category isn't exist"
    PARENT_NOT_EXIST = "Parent isn't exist"
    USER_IS_EXIST = "User already exists"
    USER_NOT_EXIST = "User isn't exist"
    BUSINESS_NOT_EXIST = "Business isn't exist"
    FORBIDDEN = "Forbidden"
    CREATED = "Instance is created"
    NOT_CREATED = "Instance isn't created"
    WRONG_FILE = "File is wrong"
    LOGIN = "Success login"
    SUCCESS = "Success"
    SOME_ERROR = "Some error"
