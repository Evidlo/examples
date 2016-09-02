// Evan Widloski
package main

import (
	"fmt"
	"math"
)

func times(x int, y int) int {
	return x * y
}

func multi_return(x int, y int) (int, int) {
	return x, y
}

func naked_return(x int, y int) (a int, b int) {
	a = x
	b = y
	return

}

// sieve of atkins
func get_primes(n int) []int {
	primes := []int{2}

	for i := 3; i <= n; i++ {
		is_prime := true
		for _, prime := range primes {
			if math.Mod(float64(i), float64(prime)) == 0 {
				is_prime = false
				break
			}
			if prime >= int(math.Sqrt(float64(n))) {
				break
			}
		}
		if is_prime {
			primes = append(primes, i)
		}
	}
	return primes
}

func main() {
	// fmt.Println("hello world!")

	// fmt.Println(times(2, 3))

	// a, b := multi_return(2, 3)
	// fmt.Println(a)
	// fmt.Println(b)

	// a, b = naked_return(2, 3)
	// fmt.Println(a)
	// fmt.Println(b)

	fmt.Println(get_primes(100000))
}
