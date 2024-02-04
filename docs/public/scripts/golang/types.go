/*
 *      Filename: types.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: 变量声明与数据类型
 *   Create Time: 2019-11-28 22:22:21
 * Last Modified: 2019-11-28 23:03:42
 */
package main

import "fmt"

var num int = 10 // 声明变量并初始化
var flag bool = false
var sayhi string = "Hello"

func Printnum(num int) {
	fmt.Println(num)
}

func main() {
	var num1, num2 = 1, 2 // 不需要显示声明类型，根据初始值自动推断数据类型
	flag1, flag2 := true, false
	name := "Go"
	Printnum(num)
	fmt.Println(num, num1, num2)
	fmt.Println(flag, flag1, flag2)
	fmt.Println(sayhi, name)
}
