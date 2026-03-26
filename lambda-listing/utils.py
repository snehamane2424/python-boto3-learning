import json


def extract_required_fields(functions):
    result = []

    for func in functions:
        result.append({
            "name": func['FunctionName'],
            "runtime": func['Runtime'],
            "memory": func['MemorySize'],
            "last_modified": func['LastModified']
        })

    return result


def save_to_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def print_functions(data):
    for func in data:
        print(f"Name: {func['name']}")
        print(f"Runtime: {func['runtime']}")
        print(f"Memory: {func['memory']}")
        print(f"Last Modified: {func['last_modified']}")
        print("-" * 40)