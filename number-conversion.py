from tkinter import *
from tkinter import messagebox


def binary_to_decimal(binary_str):
    decimal_value = 0
    for bit in binary_str:
        decimal_value = decimal_value * 2 + int(bit)
    return decimal_value


def decimal_to_binary(decimal_num):
    binary_str = ""
    while decimal_num > 0:
        binary_str = str(decimal_num % 2) + binary_str
        decimal_num //= 2
    return binary_str if binary_str else "0"


def hexadecimal_to_octal(hex_str):
    decimal_value = int(hex_str, 16)
    octal_str = ""
    while decimal_value > 0:
        octal_str = str(decimal_value % 8) + octal_str
        decimal_value //= 8
    return octal_str if octal_str else "0"


def hexadecimal_to_binary(hex_str):
    binary_str = ""
    hex_str = hex_str.upper()
    hex_to_bin_map = {
        '0': '0000', '1': '0001', '2': '0010', '3': '0011',
        '4': '0100', '5': '0101', '6': '0110', '7': '0111',
        '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
        'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
    }
    for char in hex_str:
        binary_str += hex_to_bin_map[char]
    return binary_str


def binary_to_hexadecimal(binary_str):
    decimal_value = binary_to_decimal(binary_str)
    hex_str = ""
    hex_digits = "0123456789ABCDEF"
    while decimal_value > 0:
        hex_str = hex_digits[decimal_value % 16] + hex_str
        decimal_value //= 16
    return hex_str if hex_str else "0"



def main():
   
    def convert():
        number = entry_number.get()


        if var.get() == 1:
            if not all(bit in '01' for bit in number):
                messagebox.showerror("Input Error", "Please enter a valid binary number.")
                return
            result = binary_to_decimal(number)
           
        elif var.get() == 2:
            if not number.isdigit():
                messagebox.showerror("Input Error", "Please enter a number.")
                return
            result = decimal_to_binary(int(number))
           
        elif var.get() == 3:
            result = hexadecimal_to_octal(number)
           
        elif var.get() == 4:
            result = hexadecimal_to_binary(number)
           
        elif var.get() == 5:
            if not all(bit in '01' for bit in number):
                messagebox.showerror("Input Error", "Please enter a valid binary number.")
                return
            result = binary_to_hexadecimal(number)    
           
        else:
            messagebox.showerror("Selection Error", "Please select a conversion option.")
            return
       
        result_var.set(result)
       
    root = Tk()
    root.title("Number Conversion")
    root.geometry("350x270")
    root.resizable(0, 0)
       
    Label(root, text = "Enter the number:", font = ("Arial", 12)).place(x = 30, y = 5)
    entry_number = Entry(root, font = ("Arial", 12), width = 15, bd = 2, relief = "sunken")
    entry_number.place(x = 180, y = 5)


    var = IntVar()
    Radiobutton(root, text = "Binary to Decimal", font = ("Arial", 10), variable = var, value = 1, bg = "#F0F0F0").place(x = 20, y = 40)
    Radiobutton(root, text = "Decimal to Binary", font = ("Arial", 10), variable = var, value = 2, bg = "#F0F0F0").place(x = 20, y = 70)
    Radiobutton(root, text = "Hexadecimal to Octal", font = ("Arial", 10), variable = var, value = 3, bg = "#F0F0F0").place(x = 20, y = 100)
    Radiobutton(root, text = "Hexadecimal to Binary", font = ("Arial", 10), variable = var, value = 4, bg = "#F0F0F0").place(x = 20, y = 130)
    Radiobutton(root, text = "Binary to Hexadecimal", font = ("Arial", 10), variable = var, value = 5, bg = "#F0F0F0").place(x = 20, y = 160)


    Button(root, text="Convert", font = ("Arial", 12), command = convert, bd = 2, relief = "raised").place(x = 135, y = 190)
    Label(root, text = "Result: ", font = ("Arial", 12)).place(x = 35, y = 230)


    result_var = StringVar()
    Entry(root, textvariable = result_var, font = ("Arial", 12), width = 25, bd = 2, relief = "sunken", state = "readonly").place(x = 110, y = 230)


    root.mainloop()
   
if __name__ == "__main__":
    main()