class MainA():
    foobar = 'a'

    def show(self):
        print(self.foobar)

class MainB(MainA):
    foobar = 'b'

class DerivedA(MainA):
    def show(self):
        super().show()
        print('the above line is ' + self.foobar)

class DerivedB(MainB, DerivedA):
    pass

d = DerivedA()
d.show()
d = DerivedB()
d.show()

# >>> python3 mixin_super.py
# a
# the above line is a
# b
# the above line is b
