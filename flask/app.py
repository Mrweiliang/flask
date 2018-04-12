# -*- coding: utf-8 -*-
#二级路由,承接根路由和子路由之间的装换,所有子路由都要导入该路由


from flask import Flask
import os

app=Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)