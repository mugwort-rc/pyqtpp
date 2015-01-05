# -*- coding: utf-8 -*-

import ast

def attr2list(node):
    prefix = []
    assert isinstance(node, ast.Attribute)
    if isinstance(node.value, ast.Attribute):
        prefix = attr2list(node.value)
    elif isinstance(node.value, ast.Name):
        prefix = [name2str(node.value)]
    return prefix + [node.attr]

def name2str(node):
    assert isinstance(node, ast.Name)
    return node.id
