from datetime import datetime

from app import db
from flask import request
from flask_restful import Resource
from models import SensorDataModel


class SensorData(Resource):
    def get(self):
        args = list(dict(request.args).items())

        try:
            sensor_request = self.parse_request(args)

            s = SensorDataModel(**sensor_request)
            db.session.add(s)
            db.session.commit()

            return 'data stored', 200

        except:
            return 'bad request', 400

    def parse_request(self, args):
        sensor_request = {}
        i = 0

        while i < len(args):
            key = args[i][0]
            value = args[i][1]
            key = key[2:-1]

            if key[0] == 'v' and key[-1] == 't':
                sensor_request[value] = args[i + 1][1]
                i += 1
            else:
                sensor_request[key] = value

            i += 1

        sensor_request['internal_id'] = sensor_request['id']
        sensor_request['recorded'] = datetime.strptime(
            sensor_request['date'], '%Y%m%d%H%M%S')

        del sensor_request['id']
        del sensor_request['date']

        return sensor_request
