import os
import json
import yaml
import random
import string

global_config = None
list_test = {}


class Utils(object):

    @staticmethod
    def get_report():

        global list_test
        print json.dumps(list_test, indent=4)

    @staticmethod
    def add_to_report(name_of_test):
        global list_test

        if isinstance(name_of_test, str):
            list_test.update({name_of_test: "Ok"})
        if isinstance(name_of_test, list):
            list_test.update({n: "Ok" for n in name_of_test})
        if isinstance(name_of_test, dict):
            list_test.update(name_of_test)

    @staticmethod
    def get_configuration():
        """function returns configuration for environment"""

        global global_config

        if global_config is None:
            global_config_file = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), "global_config.yaml")
            with open(global_config_file, 'r') as file:
                global_config = yaml.load(file)

        return global_config

    @staticmethod
    def gen_rand_string(object_type, size=6):
        rand_str = ''.join(random.choice(string.digits) for _ in range(size))
        return 'selenium-{}-{}'.format(object_type, rand_str)
