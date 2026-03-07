import json

source = json.loads(input())
patch = json.loads(input())
def apply_patch(source, patch):
    for key, value in patch.items():
        if value is None:
            source.pop(key, None)
        elif isinstance(value, dict) and isinstance(source.get(key), dict):
            apply_patch(source[key], value)
        else:
            source[key] = value
apply_patch(source, patch)
print(json.dumps(source, separators=(',', ':'), sort_keys=True))