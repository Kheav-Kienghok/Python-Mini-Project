from tkinter import filedialog, messagebox, Toplevel, Label, Text, Button, Tk, END
from fpdf import FPDF
import PyPDF2


class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager App")
        self.root.geometry("300x300")
        self.root.resizable(0, 0)
        self.pdf = FPDF()
        
        self.create_widgets()

    def create_widgets(self):
        
        Label(self.root, text = "Welcome to the PDF file manager", font = ("Arial", 12, "underline")).pack()
        
        self.content_box = Text(self.root, font=("Arial", 10), width=40, height=10)
        self.content_box.pack(pady = 10)

        Button(self.root, text = "Generate PDF", command = self.create_and_write_pdf_file).pack(pady = 10)

        Button(self.root, text = "Read from PDF File", command = self.read_pdf_file).pack(pady = 5)
 
    def create_and_write_pdf_file(self):
        content = self.content_box.get("1.0", END).strip()
        if not content:
            messagebox.showwarning("Warning", "The text box is empty.")
            return
  
        file_path = filedialog.asksaveasfilename(defaultextension = ".pdf", filetypes = [("PDF files", "*.pdf")])
        
        if file_path:
            self.pdf.add_page()
            self.pdf.set_font("Arial", size = 12)
            self.pdf.multi_cell(0, 10, content)
            self.pdf.output(file_path)
            messagebox.showinfo("Success", "PDF have been generated successfully!")
        else:
            messagebox.showwarning("Warning", "No file was created.")

    def read_pdf_file(self):
        file_path = filedialog.askopenfilename(defaultextension = ".pdf", filetypes = [("PDF files", "*.pdf")])
        
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    if reader.pages:
                        page = reader.pages[0]
                        content = page.extract_text()
                        if content:
                            new_file_name = file_path.split("/")[-1]
                            self.display_content(content, new_file_name)
                        else:
                            messagebox.showwarning("Warning", "The PDF file is empty or contains non-text content.")
                    else:
                        messagebox.showwarning("Warning", "The PDF file is empty.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while reading the PDF file: {e}")
        else:
            messagebox.showwarning("Warning", "No file was selected.")

            
    def display_content(self, content, file_name):
    
        list_window = Toplevel(self.root)
        list_window.title(file_name)

        list_text = Text(list_window, height = 30, width = 50)
        list_text.pack()
        
        list_text.insert(END, content)
        list_text.config(state = "disabled")

if __name__ == "__main__":
    root = Tk()
    app = FileManagerApp(root)
    root.mainloop()