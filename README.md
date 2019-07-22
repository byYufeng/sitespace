1.master分支使用6080端口，dev分支使用6081端口，标题栏跟test加以区分，并开启debug模式

当前可用模块：
    导航栏、页脚
    注册、登录
    上传、下载
    博客的查询和发表

note:
    每次request和sqllite取回的数据编码需处理统一,设置sqlite-conn中的text_factory=str以支持中文
