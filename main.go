package main

import (
	"errors"
	"fmt"
)

func calculate(a int, b int, sign string) (int, error) {
	switch sign {
	case "+":
		return a + b, nil
	case "-":
		return a - b, nil
	case "*":
		return a * b, nil
	case "/":
		if b == 0 {
			return 0, errors.New("деление на ноль")
		}
		return a / b, nil
	default:
		return 0, errors.New("неизвестный оператор")
	}
}

func main() {
	result, e := calculate(10, 15, "+")
	if e != nil {
		fmt.Println("Ошибка:", e)
		return
	}
	fmt.Println(result)
}
