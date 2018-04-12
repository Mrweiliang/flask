# -*- coding: utf-8 -*-
#主界面路由


from app import app
from flask import render_template,request,session

@app.route('/')
def index():
	loginbean = None
	if 'loginbean' in session:
		loginbean = session['loginbean']
	# return "Hello World"
	return render_template('index.html',loginbean=loginbean)


