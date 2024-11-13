# compare_properties.py
import os
import re
import sys
import json
from collections import defaultdict

REMOTE_FILES_DIR = "./remote-files/"
FILE_PATTERN = re.compile(r"(.+)_server\.properties")

def load_properties(file_path):
    """Load properties from a file into a dictionary."""
    properties = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            properties[key.strip()] = value.strip()
    return properties

def compare_properties(files, ignored_keys):
    """Compare properties across multiple files."""
    all_properties = defaultdict(dict)
    inconsistent_keys = {}

    for file in files:
        match = FILE_PATTERN.match(file)
        if not match:
            continue
        host = match.group(1)
        properties = load_properties(os.path.join(REMOTE_FILES_DIR, file))

        filtered_properties = {k: v for k, v in properties.items() if k not in ignored_keys}

        for key, value in filtered_properties.items():
            all_properties[key][host] = value

    for key, values in all_properties.items():
        if len(set(values.values())) > 1:
            inconsistent_keys[key] = values

    return inconsistent_keys

def format_output(differences):
    """Format the output as a list of lines."""
    output = []
    if differences:
        output.append("Inconsistent keys across hosts:")
        for key, hosts_values in differences.items():
            output.append(f" - {key}:")
            for host, value in hosts_values.items():
                output.append(f"     {host}: {value}")
    else:
        output.append("All properties are consistent across hosts.")
    return output

def main():
    ignored_keys = sys.argv[1].split(',')
    property_files = [f for f in os.listdir(REMOTE_FILES_DIR) if FILE_PATTERN.match(f)]
    differences = compare_properties(property_files, ignored_keys)
    output = format_output(differences)
    
    # Print output as JSON array for Ansible
    print(json.dumps(output))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 compare_properties.py <ignored_keys>")
        sys.exit(1)
    main()