# -*- coding: utf-8 -*-

import ast

from .. import util

class TestAstUtil:
    def setup_method(self, m):
        self.node = ast.parse('hoge.fuga.piyo').body[0].value

    def test_attr2list(self):
        result = util.attr2list(self.node)
        assert result == ['hoge', 'fuga', 'piyo']

    def test_name2str(self):
        result = util.name2str(self.node.value.value)
        node = ast.parse('piyo').body[0]
