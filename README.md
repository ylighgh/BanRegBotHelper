# BanRegBotHelper

使用Python写的封禁自动注册机器人的程序

# 介绍

通过分析Nginx的POST日志，可以获取每个IP的注册次数、注册邮箱以及注册时间。

这些信息可以用来评估IP是否存在恶意行为，从而决定是否需要对其进行封禁。

# 环境要求

Python 3.8.0及以上版本

# 使用

## 安装依赖

```
pip3 install requirements.txt
```

## 修改配置文件

```
cp configs/application.ini.sample configs/application.ini
```

修改配置文件中`nginx_log_file`和`denied_ip_auto_conf`的值

## 运行

```
$ python3 app.py
2023-05-25 09:39:09 5636 [INFO] deny ip->178.176.76.73 [('2023-05-23 06:28:14', 'valettipablo@gmail.com'), ('2023-05-23 06:36:17', 'hotty377@hotmail.com'), ('2023-05-23 06:55:55', 'john.michael.nups@gmail.com')]
2023-05-25 09:39:09 5636 [INFO] deny ip->178.176.74.101 [('2023-05-23 07:05:56', 'emanzano20@hotmail.com'), ('2023-05-23 07:13:38', 'oncology@2upost.com'), ('2023-05-23 07:15:34', 'vlesko@i.ua'), ('2023-05-23 07:22:55', 'ktaylor@demarcotaylorlaw.com')]
2023-05-25 09:39:09 5636 [INFO] deny ip->178.176.72.221 [('2023-05-23 07:15:56', 'zero_doubt@yahoo.com'), ('2023-05-23 07:37:32', 'JGABRA62@GMAIL.COM'), ('2023-05-23 07:40:20', 'hannahlafrance1@gmail.com')]
2023-05-25 09:39:09 5636 [INFO] deny ip->178.176.77.118 [('2023-05-23 07:21:05', 'sadarise@aol.com'), ('2023-05-23 07:37:25', 'jphongdara@mindwireless.com'), ('2023-05-23 07:58:53', 'jjabot@mindwireless.com')]
2023-05-25 09:39:09 5636 [INFO] deny ip->176.59.52.217 [('2023-05-23 07:21:28', 'rebgagne@comcast.net'), ('2023-05-23 07:28:30', 'hannahlafrance1@gmail.com'), ('2023-05-23 07:30:08', 'fawwad@acutemedical.com')]
2023-05-25 09:39:09 5636 [INFO] deny ip->31.173.84.88 [('2023-05-23 07:37:54', 'jphongdara@mindwireless.com'), ('2023-05-23 07:40:00', 'markburns12@rocketmail.com'), ('2023-05-23 07:52:23', 'dailenwalker77@gmail.com')]
2023-05-25 09:39:09 5636 [INFO] deny ip->31.173.84.221 [('2023-05-23 07:47:22', 'fawwad@acutemedical.com'), ('2023-05-23 07:48:59', 'buettner_manuela@web.de'), ('2023-05-23 07:56:37', 'SLVERNER@ME.COM')]
2023-05-25 09:39:09 5636 [INFO] deny ip->31.173.87.204 [('2023-05-23 08:00:57', 'shad8ball@gmail.com'), ('2023-05-23 08:09:02', 'fawwad@acutemedical.com'), ('2023-05-23 08:36:52', 'treblue21@gmail.com')]
2023-05-25 09:39:09 5636 [INFO] deny ip->31.173.85.198 [('2023-05-23 08:01:43', 'hannesreinhold@aol.com'), ('2023-05-23 08:16:09', 'knade@t'), ('2023-05-23 08:40:54', 'aallisdown@gmail.com'), ('2023-05-23 11:03:20', 'jstroupe@elite')]
2023-05-25 09:39:09 5636 [INFO] deny ip->178.176.74.24 [('2023-05-23 08:05:49', 'jphongdara@mindwireless.com'), ('2023-05-23 08:42:12', 'amnaeontre@gmail.com'), ('2023-05-23 08:56:27', 'dodepeji@gmail.com')]
2023-05-25 09:39:09 5636 [INFO] deny ip->176.59.57.107 [('2023-05-23 08:07:44', 'appliancemandan@gmail.com'), ('2023-05-23 08:16:40', 'ridsecretaryua@gmail.com'), ('2023-05-23 08:24:49', 'plegate@mindwireless.com'), ('2023-05-23 08:38:36', 'jphongdara@mindwireless.com')]
2023-05-25 09:39:09 5636 [INFO] deny ip->31.173.85.90 [('2023-05-23 08:23:27', 'gennieswed@yahoo.com'), ('2023-05-23 08:23:57', 'jphongdara@mindwireless.com'), ('2023-05-23 08:55:35', 'ezequielllerda@gmail.com')]
2023-05-25 09:39:09 5636 [INFO] deny ip->31.173.86.202 [('2023-05-23 09:17:43', 'jphongdara@mindwireless.com'), ('2023-05-23 10:29:21', 'amanowicz1988@gmail.com'), ('2023-05-23 10:30:08', 'yumbajoe30@gmail.com'), ('2023-05-23 11:26:23', 'bonitacyer@gmail.com'), ('2023-05-23 12:24:50', 'oramimar@grupobimbo.com')]
```

