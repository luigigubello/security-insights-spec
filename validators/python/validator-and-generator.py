#!/usr/bin/env python

import collections
import click
import jsonschema
import yaml
import re
import rfc3339_validator
import datetime
import rfc3987
import iteration_utilities


def validate_security_insights(security_insights_path, schema_path="./security-insights-schema-1.0.0.yaml"):
    with open(schema_path, 'r') as file:
        schema = file.read()
    with open(security_insights_path, 'r') as file:
        security_insights = file.read()
    validator = jsonschema.Draft7Validator(yaml.full_load(schema), format_checker=jsonschema.draft7_format_checker)
    errors = validator.iter_errors(yaml.full_load(security_insights))
    errors_json = {"errors": []}
    for error in errors:
        errors_json['errors'].append(error.__dict__)
    return errors_json


def beautiful_print(json_response):
    if json_response['errors']:
        print('Errors')
        print('-----')
        for item in json_response['errors']:
            print("Message: {}".format(item['message']))
            print("Relative schema path: {}".format(list(collections.deque(item['relative_schema_path']))))
            print("$id: {}".format(item['schema']['$id']))
            print('-----')
    else:
        print('No errors found')


def security_insights_yaml(yaml_dict):
    # need to be improved
    # really, need help :(
    security_insights_json = {}
    for key in yaml_dict['properties']:
        if key in security_insights_generic.keys():
            if 'properties' in yaml_dict['properties'][key].keys():
                for subkey in security_insights_generic[key]:
                    if security_insights_generic[key][subkey] is None:
                        security_insights_generic[key][subkey] = security_insights_generic[subkey]
                security_insights_json[key] = security_insights_generic[key]
            else:
                security_insights_json[key] = security_insights_generic[key][key]
            remove_null_values(security_insights_generic, key)
    return security_insights_json


def remove_null_values(mydict, key):
    if type(mydict[key]) is dict:
        for item in mydict[key].keys():
            if mydict[key][item] is None:
                mydict[key][item] = security_insights_generic[item]
            if type(mydict[key][item]) is list or type(mydict[key][item]) is dict:
                remove_null_values(mydict[key], item)
    if type(mydict[key]) is list:
        i = 0
        for item in mydict[key]:
            if type(item) is list or type(item) is dict:
                remove_null_values(mydict[key], i)
            i += 1


def save_yaml(yaml_dict, path):
    with open(path, 'w') as file:
        file.write(yaml_dict)


printable_result = {"result": ""}


# this custom function should fix the norway problem caused by pyyaml
# norway is nice, it's a yaml problem
def fix_norway_problem(security_insights, num, is_list, key=None):
    if type(security_insights) is dict:
        counter = 0
        for my_key in security_insights.keys():
            if type(security_insights[my_key]) is dict or type(security_insights[my_key]) is list:
                if is_list and not counter:
                    counter += 1
                    printable_value = ('  ' * (num-1)) + '- ' + my_key + ':'
                    printable_result['result'] += printable_value + '\n'
                    print(printable_value)
                else:
                    if is_list:
                        printable_value = ('  ' * (num-1)) + my_key + ':'
                    else:
                        printable_value = ('  ' * num) + my_key + ':'
                    printable_result['result'] += printable_value + '\n'
                    print(printable_value)
            num += 1
            if is_list and not counter:
                counter += 1
                fix_norway_problem(security_insights[my_key], num, True, my_key)
            else:
                if not is_list:
                    fix_norway_problem(security_insights[my_key], num, False, my_key)
                else:
                    num -= 1
                    fix_norway_problem(security_insights[my_key], num, False, my_key)
                    num += 1
            num -= 1
    elif type(security_insights) is list:
        i = 0
        while i < len(security_insights):
            num += 1
            fix_norway_problem(security_insights[i], num, True)
            i += 1
            num -= 1
    else:
        if not is_list:
            if isinstance(security_insights, str):
                printable_value = ('  ' * (num - 1)) + key + ': \'' + security_insights + '\''
                printable_result['result'] += printable_value + '\n'
                print(printable_value)
            else:
                printable_value = ('  ' * (num - 1)) + key + ': ' + str(security_insights)
                printable_result['result'] += printable_value + '\n'
                print(printable_value)
        else:
            if key is None:
                if isinstance(security_insights, str):
                    printable_value = ('  ' * (num - 2)) + '- ' + '\'' + security_insights + '\''
                    printable_result['result'] += printable_value + '\n'
                    print(printable_value)
                else:
                    printable_value = ('  ' * (num - 2)) + '- ' + str(security_insights)
                    printable_result['result'] += printable_value + '\n'
                    print(printable_value)
            else:
                if isinstance(security_insights, str):
                    printable_value = ('  ' * (num - 3)) + '- ' + key + ': \'' + security_insights + '\''
                    printable_result['result'] += printable_value + '\n'
                    print(printable_value)
                else:
                    printable_value = ('  ' * (num - 3)) + '- ' + key + ': ' + str(security_insights)
                    printable_result['result'] += printable_value + '\n'
                    print(printable_value)


