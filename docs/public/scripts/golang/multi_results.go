/*
 *      Filename: multi_results.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: function return multi results
 *   Create Time: 2019-11-24 23:03:27
 * Last Modified: 2019-11-24 23:33:20
 */
package main

import "fmt"

//func swap(str1, str2 string) (string, string) {
func swap(str1, str2 string) {
	return str2, str1
}

func main() {
	a, b := swap("hello", "world")
	fmt.Println(a, b)
}
