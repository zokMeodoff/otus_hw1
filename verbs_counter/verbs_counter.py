import ast
import os
import collections

from config import Config
from functions import flat_list, is_verb


def get_trees(path):
    trees = []
    for filename in get_filenames(path):
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None
        if tree is not None:
            trees.append(tree)
    print('trees generated')
    return trees


def get_filenames(path, file_extention='.py'):
    filenames = []
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith(file_extention):
                filenames.append(os.path.join(dirname, file))
    print('total %s files' % len(filenames))
    return filenames


def get_functions(trees):
    functions = []
    for tree in trees:
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            function = node.name.lower()
            if not (function.startswith('__') and function.endswith('__')):
                functions.append(function)
    return functions


def get_verbs_from_functions(functions):
    verbs = []
    for function_name in functions:
        verbs.extend([word for word in function_name.split('_') if is_verb(word)])
    return verbs


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_all_words_in_path(path):
    trees = get_trees(path)
    words = flat_list([get_all_names(t) for t in trees])
    function_names = [f for f in words if not (f.startswith('__') and f.endswith('__'))]

    def split_snake_case_name_to_words(name):
        return [n for n in name.split('_') if n]
    return flat_list([split_snake_case_name_to_words(function_name) for function_name in function_names])


def get_top_functions_names_in_path(path, top_size=Config.top_size):
    trees = get_trees(path)
    functions = get_functions(trees)
    function_names = [f for f in functions if not (f.startswith('__') and f.endswith('__'))]
    return collections.Counter(function_names).most_common(top_size)


def get_top_verbs_in_path(path, top_size=Config.top_size):
    trees = get_trees(path)
    functions = get_functions(trees)
    verbs = get_verbs_from_functions(functions)
    return collections.Counter(verbs).most_common(top_size)


if __name__ == '__main__':
    verb_list = []
    for project in Config.projects:
        path = os.path.join('.', project)
        if os.path.exists(path):
            verb_list += get_top_verbs_in_path(path)
    print('total %s verbs, %s unique' % (len(verb_list), len(set(verb_list))))
    for verb, occurence in verb_list:
        print(verb, occurence)