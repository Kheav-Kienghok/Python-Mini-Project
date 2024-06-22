from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QFont
import requests
import os
import sys
import time


class ChatBotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.API_KEY = os.getenv("open_ai")    # Fetching API key from environment variables for security
        self.BASE_URL = 'https://api.deepinfra.com/v1/openai/chat/completions'
        self.context = {"name": "User"}  # Initial context with default user name
        self.request_times = []  # Track request times for rate limiting
        self.RATE_LIMIT = 5  # Max 5 requests
        self.TIME_WINDOW = 60  # Per 60 seconds
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ChatBot')
        
        # Center the window on the screen
        screen = QApplication.primaryScreen().geometry()
        window_width, window_height = 700, 600
        self.setGeometry(
            (screen.width() - window_width) // 2,
            (screen.height() - window_height) // 2,
            window_width,
            window_height
        )
        
        self.setFixedSize(window_width, window_height)  # Set fixed size for the window

        font = QFont('Poppins', 12)

        # Text area to display chat history
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setFont(font)

        # Input box for user messages
        self.input_box = QLineEdit(self)
        self.input_box.setFont(font)
        self.input_box.returnPressed.connect(self.send_message)  # Connect Enter key to send message

        # Send button to send user message
        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setFont(font)

        # Layout for arranging widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(self.text_area)
        layout.addWidget(self.input_box)
        layout.addWidget(self.send_button)

        # Container widget to hold the layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def send_message(self):
        message = self.input_box.text()
        self.input_box.clear()
        
        if message.startswith('/'):
            self.handle_command(message)
            
        else:
            user_message = f'<span style="color: blue;">{self.context["name"]}: {message}</span>'

            self.text_area.append(user_message)
            
            # Check if rate limit is exceeded before sending AI response
            if self.is_rate_limited():
                error_message = f'<span style="color: red;">Meta-Llama: Rate limit exceeded. Please wait.</span>'
                self.text_area.append(error_message)
            else:
                # Use QTimer to delay AI response for a smoother experience
                QTimer.singleShot(100, lambda: self.display_ai_response(message))
                
    def get_chatbot_response(self, user_input):
        headers = {
            'Authorization': f'Bearer {self.API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            "model": "meta-llama/Meta-Llama-3-8B-Instruct",
            "messages": [
                {"role": "user", "content": user_input}
            ]
        }
        
        try:
            response = requests.post(self.BASE_URL, headers=headers, json=data)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    def is_rate_limited(self):
        current_time = time.time()
        self.request_times = [t for t in self.request_times if current_time - t <= self.TIME_WINDOW]

        if len(self.request_times) >= self.RATE_LIMIT:
            return True
        
        self.request_times.append(current_time)
        return False
            

    def display_ai_response(self, message):
        result = self.get_chatbot_response(message)

        ai_message = f'<span style="color: green;">Meta-Llama: {result}</span>'
        self.text_area.append(ai_message)
            
    def handle_command(self, command):
        if command == '/help':
            help_message = """
            <div style="text-align: center;">
                <span style="color: red;">List of commands...</span><br>
                <span style="color: red;">=========================</span>
            </div>
            
            <div style="text-align: left;">
                <span style="color: red;">/info - Provides information about the AI</span><br>
                <span style="color: red;">/exit - Exits the application</span><br>
                <span style="color: red;">/name [your_name] - Sets your name in the conversation context</span><br>
                <span style="color: red;">/clear - Clears the conversation history</span><br>
                <span style="color: red;">/time - Provides the current time</span><br>
            </div>
            """
            self.text_area.append(help_message)
            
        elif command == '/info':
            info_message = """ 
            <div style="text-align: center;">
                <span style="color: green;"><b>Info:</b> Meta Llama 3 Announcement</span><br>
            </div>
            
            <span style="color: green;">Today, Meta Llama 3 models are released for broad use.
                These models include 8B and 70B parameter variants, pretrained and fine-tuned for various tasks, 
                showcasing state-of-the-art performance across industry benchmarks. New capabilities include enhanced 
                reasoning abilities. Meta Llama 3 models are touted as the best open-source models in their class, 
                encouraging community innovation. Meta supports open access to foster advancements in AI across 
                applications, developer tools, evaluations, inference optimizations, and beyond. We're eager to see your 
                creations and welcome your feedback.
            </span>
            
            """
            self.text_area.append(info_message)

        elif command == '/exit':
            self.close()
            
        elif command.startswith('/name '):
            name = command.split(' ', 1)[1]
            self.context["name"] = name
            
            user_message = f""" 
            <div style="text-align: center;">
                <span style="color: red;">Username have been set to "{name}"</span>
            </div>
            <div style="text-align: left;">
            </div>
            """
            
            self.text_area.append(user_message)
            
        elif command == '/clear':
            self.text_area.clear()
            
        elif command == '/time':
            current_time = QDateTime.currentDateTime().toString()
            self.text_area.append(f'<span style="color: red;">Meta-Llama: Current time: {current_time}</span>')
            
        else:
            self.text_area.append(f'<span style="color: red;">Unknown command: {command}</span>')

 
if __name__ == '__main__':
    # Main application entry point
    app = QApplication(sys.argv)
    gui = ChatBotGUI()
    gui.show()
    sys.exit(app.exec_())