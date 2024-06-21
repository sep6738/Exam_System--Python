from datetime import datetime

from flask import Blueprint, render_template, jsonify, redirect, url_for, session, flash
from exam_sys_proj.src.extensions import mail, dbPool
from flask_mail import Message
from flask import request
from .forms import RegisterForm, LoginForm
import os, bcrypt, json, markdown
from markupsafe import Markup
from exam_sys_proj.dao.RegistrationCodeDAO import RegistrationCodeDAO, RegistrationCode
from exam_sys_proj.dao.UsersDAO import UsersDAO, Users
from exam_sys_proj.util.teacherUtils import TeacherUtils
from exam_sys_proj.dao.BroadcastShowDAO import BroadcastShowDAO
from ..dao.HepAndKpMediaterDAO import HepAndKpMediaterDAO
from ..dao.HomeworkOrExamPoolDAO import HomeworkOrExamPoolDAO
from ..dao.StudentCourseDAO import StudentCourseDAO
from ..dao.TeacherCourseDAO import TeacherCourseDAO
from ..util.studentcourseUtils import StudentCourseUtils
from ..util.teachercourseUtils import TeacherCourseUtils

bp = Blueprint("admin", __name__, url_prefix="/admin")


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        判断是否为bytes类型的数据是的话转换成str
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


# http://127.0.0.1:5000
@bp.route("/detail")
def detail():
    broadcast_getter = BroadcastShowDAO(dbPool)
    broadcasts = broadcast_getter.get_user_All_Broadcast(session.get("user_id"))
    if broadcasts != 'noResult':
        for broadcast in broadcasts:
            broadcast.content = json.loads(broadcast.content)
            broadcast.content['message'] = Markup(
                markdown.markdown(broadcast.content['message'], extensions=['extra', 'codehilite', 'nl2br']))
    return render_template("admin_detail.html", broadcasts=broadcasts)


users_dao = UsersDAO(dbPool)


@bp.route("/user_manage")
def user_manage():
    return render_template("admin_user_manage.html")


@bp.route('/users', methods=['GET'])
def get_users():
    try:
        # 从数据库查询用户列表
        users = users_dao.query('1', 'roleID', True) + users_dao.query('2', 'roleID', True) + users_dao.query('3',
                                                                                                              'roleID',
                                                                                                              True)
        # 将用户数据转换为字典格式
        if not users:
            return json.dumps({
        'code': 0,
        'message': "成功！",
                'data': []
    }, cls=MyEncoder)
        user_dicts = [vars(user) for user in users]
        data = []
        for user_dict in user_dicts:
            new_dict = {old_key.strip('_'): value for old_key, value in user_dict.items()}
            if new_dict['createAt']:
                new_dict['createAt'] = new_dict['createAt'].strftime('%Y-%m-%d %H:%M:%S')
            if new_dict['updateAt']:
                new_dict['updateAt'] = new_dict['updateAt'].strftime('%Y-%m-%d %H:%M:%S')
            data.append(new_dict)
        print(data)
        return json.dumps({
        'code': 0,
        'message': "成功！",
            'data': data
    }, cls=MyEncoder)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to fetch users'}), 500


@bp.route('/users/edit/<int:user_id>', methods=['GET'])
def edit_user(user_id):
    user = users_dao.query(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    return render_template('edit_user.html', user=user)


@bp.route('/users/update', methods=['POST'])
def update_user():
    try:
        # 从请求数据中获取更新后的用户数据
        data = request.form
        user_id = int(data['userID'])
        user = users_dao.query(user_id)
        if user:
            # 更新用户数据,除了密码
            user.userName = data['userName']
            user.name = data['name']
            user.email = data['email']
            user.roleID = data['roleID']
            user.updateAt = datetime.now()
            users_dao.update(user, user_id)
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to update user'}), 500


@bp.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        # 根据用户ID删除用户
        if users_dao.delete(user_id):
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to delete user'}), 500

