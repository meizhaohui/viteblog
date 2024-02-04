/*
 *      Filename: functions.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: go function
 *   Create Time: 2019-11-24 22:32:44
 * Last Modified: 2019-11-24 22:40:20
 */
package main

import "fmt"

func add(x int, y int) int {
	return x + y
}

func main() {
	fmt.Printf("%d + %d = %d\n", 11, 22, add(11, 22))
}
