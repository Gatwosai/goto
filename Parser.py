from Lexer import Lexer
from Tree import Tree


class Parser(object):
    """Синтаксический анализатор."""

    def __init__(self, path):
        super(Parser, self).__init__()
        self.lexer = Lexer(path)
        self.root = Tree(id="int", type="-", value="-")
        self.flag_interpret = False

    def S(self):
        """
        Программа. Производится два прохода по программе:
        Первый - построение дерева. 
        Второй - интерпретация.
        """
        v = self.root
        for i in range(2):
            if self.flag_interpret is True:
                print("Интерпретация:")
            self.lexer.next_tok()
            while self.lexer.sym != Lexer.EOF:
                if self.lexer.sym == Lexer.INT:
                    self.B()
                elif self.lexer.sym == Lexer.ID:  # метка либо присваивание
                    id = self.lexer.lex
                    self.lexer.next_tok()
                    if self.lexer.sym == Lexer.COLON:
                        self.lexer.lex = id
                        self.C()
                    elif self.lexer.sym == Lexer.EQUAL:
                        self.lexer.lex = id
                        self.F()
                elif self.lexer.sym == Lexer.GOTO:
                    self.E()
                else:
                    self.lexer.error(
                        "Ожидалось описание переменной или оператор")
            self.flag_interpret = True
            self.lexer.point = 0
            self.lexer.line = 1
        print("\nПолученное дерево:")
        v.show_tree()

    def B(self):
        """Описание переменной."""
        if self.lexer.sym == Lexer.INT:
            type = "int"
            self.lexer.next_tok()
            if self.lexer.sym != Lexer.ID:
                self.lexer.error("Ожидался идентификатор")
            if self.flag_interpret is False:
                self.root = self.root.add_node(
                    self.lexer.lex, type, self.lexer)
        temp = self.lexer.lex
        self.lexer.next_tok()
        if self.lexer.sym == Lexer.EQUAL:
            self.lexer.lex = temp
            self.F()
        elif self.lexer.sym != Lexer.SEMICOLON:
            self.lexer.error("Ожидался символ ;")

    def C(self):
        """Описание метки."""
        if self.lexer.sym == Lexer.COLON:  # метка
            type = "label"
            id = self.lexer.lex
            if self.flag_interpret is False:
                self.root = self.root.add_node(
                    id, type, self.lexer, self.lexer.point, self.lexer.line)
        self.lexer.next_tok()
        
    def E(self):
        """Оператор goto"""
        self.lexer.next_tok()
        if self.lexer.sym != Lexer.ID:
            self.lexer.error("Ожидалась метка")
        id = self.lexer.lex
        self.lexer.next_tok()
        if self.lexer.sym != Lexer.SEMICOLON:
            self.lexer.error("Ожидался символ ;")
        if self.flag_interpret is True:  # Переход по метке
            tree = self.root.find_up(id, "label", self.lexer)
            self.lexer.point = tree.point
            self.lexer.line = tree.line
        self.lexer.next_tok()

    def F(self):
        """Присваивание."""
        id = self.lexer.lex
        tree = self.root.find_up(id, "int", self.lexer)
        if self.lexer.sym == Lexer.ID:
            self.lexer.next_tok()
        if self.lexer.sym != Lexer.EQUAL:
            self.lexer.error("Ожидалось присваивание")
        self.lexer.next_tok()
        value = 0
        if self.lexer.sym == Lexer.CONSTINT:
            value = int(self.lexer.lex)
        elif self.lexer.sym == Lexer.ID:
            tree_temp = self.root.find_up(self.lexer.lex, "int", self.lexer)
            value = tree_temp.value
        self.lexer.next_tok()
        if self.lexer.sym != Lexer.SEMICOLON:
            self.lexer.error("Ожидался символ ;")
        if self.flag_interpret is True:
            tree.value = value
            tree.out_value()
        self.lexer.next_tok()
