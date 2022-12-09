import json

# read file
with open('../Data/questions.json', 'r', encoding="utf8") as myfile:
    data = myfile.read()

# parse file
obj = json.loads(data)

# show values
# print(obj[0]['question'])
print(obj[0]['options'])