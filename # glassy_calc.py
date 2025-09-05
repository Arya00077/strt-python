# glassy_calc.py (Modified PyQt5 Calculator with Theme Toggle)
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QWidget, QToolBar, QToolButton, QLabel
)
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Glassy Calculator")
        self.setGeometry(100, 100, 400, 500)
        
        # Theme state
        self.is_dark = False
        self.current_opacity = 1.0
        
        # Central widget with glass-like styling
        central_widget = QWidget()
        central_widget.setAttribute(Qt.WA_TranslucentBackground)
        central_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 20px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)
        self.setCentralWidget(central_widget)
        
        # Toolbar with theme toggle
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)
        
        theme_button = QToolButton()
        theme_button.setIcon(QIcon())  # Placeholder; use a moon/sun icon in real app
        theme_button.setText("🌙 Dark Mode")
        theme_button.clicked.connect(self.toggle_theme)
        toolbar.addWidget(theme_button)
        
        # Layout
        layout = QVBoxLayout()
        
        # Display
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 150);
                border-radius: 10px;
                padding: 10px;
                font-size: 24px;
                margin: 10px;
            }
        """)
        layout.addWidget(self.display)
        
        # Buttons
        button_layout = QHBoxLayout()
        for text in ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "="]:
            button = QPushButton(text)
            button.clicked.connect(self.on_button_clicked)
            button_layout.addWidget(button)
        
        layout.addLayout(button_layout)
        central_widget.setLayout(layout)
        
        # Apply light theme initially
        self.apply_theme()
    
    def toggle_theme(self):
        self.is_dark = not self.is_dark
        # Animate opacity for smooth transition
        animation = QPropertyAnimation(self.centralWidget(), b"windowOpacity")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.setStartValue(self.current_opacity)
        animation.setEndValue(0.7)  # Fade to semi-transparent during transition
        animation.finished.connect(self.apply_theme)
        animation.start()
    
    def apply_theme(self):
        # Restore full opacity
        self.setWindowOpacity(1.0)
        self.current_opacity = 1.0
        
        if self.is_dark:
            stylesheet = """
                QWidget {
                    background-color: rgba(30, 30, 30, 200);
                    color: white;
                    border-radius: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
                QPushButton {
                    background-color: rgba(50, 50, 50, 150);
                    color: white;
                    border-radius: 5px;
                    padding: 15px;
                }
                QPushButton:hover { background-color: rgba(70, 70, 70, 150); }
                QLineEdit {
                    background-color: rgba(40, 40, 40, 150);
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 24px;
                    margin: 10px;
                }
            """
        else:
            stylesheet = """
                QWidget {
                    background-color: rgba(255, 255, 255, 180);
                    color: black;
                    border-radius: 20px;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                }
                QPushButton {
                    background-color: rgba(200, 200, 200, 150);
                    color: black;
                    border-radius: 5px;
                    padding: 15px;
                }
                QPushButton:hover { background-color: rgba(220, 220, 220, 150); }
                QLineEdit {
                    background-color: rgba(255, 255, 255, 150);
                    color: black;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 24px;
                    margin: 10px;
                }
            """
        self.setStyleSheet(stylesheet)
    
    def on_button_clicked(self):
        sender = self.sender()
        text = sender.text()
        current = self.display.text()
        
        if text == "=":
            try:
                result = str(eval(current))  # Simple eval for demo; use safe_eval in production
                self.display.setText(result)
            except:
                self.display.setText("Error")
        elif text in ["+", "-", "*", "/"]:
            if current and not current[-1].isalpha():
                self.display.setText(current + text)
        else:
            self.display.setText(current + text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # For consistent look
    window = Calculator()
    window.show()
    sys.exit(app.exec_())