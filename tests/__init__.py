import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestCase(unittest.TestCase):

    @classmethod
    def fixture_path(cls, *parts):
        base_path = os.path.dirname(__file__)
        return os.path.join(base_path, 'fixtures', *parts)

    @classmethod
    def open_fixture(cls, *path):
        return open(cls.fixture_path(*path), 'r')

    @classmethod
    def read_fixture(cls, *path):
        return cls.open_fixture(*path).read()

    @classmethod
    def fixture_lines(cls, *path):
        for line in cls.open_fixture(*path).readlines():
            yield line

    @classmethod
    def fixture_line(cls, number, *path):
        for i, line in enumerate(cls.fixture_lines(*path)):
            if i + 1 == number:
                return line
        raise IndexError('fixture "{0}" does not have line {1}'.format(
            cls.fixture_path(*path), number,
        ))
