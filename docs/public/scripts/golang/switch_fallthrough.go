/*
 *      Filename: switch_fallthrough.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: switch语句中使用fallthrough关键字
 *   Create Time: 2019-12-07 21:07:54
 * Last Modified: 2019-12-07 21:13:06
 */
package main

import "fmt"

func main() {
	switch {
	case false:
		fmt.Println("1. condition is false.")
		fallthrough
	case true:
		fmt.Println("2. condition is true.")
		fallthrough
	case false:
		fmt.Println("3. condition is false.")
		fallthrough
	case true:
		fmt.Println("4. condition is true.")
	case false:
		fmt.Println("5. condition is false.")
		fallthrough
	default:
		fmt.Println("6. default case")
	}
}
