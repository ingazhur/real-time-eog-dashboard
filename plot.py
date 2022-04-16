'''
This script:
1) reads EOG data from serial port
2) plots it in real time
3) saves it to a CSV file

An alternative to Arduino's serial plotter feature that doesn't autoscale.
Used to verify that the Arduino is able to pick up blinks and eye movements from the EOG circuit.
'''
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import subprocess
import serial

period = 3.9 # Arduino writes into serial port every 3.9ms (~ 256Hz sampling frequency)

# setup .csv file
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y-%H:%M:%S")
csvfilename = "data/{}.csv".format(dt_string)
csvfile = open(csvfilename, 'x')
fieldnames = ['millis', 'adc']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

# display possible serial ports to read the data from
output = subprocess.run(["ls /dev/tty.*"], stdout=subprocess.PIPE, shell=True, text=True)
ports = output.stdout.split("\n")[:-1]
i = 0
print("\n>> Select UART/USB to read from:\n")
for port in ports:
    print("  ", i, ":", port)
    i += 1
index = int(input("\n>> ")) # prompt serial port selection
port = ports[index]
print("\nOK, opening", port)

# initialize serial port
ser = serial.Serial(port=port, baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
if ser.is_open == True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n") # print serial parameters

# Parameters
x_len = 200         # Number of points to display (arbitrary)
y_range = [0, 1023]  # Range of possible Y values to display; 10-bit ADC

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)

line, = ax.plot(xs, ys)

# Add labels
plt.title('ADC readings over Time')
plt.xlabel('Samples')
plt.ylabel('ADC [0-1023]')

# This function is called periodically from FuncAnimation
def animate(i, ys):
    # parsing millis and adc from serial port
    millis, adc = str(ser.readline())[2:][:-5].split(" ")
    millis, adc = int(millis), int(adc)

    ys.append(adc)
    print(millis, adc)
    writer.writerow({'millis': millis, 'adc': adc})

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)

    return line,

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=period,
    blit=True)

plt.show()