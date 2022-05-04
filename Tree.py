from prettytable import PrettyTable


class Tree(object):
    """Класс с деревом."""

    def __init__(self, up=None, left=None, right=None, id=None, value=None, type=None, point=None, line=None):
        super(Tree, self).__init__()
        self.up = up
        self.left = left
        self.right = right
        self.id = id
        self.value = value
        self.type = type
        self.point = point
        self.line = line

    def set_left(self):
        self.left = Tree(self, None, None)
        return self.left

    def set_right(self):
        self.right = Tree(self, None, None)
        return self.right

    def add_node(self, id, type, lexer, point=None, line=None):
        self.dup_control(id, lexer)
        new_node = self.set_left()
        new_node.id = id
        new_node.type = type
        new_node.value = "-"
        new_node.point = point
        new_node.line = line
        return new_node

    def find_up(self, id, type, lexer):
        i = self
        while i is not None and i.id != id:
            i = i.up
        if i is None:
            if type == "label":
                lexer.error("Метка не найдена", id1=id)
            elif type == "int":
                lexer.error("Идентификатор не найден", id1=id)
        return i

    def dup_control(self, id, lexer):
        i = self
        while i is not None and i.id != id and i.id != "-EMPTY-":
            i = i.up
        if i is not None and i.id == id:
            lexer.error("Повторное описание идентификатора")

    def out_value(self):
        print(self.id, "=", self.value)

    def show_tree(self):
        table = PrettyTable()
        table.field_names = [
            "Узел",
            "Тип",
            "Значение",
            "Левый потомок",
            "Правый потомок",
        ]
        self.next_node(table)
        print(table)

    def next_node(self, table):
        id_left, id_right = self.id_left_right()
        if self.type == "label":
            table.add_row([self.id, self.type, self.line, id_left, id_right])
        else:
            table.add_row([self.id, self.type, self.value, id_left, id_right])
        if self.right is not None:
            self.right.next_node(table)
        if self.left is not None:
            self.left.next_node(table)

    def id_left_right(self):
        id_left = None
        id_right = None
        if self.left is None:
            id_left = "-"
        else:
            id_left = self.left.id
        if self.right is None:
            id_right = "-"
        else:
            id_right = self.right.id
        return id_left, id_right
