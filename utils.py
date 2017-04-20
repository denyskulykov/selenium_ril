import os
import json
import yaml
import random
import string


list_test = {}


def report(test=None, action="add"):
    """action = "report", test = None

    action = "add", {"name test": "status"}
    """
    if action == "add":
        list_test.update(test)
    elif action == "report":
        print json.dumps(list_test, indent=4)


def get_configuration():
    """function returns configuration for environment"""
    global_config_file = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "global_config.yaml")

    with open(global_config_file, 'r') as file:
        global_config = yaml.load(file)

    return global_config


def gen_rand_string(object_type, size=6):
    rand_string = ''.join(random.choice(string.digits) for _ in range(size))
    return 'selenium-{}-{}'.format(object_type, rand_string)
