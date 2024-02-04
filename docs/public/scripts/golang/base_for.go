/*
 *      Filename: base_for.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: for循环语句的使用
 *   Create Time: 2019-12-07 15:49:24
 * Last Modified: 2019-12-07 16:23:40
 */
package main

import "fmt"

func main() {
	sum := 0
	for i := 0; i <= 10; i++ {
		sum += i
	}
	fmt.Println("Sum is", sum)

	nsum := 1
	for nsum < 10 {
		nsum += nsum
		fmt.Println("nsum is", nsum)
	}
	fmt.Println("nsum is", nsum)

	histring := "Hello,Golang!"

	for i, j := range histring {
		fmt.Println(i, j)
	}
}
