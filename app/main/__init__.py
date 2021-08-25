# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/06/27
from flask import Blueprint
from flask import jsonify
from flask_restful import Api

from app.main.routes.allocation import Allocation, CargoManagement, WindowsTerminal, ProgramInit

# user_blueprint = Blueprint('allocation', __name__)
# api = Api(user_blueprint)

blueprint = Blueprint('allocation', __name__)
api = Api(blueprint)

# Routes
api.add_resource(Allocation, '/allocation')
api.add_resource(CargoManagement, '/update_cargo_management')
api.add_resource(WindowsTerminal, '/stop')
api.add_resource(ProgramInit, '/init')


@blueprint.route('/demo', methods=['GET'])
def demo():
    return jsonify({"name": "flask demo"})
