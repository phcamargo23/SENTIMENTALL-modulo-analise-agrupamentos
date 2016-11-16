# -*- coding: utf-8 -*-
from flask import json
import json
import glob

def obj2JsonFile(obj, path):
    # jsonData = json.dumps(obj)

    # with open(output_dir + '/'+estado+'.json', 'w') as f:
    #     json.dump(jsonData, f)

    json_string = json.dumps(obj)  # transforma em string
    open(path, 'w').write(json_string) # salva no arquivo

#  Mesclando arquivos
def mergeFilesAndSave(dir, ext, path):
    read_files = glob.glob(dir + "/*."+ext)
    read_files.pop()  # Removendo o arquivo '_progresso.json'
    output_list = {}

    for f in read_files:
        with open(f, "rb") as infile:
            output_list.update(json.load(infile))


    json_string = json.dumps(output_list)  # transforma em string
    open(path, 'w').write(json_string)


def loadJsonFromFile(path):
    json_string = open(path).read()  # carrega arquivo json
    obj = json.loads(json_string)  # transforma em object

    return obj