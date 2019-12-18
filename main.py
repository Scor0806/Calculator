from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

import math


class CalcInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        allowed = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '+', '/', '*', '%']
        if not substring in allowed:  # If key not allowed
            return super().insert_text('', from_undo=from_undo)
        else:
            return super().insert_text(substring, from_undo=from_undo)


class CalculatorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(CalculatorWindow, self).__init__(**kwargs)

        nums = [7, 8, 9, 4, 5, 6, 1, 2, 3, '.', 0, '%']
        self.numbers = self.ids.numbers_grid

        symbls = ['-', '(', 'AC', '\u00f7', ')', 'mod', '\u00d7\u00b2', '\u03c0', '\u221a']
        self.symbols = self.ids.symbols

        last_symbls = ['C', '\u00d7', '+']
        self.last_symbls = self.ids.last_symbols

        #   ADD BUTTONS GRID
        for num in nums:
            btn = Button(text=str(num), font_size=26)
            btn.bind(on_release=self.echo_num)
            self.numbers.add_widget(btn)

        #   ADD SYMBOLS GRID
        for sym in symbls:
            btn = Button(text=str(sym), font_size=26)
            btn.bind(on_release=self.echo_num)
            self.symbols.add_widget(btn)
        eq = Button(text='=', size_hint_y=.25, font_size=26)
        eq.bind(on_release=self.evaluate_exp)
        self.ids.symbols_cont.add_widget(eq)

        #   ADD LAST SYMBOLS GRID
        for sym in last_symbls:
            btn_height = .25
            if sym == '+':
                btn_height = .5
            btn = Button(text=str(sym), size_hint_y=btn_height, font_size=26)
            btn.bind(on_release=self.echo_num)
            self.last_symbls.add_widget(btn)

    def echo_num(self, instance):
        query = self.ids.query

        if instance.text == '%' and len(query.text) > 0:
            symbols = []
            symbols.append(query.text.rfind('-'))
            symbols.append(query.text.rfind('+'))
            symbols.append(query.text.rfind('\u00f7'))
            symbols.append(query.text.rfind('\u00d7'))
            sym_ind = max(symbols)  # Get last symbol
            if sym_ind < 0:
                percent = round(float(query.text) / 100, 2)
                query.text = str(percent)
            else:
                result = query.text
                target = result[sym_ind + 1:]
                percent = round(float(target) / 100, 2)
                query.text = query.text[:sym_ind + 1] + str(percent)

        elif instance.text == '\u221a' and len(query.text) > 0:
            symbols = []
            symbols.append(query.text.rfind('-'))
            symbols.append(query.text.rfind('+'))
            symbols.append(query.text.rfind('\u00f7'))
            symbols.append(query.text.rfind('\u00d7'))
            sym_ind = max(symbols)  # Get last symbol
            if sym_ind < 0:
                sqrt = math.sqrt(float(query.text))
                query.text = str(sqrt)
            else:
                result = query.text
                target = result[sym_ind + 1:]
                sqrt = math.sqrt(float(target))
                query.text = query.text[:sym_ind + 1] + str(sqrt)

        elif instance.text == '\u00d7\u00b2':
            instance.text = '\u00b2'
            query.text += instance.text

        elif instance.text == 'AC':
            query.text = ''

        elif instance.text == 'C':
            max_ind = len(query.text)
            if query.text[max_ind - 1:] == 'd':
                query.text = query.text[:-3]
            else:
                query.text = query.text[:-1]

        else:
            query.text += instance.text

    def evaluate_exp(self, text):
        query = self.ids.query
        exp = query.text
        exp = self.resolve_sym(exp)
        result = eval(exp)
        query.text = str(result)

        self.ids.expr.text = exp
        self.ids.equal.text = '='
        self.ids.result.text = str(result)

    def resolve_sym(self, text):
        res = text.replace('\u00f7', '/').replace('\u00b2', '**2').replace('\u00d7', '*') \
            .replace('\u03c0', str(math.pi)) \
            .replace('mod', '%')
        return res


class CalculatorApp(App):
    def build(self):
        return CalculatorWindow()


if __name__ == '__main__':
    CalculatorApp().run()
