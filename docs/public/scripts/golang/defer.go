/*
 *      Filename: defer.go
 *        Author: Zhaohui Mei<mzh.whut@gmail.com>
 *   Description: defer语句的使用
 *   Create Time: 2019-12-07 21:27:21
 * Last Modified: 2019-12-07 23:09:10
 */
package main

import (
	"fmt"
	"os"
)

func main() {
	f := createFile("./defer.txt")
	defer closeFile(f)
	writeFile(f)
}

func createFile(p string) *os.File {
	fmt.Println("creating")
	f, err := os.Create(p)
	if err != nil {
		panic(err)
	}
	return f
}
func writeFile(f *os.File) {
	fmt.Println("writing")
	f.Write([]byte("hello golang!\n"))
}

func closeFile(f *os.File) {
	fmt.Println("closing")
	f.Close()
}
