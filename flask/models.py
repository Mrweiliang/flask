# -*- coding: utf-8 -*-
#前端所需要的注册表单路由


from flask import Flask
from flask_mongoengine import MongoEngine
app=Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
	'db':'figer',
	'host':'localhost',
	'port':27017
}

#创建mongo原型
mdb = MongoEngine()
mdb.init_app(app)

#print(dir(mdb))  #在这寻找类型

#类名定义 collection
class Users(mdb.Document):     #用户注册登陆表
		_id = mdb.ObjectIdField()
		email = mdb.StringField()
		pwd = mdb.StringField()
		nicheng = mdb.StringField()
		tel = mdb.StringField()
		role = mdb.IntField()     #-1.表禁止,1.表用户,2.表店铺申请中,3.表商家
		msgnum = mdb.IntField()
		updtime = mdb.StringField()
		createtime = mdb.StringField()  #FloatField 浮点类型

class Admins(mdb.Document):     #管理员表
		_id = mdb.ObjectIdField()
		email = mdb.StringField()
		pwd = mdb.StringField()
		role = mdb.IntField()

class Shops(mdb.Document):     #商家表
		_id = mdb.ObjectIdField()
		uid = mdb.ObjectIdField()
		shopname = mdb.StringField()
		address = mdb.StringField()
		lng = mdb.FloatField()   #DecimalField
		lat = mdb.FloatField()
		tel = mdb.StringField()
		idcard = mdb.StringField()     #身份证
		ownercard = mdb.StringField()   #手持身份证
		blicense = mdb.StringField()   #营业执照
		hlicense = mdb.StringField()   #卫生许可证
		updtime = mdb.StringField()
		createtime = mdb.StringField()
		flag = mdb.IntField()          #-2表强制终止,-1表驳回,0表审核中,1表审核通过
		flowid = mdb.LongField(default=0)     #店铺流水id


class Shopflow(mdb.Document):   #商家流水id表
		_id = mdb.ObjectIdField()
		flowid = mdb.LongField()


class Msgs(mdb.Document):     #消息表
		_id = mdb.ObjectIdField()
		sendflag = mdb.IntField()    #0表管理员,1表普通用户
		sendid = mdb.ObjectIdField()
		sendname = mdb.StringField()
		recflag = mdb.IntField()     #0表管理员,1表普通用户
		recid = mdb.ObjectIdField()
		# recname = mdb.StringField()
		msg = mdb.StringField()
		createtime = mdb.StringField()


class Dishsorts(mdb.Document):   #菜品分类表
		_id = mdb.ObjectIdField()
		shopid = mdb.ObjectIdField()
		uid = mdb.ObjectIdField()
		sortname = mdb.StringField()


class Foods(mdb.Document):   #菜表
		_id = mdb.ObjectIdField()
		shopid = mdb.ObjectIdField()
		uid = mdb.ObjectIdField()
		sortid = mdb.ObjectIdField()
		dishname = mdb.StringField()
		dishphoto = mdb.StringField()
		price = mdb.FloatField()
		curprice = mdb.FloatField()
		flag = mdb.IntField()

