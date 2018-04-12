# -*- coding: utf-8 -*-
#用户session劫持路由


from app import app
import os
from flask import render_template,request,session,redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES,patch_request_class,secure_filename
import time
from models import Shops
from models import Msgs
from models import Users

# UPLOAD_FOLDER=os.getcwd()+r'\static\photos\idcards'
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF'])
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()+ '/static/photos' # 文件储存地址
photos = UploadSet('photos', IMAGES) #创建UploadSet 拿到UploadSet对象 并设置文件类型为image
configure_uploads(app, photos) #使用configure_uploads()方法注册并完成相应的配置
# 用于判断文件后缀
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#用户登录
@app.route('/home',methods=['GET'])   #用户登录session验证路由
def home():
	if 'loginbean' in session:
		loginbean=session['loginbean']
		# print(loginbean)
		msglist = Msgs.objects(recid=loginbean['id'],recflag=1).order_by('-createtime').all() #将是否通过的信息,返回给前端页面显示,倒序显示
		return render_template('home/home.html',loginbean=loginbean,msglist=msglist)
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'


#获取商家申请信息被驳回
@app.route('/shopapply',methods=['GET'])
def shopapply():
	if 'loginbean' in session:
		loginbean=session['loginbean']
		# print(loginbean)
		#1.查询shops表中有无shop被驳回的记录
		shopRs = Shops.objects(uid=loginbean['id'],flag=-1).first()
		return render_template('home/shopapply.html',loginbean=loginbean,shopRs=shopRs)
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'
		

@app.route('/subapply',methods=['POST'])   #图片上传方法
def subapply():
	if 'loginbean' in session:
		loginbean = session['loginbean']
		if request.method == 'POST':
			shopid = request.form.get('shopid')   #接参,接收id前端传来请求
			if shopid==None: # 如果数据库里没有执行下面
				shop = Shops()
				#--------修改users表中role=2(审核中 )----------
				# u = Users.objects(_id=shop.uid).updata(inc__role=1)  #增加
				# u = Users.objects(_id=shop.uid).update(set__role=2)   #修改

				# msg.save()

			else: 
				shop = Shops.objects(_id=shopid,uid=loginbean['id']).first()
				# print(shop['uid'])

			shop['uid'] = loginbean['id']
			shop['shopname'] = request.form.get('shopname')
			shop['address'] = request.form.get('address')
			shop['lng'] = float(request.form.get('lng'))
			shop['lat'] = float(request.form.get('lat'))
			shop['tel'] = request.form.get('tel')   #以上是入库操作
			# shopname = request.form.get('shopname')
			

			app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()+ '/static/photos' # 文件储存地址
			configure_uploads(app, photos) #使用configure_uploads()方法注册并完成相应的配置


			fArr = ('idcard','ownercard','blicense','hlicense')
			for item in fArr:
				if item in request.files:
					f = request.files[item]
					if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
						filename = photos.save(request.files[item])
						# print(filename)
						shop[item]='/static/photos/'+filename

        # --------构建shops商家,入库插入数据
			updtime = time.strftime('%Y-%m-%d %H:%M:%S')    #将时间转换成整体显示
			# updtime = time.time()
			shop.updtime = updtime
			shop.flag=0
			if shopid==None: # 如果数据库里没有执行下面
				shop.createtime = updtime
			shop.save()
			u = Users.objects(_id=shop.uid).update(set__role=2)
			loginbean['role']=2
			session['loginbean'] = loginbean


		return redirect('/home')
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'





