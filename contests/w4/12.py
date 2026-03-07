import json

def find_differences(object1, object2):
    differences = {}
    for key, value in object1.items():
        if key not in object2:
            differences[key] = (value, None)
        elif isinstance(value, dict) and isinstance(object2[key], dict):
            nested_diff = find_differences(value, object2[key])
            if nested_diff:
                differences[key] = nested_diff
                del(object2[key])
        elif value != object2[key]:
            differences[key] = (value, object2[key])
            del(object2[key])
    for key, value in object2.items():
        if key not in object1:
            differences[key] = (None, value)
        
    return differences

def format_value(val):
    if val is None:
        return "<missing>"
    elif isinstance(val, bool):
        return str(val).lower()
    elif isinstance(val, (dict, list)):
        return json.dumps(val, separators=(',', ':'))
    else:
        return str(val)

def print_diff(key, value, prefix=""):
        current_key = f"{prefix}{key}" if prefix else key
        if isinstance(value, dict):
            for nested_key, nested_value in value.items():
                print_diff(nested_key, nested_value, current_key + ".")
        else:
            left = format_value(value[0])
            right = format_value(value[1])
            print(f"{current_key} : {left} -> {right}")

a = json.loads(input())
b = json.loads(input())
diff = find_differences(a, b)
if not diff:
    print("No differences")
else:
    for key, value in diff.items():
        print_diff(key, value)