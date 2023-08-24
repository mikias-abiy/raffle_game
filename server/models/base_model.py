#!/usr/bin/python3
"""
base_model:
    This module contains the defination of the BaseModel class.
"""


import uuid
import models
from datetime import datetime


class BaseModel:
    """
    BaseModel: A model that all objects in this project inherit
               from. This object model contains all the common
               methods and attributes that all objects in this
               project share.

    This is a documentation for the constructor method of this Class.
    Args:
        None.
    """

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key in kwargs.keys():
                if key == "updated_at" or key == "created_at":
                    setattr(self, key, datetime.fromisoformat(kwargs[key]))
                elif key != "__class__":
                    setattr(self, key, kwargs[key])
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            # models.storage.new(self)

    def __str__(self):
        s = "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)
        return (s)

    def update(self, *args, **kwargs):
        if kwargs:
            for key in kwargs.keys():
                if key == "updated_at" or key == "created_at":
                    setattr(self, key, datetime.fromisoformat(kwargs[key]))
                elif key != "__class__":
                    setattr(self, key, kwargs[key])

    def save(self):
        """
        save: updates the the value of the instance attriubte updated_at
              to the current time.
        """
        # self.updated_at = datetime.now()
        # models.storage.save()
        pass

    def to_dict(self):
        """
        to_dict: return the dictionary represenation of an instance.

        Args:
            None

        Return:
            Dictionary represenation of an instance.
        """
        self_dict = self.__dict__.copy()
        self_dict["__class__"] = type(self).__name__
        self_dict["created_at"] = self_dict["created_at"].isoformat()
        self_dict["updated_at"] = self_dict["updated_at"].isoformat()
        to_remove = []
        for key, value in self_dict.items():
            if issubclass(type(value), BaseModel):
                to_remove.append(key)

        for key in to_remove:
            self_dict.pop(key)
        return (self_dict)
