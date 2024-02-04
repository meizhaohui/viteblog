# Python Cookbook

## 第1章 数据结构和算法

### 1.1 将序列分解为单独的变量

任何序列（或可迭代的对象）都可以通过一个简单的赋值操作来分解为单独的变量。

```python
$ python3
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> p = (3, 4)
>>> x,y = p
>>> x
3
>>> y
4
>>>
```

### 1.2 从任意长度的可迭代对象中分解元素

使用`*表达式`来分解元素。

下面的统计成绩平均分的方法，去掉第一个值和最后一个值，并求值就用了这种方法。

```python
>>> def drop_first_last(grades):
...     first, *middle, last = grades
...     return sum(middle)/len(middle)
...
>>> drop_first_last([1,2,3,4])
2.5
>>> drop_first_last([1,2,3,4,5])
3.0
>>> drop_first_last([1,2,3,4,5,6])
3.5
```

### 1.3 使用双端队列保存最后N个元素

在处理过程中保留最后N条记录。

```python
>>> from collections import deque
>>> dq = deque(maxlen=3)
>>> dq
deque([], maxlen=3)
>>> dq.append(1)
>>> dq
deque([1], maxlen=3)
>>> dq.append(2)
>>> dq
deque([1, 2], maxlen=3)
>>> dq
deque([1, 2], maxlen=3)
>>> dq.append(3)
>>> dq
deque([1, 2, 3], maxlen=3)
>>> dq.append(4)
>>> dq
deque([2, 3, 4], maxlen=3)
>>> dq.appendleft(5)
>>> dq
deque([5, 2, 3], maxlen=3)
>>>
```

可以看到在两端添加数据时，当队列中数据量到达最大值3时，再新增元素时就会将之前的左侧或右侧的数据清理掉，以使新的数据能够填写进来。



### 1.4 找到最大或最小的N个元素

使用堆队列算法`heapq`模块。

参考：

- [heapq — Heap queue algorithm](https://docs.python.org/3.6/library/heapq.html)
- [heapq — 堆队列算法](https://docs.python.org/zh-cn/3.6/library/heapq.html)

> 这个模块提供了堆队列算法的实现，也称为优先队列算法。
>
> 堆是一个二叉树，它的每个父节点的值都只会小于或等于所有孩子节点（的值）。 它使用了数组来实现：从零开始计数，对于所有的 *k* ，都有 `heap[k] <= heap[2*k+1]` 和 `heap[k] <= heap[2*k+2]`。 为了便于比较，不存在的元素被认为是无限大。 堆最有趣的特性在于最小的元素总是在根结点：`heap[0]`。

提供了以下函数。

- `heapq.heappush(heap, item)`,将值压入到堆中。
- `heapq.heappop(heap)`，弹出堆中最小的元素。使用 `heap[0]` ，可以只访问最小的元素而不弹出它。
- `heapq.heapify(x)`，将列表x原地转换成堆。
- `heapq.nlargest(n, iterable, key=None)`, 从 iterable 所定义的数据集中返回前 n 个最大的元素。 如果提供了 key 则其应指定一个单参数的函数，用于从每个元素中提取比较键 (例如 key=str.lower)。 等价于: `sorted(iterable, key=key, reverse=True)[:n]`。
- `heapq.nsmallest(n, iterable, key=None)`, 从 iterable 所定义的数据集中返回前 n 个最小元素组成的列表。 如果提供了 key 则其应指定一个单参数的函数，用于从 iterable 的每个元素中提取比较键 (例如 key=str.lower)。 等价于: `sorted(iterable, key=key)[:n]`。

示例：

```python
>>> import heapq

>>> data = [3, 2, 6, 5, 4, 7, 1]

# 将列表原地转换成堆
>>> heapq.heapify(data)
>>> data
[1, 2, 3, 5, 4, 7, 6]

# 获取堆中最大的三个元素
>>> heapq.nlargest(3, data)
[7, 6, 5]

# 获取堆中最小的三个元素
>>> heapq.nsmallest(3, data)
[1, 2, 3]
```



向堆中插入压入数据：

```python
>>> h = []
>>> heapq.heappush(h, 3)
>>> h
[3]
>>> heapq.heappush(h, 2)
>>> h
[2, 3]
>>> heapq.heappush(h, 6)
>>> h
[2, 3, 6]
>>> heapq.heappush(h, 5)
>>> h
[2, 3, 6, 5]
```



从堆中弹出数据,会弹出最小数据：

```python
>>> heapq.heappop(h)
2
>>> h
[3, 5, 6]
>>> heapq.heappop(h)
3
>>> h
[5, 6]
>>> heapq.heappop(h)
5
>>> h
[6]
>>> heapq.heappop(h)
6

# 此时堆中已经为空
>>> h
[]
>>>

# 再次弹出抛出异常
>>> heapq.heappop(h)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: index out of range
```

注意事项：

- `heap[0]`最是返回最小那个元素。直接调用`heap[0]`不会弹出元素。
- 如果只是简单找到最小或最大元素，则使用`min`或`max`函数会更快。
- 如果需要找N个最小值或最大值，N值与元素个数本身的大小差不多时，通常更快的方法是先对数据进行排序，然后进行切片操作，如`sorted(items)[:N]`。



### 1.5 优先级队列

实现一个队列，并按给的优先级对元素进行排序，且每次弹出时都会返回优先级最高的那个元素。

实现代码：

```python
"""
filename: priority_queue.py
function: 实现优先级队列,并按给的优先级对元素进行排序，且每次弹出时都会返回优先级最高的那个元素。
"""

import heapq


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        """压入数据"""
        # 由于heapq是小堆，使用-priority 将正优先级数转换成一个更小的数据
        # 将self._index用于对于相同优先级的元素按压入顺序排列
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        """弹出数据"""
        return heapq.heappop(self._queue)[-1]

    @property
    def queue(self):
        return self._queue


class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Item('%s')" % self.name


if __name__ == '__main__':
    q = PriorityQueue()
    q.push(Item('foo'), 1)
    print(q.queue)
    q.push(Item('boo'), 5)
    print(q.queue)
    q.push(Item('spam'), 4)
    print(q.queue)
    q.push(Item('grok'), 1)
    print(q.queue)
    q.push(Item('grok1'), 6)
    print(q.queue)
    print('弹出')
    print(q.pop())
    print(q.pop())
    print(q.pop())
    print(q.pop())
    print(q.pop())

```

运行输出：

```sh
$ /usr/bin/python3 priority_queue.py
[(-1, 0, Item('foo'))]
[(-5, 1, Item('boo')), (-1, 0, Item('foo'))]
[(-5, 1, Item('boo')), (-1, 0, Item('foo')), (-4, 2, Item('spam'))]
[(-5, 1, Item('boo')), (-1, 0, Item('foo')), (-4, 2, Item('spam')), (-1, 3, Item('grok'))]
[(-6, 4, Item('grok1')), (-5, 1, Item('boo')), (-4, 2, Item('spam')), (-1, 3, Item('grok')), (-1, 0, Item('foo'))]
弹出
Item('grok1')
Item('boo')
Item('spam')
Item('foo')
Item('grok')
```

