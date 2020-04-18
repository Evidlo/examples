package main

import (
	// "os"
	"time"
	"fmt"
)

func test(c chan int) {

	n := 0
	// loop forever
	for {
		fmt.Println("generating next value")
		c <- n
		n++
	}
}

func main() {

	c := make(chan int)

	go test(c)

	for i := 0; i < 10; i++ {
		time.Sleep(1000 * time.Millisecond)
		fmt.Println("retrieving next value from channel")
		val := <-c
		fmt.Println("value retrieved:", val)

	}
}
