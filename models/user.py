#!/usr/bin/python3
"""Defines the User class."""
from models.base_model import BaseModel


class User(BaseModel):
    """Represent a User.

    Attributes:
        email (string): The email of the user.
        password (string): The password of the user.
        first_name (string): The first name of the user.
        last_name (string): The last name of the user.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
