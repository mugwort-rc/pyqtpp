# -*- coding: utf-8 -*-

import ast

from ..pyqtparser import (
    BasicType, PyQtType, UnknownType,
    TypeParser,
    PyQtClass, PyQtSignal,
)

class TestBase(object):
    def parse_body(self, source):
        return ast.parse(source).body[0]

    def parse_expr(self, source):
        return self.parse_body(source).value

class TestBasicType(TestBase):
    def test_bool(self):
        node = self.parse_expr('bool')
        type = BasicType.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'bool'
        assert type.toStr() == 'bool'

    def test_int(self):
        node = self.parse_expr('int')
        type = BasicType.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'int'
        assert type.toStr() == 'int'

    def test_long(self):
        node = self.parse_expr('long')
        type = BasicType.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'long'
        assert type.toStr() == 'long'

    def test_float(self):
        node = self.parse_expr('float')
        type = BasicType.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'float'
        assert type.toStr() == 'float'

    def test_complex(self):
        node = self.parse_expr('complex')
        type = BasicType.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'complex'
        assert type.toStr() == 'std::complex<double>'

    def test_str(self):
        node = self.parse_expr('str')
        type = BasicType.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'str'
        assert type.toStr() == 'QString'

    def test_unicode(self):
        node = self.parse_expr('unicode')
        type = BasicType.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'unicode'
        assert type.toStr() == 'QString'

    def test_tuple(self):
        node = self.parse_expr('tuple')
        type = BasicType.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'tuple'
        assert type.toStr() == 'QVariant'

    def test_list(self):
        node = self.parse_expr('list')
        type = BasicType.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'list'
        assert type.toStr() == 'QVariant'

    def test_dict(self):
        node = self.parse_expr('dict')
        type = BasicType.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'dict'
        assert type.toStr() == 'QVariant'


class TestPyQtType(TestBase):
    def test_qobject(self):
        node = self.parse_expr('QObject')
        type = PyQtType.parse(node)
        assert isinstance(type, PyQtType)
        assert type.name == 'QObject'
        assert type.toStr() == 'QObject'


class TestUnknownType(TestBase):
    def test_knowntype(self):
        node = self.parse_expr('Qt.QObject')
        type = UnknownType.parse(node)
        assert isinstance(type, UnknownType)
        assert type.name == 'Qt::QObject'
        assert type.toStr() == 'Qt::QObject'

    def test_unknowntype(self):
        node = self.parse_expr('hoge.fuga')
        type = UnknownType.parse(node)
        assert isinstance(type, UnknownType)
        assert type.name == 'hoge::fuga'
        assert type.toStr() == 'hoge::fuga'


class TestTypeParser(TestBase):
    def test_bool(self):
        node = self.parse_expr('bool')
        type = TypeParser.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'bool'
        assert type.toStr() == 'bool'

    def test_int(self):
        node = self.parse_expr('int')
        type = TypeParser.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'int'
        assert type.toStr() == 'int'

    def test_long(self):
        node = self.parse_expr('long')
        type = TypeParser.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'long'
        assert type.toStr() == 'long'

    def test_float(self):
        node = self.parse_expr('float')
        type = TypeParser.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'float'
        assert type.toStr() == 'float'

    def test_complex(self):
        node = self.parse_expr('complex')
        type = TypeParser.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'complex'
        assert type.toStr() == 'std::complex<double>'

    def test_str(self):
        node = self.parse_expr('str')
        type = TypeParser.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'str'
        assert type.toStr() == 'QString'

    def test_unicode(self):
        node = self.parse_expr('unicode')
        type = TypeParser.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'unicode'
        assert type.toStr() == 'QString'

    def test_tuple(self):
        node = self.parse_expr('tuple')
        type = TypeParser.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'tuple'
        assert type.toStr() == 'QVariant'

    def test_list(self):
        node = self.parse_expr('list')
        type = TypeParser.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'list'
        assert type.toStr() == 'QVariant'

    def test_dict(self):
        node = self.parse_expr('dict')
        type = TypeParser.parse(node)
        assert isinstance(type, BasicType)
        assert type.name == 'dict'
        assert type.toStr() == 'QVariant'

    def test_qobject(self):
        node = self.parse_expr('QObject')
        type = TypeParser.parse(node)
        assert isinstance(type, PyQtType)
        assert type.name == 'QObject'
        assert type.toStr() == 'QObject'

    def test_unknowntype(self):
        node = self.parse_expr('hoge.fuga')
        type = TypeParser.parse(node)
        assert isinstance(type, UnknownType)
        assert type.name == 'hoge::fuga'
        assert type.toStr() == 'hoge::fuga'


