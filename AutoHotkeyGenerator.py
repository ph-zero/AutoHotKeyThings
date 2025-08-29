import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QScrollArea,
                             QGridLayout, QMessageBox, QFrame, QComboBox, QGroupBox, QRadioButton)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush

class AHKGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoHotkey Script Generator")
        self.setGeometry(100, 100, 1200, 850)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QWidget {
                color: white;
                font-family: 'Segoe UI';
            }
            QLabel {
                padding: 5px;
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid #6cbbf2;
                border-radius: 5px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 0.15);
                border: 2px solid #6cbbf2;
            }
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border: none;
                border-radius: 5px;
                color: white;
                padding: 12px 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #3498db);
            }
            QPushButton#copy-btn {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
            }
            QPushButton#copy-btn:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #2ecc71);
            }
            QPushButton#reset-btn {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
            }
            QPushButton#reset-btn:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c0392b, stop:1 #e74c3c);
            }
            QComboBox {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid #6cbbf2;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: #2c3e50;
                color: white;
                selection-background-color: #6cbbf2;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #6cbbf2;
                border-left-style: solid;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QComboBox::down-arrow {
                image: url(none);
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6cbbf2;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #6cbbf2;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                color: #6cbbf2;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
            }
            QRadioButton {
                spacing: 8px;
                font-size: 14px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid #6cbbf2;
                background: rgba(255, 255, 255, 0.1);
            }
            QRadioButton::indicator:checked {
                background: #6cbbf2;
                border: 2px solid #6cbbf2;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Monaco', monospace;
                border-radius: 5px;
                padding: 10px;
            }
            QFrame {
                background-color: rgba(255, 255, 255, 0.08);
                border-radius: 10px;
            }
        """)
        
        self.initUI()
        
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("AutoHotkey Script Generator")
        header.setAlignment(Qt.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: #6cbbf2; margin-bottom: 10px;")
        layout.addWidget(header)
        
        subtitle = QLabel("Create custom scripts for Shift + Function key combinations")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #a8d8ea; font-size: 14px; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Version selection
        version_group = QGroupBox("AutoHotkey Version")
        version_layout = QHBoxLayout(version_group)
        
        self.v1_radio = QRadioButton("AutoHotkey v1.0 (Legacy)")
        self.v1_radio.setChecked(True)
        self.v2_radio = QRadioButton("AutoHotkey v2.0 (Latest)")
        
        version_layout.addWidget(self.v1_radio)
        version_layout.addWidget(self.v2_radio)
        version_layout.addStretch()
        
        layout.addWidget(version_group)
        
        # Instructions
        instructions = QLabel(
            "This tool generates an AutoHotkey script that will output custom text "
            "when you press Shift + any function key (F1 to F12).\n\n"
            "Simply enter the text you want each key combination to produce, then click 'Generate Script'. "
            "You can use dynamic fields like {A_YYYY} for current year, {A_MM} for month, etc."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.5;
        """)
        layout.addWidget(instructions)
        
        # Input fields for F1-F12
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: transparent; border: none;")
        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        self.input_fields = []
        for i in range(12):
            row = i // 3
            col = i % 3
            
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: rgba(0, 0, 0, 0.2);
                    border-radius: 8px;
                }
            """)
            frame_layout = QVBoxLayout(frame)
            frame_layout.setContentsMargins(15, 15, 15, 15)
            
            label = QLabel(f"Shift + F{i+1}:")
            label.setStyleSheet("color: #6cbbf2; font-weight: bold;")
            
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Text to output when Shift+F{i+1} is pressed")
            
            frame_layout.addWidget(label)
            frame_layout.addWidget(input_field)
            scroll_layout.addWidget(frame, row, col)
            
            self.input_fields.append(input_field)
        
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        generate_btn = QPushButton("Generate Script")
        generate_btn.clicked.connect(self.generate_script)
        
        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.setObjectName("copy-btn")
        copy_btn.clicked.connect(self.copy_to_clipboard)
        
        reset_btn = QPushButton("Reset Form")
        reset_btn.setObjectName("reset-btn")
        reset_btn.clicked.connect(self.reset_form)
        
        button_layout.addWidget(generate_btn)
        button_layout.addWidget(copy_btn)
        button_layout.addWidget(reset_btn)
        layout.addLayout(button_layout)
        
        # Output
        output_label = QLabel("Generated AutoHotkey Script")
        output_label.setStyleSheet("color: #6cbbf2; font-size: 18px; font-weight: bold;")
        layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText(
            "; Your AutoHotkey script will appear here\n"
            "; Fill out the form above and click 'Generate Script'"
        )
        layout.addWidget(self.output_text)
        
        # Footer
        footer = QLabel(
            "Note: To use this script, save it as a .ahk file and run it with AutoHotkey installed on your system. "
            "Make sure to use the correct version of AutoHotkey for your script."
        )
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 12px; margin-top: 10px;")
        layout.addWidget(footer)
    
    def generate_script(self):
        is_v2 = self.v2_radio.isChecked()
        
        if is_v2:
            script_lines = [
                "; AutoHotkey v2.0 Script Generated by Python UI",
                "; Shift + Function Key Text Expander",
                "",
                "#Requires AutoHotkey v2.0",
                "",
                "; Shift + Function key hotkeys with text output",
                ""
            ]
        else:
            script_lines = [
                "; AutoHotkey v1.0 Script Generated by Python UI",
                "; Shift + Function Key Text Expander",
                "",
                "#NoEnv",
                "SendMode Input",
                "SetWorkingDir %A_ScriptDir%",
                "",
                "; Shift + Function key hotkeys with text output",
                ""
            ]
        
        for i, input_field in enumerate(self.input_fields):
            text = input_field.text().strip()
            if text:
                # Replace AHK variables with the proper format
                text = self.process_ahk_variables(text, is_v2)
                
                if is_v2:
                    script_lines.extend([
                        f"+F{i+1}:: {{",
                        f"    Send \"{text}\"",
                        "}",
                        ""
                    ])
                else:
                    script_lines.extend([
                        f"+F{i+1}::",
                        f"    Send, {text}",
                        "    Return",
                        ""
                    ])
        
        if is_v2:
            script_lines.extend([
                "; Add more hotkeys as needed",
                "",
                "Esc:: {",
                "    MsgBox \"Exit Script? Press OK to exit\", \"Exit Confirmation\", \"OKCancel\"",
                "    if (MsgBoxResult = \"OK\")",
                "        ExitApp",
                "}"
            ])
        else:
            script_lines.extend([
                "; Add more hotkeys as needed",
                "",
                "Esc::",
                "    MsgBox, Exit Script? Press OK to exit",
                "    ExitApp",
                "Return"
            ])
        
        script = "\n".join(script_lines)
        self.output_text.setPlainText(script)
    
    def process_ahk_variables(self, text, is_v2):
        # Replace our placeholder format with proper AHK variables
        replacements = {
            "{A_YYYY}": "{A_YYYY}" if is_v2 else "%A_YYYY%",
            "{A_YY}": "{A_YY}" if is_v2 else "%A_YY%",
            "{A_MM}": "{A_MM}" if is_v2 else "%A_MM%",
            "{A_DD}": "{A_DD}" if is_v2 else "%A_DD%",
            "{A_Hour}": "{A_Hour}" if is_v2 else "%A_Hour%",
            "{A_Min}": "{A_Min}" if is_v2 else "%A_Min%",
            "{A_Sec}": "{A_Sec}" if is_v2 else "%A_Sec%",
            "{A_MSec}": "{A_MSec}" if is_v2 else "%A_MSec%",
            "{A_Now}": "{A_Now}" if is_v2 else "%A_Now%",
            "{A_TickCount}": "{A_TickCount}" if is_v2 else "%A_TickCount%",
            "{A_UserName}": "{A_UserName}" if is_v2 else "%A_UserName%",
            "{A_ComputerName}": "{A_ComputerName}" if is_v2 else "%A_ComputerName%",
            "{Clipboard}": "{A_Clipboard}" if is_v2 else "%Clipboard%",
            "{Enter}": "{Enter}" if is_v2 else "{Enter}",
            "{Tab}": "{Tab}" if is_v2 else "{Tab}",
            "{Space}": "{Space}" if is_v2 else "{Space}",
            "{Backspace}": "{Backspace}" if is_v2 else "{Backspace}"
        }
        
        for placeholder, replacement in replacements.items():
            text = text.replace(placeholder, replacement)
        
        return text
    
    def copy_to_clipboard(self):
        script = self.output_text.toPlainText()
        if script.strip():
            clipboard = QApplication.clipboard()
            clipboard.setText(script)
            QMessageBox.information(self, "Copied", "Script copied to clipboard!")
        else:
            QMessageBox.warning(self, "Warning", "No script to copy. Please generate a script first.")
    
    def reset_form(self):
        for input_field in self.input_fields:
            input_field.clear()
        self.output_text.clear()
        self.v1_radio.setChecked(True)
        self.output_text.setPlaceholderText(
            "; Your AutoHotkey script will appear here\n"
            "; Fill out the form above and click 'Generate Script'"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = AHKGeneratorApp()
    window.show()
    
    sys.exit(app.exec_())