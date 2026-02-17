class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def add(self, another_pair):
        print(f"Result: {self.a + another_pair.a} {self.b + another_pair.b}")
    
a, b, c, d = map(int, input().split())
p1 = Pair(a, b)
p2 = Pair(c, d)
p1.add(p2)