class TestPyQtSignal(TestBase):
    def test_signal(self):
        node = self.parse_body('signal = pyqtSignal()')
        signals = PyQtSignal.parse(node)
        assert len(signals) == 1
        signal = signals[0]
        assert isinstance(signal, PyQtSignal)
        assert signal.name == 'signal'
        assert len(signal.params) == 0
        assert signal.toCppDefinition() == 'void signal();'

    def test_signal_with_param(self):
        node = self.parse_body('signal = pyqtSignal(int)')
        signals = PyQtSignal.parse(node)
        assert len(signals) == 1
        signal = signals[0]
        assert isinstance(signal, PyQtSignal)
        assert signal.name == 'signal'
        assert len(signal.params) == 1
        assert signal.params[0].name == 'int'
        assert signal.toCppDefinition() == 'void signal(int);'

    def test_signal_with_pyqt_param(self):
        node = self.parse_body('signal = pyqtSignal(QObject)')
        signals = PyQtSignal.parse(node)
        assert len(signals) == 1
        signal = signals[0]
        assert isinstance(signal, PyQtSignal)
        assert signal.name == 'signal'
        assert len(signal.params) == 1
        assert signal.params[0].name == 'QObject'
        assert signal.toCppDefinition() == 'void signal(QObject);'


SIMPLE_CLASS_EXAMPLE = """
class Test:
    pass
"""

QOBJECT_BASED_EXAMPLE = """
class Test(QObject):                 # [0]
    signal = QtCore.pyqtSignal(int)  # [1]
    test = QtCore.pyqtSignal(str)    # [2]
"""


class TestPyQtClass(TestBase):
    def test_simple_class(self):
        node = self.parse_body(SIMPLE_CLASS_EXAMPLE)
        cls = PyQtClass.parse(node)

        assert len(cls.bases) == 0
        assert len(cls.slots) == 0
        assert len(cls.signals) == 0
        assert len(cls.members) == 0

        # header
        hpp = cls.toCppHeader()
        # name
        assert 'class Test {\n' in hpp
        assert '\n    Test();\n' in hpp
        assert '\n    ~Test();\n' in hpp

    def test_qobject_based(self):
        node = self.parse_body(QOBJECT_BASED_EXAMPLE)
        cls = PyQtClass.parse(node)
        # 0
        assert len(cls.bases) == 1
        assert cls.bases[0].name == 'QObject'
        # 1, 2
        assert len(cls.signals) == 2
        # 1
        assert cls.signals[0].name == 'signal'
        assert len(cls.signals[0].params) == 1
        assert cls.signals[0].params[0].name == 'int'
        # 2
        assert cls.signals[1].name == 'test'
        assert len(cls.signals[1].params) == 1
        assert cls.signals[1].params[0].name == 'str'

        # header
        hpp = cls.toCppHeader()
        # name
        assert 'class Test :\n' in hpp
        assert '\n    Test();\n' in hpp
        assert '\n    ~Test();\n' in hpp
        # inherit
        assert '\n    public QObject\n{' in hpp
        # signals
        assert '\nsignals:\n' in hpp
        assert '\n    void signal(int);\n' in hpp
        assert '\n    void test(QString);\n' in hpp
