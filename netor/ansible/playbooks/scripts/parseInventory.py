import sys
import ast

print("Hostname: " + str(sys.argv[1]))
host_detail = sys.argv[2]
host_detail2dict = ast.literal_eval(host_detail)
for key, value in host_detail2dict.items():
    print('{}: {}'.format(key, value))

f = open("./tmp/output.txt","a+")
f.write("Hostname: " + str(sys.argv[1] + "\n"))
for key, value in host_detail2dict.items():
    f.write('{}: {} \n'.format(key, value))
f.write("\n")
f.close

