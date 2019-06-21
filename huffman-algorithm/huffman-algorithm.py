from collections import OrderedDict

text = input("Input text: ")

dic = {}
for c in text:
    if c in dic:
        dic[c] += 1
    else:
        dic[c] = 1

temp = OrderedDict(sorted(dic.items(), key = lambda t: t[1]))

lista = list((quantity, item) for item, quantity in temp.items()) #list -> [(quantity, char)]
result = dict((item, "") for item in temp.keys()) #dicionary -> {"char": "binary code"}

while len(lista) > 1:
    t = [] #list with char

    #pop the two smallest values
    s0 = lista.pop(0)
    s1 = lista.pop(0)
    
    for item in s0[1]:
        t.append(item)
        result[item] = '0' + result[item]

    for item in s1[1]:
        t.append(item)
        result[item] = '1' + result[item]
        
    lista.append([s0[0] + s1[0], t]) #add a new item in the list with the sum of the two smallest values
    lista = sorted(lista, key = lambda p: p[0]) #sort list by quantity

print("Char | Quantity | Huffman Code")

for item, quantity in temp.items():
    print(item, quantity, result[item])
