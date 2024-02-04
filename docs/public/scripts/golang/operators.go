/*
 *      Filename: operators.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: 运算符
 *   Create Time: 2019-11-28 23:36:59
 * Last Modified: 2019-11-28 23:46:51
 */
package main

import "fmt"

func checknum(num1, num2 int) {
	fmt.Printf("%d >  %d :%t\n", num1, num2, num1 > num2)
	fmt.Printf("%d <  %d :%t\n", num1, num2, num1 < num2)
	fmt.Printf("%d == %d :%t\n", num1, num2, num1 == num2)
	fmt.Printf("%d != %d :%t\n", num1, num2, num1 != num2)
	fmt.Printf("%d >= %d :%t\n", num1, num2, num1 >= num2)
	fmt.Printf("%d <= %d :%t\n", num1, num2, num1 <= num2)
}

func main() {
	var a, b = 1, 2
	checknum(a, b)
}
