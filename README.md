# 沙河西区电费查询脚本
西区宿舍晚上充不了电费，为防止大半夜没电，需要定期查看电费，索性写了个脚本，定期自动查询电费，当余量小于设定值的时候自动发邮件通知。发送的邮件是英文的，因为powershell默认不支持中文。
灵感来自于[BUAA-NewNorthAPI](https://github.com/moonmagian/BUAA-NewNorthAPI)项目，尝试着抓取了西区的API。

## 使用前准备
1. 确保你在中湾沙河物业的公众号上绑定的你的学号。
2. 准备一个开启smtp服务的邮箱，记下smtp的服务器和授权码。QQ邮箱的开启方法点[这里](https://zhuanlan.zhihu.com/p/643897161)。163邮箱点[这里](https://blog.csdn.net/liuyuinsdu/article/details/113878840)，注意163邮箱需要把端口改为465。其他邮箱的方法可以参考前两个。

## 脚本配置
下载源代码中的python脚本文件，将文件放在你喜欢的地方。

使用文编编辑器打开再在好的脚本，修改根据自己的情况修改配置。
- url：默认为西区中湾物业的接口，新北区的接口请查看[这里](https://github.com/moonmagian/BUAA-NewNorthAPI)。
- student_id：你的学号。
- receive_email：接受通知的邮箱，支持多个邮箱，邮箱之间用逗号分隔。
- sender_email：发送邮件的邮箱。
- password：smtp服务的授权码，不是登录邮箱时的密码。
- smtp_server：smtp服务器地址。
- smtp_port：smtp服务器端口，默认为587，163邮箱需要把端口改为465。
- threshold：当电费小于此值时，发送邮件通知。

## 自动运行
该脚本只执行一次查询，要实现定期自动运行，请将脚本添加到Windows的计划任务程序，根据自己的需要选择执行条件，例如每天定时执行或每次启动电脑时自动执行。关于任务计划程序的使用方法可以参考[这里](https://blog.csdn.net/qq_41587516/article/details/112446587)。