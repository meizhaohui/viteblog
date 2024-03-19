#!/usr/bin/python
import json
import shlex
import sys
args_file = sys.argv[1]
with open(args_file) as file:
    args_data = file.read()
arguments = shlex.split(args_file)
for arg in arguments:
    if "=" in arg:
        (key, value) = arg.split('=')
        if key == 'enable' and value == 'yes':
            data = {}
            data['key'] = 'value'
            data['list'] = ['one', 'two', 'three']
            data['dict'] = {'Name': 'Ansible'}
            print(json.dumps({"ansible_facts": data}, indent=4))
        else:
            print('info module usage error')
    else:
        print('info module need one parameter')
