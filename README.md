# gcf (g-cores.com fans)

A Gadio information mining tool for g-cores.com fans.
The project is maintained at github.com/bfdw/gcf.

## 安装gcf

```
pip install gcf
```

## 查看帮助文档

```
gcf --help
```

```
gcf career --help
gcf update --help
```

## 简单查询示例

进行查询前，请先更新数据

```
gcf update
```

列出所有西蒙参与的节目

```
gcf -d '西蒙'
gcf --dj '西蒙'
```

列出所有四十二与Ryoma这一CP参与的节目

```
gcf -d '四十二#Ryoma'
gcf --dj '四十二#Ryoma'
```

列出所有PRO节目

```
gcf -p 'GADIO pro'
gcf --prog 'GADIO pro'
```

列出所有题目中包含'兽'的节目

```
gcf -tt '兽'
gcf --title '兽'
```

列出2018年前五个月的所有节目

```
gcf -t 20180101 20180531
gcf --time 20180101 20180531
```

导出数据到当前目录下的gcf.csv

```
gcf -e
gcf --export
```

尽展示标题、栏目两个数据列 

```
gcf -c 'title#program'
gcf --col 'title#program'
```

列出最近的10期节目

```
gcf -r 10
gcf --recent 10
```

## 复合查询示例

列出最近5期由西蒙、四十二、Ryoma三人同时出场的PRO节目

```
gcf -d '西蒙#四十二#Ryoma' -p 'GADIO pro' -r 5
gcf --dj '西蒙#四十二#Ryoma' --prog 'GADIO pro' --recent 5
```

## 生涯模式示例

列出西蒙2015年以来每季度出台次数

```
gcf --dj '西蒙' --time 20150101 20190101 career --size Q --ratio 0.5
```

列出西蒙2017年以来每月出台率

```
gcf --dj '西蒙' --time 20170101 20171231 career --size M --ratio 0.2 --perc
```

## 简单统计示例

统计各栏目的数量，以及所有主持、嘉宾的出台次数

```
gcf statistic
```