#! /usr/bin/env python
# -*- coding: utf-8 -*-


import json
import datetime
import decimal
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x.name for x in obj.__table__.columns]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:  # 添加了对datetime的处理
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.date):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.timedelta):
                        fields[field] = (datetime.datetime.min + data).time().isoformat()
                    elif isinstance(data, decimal.Decimal):
                        fields[field] = str(data)
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return int(obj.timestamp())
        elif isinstance(obj, datetime.date):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)


def sqlalchemy_serialize(data):
    return json.dumps(data, cls=AlchemyJsonEncoder)
