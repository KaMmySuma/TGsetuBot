# 原项目：[SetuBot 色图机器人](https://github.com/DullJZ/SetuBot)

我只是修改了一点点内容让它更符合我的设置，这个仓库的目的只是为了备份我的设置

## 自建机器人
1. 克隆代码
2. 在token.txt文件中填入你的机器人token，格式为：
```
123456:abcdefgh
```
3. 自行获取pixiv的REFRESH_TOKEN，并写入pixiv_token.txt文件中，获取方法参见https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde
4. 安装`requirements.txt`中的库
5. 运行start.py

## Bot指令
- /setu -抽取一张随机涩图~。
- /setu_r18 -不够涩！抽取一张r18涩图。
-  /pixiv_ranking -获取p站排行榜前5名的作品；私聊中可添加参数num=？自定义数量：例：/pixiv_ranking num=3。
- /pixiv_ranking_r18 -获取p站r18排行榜前5名的作品；私聊中可添加参数num=？自定义数量：例：/pixiv_ranking_r18 num=3。

为避免刷屏，以下命令私聊可用（注意空格）：

- /pixiv_id 插画ID -获取指定pid的全部插画。
- /pixiv_search 关键词 -进行关键词搜索，默认获取前5个结果，可添加参数num=？自定义数量：例：/pixiv_search 猫娘 num=3。

## 问题
已知在非中文操作系统上运行会出现Unicode Decode错误，疑为PyTelgramBotAPI的问题，不准备修了。
## 鸣谢
1. [Telegram](https://telegram.org/)
2. [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
3. [cloudscraper](https://github.com/VeNoMouS/cloudscraper)
4. [pycharm](https://www.jetbrains.com/pycharm/)
5. [色图api](https://github.com/yuban10703/SetuAPI)
6. [pixiv](https://www.pixiv.net/)
7. [pixivpy](https://github.com/upbit/pixivpy)
## 打赏
如果你喜欢这个项目，请赏[原作者](https://github.com/DullJZ/SetuBot)一杯咖啡！