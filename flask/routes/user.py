# -*- coding: utf-8 -*-
#注册登陆的路由


from app import app
from flask import render_template,request,redirect,session
import time
from models import Users

#注册方法
@app.route('/zhuce',methods=['POST'])
def zhuce():
	if request.method == 'POST':
		u = Users()  #插库的时候,需要将插入的内容,插到这里面
		list = ['email','pwd','nicheng','tel']
		for item in list:
			u[item]=request.form.get(item)
		u.role=1
		u.msgnum=0
		updtime = time.strftime('%Y-%m-%d %H:%M:%S')    #将时间转换成整体显示
		# updtime = time.time()
		u.updtime = updtime
		u.createtime = updtime
		try:   #例外捕获
			u.save() #存入数据
			return '<script>alert("注册成功");location.href="/";</script>'
		except Exception as err:
			estr = str(err)
			if estr.find('emailuiq')>0:
				return 'email重复'
			elif estr.find('teluiq')>0:
				return '电话号码重复'
			elif estr.find('nichenguiq')>0:
				return '昵称重复'
			else:
				return '数据库异常'

#登录方法
@app.route('/login',methods=['POST'])
def login():
	if request.method == 'POST':
			email=request.form.get('email')  #前端页面提交上来的值,准备进行查库操作
			pwd = request.form.get('pwd')
			u = Users.objects(email=email,pwd=pwd).first() #进行查库操作,将查询到的信息给u,如果有或者没有
			if u!=None:
				# return '登录成功'
				loginbean = {'id':str(u._id),'nicheng ':u.nicheng ,'role':u.role,'msgnum':u.msgnum}
				session['loginbean']=loginbean
				return redirect('/home')     #登陆成功,跳转home页面/需要导入
			else:
				return '账号/密码错误'


@app.route('/logout',methods=['GET'])        #用户注销
def logout():
	if 'loginbean' in session:
		del session['loginbean']
	return redirect('/')






