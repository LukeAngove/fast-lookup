#!/usr/bin/env python3

import yaml
import json

if __name__ == '__main__':
    with open('dict.json') as f:
        data = json.load(f)

    with open('words.yml', 'w') as f:
        # Convert to set to remove redundant entries; we don't need them for this list
        f.write(yaml.dump(sorted(set(data.values()))))
