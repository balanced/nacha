"""
"""
__version__ = '0.1.0'

__all__ = [
    'FileHeader',
    'CompanyBatchHeader',
    'EntryDetailRecord',
    'EntryDetailAddendum',
    'CompanyBatchControlRecord',
    'FileControlRecord',
]

from .packages import bryl


Numeric = bryl.Numeric

Alphanumeric = bryl.Alphanumeric


class Record(bryl.Record):

    record_type = Alphanumeric(1)



class FileHeader(Record):

    record_type = Record.record_type.constant('1')

    priority_code = Numeric(2).constant(1)

    immediate_destination = Numeric(10, pad=b' ')

    immediate_origin = Alphanumeric(10)

    file_creation_date = Numeric(6)

    file_creation_time = Numeric(4)

    file_id_modifier = Alphanumeric(1)

    record_size = Numeric(3).constant(94)

    blocking_factor = Numeric(2).constant(10)

    format_code = Numeric(1).constant(1)

    immediate_destination_name = Alphanumeric(23)

    immediate_origin_name = Alphanumeric(23)

    reference_code = Alphanumeric(8, default='')


class CompanyBatchHeader(Record):

    record_type = Record.record_type.constant('5')

    service_class_code = Numeric(3)

    company_name = Alphanumeric(length=16)

    company_discretionary_data = Alphanumeric(length=20, required=False)

    company_id = Alphanumeric(10)

    standard_entry_class = Alphanumeric(3)

    company_entry_description = Alphanumeric(10)

    company_descriptive_date = Alphanumeric(6)

    effective_entry_date = Numeric(6)

    # NOTE: this field is reserved for the banks
    settlement_date = Alphanumeric(3)

    originator_status = bryl.Numeric(1).constant(1)

    originating_dfi_id = Numeric(8)

    batch_number = Numeric(7)


class EntryDetailRecord(Record):

    record_type = Record.record_type.constant('6')

    transaction_code = Numeric(2)

    receiving_dfi_trn = Numeric(8)

    receiving_dfi_trn_check_digit = Numeric(1)

    receiving_dfi_account_number = Alphanumeric(17, align=Alphanumeric.RIGHT)

    amount = Numeric(10)

    # TODO: has dependencies
    individual_id = Alphanumeric(15)

    # TODO: has dependencies
    individual_name = Alphanumeric(22)

    # TODO: specific to wells fargo
    discretionary_data = Alphanumeric(2)

    addenda_record_indicator = Numeric(1)

    trace_number = Numeric(15)

    @property
    def routing_number(self):
        return self.receiving_dfi_trn + self.receiving_dfi_trn_check_digit


class EntryDetailAddendum(Record):

    record_type = Record.record_type.constant('7')

    addenda_type = Numeric(2).constant(5)

    payment_related_information = Alphanumeric(80)

    addenda_sequence_number = Numeric(4)

    entry_detail_sequence_number = Numeric(7)


class CompanyBatchControlRecord(Record):

    record_type = Record.record_type.constant('8')

    service_class_code = Numeric(3)

    entry_addenda_count = Numeric(6)

    entry_hash = Numeric(10)

    total_batch_debit_entry_amount = Numeric(12)

    total_batch_credit_entry_amount = Numeric(12)

    company_id = Alphanumeric(10)

    message_authentication_code = Alphanumeric(19).reserved()

    blank = Alphanumeric(6).reserved()

    originating_dfi_id = Numeric(8)

    batch_number = Numeric(7)


class FileControlRecord(Record):

    record_type = Record.record_type.constant('9')

    batch_count = Numeric(6)

    block_count = Numeric(6)

    entry_addenda_record_count = Numeric(8)

    entry_hash_total = Numeric(10)

    total_file_debit_entry_amount = Numeric(12)

    total_file_credit_entry_amount = Numeric(12)

    filler = Alphanumeric(39).reserved()
