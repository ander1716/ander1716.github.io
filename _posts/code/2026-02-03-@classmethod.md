---
layout: post
title:  "python中的@classmethod装饰器"
date:   2026-02-03
last_modified_at: 2026-02-03
categories: [代码片段]
tags: [code]
cover: https://qiniu.zhuyucun.cn/uploads/1764853276621_kn1jl7.jpg
excerpt: >
  介绍@classmethod装饰器的使用方法。
---

## 功能和问题
- 功能描述：@classmethod是一个装饰器，用于定义类方法。类方法是一种特殊的方法，它可以直接通过类调用，而不需要实例化类。

## 代码片段展示
``` py
# 代码片段
class Person:
    area = "中国"
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def show(cls):
        print(cls.area)

    def say(self):
        print(self.name, self.age)


p1 = Person("李四", 12)
print(p1.name, p1.age, p1.area)

Person.show()

p1.show()
p1.say()

```
与@staticmethod的区别：
- @classmethod装饰的方法可以通过类调用，也可以通过实例调用。
- @staticmethod装饰的方法只能通过类调用，不能通过实例调用。
- @classmethod装饰的方法可以访问类的属性，而@staticmethod装饰的方法不能访问类的属性（‼️第一个参数不是self）。

## 总结

