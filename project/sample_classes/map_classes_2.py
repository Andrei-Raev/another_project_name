class block:
    def __init__(self, y, x, typ,
                 razr):  # ���������� x, ���������� y, ��� �����(������, �����...), �������������(True, False)
        self.y = y
        self.x = x
        self.typ = typ

    def get_x(self):  # ���������� ���������� x
        return self.x

    def get_y(self):  # ���������� ���������� y
        return self.y

    def get_razr(self):
        return self.razr


class r_block(block):
    def __init__(self, y, x, typ, razr=True):
        self.y = y
        self.x = x
        self.typ = typ
        self.razr = razr

    def get_typ(self):
        return self.typ


class nr_block(block):
    def __init__(self, y, x, typ, razr=False):
        self.y = y
        self.x = x
        self.typ = typ
        self.razr = razr

    def get_typ(self):
        return self.typ


class build(nr_block):
    def __init__(self, y, x, strykt=[[]],
                 razr=False):  # ���������� x, ���������� y, ������ ������ = [[�����_1...], [�����_2...]], �������������(True, False)
        self.y = y
        self.x = x
        self.strykt = strykt
        self.razr = razr

    def strykt(self):
        return self.strykt

    def destroy(self, y, x):
        for i in self.strykt:
            for g in i:
                if g.get_x == x and g.get_y == y:
                    q = i.index(g)
                    del i[q]
