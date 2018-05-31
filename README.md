# gcf (g-cores.com fans)
A Gadio information mining tool for g-cores.com fans.
The project is maintained at github.com/bfdw/gcf.

## 简单查询。

列出所有西蒙参与的节目
gcf -d '西蒙'
gcf --dj '西蒙'

列出所有四十二与Ryoma这一CP参与的节目
gcf -d '四十二#Ryoma'
gcf --dj '四十二#Ryoma'

列出所有PRO节目
gcf -p 'GADIO pro'
gcf --prog 'GADIO pro'

列出所有题目中包含'兽'的节目
gcf -tt '兽'
gcf --title '兽'

列出2018年前五个月的所有节目
gcf -t 20180101 20180531
gcf --time 20180101 20180531

导出数据到gcf.cvs
gcf -e
gcf --export

尽展示标题、栏目两个数据列 
gcf -c 'title#program'
gcf --col 'title#program'
(默认列为date#title#dj)
(备选列有date,title,dj,program,index,url,mp3)

列出最近的10期节目
gcf -r 10
gcf --recent 10

## 复合查询

列出最近5期由西蒙、四十二、Ryoma三人同时出场的PRO节目
gcf -d '西蒙#四十二#Ryoma' -p 'GADIO pro' -r 5

## 生涯模式

列出西蒙2015年以来每季度出台次数
gcf --dj '西蒙' --time 20150101 20190101 career --size Q --ratio 0.5

列出西蒙2015年以来每季度出台率
gcf --dj '西蒙' --time 20150101 20190101 career --size Q --ratio 0.5 --perc

## 简单统计

统计各栏目的数量，以及所有主持、嘉宾的出台次数
gcf statistic

## HB查询

过去100期里，谁成为了四十二的心头好？
gcf --recent 100 --dj '四十二' statistic
+----+--------------+---------+
|    | DJ           |   Count |
|----+--------------+---------|
|  1 | 四十二        |     100 |
|  2 | Ryoma        |      54 |
|  3 | Nadya        |      48 |
|  4 | xizongbu     |      36 |
答案是 Ryoma ！

2017年，是谁？在哪？叉了Hardy几次？
gcf --dj 'Hardy' --time 20170101 20171231 statistic
+----+------------+---------+
|    | Program    |   Count |
|----+------------+---------|
|  1 | gadio      |       9 |
|  2 | GADIO News |       2 |
|  3 | GADIO pro  |       2 |
|  4 | 特别二次元  |       1 |
+----+------------+---------+
+----+----------------+---------+
|    | DJ             |   Count |
|----+----------------+---------|
|  1 | Hardy          |      14 |
|  2 | 西蒙            |       7 |
|  3 | Nadya          |       7 |
|  4 | Ryoma          |       4 |

西蒙，Nadya，Ryoma仨人在常规节目，新闻节目，Pro节目，甚至特别二次元都叉了Hardy。
