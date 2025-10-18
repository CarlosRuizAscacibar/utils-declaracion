from modelos.split import Split
import json
from typing import List


def read_all_splits(json_path:str) -> List[Split]:
    contents = ''
    with open(json_path, 'r', encoding='utf8') as f:
        contents = f.read()

    splits = []
    json_splits = json.loads(contents)
    for x in json_splits:
        split = Split(**x)
        splits.append(split)
    return splits
    
