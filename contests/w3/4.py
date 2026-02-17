class StringHandler:
    def printString(self):
        print(self.string.upper())

    def getString(self):
        string = input()
        self.string = string
    
str_obj = StringHandler()
str_obj.getString()
str_obj.printString()

    