from pathlib import Path
import uuid
import argparse
import os
import json
import time

# TODO: add node metadata validation
# TODO: refactor

network_location = Path('/home/jordan/brain/')

def createNode(title: str = '') -> None:
    node_id = uuid.uuid4()
    path = Path(f'{node_id}.md')
    path.touch()
    metadata_header = ['---\n',f'ID:{node_id}\n',f'TITLE:{title}\n','TAGS:\n','---\n']
    with open(path, 'w') as file:
        file.writelines(metadata_header)
    print(f'Created a new node with ID:{node_id}')
    return None

def getNodeProperties(node: Path) -> dict:
    properties = {}
    with open(node, 'r') as file:
        header = []
        for _ in range(5):
            header.append(file.readline())
        properties['id'] = header[1].split(':')[1].strip()
        properties['title'] = header[2].split(':')[1].strip()
        properties['tags'] = header[3].split(':')[1].strip().split(',')
    return properties

def getNodes(path: Path) -> list:
    nodes = path.glob('*.md')
    node_properties_list = [getNodeProperties(node) for node in nodes]
    return node_properties_list

def refreshDatabase() -> None:
    start_time = time.time()
    db_path = Path.cwd()/Path('.database.json')
    if not db_path.exists():
        db_path.touch()
    else:
        db_path.unlink()
        db_path.touch()
    db_path.write_text(json.dumps(getNodes(network_location)))
    elapsed_time = time.time() - start_time
    print(f'Updated Database in {elapsed_time}s')
    return None 

def printDatabaseJSON() -> None:
    db_path = Path.cwd()/Path('.database.json')
    with open(db_path, 'r') as file:
        print(file.read())
    return None

def main():
    os.chdir(network_location)

    parser = argparse.ArgumentParser(description='Does Neuron Stuff')
    command = parser.add_mutually_exclusive_group(required=True)
    command.add_argument('command', help='Command to issue: new or refresh, get_nodes', nargs='?', choices=('new', 'refresh', 'get_nodes'))
    args = parser.parse_args()
    if args.command=='new':
        createNode()
        refreshDatabase()
    elif args.command=='refresh':
        refreshDatabase()
    elif args.command=='get_nodes':
        printDatabaseJSON()
    return None

if __name__ == '__main__':
    main()
