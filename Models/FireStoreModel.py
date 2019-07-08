# coding: UTF-8
import os
import logging
from schematics.exceptions import DataError
from firebase_admin import firestore

class FireStoreModel:
    __collection:object
    __error:DataError

    def __init__(self, data=None):
        db = firestore.client()

        self.__collection = db.collection(self.__class__.__name__)
        self.__error = None

        # set all data
        self.set_all(data)

    def query(self):
        return self.__collection

    def save(self, data=None):
        self.set_all(data)

        self.__error = self.validation()
        if self.__error is not None:
            return False

        entity = self.__collection.document(self.id if hasattr(self, 'id') else None)

        data = {}
        for key in self._data:
            if key == 'id':
                continue
            data[key] = getattr(self, key)
        return entity.set(data)

    def validation(self):
        try:
            # schematics.validate()
            self.validate()
        except DataError as e:
            return e
        return None

    def set_all(self, data):
        if type(data) == dict:
            for key in data.keys():
                setattr(self, key, data[key])

    def get_errors(self):
        return self.__error
