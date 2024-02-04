# mysql数据库求字段的总和、总数与均值

[[toc]]

## 概述  

- MySQL的`SUM`函数是用来求出各种记录中的字段的总和。

- MySQL的`COUNT`函数是用来求出各种记录中的字段的总数。

- MySQL的`AVG`函数是用来求出各种记录中的字段的平均值。

## 求和`SUM`

```sql
SELECT SUM(column_name) FROM table_name WHERE condition
```

## 统计所有记录的数量`COUNT`

```sql
SELECT COUNT(*) FROM table_name
```

## 统计某列的数量`COUNT`
    
```sql    
SELECT COUNT(column_name) FROM table_name WHERE condition
```

## 统计某列不重复的数量，使用`DISTINCT`

```sql
SELECT COUNT(DISTINCT column_name) FROM table_name
```

## 求均值SVG

```sql
SELECT SVG(column_name) FROM table_name WHERE condition
```