# defined according security-insights-schema-v1.0.0
def unwind_if_then(dictionary):
    opt_requirement = {}
    for key in dictionary['if']['properties'].keys():
        opt_requirement[key] = dictionary['if']['properties'][key]['const']
    opt_requirement['required'] = dictionary['then']['required']
    return opt_requirement


security_insights_generic = {}


def unwind_properties(dictionary):
    if 'properties' in dictionary:
        security_insights_temp = {}
        requirements = []
        opt_requirements = []
        if 'required' in dictionary:
            requirements = dictionary['required']
        if 'if' in dictionary:
            opt_requirements.append(unwind_if_then(dictionary))
        if 'else' in dictionary:
            opt_requirements.append(unwind_if_then(dictionary['else']))
        for key in requirements:
            security_insights_generic[key] = security_insights_temp
            if 'items' in dictionary['properties'][key]:
                security_insights_temp[key] = unwind_items(dictionary['properties'][key], True)
            else:
                unwind_properties(dictionary['properties'][key])
                security_insights_temp[key] = properties_dialog(dictionary['properties'][key], True)
        for item in opt_requirements:
            for key in item.keys():
                if key != 'required':
                    for element in item['required']:
                        if element not in requirements and security_insights_temp[key] == item[key]:
                            security_insights_generic[element] = security_insights_temp
                            if 'items' in dictionary['properties'][element]:
                                security_insights_temp[element] = unwind_items(dictionary['properties'][element],
                                                                               True)
                            else:
                                unwind_properties(dictionary['properties'][element])
                                security_insights_temp[element] = properties_dialog(dictionary['properties'][element],
                                                                                    True)
                            requirements.append(element)
        for key in list(set(dictionary['properties'].keys()) - set(requirements)):
            question = input("The property [{}] is optional. Do you want to add it? [Y/n]".format(key))
            if question.lower() == 'y':
                security_insights_generic[key] = security_insights_temp
                if 'items' in dictionary['properties'][key]:
                    security_insights_temp[key] = unwind_items(dictionary['properties'][key], False)
                else:
                    unwind_properties(dictionary['properties'][key])
                    security_insights_temp[key] = properties_dialog(dictionary['properties'][key], False)
        if '$id' in dictionary.keys():
            security_insights_generic[str(dictionary['$id'].split('/')[-1])] = security_insights_temp
        return security_insights_temp


def unwind_items(dictionary, required=False):
    if 'items' in dictionary:
        for item in dictionary['items']['anyOf']:
            if 'properties' in item.keys():
                items_array = []
                if required:
                    items_array = [unwind_properties(dictionary['items']['anyOf'][0])]
                    question = input('Do you want to add a new element? [y/N]')
                else:
                    question = 'y'
                while question == 'y':
                    items_array.append(unwind_properties(dictionary['items']['anyOf'][0]))
                    question = input('Do you want to add a new element? [y/N]')
                return list(iteration_utilities.unique_everseen(items_array))
            else:
                if required:
                    item_value = properties_dialog(item, required)
                else:
                    question = input('Do you want to add a new element? [y/N]')
                    if question == 'y':
                        item_value = properties_dialog(item, required)
                    else:
                        item_value = ''
                if not item_value:
                    return []
                else:
                    items_array = [item_value]
                    question = input('Do you want to add a new element? [y/N]')
                    while question == 'y':
                        item_value = properties_dialog(item, False)
                        items_array.append(item_value)
                        question = input('Do you want to add a new element? [y/N]')
                    return list(set(items_array))


