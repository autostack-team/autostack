mystring = "My favorite color is blue,\nbut I'm not a fan of teal,\nand green is ugly."
mylines = mystring.splitlines()
lastline = mylines[-1]
print("Last line: " + lastline)
mywords = lastline.split()
firstword = mywords[0]
print("First word of last line: " + firstword)
firstword_withoutlastcharacter = firstword[:-1]
print("First word without last character: " + firstword_withoutlastcharacter)


#myarray = mystring.split()
#matching = [s for s in myarray if "avor" in s]
#print(matching)
