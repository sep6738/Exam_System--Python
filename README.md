# python大作业
### 环境说明
此项目经过测试在python 3.10，3.12均能运行；
数据库请安装mysql 8.0以上版本，经过测试mysql最新版可以运行
### 安装依赖
```dos
pip install -r requirements.txt
```
### 配置文件说明
在运行项目之前需要在util/目录下建立一个config.yaml，并在yaml文件中填入配置信息，如下：
```yaml
database:
  host: localhost
  # 数据库ip地址
  user: 
  # mysql数据库的用户名
  password: 
  # 数据库密码
  database: 
  # 数据库名，如：exam_sys
  mincached: 1
  # 最小连接数
  maxcached: 20
  # 最大连接数

```
### 分工安排
4人小组两人做前端，两人做后端

![](https://tse3-mm.cn.bing.net/th/id/OIP-C.LBVzOA0WvDhthZCpBMO3PgHaHZ?rs=1&pid=ImgDetMain)

### 项目介绍
目前将后端的数据库连接的框架写完了，框架分为dao，orm，util3个部分
##### dao
负责处理所有数据库增删改查的操作，有一个父类basedao，其他类均继承于该类，basedao实现了对数据库最基本的增删改操作，其他子类会根据需求完成特定的增删改。
##### orm
实现数据表到实体的映射，一张表是一个类，一行数据是一个对象，一个属性对应一个变量。设立了set和get方法，可以实现对数据的简单格式转化和处理。目前在不直接访问类中受保护的变量的情况下，任何对里面变量的更改都会通过set方法，所以在实现set方法时必须处理空值等情况，获取变量值若不直接访问类中受保护的变量，则会通过get方法。
##### util
对项目里面的静态和常用方法封装，保存配置文件

### 说明
请各位组员将自己的代码中引入的依赖写到requirements.txt中.
运行前请修改exam_sys_proj/util/config.yaml连接自己的数据库
commit&push前请reformat code

### 网页
运行app.py以打开网页

注册页面：http://127.0.0.1:5000/auth/register

登录页面：http://127.0.0.1:5000/auth/login

测试账户：
student@test.com
teacher@test.com
admin@test.com
密码都是123456789，需要在数据库运行insert.sql后使用

![](https://p3-pc-sign.douyinpic.com/tos-cn-i-0813/226b9baade6c45058933a63fb6cadcf9~tplv-dy-aweme-images-v2:3000:3000:q75.webp?biz_tag=aweme_images&from=3213915784&s=PackSourceEnum_AWEME_DETAIL&sc=image&se=false&x-expires=1719763200&x-signature=a4becisRjxm%2F%2B%2FjinVd1Z2zPyAY%3D)
