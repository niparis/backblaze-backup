""" B2 Uploader

ref https://www.backblaze.com/b2/docs/quick_command_line.html

Usage:
  b2upload.py --bucket <bucket> [--directory <directory>]

Options:
  -h --help         Show this screen.
  --bucket <bucket>   how many users to process (max)
  --directory <directory>     restrict to one userid
"""
import os
import sys
import subprocess

import json

import configparser                     # py3

import cerberus
from cerberus import Validator
from docopt import docopt



def read_conf():
    config = configparser.ConfigParser()
    homedir = os.path.expanduser('~')
    conf_file = os.path.join(homedir, '.backblaze')

    if not os.path.isfile(conf_file):
        print('can not find .backblaze configuration file in your home director (checked : {})'.format(homedir))
        print('Please check the readme')
        sys.exit(1)

    config.read(conf_file)

    return config['backblaze']  ## py3

def cerberus_validation(schema, kwargs):
    """
        Validates a cerberus schema
            Displays errors & raise exception if validation fails
    """
    errors = schema.validate(kwargs)

    if not schema.validate(kwargs):
        msg = ''
        for key, value in schema.errors.items():
            msg += 'key: {} - {}'.format(key, value)
        raise cerberus.ValidationError(msg)


def execute_command(command, stdout=subprocess.PIPE):
    try:
        retval = subprocess.run(['b2'] + command.split(' '), stdout=stdout, check=True)
    except subprocess.CalledProcessError:
        return False
    except OSError:
        print('b2 not installed')
        return False

    return retval

def is_authorized():
    return execute_command('list_buckets', subprocess.DEVNULL)

def decode_list_buckets(completed):
    list_buckets = completed.stdout.decode('utf-8').split('\n')
    retval = []
    for bucket in list_buckets:
        if len(bucket) > 0:
            retval.append(bucket.split(' ')[-1])

    return retval

def decode_list_files(completed):
    jsonobject = json.loads(completed.stdout.decode('utf-8'))
    return [i.get('fileName') for i in jsonobject.get('files')]

def authorize(config):
    cmd = 'authorize_account {accountid} {applicationkey}'.format(**config)
    return execute_command(cmd)


def upload_folder(bucket, directory, config):

    if not is_authorized():
        res = authorize(config)
        if not res:
            print('authorization failed')
            sys.exit(1)
        else:
            print('Account authorized succesfully')

    ## Checks if the bucket exists. If it doesnt, create it
    bucket_list = decode_list_buckets(execute_command('list_buckets'))
    if bucket not in bucket_list:
        resp = execute_command('create_bucket {} allPrivate'.format(bucket))
        if resp:
            print('Bucket {} created'.format(bucket))
        else:
            print('error trying to create bucket {}'.format(bucket))
            sys.exit(1)

    ##
    list_files = decode_list_files(execute_command('list_file_names {}'.format(bucket)))


    for root, dirnames, filenames in os.walk(directory):
        if filenames:
            for fname in filenames:
                fullpath = os.path.join(root, fname)
                uploadpath = os.path.relpath(fullpath, directory)
                if uploadpath not in list_files:
                    cmd = 'upload_file {bucket} {fname} {fpath}'.format(bucket=bucket, fname=fullpath, fpath=uploadpath)
                    execute_command(cmd)
                else:
                    print('{} already uploaded. skipping...'.format(fname))



# if __name__ == "__main__":
def main():
    arguments = docopt(__doc__, version='b2 uploader 1.0')

    schema = Validator({
                        "--bucket"        : {'type': 'string', 'required': True, 'minlength': 6},
                        "--directory"     : {'type': 'string', 'required': False, 'nullable': True},
        })

    cerberus_validation(schema, arguments)

    bucket = arguments.get('--bucket')
    directory = arguments.get('--directory')
    config = read_conf()

    if not directory:
        directory = os.getcwd()

    upload_folder(bucket=bucket, directory=directory, config=config)

if __name__ == "__main__":
    main()
