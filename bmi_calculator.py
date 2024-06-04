from tkinter import *
from tkinter import messagebox
from webbrowser import open as open_url


def main():
    
    def bmi_calculate():

        if not user_height.get().isdigit() or not user_weight.get().isdigit():
            messagebox.showerror("Error", "Please enter valid numbers!")
            return None, None

        height_in_m = float(user_height.get()) * 0.01     #Convert cm to m
        weight_in_kg = float(user_weight.get())

        if height_in_m <= 0 or weight_in_kg <= 0:
            messagebox.showerror("Error", "Height and Weight cannot be less than or equal to zero!")
            return None, None
        
        bmi_value = weight_in_kg / (height_in_m * height_in_m)
        
        if bmi_value < 18.5:
            result = "Underweight"      
        elif bmi_value < 25:
            result = "Normal"
        elif bmi_value < 30:
            result = "Overweight"
        else:
            result = "Obese"
        
        return bmi_value, result
    
    def show_bmi():
        
        bmi_value, result = bmi_calculate()
        
        if bmi_value is None or result is None:
            return
        
        if result == "Underweight":
            click_btn.config(text=f"Click here for more information about {result.lower()}", command = open_link_underweight)
            click_btn.place(x = 150, y = 330)
        elif result == "Overweight" or result == "Obese":
            click_btn.config(text=f"Click here for more information about {result.lower()}", command = open_link_obesity)
            click_btn.place(x = 150, y = 330)
        else:
            click_btn.place_forget()
        
        final_result.config(text=f"{user_name.get().capitalize()}'s BMI is {result} with a score of {bmi_value:.1f}")
        
        
    def open_link_underweight():
        open_url("https://www.healthdirect.gov.au/what-to-do-if-you-are-underweight")
    
    def open_link_obesity():
        open_url("https://www.healthdirect.gov.au/obesity")
        

    root = Tk()
    root.title("BMI Calculation")
    root.geometry("700x500")
    root.resizable(0, 0)

    Label(root, text = "Welcome to BMI Calculation", font = ("Arial", 25, "bold")).place(x = 130, y = 10)
    Label(root, text = "Please enter your height in cm and weight in kg to get your BMI result", font = ("Arial", 15)).place(x = 50, y = 70)

    Label(root, text = "Name:", font = ("Arial", 13)).place(x = 170, y = 120)
    user_name = Entry(root, textvariable = StringVar(), font = ("Arial", 13))
    user_name.place(x = 450, y = 120)

    Label(root, text = "Height in cm:", font = ("Arial", 13)).place(x = 150, y = 150)
    user_height = Entry(root, textvariable = StringVar(), font = ("Arial", 13))
    user_height.place(x = 450, y = 150)

    Label(root, text = "Weight in kg:", font = ("Arial", 13)).place(x = 150, y = 180)
    user_weight = Entry(root, textvariable = StringVar(), font = ("Arial", 13))
    user_weight.place(x = 450, y = 180)
    
    
    Button(root, text = "Calculate", font = ("Arial", 14), fg = "white", bg = "Green", width = 10, height = 2, command = show_bmi).place(x = 295, y = 220)

    final_result = Label(root, text = "", font = ("Arial", 13))
    final_result.place(x = 190, y = 300)
    
    click_btn = Button(root, text = "", font = ("Arial", 12), fg = "white", bg = "Blue", width = 45, height = 2)
    click_btn.place_forget()

    Button(root, text = "Exit", font = ("Arial", 14), fg = "White", bg = "Red", width = 6, height = 2, command = root.quit).place(x = 310, y = 385)

    root.mainloop()
    
    
if __name__ == "__main__":
    main()