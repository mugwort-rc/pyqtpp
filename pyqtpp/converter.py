# -*- coding: utf-8 -*-

import ast

import pyqtparser

def convert(source):
    result = []
    node = ast.parse(source)
    for child in node.body:
        if isinstance(child, ast.ClassDef):
            result.append(pyqtparser.PyQtClass.parse(child))
    return result
