# -*- coding: utf-8 -*-
#根路由,所有新的路由都需要在此注册


from app import app
import routes.index
import routes.user
import routes.home
import routes.admin
import routes.dish
import routes.wxuser
import routes.wxdish


if __name__ == '__main__':
	app.run(debug=True) #如果你启用了调试支持，服务器会在代码修改后自动重新载入，并在发生错误时提供一个相当有用的调试器。   (port=80,改端口号,80为默认端口,浏览器打开时不输入端口,默认为80)

	