def properties_dialog(schema_property, required=False):
    # need to improve
    if 'description' in schema_property.keys() or schema_property['$id'].split('/')[-1] == '0':
        if schema_property['$id'].split('/')[-1] != '0':
            if required:
                print("(required) Property: {}".format(schema_property['$id'].split('/')[-1]))
            else:
                print("Property: {}".format(schema_property['$id'].split('/')[-1]))
        else:
            if required:
                print("(required) Property: {}".format(schema_property['$id'].split('/')[-4]))
            else:
                print("Property: {}".format(schema_property['$id'].split('/')[-4]))
        if 'description' in schema_property.keys():
            print("{}".format(schema_property['description']))
        value = input("Value: ")
        if required:
            while not value:
                value = input("Value: ")
        else:
            if not value:
                return value
        if 'type' in schema_property.keys():
            type_boolean = type_check(value, schema_property['type'])
            while not type_boolean:
                value = input("Value: ")
                type_boolean = type_check(value, schema_property['type'])
            if schema_property['type'] == 'boolean':
                if value == 'True':
                    value = bool('True')
                else:
                    value = bool('')
            if schema_property['type'] == 'integer':
                value = int(value)
        if 'format' in schema_property.keys():
            format_boolean = format_check(value, schema_property['format'])
            while not format_boolean:
                value = input("Value: ")
                format_boolean = format_check(value, schema_property['format'])
        if 'pattern' in schema_property.keys():
            pattern_boolean = pattern_check(value, schema_property['pattern'])
            while not pattern_boolean:
                value = input("Value: ")
                pattern_boolean = pattern_check(value, schema_property['pattern'])
        if 'enum' in schema_property.keys():
            enum_boolean = enum_check(value, schema_property['enum'])
            while not enum_boolean:
                value = input("Value: ")
                enum_boolean = enum_check(value, schema_property['enum'])
        return value


def type_check(value, input_type):
    if input_type == 'string':
        return isinstance(value, str)
    if input_type == 'boolean':
        if str(value) in ['True', 'False']:
            return True
        else:
            return False
    if input_type == 'integer':
        return value.isdigit()


def format_check(value, input_format):
    if input_format == 'iri':
        try:
            rfc3987.parse(value, rule='URI')
            return True
        except ValueError:
            return False
    if input_format == 'date-time':
        return rfc3339_validator.validate_rfc3339(value)
    if input_format == 'date':
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    if input_format == 'idn-email':
        try:
            return True
        except ValueError:
            return False


def pattern_check(value, pattern):
    if re.match(pattern, value):
        return True
    else:
        print('regex error')
        return False


def enum_check(value, enum):
    if value in enum:
        return True
    else:
        return False


# not used in the proper way :(
class NaturalOrderGroup(click.Group):
    def list_commands(self, ctx):
        return self.commands.keys()


@click.group(cls=NaturalOrderGroup)
def security_insights_cli():
    """
    🌈 SECURITY INSIGHTS Generator and Validator\n
    Made with ❤️ by Luigi Gubello\n
    """
    pass


@click.command(help='Verify the SECURITY INSIGHTS yaml according to the schema.')
@click.argument('path', nargs=1, type=click.Path(exists=True))
@click.argument('schema', nargs=1, type=click.Path(exists=True), required=False)
@click.option('--json', 'json_dict', is_flag=True, help='Optional. Print JSON result.')
def verify(path, schema, json_dict):
    if not json_dict:
        response = validate_security_insights(path, schema)
        beautiful_print(response)
    else:
        response = validate_security_insights(path, schema)
        print(response)


@click.command(help='Create the SECURITY INSIGHTS yaml satisfying the schema.')
@click.argument('path', nargs=1, type=click.Path(), required=False, default="./SECURITY-INSIGHTS.yml")
@click.argument('schema', nargs=1, type=click.Path(exists=True), required=False,
                default="./security-insights-schema-1.0.0.yaml")
def create(path, schema):
    with open(schema, 'r') as file:
        schema = file.read()
    yaml_dict = yaml.full_load(schema)
    unwind_properties(yaml_dict)
    security_insights_json = security_insights_yaml(yaml_dict)
    print('\nSECURITY INSIGHTS\n')
    fix_norway_problem(security_insights_json, 0, False)
    save_yaml(printable_result['result'][:-1], path)

    
security_insights_cli.add_command(verify)
security_insights_cli.add_command(create)

if __name__ == "__main__":
    security_insights_cli()
