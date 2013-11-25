#!/usr/bin/python
import json

f = open('json_titles.txt').readlines()
s = open('old_json_titles.txt').readlines()

old_json_obj_list = []
new_json_obj_list = []
for line in f:
    old_json_obj_list.append(json.loads(line))
    
for line in s:
    new_json_obj_list.append(json.loads(line))

for old_obj in old_json_obj_list:
    if 'metacritic_userscore_meter' in old_obj:
        found = False
        for new_obj in new_json_obj_list:
            if 'metacritic_userscore_meter' in new_obj and old_obj['imdb_id'] == new_obj['imdb_id']: 
                old_obj['metacritic_userscore_meter'] = new_obj['metacritic_userscore_meter']
                found = True

        if found is False:
            old_obj.pop('metacritic_userscore_meter')
            old_obj.pop('metacritic_userscore_total')

for obj in old_json_obj_list:
    print json.dumps(obj)
