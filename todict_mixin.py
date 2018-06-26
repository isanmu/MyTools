#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/26/2018 13:41
# @Author  : Winson
# @User    : winswang
# @Site    : 
# @File    : todict_mixin.py
# @Project : MyTools
# @Software: PyCharm
from pprint import pprint
import json


class ToDictMixin(object):
    """
    transfer obj in memory to dict and serialization(序列化) it.
    """
    def to_dict(self):
        # pprint(self.__dict__)
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            print('dict:', value)
            return self._traverse_dict(value)
        elif isinstance(value, list):
            print('list: ', value)
            return [self._traverse(key, i) for i in value]
        # 判断一个对象里面是否有__dict__属性或者__dict__方法，
        # 返回BOOL值，有__dict__特性返回True， 否则返回False
        elif hasattr(value, '__dict__'):
            print('hasattr: ', value)
            return self._traverse_dict(value.__dict__)
        else:
            # print(value)
            return value


class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        # 实际上，parent指向变量则正常应用，而偌指向‘根’，将导致循环引用
        self.parent = parent

    def _traverse(self, key, value):
        if(isinstance(value, BinaryTreeWithParent) and
                key == 'parent'):
            return value.value
        else:
            return super()._traverse(key, value)


class HasattrDictTest:
    def __init__(self, var):
        self.var = var


class JsonMixin(object):
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        pprint(kwargs)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())


class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        print(switch)
        self.switch = Switch(**switch)
        self.machines = [Machine(**kwargs) for kwargs in machines]


class Switch(ToDictMixin, JsonMixin):
    def __init__(self, ports=None, speed=None):
        # super()._traverse_dict(switch)
        self.ports = ports
        self.speed = speed


class Machine(ToDictMixin, JsonMixin):
    def __init__(self, cores=None, ram=None, disk=None):
        self.cores = cores
        self.ram = ram
        self.disk = disk


tree = BinaryTree(HasattrDictTest(10))
tree.left = BinaryTree(7, right=BinaryTree(9))
tree.right = BinaryTree(13, left=BinaryTree(11))
# tree.right = BinaryTree(13, left=tree.left)

root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)

# pprint(tree.to_dict())
# pprint(root.to_dict())


serialized = """{
    "switch": {"ports": 5, "speed": 1e9},
    "machines": [
        {"cores": 8, "ram": 32e9, "disk": 5e12},
        {"cores": 4, "ram": 16e9, "disk": 1e12}
    ]
}
"""

deserialized = DatacenterRack.from_json(serialized)
roundtrip = deserialized.to_json()

pprint(roundtrip)
assert json.loads(serialized) == json.loads(roundtrip)