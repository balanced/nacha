# coding: utf-8
from __future__ import unicode_literals

import nacha

from . import TestCase


class TestAlphaNumeric(TestCase):

    def setUp(self):
        self.field = nacha.Alphanumeric(18)

    def test_expectations(self):
        field = self.field.pack('X9X')
        self.assertEqual('%s' % field, 'X9X'.ljust(18, ' '))

    def test_when_doesnt_validate(self):
        with self.assertRaises(nacha.Alphanumeric.error_type) as exc:
            self.field.pack('BALANCEDバカ'.encode('utf-8'))
        self.assertIn(
            b'has invalid character', exc.exception.message,
        )

    def test_attributes(self):
        self.assertEqual(self.field.length, 18)


class TestNumeric(TestCase):

    def setUp(self):
        self.field = nacha.Numeric(9)

    def test_expectations(self):
        value = self.field.pack('1')
        self.assertEqual('%s' % value, '1'.rjust(9, '0'))

    def test_when_doesnt_validate(self):
        with self.assertRaises(nacha.Numeric.error_type) as exc:
            self.field.pack('%^&')
        self.assertIn(
            ' value %^& for - must be a whole number', str(exc.exception)
        )

    def test_attributes(self):
        self.assertEqual(self.field.length, 9)
