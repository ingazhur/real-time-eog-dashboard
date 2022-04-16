/*
read.go

To run:
tinygo flash -target arduino -port /dev/cu.usbmodem11301 read.go
*/

package main

import (
	"machine"
	"time"
)

func main() {
	machine.InitADC()
	analogPin := machine.ADC{0}
	analogPin.Configure(machine.PinConfig{Mode: machine.PinOutput})

	for {
		myTime := time.Now()
		print(myTime, " ", analogPin.Get(), "\n")
		time.Sleep(time.Millisecond * 4)
	}
}
