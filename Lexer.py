class Lexer(object):
    def __init__(self, path):
        self.point = 0
        self.line = 1
        self.lex = None
        self.sym = None
        self.text = self.read_file(path)

    (
        INT,
        ID,
        CONSTINT,
        GOTO,
        EQUAL,
        SEMICOLON,
        COLON,
        EOF,
    ) = range(8)
    # специальные символы языка
    SYMBOLS = {
        "=": EQUAL,
        ";": SEMICOLON,
        ":": COLON,
    }

    # ключевые слова
    WORDS = {"goto": GOTO, "int": INT}

    def error(self, msg, id1=None):
        if id1 is not None:
            print("Семантическая ошибка: %s\nПолучено: %s\nСтрока: %d" %
                  (msg, id1, self.line))
        else:
            print("Ошибка: %s\nПолучено: %s\nСтрока: %d" %
                  (msg, self.lex, self.line))
        exit(1)

    def read_file(self, path):
        with open(path, "r") as file:
            text = file.read()
        lines = text.split("\n")
        print("Текст программы:")
        for i in range(len(lines)):
            print(i + 1, ") ", lines[i], sep='')
        return text

    def next_tok(self):
        self.sym = None
        while self.sym is None:
            if self.point == len(self.text):
                self.sym = Lexer.EOF
                self.lex = "$"
            elif self.text[self.point] == "\n":
                self.point += 1
                self.line += 1
            elif self.text[self.point].isspace():
                self.point += 1
            elif self.text[self.point] in Lexer.SYMBOLS:
                self.sym = Lexer.SYMBOLS[self.text[self.point]]
                self.lex = self.text[self.point]
                self.point += 1
            elif self.text[self.point].isdigit():
                self.lex = ""
                while self.text[self.point].isdigit():
                    self.lex += self.text[self.point]
                    self.point += 1
                self.sym = Lexer.CONSTINT
            elif self.text[self.point].isalpha():
                self.lex = ""
                while (
                    self.text[self.point].isalpha()
                    or self.text[self.point].isdigit()
                ):
                    self.lex += self.text[self.point]
                    self.point += 1
                if self.lex in Lexer.WORDS:
                    self.sym = Lexer.WORDS[self.lex]
                else:
                    self.sym = Lexer.ID
            else:
                self.lex = self.text[self.point]
                self.error("Неизвестный символ")
