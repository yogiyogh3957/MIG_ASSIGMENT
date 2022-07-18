from main.models import AuthModel, ActivityModel
from flask import request, make_response, jsonify
from main.config import Config_app
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user, create_access_token, get_jwt

import datetime
timezone_diff = datetime.timedelta(hours = 7)
GMT_timezone = datetime.timezone(timezone_diff)
x = datetime.datetime.now(GMT_timezone)
full_of_time = x.strftime('%c')

from main import app, db, jwt_app

import redis
# jwt_redis_blocklist = redis.StrictRedis(
#     host="localhost", port=6379, db=0, decode_responses=True
# )
jwt_redis_blocklist = redis.StrictRedis(
    host="redis-14313.c239.us-east-1-2.ec2.cloud.redislabs.com", port=14313, db=0, decode_responses=True, password='WUfXdziRszDKEcZHMN5iOVMcoZgI6j5s'
)

@jwt_app.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

@jwt_app.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt_app.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return AuthModel.query.filter_by(id=identity).one_or_none()

@app.route('/api/register', methods=['POST'])
def signup_user():
    dataUsername = request.form.get('username')
    dataPassword = request.form.get('password')
    user = AuthModel.query.filter_by(username=dataUsername).first()

    if not user:
        if dataUsername and dataPassword:
            dataModel = AuthModel(username=dataUsername, password=dataPassword)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg": "Registrasi berhasil"}), 200)
        return jsonify({"msg": "Username / password tidak boleh kosong"})
    else:
        return jsonify({"msg": "Username registered"})

@app.route('/api/login', methods=['POST'])
def login_user():
    dataUsername = request.form.get('username')
    dataPassword = request.form.get('password')

    user = AuthModel.query.filter_by(username=dataUsername).one_or_none()
    queryUsername = [data.username for data in AuthModel.query.all()]
    queryPassword = [data.password for data in AuthModel.query.all()]
    if dataUsername in queryUsername and dataPassword in queryPassword:
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Login gagal, silahkan coba lagi !!!"})

@app.route('/api/logout', methods=('GET', 'POST'))
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=Config_app.ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")

@app.route('/api/addactivity', methods=['POST'])
@jwt_required()
def add_activity():
    data = request.get_json()
    dataOwned = current_user.id
    dataType = data["type"]
    dataTime = full_of_time

    if dataOwned and dataType and dataTime:
        dataModel = ActivityModel(owned_by=dataOwned, type=dataType, time=dataTime)
        db.session.add(dataModel)
        db.session.commit()
        return make_response(jsonify({"msg": "add activity success"}), 200)
    return jsonify({"msg": "failed adding data"})

@app.route('/api/edit_activity/<int:id>', methods=["GET", "POST"])
@jwt_required()
def edit_activity(id):
    activity_to_edit = ActivityModel.query.get(id)
    dataType = request.form.get('type')
    activity_to_edit.type = dataType

    db.session.commit()
    return jsonify({"msg":"data_edited"})

@app.route('/api/delete_activity/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_activity(id):
    activity_to_delete = ActivityModel.query.get(id)
    db.session.delete(activity_to_delete)
    db.session.commit()
    return jsonify({"msg":"data_deleted"})

@app.route('/api/getallactivity', methods=['GET'])
@jwt_required()
def get_all_activity():
    data = ActivityModel.query.all()
    id = [o.id for o in data]
    owned_by = [x.owned_by for x in data]
    type = [x.type for x in data]
    time = [x.time for x in data]
    data_output = []
    for data in range(len(id)):
        output = {
            "id" : id[data],
            "owned_by" : owned_by[data],
            "type" : type[data],
            "time" : time[data]
        }
        data_output.append(output)
    print(data_output)
    return jsonify(data_output)

@app.route('/api/getmyactivity/', methods=['GET'])
@jwt_required()
def get_my_activity():
    data = ActivityModel.query.filter_by(owned_by=current_user.id).all()
    id = [o.id for o in data]
    owned_by = [x.owned_by for x in data]
    type = [x.type for x in data]
    time = [x.time for x in data]
    data_output = []
    for data in range(len(id)):
        output = {
            "id": id[data],
            "owned_by": owned_by[data],
            "type": type[data],
            "time": time[data]
        }
        data_output.append(output)
    print(data_output)
    return jsonify(data_output)