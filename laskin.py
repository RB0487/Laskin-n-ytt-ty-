import math
import re
import tkinter
import customtkinter as ctk
class Laskin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.history = []
        self.resizable(False, False)
        self.title("Laskin")
        self.geometry("525x500")

        self.expression = ""

        # Display
        self.display = ctk.CTkEntry(
            self,
            justify="right",
            height=60,
            corner_radius=5,
            font=("Arial", 20)
        )

        self.display.pack(padx=10, pady=10, fill="x")

        # Keyboard bindings
        self.bind("<Return>", lambda e: self.on_button_click("="))
        self.bind("<Key>", self.key_input)
        self.bind("<KP_Enter>", lambda e: self.on_button_click("="))
        self.bind("<KP_Space>",lambda e: self.on_button_click("="))

        # Buttons
        buttons = [
            ("C", 1, 0),
            ("(", 1, 1),
            (")", 1, 2),
            ("/", 1, 3),
            ("⌫", 1, 4),
            ("n!",1,5),

            ("7", 2, 1),
            ("8", 2, 2),
            ("9", 2, 3),
            ("*", 2, 0),
            ("π", 2, 4),
            ("log",2,5),
            ("↑",2,6),

            ("4", 3, 1),
            ("5", 3, 2),
            ("6", 3, 3),
            ("-", 3, 0),
            ("x^2", 3, 4),
            ("e",3,5),
            ("↓",3,6),

            ("1", 4, 1),
            ("2", 4, 2),
            ("3", 4, 3),
            ("+", 4, 0),
            ("√x", 4, 4),
            ("exp",4,5),

            (".", 5, 1),
            ("0", 5, 2),
            ("%", 5, 3),
            ("1/x", 5, 4),
            ("x^y", 5,5),
            ("+/-", 5, 0),
            ("Hist.", 1, 6),
        ]

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(padx=5, pady=5)

        for text, row, col in buttons:
            button = ctk.CTkButton(
                self.button_frame,
                text=text,
                font=("Arial", 20),
                width=65,
                height=65,
                corner_radius=15,
                command=lambda t=text: self.on_button_click(t),
                fg_color="#fdfdfd",
                text_color="#000000"
            )

            button.grid(row=row, column=col, padx=2, pady=2)

        # Equal button
        self.equal_btn = ctk.CTkButton(
            self.button_frame,
            text="=",
            font=("Arial", 20),
            width=375,
            height=65,
            corner_radius=15,
            command=lambda: self.on_button_click("="),
            fg_color="#412D2D"
        )

        self.equal_btn.grid(row=7, column=0, columnspan=7, padx=2, pady=2)
        
    #Formats given inputs and makes it so the calculation can go trought
    def format_expression(self, expr):
        # Constants
        expr = expr.replace("π", str(math.pi))
        expr = expr.replace("e", str(math.e))

        # Powers
        expr = expr.replace("^", "**")

        # Percentages
        expr = re.sub(r'(\d+(\.\d+)?)%', r'(\1/100)', expr)

        # Factorials
        expr = re.sub(r'(\d+)!', r'math.factorial(\1)', expr)

        while "√" in expr:
            index = expr.find("√")

            end = index + 1

            while end < len(expr) and expr[end] not in "+-*/":
                end += 1

            value = expr[index + 1:end]

            expr = (
                expr[:index]
                + f"math.sqrt({value})"
                + expr[end:]
            )
        # log(...)
        expr = expr.replace("log(", "math.log(")

        # exp(...)
        expr = expr.replace("exp(", "math.exp(")

        return expr 
    
    #Special Symbols and operatives (needs math libabary to function)
    def evaluate_expression(self):
        return eval(self.format_expression(self.expression), {"math": math})
   
    #Keyboard inputs and list of allowed inputs
    def key_input(self, event):
        allowed = "0123456789+-*/().%"

        if event.keysym == "Return":
            self.on_button_click("=")

        elif event.keysym == "BackSpace":
            self.on_button_click("⌫")

        elif event.char in allowed:
            self.on_button_click(event.char)

        #Buttons symbols and operatives
    def on_button_click(self, char):

        if char == "C":
            self.expression = ""
            self.update_display()

        elif char == "%":
            self.expression += "%"
            self.update_display()

        elif char == "1/x":
            self.expression = f"1/({self.expression})"
            self.update_display()

        
        elif char == "=":
            try:
             formatted = self.format_expression(self.expression)
             original = self.expression
             result = str(eval(formatted))
             self.history.append(f"{original} = {result}")
             self.expression = result
             self.update_display()
             self.update_history_display()
            except Exception as e:
                self.show_error()

        elif char == "⌫":
            self.expression = self.expression[:-1]
            self.update_display()

        elif char == "π":
            self.expression += "π"
            self.update_display()

        elif char == "x^2":
            self.expression += "^2"
            self.update_display()

        elif char == "√x":
            self.expression = f"√({self.expression})"
            self.update_display()
        elif char == "x^y":
            self.expression += "^"
            self.update_display()
        elif char == "n!":
            self.expression += "!"
            self.update_display()
        elif char == "log":
            self.expression = f"log({self.expression})"
            self.update_display()
        elif char == "e":
            try:
             self.expression += "e"
             self.update_display()
            except Exception:
                self.show_error()
        elif char == "exp":
            self.expression = f"exp({self.expression})"
            self.update_display()
        elif char == "+/-":
            try:
                val = self.evaluate_expression()
                result=str(-val)
                self.expression = result
                self.update_display()
            except Exception:
                self.show_error()
        elif char == "↑":
            try:
                val = self.evaluate_expression()
                result = math.ceil(val * 100000) / 100000
                self.expression = str(result)
                self.update_display()
            except Exception:
                self.show_error()

        elif char == "↓":
            try:
                val = self.evaluate_expression()
                result = math.floor(val * 100000) / 100000

                self.expression = str(result)
                self.update_display()
            except Exception:
                self.show_error()
        elif char == "Hist.":
            self.open_history_window()
        else:
            self.expression += char
            self.update_display()

    def update_display(self):
        self.display.delete(0, "end")
        self.display.insert(0, self.expression)
    def open_history_window(self):

        if hasattr(self, "history_window") and self.history_window.winfo_exists():
            self.history_window.lift()
            return

        self.history_window = ctk.CTkToplevel(self)
        self.history_window.title("Laskin historia")
        self.history_window.geometry("400x400")

        self.history_textbox = ctk.CTkTextbox(
            self.history_window,
            font=("Arial", 18)
        )
        self.history_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_history_display()
    def update_history_display(self):

        if not hasattr(self, "history_textbox"):
            return

        if not self.history_textbox.winfo_exists():
            return

        self.history_textbox.configure(state="normal")
        self.history_textbox.delete("1.0", "end")

        for item in self.history:
            self.history_textbox.insert("end", item + "\n")

        self.history_textbox.configure(state="disabled")
    def show_error(self):
        self.display.delete(0, "end")
        self.display.insert(0, "Error")
        self.expression = ""


app = Laskin()
app.mainloop()


#Shit that are broken/funky
#1. Function n!, 1/x, %, √x, x^2, x^y, log, exp. does the calculation straight and not show in history nor does show in calculator app. I want those function to become show in calculator monitor as for example: 1/2051, 8!, 100%, √25, 5^2, 6^9, log(91), exp(21) but still able to do the function normally
#2. if i do calculation like 2(3-1)/4 it gives error as output because the FIRST operation is done in int not as float value... 