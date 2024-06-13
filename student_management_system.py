import mysql.connector
from tkinter import *

# Disable this three lines  
with open("secret.txt", "r") as file:
    username = file.readline()
    password = file.readline()

def connect_to_db():
    global db
    try:
        db = mysql.connector.connect(
            host = "localhost",
            user = username,    # Replace with your actual user name
            password = password,  # Replace with your actual password
            database = "Student_database"  # Replace with your actual database name
        )
        
        cursor = db.cursor()
    
        cursor.execute("""CREATE TABLE IF NOT EXISTS student (
                Student_ID INTEGER PRIMARY KEY,
                Name VARCHAR(50),
                Major VARCHAR(50),
                Address VARCHAR(255),
                Gender VARCHAR(10),
                Birthdate VARCHAR(25));
                 """)
        
    except mysql.connector.Error as err:
        status_label.config(text = f"Error connecting to database: {str(err)}", fg = "red")


def add_student():
    try:
        studentID = studentID_entry.get()
        name = name_entry.get()
        major = major_entry.get()
        address = address_entry.get()
        gender = gender_entry.get()
        birth = dob_entry.get()

        # Validate entries (add checks for other fields as needed)
        if not name or not major or not address or not gender or not studentID or not birth:
            raise ValueError("Please fill in all required fields.")
        
        new_student_info = [studentID, name, major, address, gender, birth]
    
        # Check if the new entries match the example student info
        if new_student_info == example_student_info:
            raise ValueError("Information already exists. Provide new information.")

        # Connect to database if not already connected
        if not db:
            connect_to_db()

        cursor = db.cursor()
        sql = """
            INSERT INTO student (Student_ID, Name, Major, Address, Gender, Birthdate)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (studentID, name, major, address, gender, birth))
        db.commit()

        status_label.config(text = "Student added successfully!", fg = "green")

        # Clear entry fields for next input
        name_entry.delete(0, END)
        major_entry.delete(0, END)
        address_entry.delete(0, END)
        gender_entry.delete(0, END)
        studentID_entry.delete(0,END)
        dob_entry.delete(0, END)

    except (mysql.connector.Error, ValueError) as err:
        status_label.config(text = f"{str(err)}", fg="red")

def list_students():
    try:
        if not db:
            connect_to_db()

        cursor = db.cursor()
        cursor.execute("SELECT * FROM student")
        students = cursor.fetchall()

        # Create a new window to display the list of students
        list_window = Toplevel(root)
        list_window.title("List of Students")

        # Create a text widget to display the list
        list_text = Text(list_window, height=10, width=50)
        list_text.pack()

        # Insert student records into the text widget
        for student in students:
            list_text.insert(END, f"Student ID: {student[0]}\nName: {student[1]}\nMajor: {student[2]}\nAddress: {student[3]}\nGender: {student[4]}\nDate of Birth: {student[5]}\n\n")

    except mysql.connector.Error as err:
        status_label.config(text = f"Error: {str(err)}", fg = "red")

def update_student():
    try:
        if not db:
            connect_to_db()

        cursor = db.cursor()

        # Retrieve user input
        student_id = studentID_entry_update.get()
        field = field_entry.get()
        new_value = new_value_entry.get()

        # Validate user input
        if not student_id or not field or not new_value:
            raise ValueError("Please fill in all required fields.")

        # Construct SQL query
        sql = f"UPDATE student SET {field} = %s WHERE Student_ID = %s"
        cursor.execute(sql, (new_value, student_id))
        db.commit()

        status_label.config(text = "Student record updated successfully!", fg = "green")

    except (mysql.connector.Error, ValueError) as err:
        status_label.config(text = f"Error: {str(err)}", fg = "red")


root = Tk()
root.title("Student Management System")
root.geometry("327x400")
root.resizable(0, 0)

example_student_info = ["0003638", "John Doe", "Computer Science", "Phnom Penh, Cambodia", "Male", "2000-01-01"]

# Label and Entry fields using grid layout
Label(root, text = "Name:", font = ("Arial", 11, "bold")).grid(row = 0, column = 0, sticky="w")
name_entry = Entry(root, font = ("Arial", 10), width = 29)
name_entry.grid(row = 0, column = 1)
name_entry.insert(0, f"{example_student_info[1]}")
name_entry.bind("<Button-1>", lambda exit: name_entry.delete(0, "end"))

Label(root, text = "Major:", font = ("Arial", 11, "bold")).grid(row = 1, column = 0, sticky = "w")
major_entry = Entry(root, font = ("Arial", 10), width = 29)
major_entry.grid(row = 1, column = 1)
major_entry.insert(0, f"{example_student_info[2]}")
major_entry.bind("<Button-1>", lambda exit: major_entry.delete(0, "end"))


Label(root, text="Address:", font = ("Arial", 11, "bold")).grid(row = 2, column = 0, sticky = "w")
address_entry = Entry(root, font = ("Arial", 10), width = 29)
address_entry.grid(row = 2, column = 1)
address_entry.insert(0, f"{example_student_info[3]}")
address_entry.bind("<Button-1>", lambda exit: address_entry.delete(0, "end"))

Label(root, text = "Gender:", font = ("Arial", 11, "bold")).grid(row = 3, column = 0, sticky = "w")
gender_entry = Entry(root, font = ("Arial", 10), width = 29)
gender_entry.grid(row = 3, column = 1)
gender_entry.insert(0, f"{example_student_info[4]}")
gender_entry.bind("<Button-1>", lambda exit: gender_entry.delete(0, "end"))

Label(root, text = "Student ID:", font = ("Arial", 11, "bold")).grid(row = 4, column = 0, sticky = "w")
studentID_entry = Entry(root, font = ("Arial", 10), width = 29)
studentID_entry.grid(row = 4, column = 1)
studentID_entry.insert(0, f"{example_student_info[0]}")
studentID_entry.bind("<Button-1>", lambda exit: studentID_entry.delete(0, "end"))

Label(root, text = "Date of Birth:", font = ("Arial", 11, "bold")).grid(row = 5, column = 0,  sticky = "w")
dob_entry = Entry(root, font = ("Arial", 10), width = 29)
dob_entry.grid(row = 5, column = 1)
dob_entry.insert(0, f"{example_student_info[5]}")
dob_entry.bind("<Button-1>", lambda exit: dob_entry.delete(0, "end"))

# Add button
add_button = Button(root, text = "Add Student", bg = "Green", fg = "white", font = ("Arial", 10), command = add_student)
add_button.grid(row = 6, column = 0, columnspan = 2, pady = 15)

# Add button to list all students
list_button = Button(root, text = "List All Students", bg = "Green", fg = "white", font = ("Arial", 10), command = list_students)
list_button.grid(row = 13, column = 0, columnspan = 2, pady = 5)


Label(root, text = "Student ID:", font = ("Arial", 11, "bold")).grid(row = 8, column = 0, sticky = "w")
studentID_entry_update = Entry(root, font = ("Arial", 10), width = 29)
studentID_entry_update.grid(row = 8, column = 1, pady = 5)

Label(root, text = "Field to update:", font = ("Arial", 11, "bold")).grid(row = 9, column = 0, sticky = "w")
field_entry = Entry(root, font = ("Arial", 10), width = 29)
field_entry.grid(row=9, column=1)

Label(root, text = "New value:", font = ("Arial", 11, "bold")).grid(row = 10, column = 0, sticky = "w")
new_value_entry = Entry(root, font = ("Arial", 10), width = 29)
new_value_entry.grid(row=10, column=1)

# Add button to update student record
update_button = Button(root, text = "Update Student", bg = "Green", fg = "white", font = ("Arial", 10), command = update_student)
update_button.grid(row = 11, column = 0, columnspan = 2, pady = 10)


# Status label for feedback
status_label = Label(root, text = "")
status_label.grid(row = 7, column = 0, columnspan = 2)

# Connect to database automatically (uncomment if preferred)
connect_to_db()

# Main event loop
root.mainloop()