__author__ = 'Ryan'

from xlrd import open_workbook


class Excel(object):
    __file_name = ""
    __book = None
    __sheet = None

    def __init__(self):
        pass

    def open_book(self, file_name):
        self.__file_name = file_name
        self.__book = open_workbook(file_name)

    def open_sheet_by_name(self, sheet_name):
        self.__sheet = self.__book.sheet_by_name(sheet_name)

    def get_max_row(self):
        return self.__sheet.nrows

    def get_max_col(self):
        return self.__sheet.ncols

    def open_sheet_by_index(self, sheet_index):
        self.__sheet = self.__book.sheet_by_index(sheet_index)

    def read_cell(self, row, col):
        return self.__sheet.cell(row, col).value

    def read_block(self, begain_row, end_row, begain_col, end_col):
        if begain_row >= end_row:
            print "The number of row is wrong, from %d to %d" % (begain_row, end_row)
            return None
        if begain_col >= end_col:
            print "The number of col is wrong, from %d to %d" % (begain_col, end_col)
            return None
        data = list()
        for row in range(begain_row, end_row):
            data_row = list()
            for col in range(begain_col, end_col):
                data_row.append(self.__sheet.cell(row, col).value)
            data.append(data_row)
        return data

    def read_cols(self, begain_row, end_row, cols):
        if begain_row >= end_row:
            print "The number of row is wrong, from %d to %d" % (begain_row, end_row)
            return None
        data = list()
        for row in range(begain_row, end_row):
            data_row = list()
            for col in cols:
                data_row.append(self.__sheet.cell(row, col).value)
            data.append(data_row)
        return data