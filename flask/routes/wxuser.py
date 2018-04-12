# 微信登录提交路由

from flask import Flask, request,session
from flask_restful import Api, Resource, reqparse
from app import app
from models import Users

api = Api(app)


class WxUser(Resource):
	def get(self):
		print('调用get')
		print(request.args)
		print(request.args.to_dict())
		print(request.args.get('email'))
		print(request.args.get('pwd'))
		return {'hello': 'world'}
	def post(self):
		print('调用post')
		#req = parser.parse_args(strict=True)
		#json_data = parser.parse_args(force=True)

		# print(request.get_json())
		# print(request.get_json()['email'])

		email=request.get_json()['email']  #前端页面提交上来的值,准备进行查库操作
		pwd = request.get_json()['pwd']
		u = Users.objects(email=email,pwd=pwd).first() #进行查库操作,将查询到的信息给u,如果有或者没有
		if u!=None:
			# return '登录成功'
			loginbean = {'id':str(u._id),'nicheng ':u.nicheng ,'role':u.role,'msgnum':u.msgnum}
			session['loginbean']=loginbean
			return '登录成功'
		else:
			return '账号/密码错误'


api.add_resource(WxUser, "/wxuser") # 设置路由
