/*
blink.go

To run:
tinygo flash -target arduino -port /dev/cu.usbmodem11301 blink.go
*/

package main

import (
	"machine"
	"time"
)

func main() {
	led := machine.LED
	led.Configure(machine.PinConfig{Mode: machine.PinOutput})
	for {
		led.High()
		time.Sleep(time.Millisecond * 1000)
		led.Low()
		time.Sleep(time.Millisecond * 1000)
	}
}
