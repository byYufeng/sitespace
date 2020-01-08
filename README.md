1.master分支使用6080端口，dev分支使用6081端口，标题栏用test加以区分，并开启debug模式

当前可用模块：
    导航栏、页脚
    注册、登录
    上传、下载
    博客的查询和发表

note:
    每次request和sqllite取回的数据编码需处理统一,设置sqlite-conn中的text_factory=str以支持中文

autocomplete:
- 前后端交互已完成
- 待解决问题：
    1.按键后才触发绑定，需再次触发（比如输个字符并删除后）才能自动提示
    2.不支持中文，后端收到的请求是拼音
    3.样式不对


PS. 
it seems that edit of html also reload from flask 1.0
