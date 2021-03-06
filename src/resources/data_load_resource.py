from flask import request, jsonify, json
from flask_restful import  Resource
from flask_jwt import jwt_required, current_identity
from flasgger import swag_from

from services.data_load_service import DataLoadService
from utils.util import model_to_dict

class DataLoadResource (Resource):

    data_load_service = DataLoadService()

    @jwt_required()
    @swag_from('../../spec/data_load/entity.yml')
    def get(self):
        try:
            self.data_load_service.session_info = current_identity
            code = request.args.get('code')
            key = request.args.get('key')
            param = request.args.get('param')
            res_data = eval("self.data_load_service.{}".format(code+"(key, param)"))
            res_json = {'status': 1, 'data': res_data}
        except Exception as e:
            print(e)
            if e.args:
                res_data = e.args[0]
            else:
                res_data = e
            res_json = {'status': 0, 'error': res_data}

        return jsonify(res_json)