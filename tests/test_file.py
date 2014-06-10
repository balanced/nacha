import datetime
import StringIO

import nacha

from . import TestCase


class TestWriter(TestCase):

    credits = [
        {
            'transaction_code': nacha.EntryDetail.transaction_code.CHECKING_CREDIT,
            'receiving_dfi_routing_number': 112345678,
            'receiving_dfi_account_number': '1123456789',
            'individual_name': 'Test Credit 1',
            'individual_id': '98789789',
            'amount': 12345,

        },
        {
            'transaction_code': nacha.EntryDetail.transaction_code.CHECKING_CREDIT,
            'receiving_dfi_routing_number': 131541348,
            'receiving_dfi_account_number': '1312545400',
            'individual_name': 'Test Credit 2',
            'individual_id': '12312312',
            'amount': 145,
        },
    ]

    def test_it(self):
        created_at = datetime.datetime(
            year=2013, month=1, day=16, hour=15, minute=5
        )
        io = StringIO.StringIO()
        writer = nacha.Writer(io)
        with writer.begin_file(
                 immediate_destination=91000019,
                 immediate_destination_name='WELLS FARGO',
                 immediate_origin=1273720697,
                 immediate_origin_name='ALALALAD PAYMENTS',
                 created_at=created_at,
             ):
            with writer.begin_company_batch(
                     service_class_code=nacha.CompanyBatchHeader.service_class_code.MIXED_DEBITS_CREDITS,
                     company_name='ALALALAD',
                     company_id=2273720697,
                     standard_entry_class=nacha.CompanyBatchHeader.standard_entry_class.PPD,
                     company_entry_description='payouts',
                     originating_dfi_id='12737206',
                     effective_entry_date=None,
                     company_discretionary_data='ACH Settlement',
                 ):
                for credit in self.credits:
                    writer.entry(**credit)

        self.maxDiff = None
        expected_lines = [
            l.replace('\n', '') for l in self.fixture_lines('sample')
        ]
        lines = unicode(io.getvalue()).split('\n')[:-1]
        self.assertEqual(lines, expected_lines)


class TestReader(TestCase):

    def _read(self, *fixture):
        reader = nacha.Reader(self.open_fixture(*fixture))
        records = list(reader)
        expected_lines = [l.rstrip('\n') for l in self.fixture_lines(*fixture)]
        lines = [
            record.dump()
            for record in records
        ]
        self.assertEqual(expected_lines, lines)
        return records

    def test_it(self):
        records = self._read('sample')
        self.assertEqual(len(records), 6)
        file_header, file_control = records[0], records[-1]
        self.assertEqual(file_control.batch_count, 1)
        batch_header, batch_control = records[1], records[-2]
        self.assertEqual(batch_control.entry_addenda_count, 2)
        self.assertEqual(file_control.entry_addenda_record_count, 2)
        self.assertEqual(file_header.immediate_origin, '1273720697')
        self.assertEqual(batch_header.company_id, '2273720697')

    def test_it_with_addenda(self):
        records = self._read('sample_with_addenda')
        self.assertEqual(len(records), 7)
        file_header, file_control = records[0], records[-1]
        self.assertEqual(file_control.batch_count, 1)
        batch_header, batch_control = records[1], records[-2]
        self.assertEqual(batch_control.entry_addenda_count, 3)
        self.assertEqual(file_control.entry_addenda_record_count, 3)
        self.assertEqual(file_header.immediate_origin, '1273720697')
        self.assertEqual(batch_header.company_id, '2273720697')

    def test_it_batched_by_descriptor(self):
        records = self._read('sample_batched_by_descriptor')
        self.assertEqual(len(records), 74)
        file_control = records[-1]
        self.assertEqual(file_control.batch_count, 6)
        company_ids = [
            record.company_id
            for record in records
            if isinstance(record, nacha.CompanyBatchHeader)
        ]
        self.assertItemsEqual(company_ids, ['2273720697'] * 6)
