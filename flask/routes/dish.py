#菜品信息路由


from app import app
import os
from flask import render_template,request,session,redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES,patch_request_class,secure_filename
import time
from models import Shops
from models import Dishsorts
from models import Foods

# UPLOAD_FOLDER=os.getcwd()+r'\static\photos\idcards'
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF'])


photos = UploadSet('photos', IMAGES) #创建UploadSet 拿到UploadSet对象 并设置文件类型为image


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS



@app.route('/sortmanager',methods=['GET'])  #点击分类管理的路由
def sortmanager():
	if 'loginbean' in session:
		loginbean=session['loginbean']
		shopid = request.args.get('shopid') #接收前端传来的id
		myshops = Shops.objects(uid=loginbean['id'],flag=1).first()  #将页面请求获取id进行查库获取,all为显示所有
		sortlist = Dishsorts.objects(shopid=myshops._id).all()  #将库里的菜单在前端页面显示
		return render_template('dish/sortmanager.html',loginbean=loginbean,shopid=myshops._id,sortlist=sortlist,flowid=myshops.flowid)
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'


@app.route('/addsort',methods=['POST'])   #提交菜单分类模态框路由
def addsort():
	if 'loginbean' in session:
		loginbean=session['loginbean']
		#菜单信息进行入库操作
		ds = Dishsorts()
		ds.shopid = request.form.get('shopid')
		ds.uid = loginbean['id']
		ds.sortname = request.form.get('sortname')
		ds.save()
		return redirect('/sortmanager')
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'


@app.route('/updataSort',methods=['POST']) #修改菜单信息路由
def updataSort():
	if 'loginbean' in session:
		loginbean = session['loginbean']
		sortid = request.form.get('sortid')  #将重新获取的进行入库
		sortname = request.form.get('sortname')
		if sortname!='':  #判断更改后的,库里是否有,如果有将更改信息入库
			Dishsorts.objects(_id=sortid).update(set__sortname=sortname)
		return redirect('/sortmanager')
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'



@app.route('/menu',methods=['GET'])  #点击菜品分类路由
def menu():
	if 'loginbean' in session:
		loginbean=session['loginbean']
		myshops = Shops.objects(uid=loginbean['id'],flag=1).first()
		sortlist = Dishsorts.objects(shopid=myshops._id).all()   #将菜品分类传到前端全部显示

		sortid=sortlist[0]._id  #将菜单里的菜全部显示
		if request.args.get('sortid')!=None:
			sortid=request.args.get('sortid')
		dishRs=Foods.objects(sortid=sortid).all()  #将该菜单下的菜全部显示

		return render_template('dish/menu.html',loginbean=loginbean,shopid=myshops._id,sortlist=sortlist,dishRs=dishRs)
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'


@app.route('/upload',methods=['POST'])   #菜品上传路由
def upload():
	if 'loginbean' in session:
		loginbean = session['loginbean']
		if request.method == 'POST':
		
			food = Foods()   #存入到该库下
			food.dishname=request.form.get('dishname')
			food.price=float(request.form.get('price'))
			food.sortid=request.form.get('sortid')
			food.shopid=request.form.get('shopid')
			food.uid=loginbean['id']


			app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()+ '/static/dishimg'
			configure_uploads(app, photos)   #次级目录下进行保存操作

			
			f = request.files["dishphoto"]
			if f and allowed_file(f.filename):
				filename = photos.save(request.files["dishphoto"])
				# print(filename)
				food.dishphoto='/static/dishimg/'+filename  #图片上传入库操作
				
			food.save()  #将上传的进行入库操作
		return redirect('./menu?sortid='+food.sortid)   #每进行一次菜单下的菜提交,则跳到对应的菜单下
	else:
		return '<script>alert("session过期,请重新登录");location.href="/";</script>'

