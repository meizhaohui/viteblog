/*
 *      Filename: base_defer.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: defer语句的使用
 *   Create Time: 2019-12-07 21:27:21
 * Last Modified: 2019-12-07 22:54:38
 */
package main

import "fmt"

func main() {
	defer fmt.Println("World")
	fmt.Println("Hello")
	for i := 0; i < 4; i++ {
		defer fmt.Println(i)
	}
}
