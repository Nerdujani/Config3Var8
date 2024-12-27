from tomllib import loads
from sys import stdin, exit


class Parser:
    def __init__(self):
        self.s = ''

    def rec_parse(self, element, indent, key=''):
        def add_string(string):
            self.s += ' ' * 4 * indent
            if key:
                self.s += f'{key} = '
            self.s += string
            self.s += '\n'

        if isinstance(element, int) or isinstance(element, float):
            add_string(str(element))

        elif isinstance(element, list):
            add_string("({")
            comas = len(element) - 1
            for el in element:
                self.rec_parse(el, indent + 1)
                if comas > 0:
                    self.s = self.s[:-1] + ',\n'
                    comas -= 1
            self.s += ' ' * 4 * indent
            self.s += '})\n'

        elif isinstance(element, dict):
            add_string('dict(')
            comas = len(element) - 1
            for key, value in element.items():
                self.rec_parse(value, indent + 1, key)
                if comas > 0:
                    self.s = self.s[:-1] + ',\n'
                    comas -= 1

            self.s += ' ' * 4 * indent
            self.s += ')\n'

    def load_toml(self, text):
        try:
            data = loads(text)
        except:
            print('Некорректный ввод')
            return
        if data == text:
            print('Некорректный ввод')
            return
        return data


if __name__ == '__main__':
    std_input = stdin.read()
    parser = Parser()
    yaml_data = parser.load_toml(std_input)
    try:
        parser.rec_parse(yaml_data, 0)
    except:
        print('Что-то пошло не так')
    print(parser.s)
