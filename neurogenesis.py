#!/usr/bin/python

from pathlib import Path
import uuid
import argparse
import os
import json
import time


config_path = Path.home() / Path('.config/neurogenesis/config.json')

# Default user configuration
default_user_config = {
    'notes_directory': '~/cerebrum'
}

# user configured globals
notes_directory = None


def createNode(title: str = '') -> None:
    node_id = uuid.uuid4()
    path = Path(f'{node_id}.md')
    path.touch()
    metadata_header = [
        '---\n', f'ID:{node_id}\n', f'TITLE:{title}\n', 'TAGS:\n', '---\n'
    ]
    with open(path, 'w') as file:
        file.writelines(metadata_header)
    print(f'Created a new node with ID:{node_id} and TITLE:{title}')
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
    db_path = Path.cwd() / Path('.database.json')
    if not db_path.exists():
        db_path.touch()
    else:
        db_path.unlink()
        db_path.touch()
    db_path.write_text(json.dumps(getNodes(notes_directory)))
    elapsed_time = time.time() - start_time
    print(f'Updated Database in {elapsed_time}s')
    return None


def printDatabaseJSON() -> None:
    db_path = Path.cwd() / Path('.database.json')
    with open(db_path, 'r') as file:
        print(file.read())
    return None


def createConfig() -> None:
    config_dir = Path.home() / Path('.config/neurogenesis')
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path.touch()

    # initialize config
    with open(config_path, 'w') as file:
        file.writelines(json.dumps(default_user_config))

    return None


def readConfig() -> None:
    if not config_path.exists():
        createConfig()
        print(
            f'Initialized a new configuration file at {config_path}'
        )
    with open(config_path, 'r') as config:
        user_config = json.load(config)

    global notes_directory
    notes_directory = Path(user_config['notes_directory']).expanduser()

    return None


def main():
    readConfig()
    os.chdir(notes_directory)

    parser = argparse.ArgumentParser(
        prog='Neurogenesis',
        description='Does Neurogenesis Stuff'
    )
    subparsers = parser.add_subparsers(dest='command', help='sub-command help')

    new_parser = subparsers.add_parser('new', help='creates a new node')
    new_parser.add_argument('--title', help='title for the new node')

    subparsers.add_parser('refresh', help='refreshes the database')
    subparsers.add_parser('get_nodes', help='returns node data in JSON format')

    args = parser.parse_args()
    if args.command == 'new':
        createNode(title=args.title)
        refreshDatabase()
    elif args.command == 'refresh':
        refreshDatabase()
    elif args.command == 'get_nodes':
        printDatabaseJSON()
    return None


if __name__ == '__main__':
    main()
