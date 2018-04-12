# -*- coding: utf-8 -*-
#管理员界面路由


from app import app   #导入二级路由,所有新建的路由都需要导入
from flask import render_template,request,session,redirect
from models import Admins
from models import Shops
from models import Users
from models import Msgs
from models import Shopflow
import time


@app.route('/adminLogin',methods=['POST'])   #管理员登录
def adminLogin():
	if request.method == 'POST':
			email=request.form.get('email')
			pwd = request.form.get('pwd')
			u = Admins.objects(email=email,pwd=pwd).first() 
			if u!=None:
				adminbean = {'id':str(u._id),'email':u.email,'role':u.role}
				session['adminbean']=adminbean
				return redirect('/applyList')
			else:
				return '账号/密码错误'

# @app.route('/adminhomes',methods=['GET'])
# def adminhomes():
# 	return render_template('admin/adminhomes.html')

@app.route('/adminhomes',methods=['GET'])   #管理员session验证路由
def adminhomes():
	if 'adminbean' in session:
		adminbean=session['adminbean']
		print(adminbean)
		return render_template('admin/adminhomes.html',adminbean=adminbean)
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'


@app.route('/adminlogout',methods=['GET'])    #管理员注销
def adminlogout():
	if 'adminbean' in session:
		del session['adminbean']
	return redirect('/')


#管理员登录成功看到商家申请信息
@app.route('/applyList',methods=['GET'])
def applyList():
	if 'adminbean' in session:
		adminbean=session['adminbean']
		#查询数据库,获取商家申请的列表
		applist = Shops.objects(flag=0).all()
		return render_template('admin/applyList.html',applist=applist)
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'


#管理员查界面,点击"查看"商家申请的详细信息
@app.route('/shopinfo',methods=['GET'])
def shopinfo():
	#1.检验session
	if 'adminbean' in session:
		# adminbean=session['adminbean']
	#2.接收shopid
		shopid = request.args.get('shopid')
	#3.查库=>结果集rs
		rs = Shops.objects(_id=shopid).first()
	#4.渲染到页面
		return render_template('admin/shopinfo.html',rs=rs)
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'
		

	#管理员驳回申请
@app.route('/refuseShopApply',methods=['POST'])
def refuseShopApply():
	if 'adminbean' in session:
		adminbean=session['adminbean']
		#接收shopid,uid
		shopid = request.form.get('shopid')
		uid = request.form.get('uid')
		msg = request.form.get('msg')
		#修改库,插入消息
		u = Users.objects(_id=uid).update(set__role=1)
		s = Shops.objects(_id=shopid).update(set__flag=-1)
        #消息表入库
		m = Msgs()
		m.sendflag=0
		m.sendid=adminbean['id']
		m.sendname='管理员'
		m.recflag=1
		m.recid=uid
		m.msg='您的申请被驳回'+msg
		m.createtime=time.strftime('%Y-%m-%d %H:%M:%S')
		m.save()
		#跳回到applyList界面
		return redirect('/applyList')
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'


#管理员同意申请
@app.route('/agreeshopapply',methods=['GET'])
def agreeshopapply():
	if 'adminbean' in session:
		adminbean=session['adminbean']
		#接收shopid,uid
		shopid = request.args.get('shopid')
		uid = request.args.get('uid')

		Shopflow.objects().update(inc__flowid=1)
		shopflow = Shopflow.objects().first()
		#修改库,插入消息
		u = Users.objects(_id=uid).update(set__role=3)
		s = Shops.objects(_id=shopid).update(set__flag=1,set__flowid=shopflow.flowid)
        #消息表入库
		m = Msgs()
		m.sendflag=0
		m.sendid=adminbean['id']
		m.sendname='管理员'
		m.recflag=1
		m.recid=uid
		m.msg='您的申请已通过'
		m.createtime=time.strftime('%Y-%m-%d %H:%M:%S')
		m.save()
		#跳回到applyList界面
		return redirect('/applyList')
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'


