Input=input()
dictionary = {}
List=[]
for character in Input:
    if character not in dictionary:
        dictionary[character]=1
        List.append(character)
    else:
        List.append("-")
Output = ''.join(List)
print(Output)