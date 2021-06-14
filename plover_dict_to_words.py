import yaml
import json

if __name__ == '__main__':
    with open('dict.json') as f:
        data = json.load(f)

    with open('words.yml', 'w') as f:
        f.write(yaml.dump(list(data.values())))
