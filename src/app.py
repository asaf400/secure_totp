"""
Safe totp

Usage:
  totp.py (create | update | install) <name> <key>
  totp.py (delete | remove) <name>
  totp.py list
  totp.py remove_duplicates
  totp.py <name>

Options:
  -h --help     Show this screen.
"""

from mintotp import totp
from tinydb import Query,TinyDB
from models.encrypted_tinystorage import EncryptedJSONStorage
from itertools import groupby
import keyring
import sys
import tabulate
from docopt import docopt
from pathlib import Path

db = TinyDB(Path('~/.totp/db.json'),storage=EncryptedJSONStorage)

def crud():
    pass

def create(name,key):
    search = Query()
    data = db.search(search.name == name)[0]
    if data:
        return "Docuement already exists, please use update to override value"
    return db.insert({'name': name, 'key': key})

def update(name,key):
    search = Query()
    return db.update({'key': key}, search.name == name)

def delete(name):
    search = Query()
    return db.remove(search.name == name)

def list():
    return tabulate.tabulate(db.all(),headers='keys')

def remove_duplicates():
    entire_data = db.all()
    data = [k for k,v in groupby(sorted(entire_data,key=lambda x: x['name']))]
    keep = [x.doc_id for x in data]
    remove = [x.doc_id for x in entire_data if x.doc_id not in keep]
    duplicates = [x for x in entire_data for y in remove if x.doc_id==y]
    print(f"Removing IDs: {remove}, Keeping: {keep}, duplicates are: {duplicates}")
    return db.remove(doc_ids=remove)


def lookup(name):
    search = Query()
    data = db.search(search.name == name)[0]
    return totp(data['key'].strip())

def main(*args):
    arguments = docopt(__doc__)
    # if any([arguments.get(i, False) for i in ['create','install','update','delete','remove','list']]):
    if arguments['create'] or arguments['install']:
        print(create(arguments['<name>'],arguments['<key>']))
    elif arguments['update']:
        print(update(arguments['<name>'], arguments['<key>']))
    elif arguments['delete'] or arguments['remove']:
        print(delete(arguments['<name>']))
    elif arguments['list']:
        print(list())
    elif arguments['remove_duplicates']:
        print(remove_duplicates())
    else:
        results = lookup(arguments['<name>'])
        print(results)

if __name__ == '__main__':
    main(sys.argv[1:])

# key.strip(), time_step=30, digits=6, digest='sha1
# '

