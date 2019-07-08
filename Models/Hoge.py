# coding: UTF-8

from schematics.models import Model
from schematics.types import IntType, StringType, EmailType, ListType
from Models.FireStoreModel import FireStoreModel

import logging

class Hoge(Model, FireStoreModel):
    id = StringType()
    user_id = StringType(required=True)
    email = EmailType(required=True)
    name = StringType(required=True, min_length=3, max_length=32)
    category = ListType(IntType(required=True))

    def __init__(self, data=None, trusted_data=None, deserialize_mapping=None, init=True, partial=True, strict=True, validate=False, app_data=None, lazy=False, **kwargs):

        FireStoreModel.__init__(self, data)

        Model.__init__(self, data, trusted_data, deserialize_mapping, init, partial, strict, validate, app_data, lazy=False, **kwargs)
