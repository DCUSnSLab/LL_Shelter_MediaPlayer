a = "0"
chek = int(a[0])
try:
    data = int(a[1:])
except:
    data = chek
print(chek, data)
