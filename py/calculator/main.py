import tkinter as tk
import math

BIG_FONT_STYLE = ("Verdana", 40, "bold")
SMALL_FONT_STYLE = ("Verdana", 16)
NUMBERS_FONT_STYLE = ("Verdana", 24, "bold")
DEFAULT_FONT_STYLE = ("Verdana", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"


class CalcApp:
    def __init__(self):
        self.app = tk.Tk()
        self.app.geometry("667x375")
        self.app.title("CalcApp")

        self.total_expr = ""
        self.current_expr = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.numbers = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+", "log": "log"}
        self.buttons_frame = self.create_buttons_frame()
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_number_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.create_exp_button()
        self.create_log_button()
        self.create_sin_button()
        self.create_cos_button()
        self.create_tan_button()
        self.create_factorial_button()
        self.create_ln_button()
        self.bind_keys()

    def bind_keys(self):
        self.app.bind("<Return>", lambda event: self.evaluate())
        for key in self.numbers:
            self.app.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.app.bind(key, lambda event, operator=key: self.append_operator(operator))
        
        self.app.bind("<BackSpace>", lambda event: self.current_expr[:-1])
        self.app.bind("<Escape>", lambda event: self.clear())
        self.app.bind("c", lambda event: self.clear())

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def factorial(self):
        self.current_expr = str(math.factorial(int(self.current_expr)))
        self.update_label()

    def create_factorial_button(self):
        button = tk.Button(self.buttons_frame, text="n!", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                        borderwidth=0, command=self.factorial)
        button.grid(row=5, column=1, sticky=tk.NSEW)

    def ln(self):
        self.current_expr = str(math.log(float(self.current_expr)))
        self.update_label()

    def create_ln_button(self):
        button = tk.Button(self.buttons_frame, text="ln", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                        borderwidth=0, command=self.ln)
        button.grid(row=5, column=2, sticky=tk.NSEW)

    def log(self):
        self.current_expr = str(math.log(float(self.current_expr)))
        self.update_label()

    def create_log_button(self):
        button = tk.Button(self.buttons_frame, text="log", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.log)
        button.grid(row=0, column=5, sticky=tk.NSEW)

    def exp(self):
        self.current_expr = str(math.exp(float(self.current_expr)))
        self.update_label()
        
    def create_exp_button(self):
        button = tk.Button(self.buttons_frame, text="exp", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.exp)
        button.grid(row=1, column=5, sticky=tk.NSEW)

    def sin(self):
        self.current_expr = str(math.sin(float(self.current_expr)))
        self.update_label()

    def create_sin_button(self):
        button = tk.Button(self.buttons_frame, text="sin", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sin)
        button.grid(row=2, column=5, sticky=tk.NSEW)

    def cos(self):
        self.current_expr = str(math.cos(float(self.current_expr)))
        self.update_label()

    def create_cos_button(self):
        button = tk.Button(self.buttons_frame, text="cos", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.cos)
        button.grid(row=3, column=5, sticky=tk.NSEW)

    def tan(self):
        self.current_expr = str(math.tan(float(self.current_expr)))
        self.update_label()

    def create_tan_button(self):
        button = tk.Button(self.buttons_frame, text="tan", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.tan)
        button.grid(row=4, column=5, sticky=tk.NSEW)


    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expr, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expr, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=BIG_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.app, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expr += str(value)
        self.update_label()

    def create_number_buttons(self):
        for number, grid_value in self.numbers.items():
            button = tk.Button(self.buttons_frame, text=str(number), bg=WHITE, fg=LABEL_COLOR, font=NUMBERS_FONT_STYLE,
                               borderwidth=0, command=lambda x=number: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expr += operator
        self.total_expr += self.current_expr
        self.current_expr = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expr = ""
        self.total_expr = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expr = str(eval(f"{self.current_expr}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expr = str(eval(f"{self.current_expr}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expr += self.current_expr
        self.update_total_label()
        try:
            self.current_expr = str(eval(self.total_expr))

            self.total_expr = ""
        except Exception:
            self.current_expr = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.app)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expr
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expr[:11])

    def run(self):
        self.app.mainloop()


def main():
    calc_app = CalcApp()
    calc_app.run()

if __name__ == "__main__":
    main()
    exit()