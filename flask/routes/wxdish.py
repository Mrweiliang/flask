# 微信查询提交信息路由

from flask import Flask, request,session
from flask_restful import Api, Resource, reqparse
from app import app
from models import Shops
from models import Dishsorts
from models import Foods
import json

api = Api(app)


class WxEnterRRt(Resource):#微信获取商家菜单信息路由
	def get(self):
		flowid = request.args.get('flowid')
		shop = Shops.objects(flowid=flowid).first()
		dishsorts = Dishsorts.objects(shopid=shop._id).all()
		sortid=dishsorts[0]._id
		dishes = Foods.objects(sortid=sortid).all()
		list = [shop.shopname,dishsorts.to_json(),dishes.to_json()]#默认显示第一个分类
		return json.dumps(list)


class getDishBySortid(Resource):#点击菜单显示某个菜单里面的菜
	def get(self):
		sortid = request.args.get('sortid')#接收前端点击获取的菜单分类id
		dishes = Foods.objects(sortid=sortid).all()#查到的数据,赋给dishes
		print(dishes.to_json())
		return json.dumps(dishes.to_json())#查询到的数据,转换成字符串,传给前端进行接收



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
		email=request.get_json()['email'] 
		pwd = request.get_json()['pwd']
		u = Users.objects(email=email,pwd=pwd).first() 
		if u!=None:
			# return '登录成功'
			loginbean = {'id':str(u._id),'nicheng ':u.nicheng ,'role':u.role,'msgnum':u.msgnum}
			session['loginbean']=loginbean
			return '登录成功'
		else:
			return '账号/密码错误'


api.add_resource(WxEnterRRt, "/wxenterrRRt") # 设置路由
api.add_resource(getDishBySortid, "/getDishBySortid")
