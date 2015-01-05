# -*- coding: utf-8 -*-

import ast

from PyQt4 import Qt, QtCore

from . import util

CPP_CLASS_HEADER_BASE = '''class {0} {1}{{
public:
    {0}();
    ~{0}();

{2}
}};'''

QT_SIGNAL_HEADER_BASE = '''signals:\n    {0}\n'''
QT_SIGNAL_FUNCTION_BASE = 'void {0}({1});'


class ParserBase(object):
    def __init__(self, node):
        self.source_node = node

    @property
    def source_node(self):
        return self.__source_node

    @source_node.setter
    def source_node(self, node):
        self.__source_node = node


class PyQtClass(ParserBase):
    def __init__(self, node):
        super(PyQtClass, self).__init__(node)
        self.bases = []
        self.slots = []
        self.signals = []
        self.members = []

    def toCppHeader(self):
        return CPP_CLASS_HEADER_BASE.format(self.name, self._bases(), self._header())

    def _bases(self):
        if self.bases:
            return ':\n    public {}\n'.format(
                ',\n    public '.join([x.toStr() for x in self.bases])
            )
        return ''

    def _header(self):
        body = []
        # members
        # signals
        signals = []
        for signal in self.signals:
            signals.append(signal.toCppDefinition())
        if signals:
            body.append(QT_SIGNAL_HEADER_BASE.format('\n    '.join(signals)))
        # slots
        return '\n'.join(body)

    @property
    def name(self):
        return self.source_node.name

    @staticmethod
    def parse(node):
        result = PyQtClass(node)
        for child in node.bases:
            type = TypeParser.parse(child)
            if type is None:
                raise UnknownType
            result.bases.append(type)
        for child in node.body:
            if isinstance(child, ast.Assign):
                result.signals += PyQtSignal.parse(child)
        return result


class PyQtSignal(ParserBase):
    def __init__(self, node, name, params=[]):
        super(PyQtSignal, self).__init__(node)
        self.name = name
        self.params = params

    def toCppDefinition(self):
        return QT_SIGNAL_FUNCTION_BASE.format(
            self.name,
            ', '.join([x.toStr() for x in self.params])
        )

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, params):
        self.__params = params

    @classmethod
    def parse(cls, node):
        # check assign of pyqtSignal
        if not isinstance(node, ast.Assign):
            return []
        # assign target
        names = []
        for target in node.targets:
            if isinstance(target, ast.Name):
                names.append(target.id)
        # check call of pyqtSignal
        if isinstance(node.value, ast.Call) and cls._isPyQtSignal(node.value.func):
            # signal args
            args = []
            for arg in node.value.args:
                # Basic type
                type = TypeParser.parse(arg)
                if type is not None:
                    args.append(type)
                else:
                    raise UnknownType
            # build signals
            result = []
            for name in names:
                result.append(PyQtSignal(node, name, args))
            return result
        # is not pyqtSignal
        return []

    @classmethod
    def _isPyQtSignal(cls, node):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            return node.value.id == 'QtCore' and node.attr == 'pyqtSignal'
        elif isinstance(node, ast.Name):
            return node.id == 'pyqtSignal'
        return False


class TypeException(Exception):
    pass

class UnknownType(TypeException):
    pass


class TypeParser(object):

    TYPES = []

    @classmethod
    def parse(cls, node):
        for parser in cls.TYPES:
            result = parser.parse(node)
            if result is not None:
                return result
        return None

    @classmethod
    def register(cls, parser):
        cls.TYPES.append(parser)


class TypeBase(ParserBase):
    def __init__(self, node, name):
        super(TypeBase, self).__init__(node)
        self.name = name

    def toStr(self):
        return self.name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name


class BasicType(TypeBase):

    AllTypes = [
        'bool',
        'int',
        'long',
        'float',
        'complex',
        'str',
        'unicode',
        'tuple',
        'list',
        'dict',
    ]

    def toStr(self):
        if self.name in ['str', 'unicode']:
            return 'QString'
        elif self.name in ['tuple', 'list', 'dict']:
            return 'QVariant'
        elif self.name == 'complex':
            return 'std::complex<double>'
        else:
            return super(BasicType, self).toStr()

    @classmethod
    def parse(cls, node):
        if isinstance(node, ast.Name) and node.id in cls.AllTypes:
            return BasicType(node, node.id)
        return None


class PyQtType(TypeBase):

    AllTypes = []

    @classmethod
    def parse(cls, node):
        if isinstance(node, ast.Attribute) and node.attr in cls.AllTypes:
            return PyQtType(node, node.attr)
        elif isinstance(node, ast.Name) and node.id in cls.AllTypes:
            return PyQtType(node, node.id)
        return None

    @classmethod
    def register(cls, name):
        cls.AllTypes.append(name)


class UnknownType(TypeBase):

    AllTypes = []

    @classmethod
    def parse(cls, node):
        if isinstance(node, ast.Attribute):
            return UnknownType(node, '::'.join(util.attr2list(node)))
        elif isinstance(node, ast.Name):
            return UnknownType(node, util.name2str(node))
        return None

    @classmethod
    def register(cls, name):
        cls.AllTypes.append(name)


# register
def pyqt_register(base):
    for name in dir(base):
        if isinstance(getattr(Qt, name), QtCore.pyqtWrapperType):
            PyQtType.register(name)

pyqt_register(Qt)

TypeParser.register(BasicType)
TypeParser.register(PyQtType)
TypeParser.register(UnknownType)
