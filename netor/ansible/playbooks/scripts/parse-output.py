import sys
import ast

print("len sys.argv= " + str(len(sys.argv)))
print("sys.argv= " + str(sys.argv))
string = (sys.argv[1])

dic = ast.literal_eval(string)

print(type(dic))


