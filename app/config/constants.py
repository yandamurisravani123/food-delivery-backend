from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    CUSTOMER = "customer"
    DRIVER = "driver"
    RESTAURANT = "restaurant"


class TokenType(str, Enum):
    ACCESS = "access"
