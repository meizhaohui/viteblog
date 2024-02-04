# php学习笔记

- 本文档记录php学习过程中的点点滴滴。
- php在线调试环境 [https://www.runoob.com/try/runcode.php?filename=demo_syntax&type=php](https://www.runoob.com/try/runcode.php?filename=demo_syntax&type=php)

1. 使用`array_rand()`函数从数组中随机选择一个或多个元素

```php
<?php
$all = array("red", "green", "blue", "yellow", "brown");
// 从列表中随机选择三个元素
$random_keys = array_rand($all, 3);
echo $all[$random_keys[0]]."<br>";
echo $all[$random_keys[1]]."<br>";
echo $all[$random_keys[2]];
?>
```
