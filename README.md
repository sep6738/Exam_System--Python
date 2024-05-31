# python大作业
### 安装依赖
```dos
pip install -r requirements.txt
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

### 网页
运行app.py以打开网页

注册页面：http://127.0.0.1:5000/auth/register

登录页面：http://127.0.0.1:5000/auth/login

![](https://i0.hdslb.com/bfs/archive/30ca2e0f0976beb4262b616e437a9c7d4d1198f5.jpg@336w_190h_1c_!web-video-rcmd-cover.avif)