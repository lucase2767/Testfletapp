from dataclasses import field

import flet as ft

# this file implements a simple calculator using Flet framework
# - custom button controls for digits/actions
# - dynamic sizing based on page resize
# - basic arithmetic operations with error handling
# - result display anchored at bottom


@ft.control
class CalcButton(ft.Button):
    # base button used by calculator; supports an 'expand' property
    expand: int = field(default_factory=lambda: 1)


@ft.control
class DigitButton(CalcButton):
    # button style for numerical digits
    bgcolor: ft.Colors = ft.Colors.WHITE_24
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class ActionButton(CalcButton):
    # style for arithmetic operator buttons (+, -, *, / and =)
    bgcolor: ft.Colors = ft.Colors.ORANGE
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class ExtraActionButton(CalcButton):
    # style for secondary actions (AC, +/-, %)
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
    color: ft.Colors = ft.Colors.BLACK


@ft.control
class CalculatorApp(ft.Container):
    def init(self):
        # initialize state and appearance
        self.reset()  # clear any existing computation
        # width will be set dynamically by the page resize handler
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 20
        # text control showing current result/value
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)

        # layout: vertical column of rows representing calculator display and buttons
        # alignment=END ensures extra vertical space appears above the controls
        self.content = ft.Column(
            # push controls to bottom of the container
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.Row(
                    # result row
                    controls=[self.result],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(content="AC", on_click=self.button_clicked),
                        ExtraActionButton(content="+/-", on_click=self.button_clicked),
                        ExtraActionButton(content="%", on_click=self.button_clicked),
                        ActionButton(content="/", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="7", on_click=self.button_clicked),
                        DigitButton(content="8", on_click=self.button_clicked),
                        DigitButton(content="9", on_click=self.button_clicked),
                        ActionButton(content="x", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="4", on_click=self.button_clicked),
                        DigitButton(content="5", on_click=self.button_clicked),
                        DigitButton(content="6", on_click=self.button_clicked),
                        ActionButton(content="-", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="1", on_click=self.button_clicked),
                        DigitButton(content="2", on_click=self.button_clicked),
                        DigitButton(content="3", on_click=self.button_clicked),
                        ActionButton(content="+", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            content="0", expand=2, on_click=self.button_clicked
                        ),
                        DigitButton(content=".", on_click=self.button_clicked),
                        ActionButton(content="=", on_click=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        # event handler for all buttons
        data = e.control.content
        # clear on error or AC pressed
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            # digit or decimal point input
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "x", "/"):
            # perform pending calculation and store operator for next
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                # reset on error
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data in ("="):
            # equals pressed: compute result and optionally log
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            if self.result.value != "Error":
                print("hello world")
            self.reset()

        elif data in ("%"):
            # percentage operation
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data in ("+/-"):
            # toggle sign of current value
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)

            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        self.update()

    def format_number(self, num):
        # strip trailing .0 from whole numbers
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):
        # perform arithmetic based on operator
        if operator == "+":
            return self.format_number(operand1 + operand2)

        elif operator == "-":
            return self.format_number(operand1 - operand2)

        elif operator == "x":
            return self.format_number(operand1 * operand2)

        elif operator == "/":
            # handle division by zero
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)
    

    def reset(self):
        # clear calculator state for a new operation
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True

def main(page: ft.Page):
    page.title = "Calc App"
    # create main calculator control
    calc = CalculatorApp()

    # add calculator container to the page
    page.add(calc)

    # set initial width/height and update on resize for dynamic dimensioning
    def _resize(e):
        # subtract padding (20 left + 20 right) so it fits nicely
        calc.width = max(0, page.width - 40)
        # also adjust height, leaving a little top/bottom margin
        calc.height = max(0, page.height - 40)
        calc.update()

    page.on_resize = _resize
    # call once to initialize dimensions immediately
    _resize(None)

# launch the application event loop
ft.run(main)