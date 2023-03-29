import serial
import serial.tools.list_ports
import tkinter as tk
import tkinter.ttk as ttk

# Find available serial ports
available_ports = [port.device for port in serial.tools.list_ports.comports()]

# Print the list of available ports to the console
print("Available serial ports:")
for port in available_ports:
    print("- {}".format(port))

# Create a list of available baud rates
baud_rates = [9600, 19200, 38400, 57600, 115200]

# Define a function to update the frequency label with the current value
def update_frequency():
    try:
        # Read an integer value from UART representing a period in milliseconds
        period_ms = int(ser.readline().decode().strip())
        print(period_ms)
        period_ms = period_ms*10
        
        # Convert the period to a frequency in Hz
        frequency = 1000.0 / period_ms
        #print(frequency)
        # Update the frequency label with the result
        frequency_label.config(text="Frequency: {:.3f} Hz".format(frequency))
    except (ZeroDivisionError,ValueError):
        # If the input is not a valid integer, ignore it
        pass

    # Schedule the next update after a short delay
    root.after(100, update_frequency)

# Define a function to update the serial port when the dropdown is changed
def update_port(*args):
    global ser
    selected_port = port_variable.get()
    ser.close()
    ser = serial.Serial(selected_port, baud_variable.get())
    ser.timeout = 1

# Create the main window
root = tk.Tk()
root.title("Frequency Monitor")
root.geometry("800x600")

# Create a custom style
style = ttk.Style()
style.theme_use("clam")
style.configure(".", font=("Arial", 10), foreground="black", background="white")
style.configure("TLabel", padding=5)
style.configure("TButton", padding=5)
style.configure("TCombobox", padding=5)

# Create dropdown menu for selecting the serial port
port_variable = tk.StringVar(root)
port_variable.set(available_ports[0])
port_menu = ttk.Combobox(root, textvariable=port_variable, values=available_ports, state="readonly")
port_menu.bind("<<ComboboxSelected>>", update_port)
port_menu.pack(pady=5)

# Create dropdown menu for selecting the baud rate
baud_variable = tk.IntVar(root)
baud_variable.set(baud_rates[0])
baud_menu = ttk.Combobox(root, textvariable=baud_variable, values=baud_rates, state="readonly")
baud_menu.bind("<<ComboboxSelected>>", update_port)
baud_menu.pack(pady=5)

# Open the initial serial port
ser = serial.Serial(port_variable.get(), baud_variable.get())
ser.timeout = 1

# Create a label to display the frequency value
frequency_label = ttk.Label(root, text="", font=("Arial", 14))
frequency_label.pack(pady=20)

# Start the update loop
update_frequency()

# Start the main event loop
root.mainloop()
