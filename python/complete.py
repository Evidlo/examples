#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
from passhole.passhole import open_databases, split_db_prefix, join_db_prefix, get_database
from pykeepass_cache import PyKeePass
import os

def github_org_members(prefix, parsed_args, **kwargs):
    try:
        db, path = split_db_prefix(prefix)
        databases = open_databases()

        # complete db prefix
        if path is None:
            results = ['@{}/'.format(db) for db in databases.keys()]
            return results

        # complete groups/entries
        else:
            kp = get_database(databases, prefix)
            # kp = PyKeePass('/home/evan/.passhole.kdbx')

            basepath = os.path.dirname(path).lstrip('/') + '/'
            parent_group = kp.find_groups(path=basepath, first=True)

            if parent_group is not None:
                results = []
                for e in parent_group.entries + parent_group.subgroups:
                    results.append(join_db_prefix(db, e.path))
                return results
            else:
                return None

    except Exception:
        import traceback
        open('/tmp/dump', 'w').write(traceback.format_exc())

parser = argparse.ArgumentParser()
parser.add_argument("-m", help="GitHub member").completer = github_org_members

argcomplete.autocomplete(parser)
args = parser.parse_args()

print(args.m)
