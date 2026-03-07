import json

obj = json.loads(input())
quries = int(input())
for _ in range(quries):
    q = input()
    keys = q.replace("]", "").replace("[", ".").split(".")
    keys = [k for k in keys if k] 
    
    value = obj
    found = True
    
    for key in keys:
        if key.isdigit():
            try:
                value = value[int(key)]
            except (IndexError, TypeError):
                found = False
                break
        else:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                found = False
                break
    
    if not found:
        print("NOT_FOUND")
    elif value is None:
        print("null")
    elif isinstance(value, bool):
        print(str(value).lower())
    elif isinstance(value, (dict, list)):
        print(json.dumps(value, separators=(',', ':')))
    elif isinstance(value, str):
        print(f'"{value}"')
    else:
        print(value)


