import json
import sys


merged_array = []

# Read the input arrays from stdin
input_data = sys.stdin.readlines()

try:
    # Parse each line as JSON array and extend the merged_array
    for line in input_data:
        line.strip()
        array = json.loads(line)
        if isinstance(array, list):
            merged_array.extend(array)
except json.JSONDecodeError:
    print("Invalid JSON input.")


print(json.dumps(merged_array))
