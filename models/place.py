#!/usr/bin/python3
"""Defines the Place class."""

from models.base_model import BaseModel


class Place(BaseModel):
    """Represent a place.

    Attributes:
        city_id (string): The City id.
        user_id (string): The User id.
        name (string): The name of the place.
        description (string): The description of the place.
        number_rooms (integer): The number of rooms of the place.
        number_bathrooms (integer): The number of bathrooms of the place.
        max_guest (integer): The maximum number of guests of the place.
        price_by_night (integer): The price by night of the place.
        latitude (float): The altitude of the place.
        longitude (float): The longitude of the place.
        amenity_ids (list): A list of Amenity ids.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
