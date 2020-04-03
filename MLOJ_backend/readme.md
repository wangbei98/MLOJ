[TOC]

## 运行

```
1. cd 进 MLOJ_backend
2. pipenv install (下载所需的所有依赖)
3. pipenv shell （进入pipenv的shell环境）
4. flask run (运行)
4. flask initdb -- drop 删除所有数据库并重新初始化数据库
```


## 后端目录结构

```
MLOJ_backend
	|
	| -- APIS （API设计）
		  | -- admin.py  管理员操作
		  | -- auth.py 用户登入等出相关
		  | -- user.py  普通用户操作
	|
	| -- .flaskenv (flask 配置文件)
	| 
	| -- app.py (项目入口文件)
	|
	| -- extensions.py 定义一些扩展工具 
	|
	| -- models.py  定义数据库类
	|
	| -- Pipfile/Pipfile.lock 虚拟环境下载的依赖包信息 
	|
	| -- resources 文件目录
```

## API设计

### 设计资源端点

* 用户登录/注册/登出
* 获取用户信息
* 获取所有课程
* 新建课程
* 删除课程
* 获取课程信息
* 修改课程信息
* 上传课件
* 下载课件
* 新建作业
* 删除作业
* 获取作业信息
* 修改作业信息
* 上传数据集
* 下载数据集
* 上传作业
* 批改作业



| 资源       | URL                             | 实现方法/对应功能                                            | 实现等级 | 服务端是否完成部署 |
| ---------- | ------------------------------- | ------------------------------------------------------------ | -------- | ------------------ |
| 注册       | /api/register                   | POST (uid=xx,username=xx) 注册                               | P0       | √                  |
| 登录       | /api/login                      | POST(uid=xxx,password=xx)登录                                | P0       | √                  |
| 登出       | /api/logout                     | GET                                                          | P0       | √                  |
| 当前用户   | /api/user/getcur                | 学生：GET(获取当前用户的信息)                                | P3       | √                  |
| 课件       | /api/courseware?cwid=xxx        | 学生&老师：GET下载cwid=xxx的课件<br/>老师：DELETE删除课件    | P1       | √                  |
| 所有课件   | /api/coursewares                | 学生&老师：GET获得所有课件信息<br>老师：POST(file=xxx) 上传 <br> | P1       | √                  |
| 单个作业题 | /api/homework?hid=xxx           | 学生&老师：GET 获取<br/>老师：PUT (homeworkname=xxx,homeworkdesc=xxx,type=1)修改<br/>老师：DELETE 删除 | P1       | √                  |
| 所有作业题 | /api/homeworks                  | 学生&老师：GET 获取全部作业题的信息<br/>老师：POST(homeworkname=xxx,homeworkdesc=xxx,type=x)为homework为xxx的课程新建作业题，作业题类型为x | P1       | √                  |
| 数据集     | /api/homework/dataset?fid = xxx | 学生&老师：GET 下载fid=xxx的数据集<br/>老师：DELETE删除数据集 fid = xxx | P2       |                    |
| 数据集     | /api/homework/datasets          | 学生：GET 获取xxx作业题对应的所有数据集 （不包括答案）hid=xx<br/>老师：GET 获取xxx作业题对应的所有数据集 （包括答案）hid=xx<br/>老师：POST(file=xx) hid = xxx & ftype=x为xxx上传数据集<br/> ftype = 0 ：数据集； 1：测试集；-1 ：答案集 | P2       |                    |
| 作业       | /api/homework/submit?hid=xxx    | 学生&老师：GET获取xxx学生的xxx作业信息<br/>学生：POST(file=xxx) 这个学生提交这次作业的答案 | P2       |                    |
| 分数       | /api/homework/score?hid=xxx     | 老师：POST(score=xxxx) 为这个人的这个作业打分<br>GET（获取分数） | P2       |                    |
| 学生作业   | /api/homework/students?hid=xxx  | 老师：GET 获取某作业下所有学生的完成情况                     |          |                    |
|            |                                 |                                                              |          |                    |
|            |                                 |                                                              |          |                    |


## 返回值协议

| code | message                       | Data | 说明                       |
| ---- | ----------------------------- | ---- | -------------------------- |
| 0    | ok                            |      | 成功                       |
| 10   | database error                |      | 未知数据库错误             |
| 11   | node not exist, query fail    |      | 当前节点在数据库中不存在   |
| 12   | node already exist, add fail  |      | 目标节点已经存在，插入失败 |
|      |                               |      |                            |
| 20   | File error                    |      | 未知文件错误               |
| 21   | file already exist, save fail |      | 文件已存在，保存失败       |
| 22   | file not exist                |      | 目标文件不存在             |
| 23   | illegal filename              |      | 文件名不合法               |
| 24   | preview  not allowed          |      | 文件不支持预览             |
| 25   | delete fail                   |      | 删除数据失败               |
| 26   | modify fail                   |      | 修改失败                   |
| 27   | insert fail                   |      | 插入失败                   |
|      |                               |      |                            |
| 30   | user error                     |      | 用户相关错误               |
| 31   | user not found                 |      | 用户不存在                 |
| 32   | already authenticated          |      | 用户已经登录               |
| 33   | login fail                     |      | 登录失败                   |
| 34   | user add fail                  |      |                            |
| 35   | get current_user fail          |      |                            |
| 36 | permission denied |      | 无操作权限 |
|      |                               |      |                            |
|      |                               |      |                            |

​	



## TODO

- [ ] 后台：url参数检查 （防御式编程）  (空值，错误值，压根没有这个字段)
- [x] 权限管理