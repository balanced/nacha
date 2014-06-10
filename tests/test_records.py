import datetime

import nacha

from . import TestCase


class TestRecord(TestCase):

    pass


class TestFileHeader(TestRecord):

    def setUp(self):
        self.record = self.fixture_line(1, 'sample').strip('\n')
        self.assertEqual(len(self.record), nacha.FileHeader.length)

    def test_construction_of_file_record_from_string(self):
        fh = nacha.FileHeader.load(self.record)

        self.assertEqual(fh.record_type, '1')
        self.assertEqual(fh.priority_code, 1)
        self.assertEqual(fh.immediate_destination, 91000019)
        self.assertEqual(fh.immediate_origin, '1273720697')

        self.assertIsNotNone(fh.file_creation_date)
        self.assertIsNotNone(fh.file_creation_time)

        self.assertRegexpMatches(fh.file_id_modifier, r'[A-Z]')
        self.assertEqual(fh.record_size, 94)
        self.assertEqual(fh.blocking_factor, 10)
        self.assertEqual(fh.format_code, 1)
        self.assertEqual(fh.immediate_destination_name, 'WELLS FARGO')
        self.assertEqual(fh.immediate_origin_name, 'ALALALAD PAYMENTS')

        self.assertEqual(fh.reference_code, '')

    def test_serialization_of_record(self):
        fh = nacha.FileHeader.load(self.record)
        self.assertEqual(len(fh.dump()), nacha.FileHeader.length)
        self.assertEqual(fh.dump(), self.record)

    def test_construction_of_file_record(self):
        fh_original = nacha.FileHeader.load(self.record)
        fh = nacha.FileHeader(
            immediate_destination='91000019',
            immediate_origin='1273720697',
            file_id_modifier='A',
            file_creation_date=fh_original.file_creation_date,
            file_creation_time=fh_original.file_creation_time,
            immediate_destination_name='WELLS FARGO',
            immediate_origin_name='ALALALAD PAYMENTS',
        )
        self.assertEqual(fh.dump(), self.record)
        self.assertEqual(len(fh.dump()), nacha.FileHeader.length)

    def test_construction_of_invalid_record_throws_exception(self):
        with self.assertRaises(LookupError) as exc:
            fh = nacha.FileHeader(immediate_destination='091000019')
            fh.dump()

        ex = exc.exception
        self.assertEqual(
            ex.message, 'FileHeader.immediate_origin value is missing',
        )

class TestCompanyBatchHeader(TestRecord):

    def setUp(self):
        self.record = self.fixture_line(2, 'sample').strip('\n')
        self.assertEqual(len(self.record), nacha.CompanyBatchHeader.length)

    def test_construction_of_company_batch_header_record(self):
        cbh = nacha.CompanyBatchHeader.load(self.record)
        self.assertEqual(cbh.record_type, '5')
        self.assertEqual(cbh.service_class_code, 200)
        self.assertEqual(cbh.company_name, 'ALALALAD')
        self.assertEqual(cbh.company_discretionary_data, 'ACH Settlement')
        self.assertEqual(cbh.company_id, '2273720697')
        self.assertEqual(cbh.standard_entry_class, 'PPD')
        self.assertEqual(cbh.company_entry_description, 'payouts')
        self.assertEqual(cbh.company_descriptive_date, '')
        self.assertEqual(cbh.effective_entry_date, datetime.date(2013, 1, 16))
        self.assertEqual(cbh.settlement_date, '')
        self.assertEqual(cbh.originator_status, 1)
        self.assertEqual(cbh.originating_dfi_id, 12737206)
        self.assertEqual(cbh.batch_number, 1)


class TestEntryDetail(TestRecord):

    def setUp(self):
        fixture = self.fixture_line(3, 'sample')
        self.record = fixture.strip('\n')
        self.assertEqual(len(self.record), nacha.EntryDetail.length)

    def test_construction_of_entry_detail_record(self):
        edr = nacha.EntryDetail.load(self.record)
        self.assertEqual(edr.record_type, '6')
        self.assertEqual(edr.transaction_code, 22)
        self.assertEqual(edr.receiving_dfi_trn, 11234567)
        self.assertEqual(edr.receiving_dfi_trn_check_digit, 8)
        self.assertEqual(edr.receiving_dfi_account_number, '1123456789')
        self.assertEqual(edr.amount, 12345)
        self.assertEqual(edr.individual_id, '98789789')
        self.assertEqual(edr.individual_name, 'Test Credit 1')
        self.assertEqual(edr.discretionary_data, '')
        self.assertEqual(edr.addenda_record_indicator, 0)
        self.assertEqual(edr.trace_number, 127372060000001)

    def test_serialization_of_record(self):
        fh = nacha.EntryDetail.load(self.record)
        self.assertEqual(fh.dump(), self.record)
        self.assertEqual(len(fh.dump()), nacha.EntryDetail.length)


class TestCompanyBatchControl(TestRecord):

    def setUp(self):
        fixture = self.fixture_line(5, 'sample')
        self.record = fixture.strip('\n')
        self.assertEqual(len(self.record), nacha.CompanyBatchControl.length)

    def test_construction_of_company_batch_control_record(self):
        cbcr = nacha.CompanyBatchControl.load(self.record)
        self.assertEqual(cbcr.record_type, '8')
        self.assertEqual(cbcr.service_class_code, 200)
        self.assertEqual(cbcr.entry_addenda_count, 2)
        self.assertEqual(cbcr.entry_hash, 24388701)
        self.assertEqual(cbcr.total_batch_debit_entry_amount, 0)
        self.assertEqual(cbcr.total_batch_credit_entry_amount, 12490)
        self.assertEqual(cbcr.company_id, '2273720697')
        self.assertEqual(cbcr.message_authentication_code, '')
        self.assertEqual(cbcr.blank, '')
        self.assertEqual(cbcr.originating_dfi_id, 12737206)
        self.assertEqual(cbcr.batch_number, 1)


class TestFileControl(TestRecord):

    def setUp(self):
        fixture = self.fixture_line(6, 'sample')
        self.record = fixture.strip('\n')
        self.assertEqual(len(self.record), nacha.FileControl.length)

    def test_construction_of_file_control_record(self):
        fcr = nacha.FileControl.load(self.record)
        self.assertEqual(fcr.record_type, '9')
        self.assertEqual(fcr.batch_count, 1)
        self.assertEqual(fcr.block_count, 2)
        self.assertEqual(fcr.entry_addenda_record_count, 2)
        self.assertEqual(fcr.entry_hash_total, 24388701)
        self.assertEqual(fcr.total_file_debit_entry_amount, 0)
        self.assertEqual(fcr.total_file_credit_entry_amount, 12490)
        self.assertEqual(fcr.filler, '')


class TestEntryDetailAddendum(TestRecord):

    def setUp(self):
        fixture = self.fixture_line(5, 'sample_with_addenda')
        self.record = fixture.strip('\n')
        self.assertEqual(len(self.record), nacha.EntryDetailAddendum.length)

    def test_construction_of_file_control_record(self):
        record = nacha.EntryDetailAddendum.load(self.record)
        self.assertEqual(record.record_type, '7')
        self.assertEqual(record.addenda_type, 5)
        self.assertEqual(
            record.payment_related_information,
            '0*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*002010',
        )
        self.assertEqual(record.addenda_sequence_number, 1)
        self.assertEqual(record.entry_detail_sequence_number, 2)
