#!/usr/bin/env python3

import time

from ctypes import *

from dmsql import *

def connect(connection_string):
    return Connection(connection_string)

apilevel = "2.0"

threadsafety = 0

paramstyle = "qmark"

class Warning(Exception):
    pass

class Error(Exception):
    pass

class InterfaceError(Error):
    pass

class DatabaseError(Error):
    pass

class DataError(DatabaseError):
    pass

class OperationalError(DatabaseError):
    pass

class IntegrityError(DatabaseError):
    pass

class InternalError(DatabaseError):
    pass

class ProgrammingError(DatabaseError):
    pass

class NotSupportedError(DatabaseError):
    pass

environment_handle = SQLHANDLE()
SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, byref(environment_handle))
SQLSetEnvAttr(environment_handle, SQL_ATTR_ODBC_VERSION, SQL_OV_ODBC3, SQL_IS_UINTEGER)

class Connection:
    def __init__(self, connection_string):
        self.Warning = Warning
        self.Error = Error
        self.InterfaceError = InterfaceError
        self.DatabaseError = DatabaseError
        self.DataError = DataError
        self.OperationalError = OperationalError
        self.IntegrityError = IntegrityError
        self.InternalError = InternalError
        self.ProgrammingError = ProgrammingError
        self.NotSupportedError = NotSupportedError
        self.messages = []
        self.errorhandler = None
        self.connection_handle = SQLHANDLE()

        sqlchar_connection_string = cast(create_string_buffer(str(connection_string).encode()), POINTER(SQLCHAR))

        if environment_handle == SQL_NULL_HENV:
            raise self.InterfaceError("NO ENVIRONMENT HANDLE")

        sr = SQLAllocHandle(SQL_HANDLE_DBC, environment_handle, byref(self.connection_handle))

        if (not sr == SQL_SUCCESS) and (not sr == SQL_SUCCESS_WITH_INFO):
            raise self.InterfaceError("UNABLE TO ALLOC CONNECTION")

        sr = SQLDriverConnect(self.connection_handle,
                              SQL_NULL_HANDLE,
                              sqlchar_connection_string, SQL_NTS,
                              SQL_NULL_SQLCHAR, 0, SQL_NULL_SQLSMALLINT,
                              SQL_DRIVER_NOPROMPT)

        if (not sr == SQL_SUCCESS) and (not sr == SQL_SUCCESS_WITH_INFO):
            SQLFreeHandle(SQL_HANDLE_DBC, self.connection_handle)
            raise self.InterfaceError("BAD CONNECTION")

        self.autocommit(False)

    def close(self):
        SQLDisconnect(self.connection_handle)
        SQLFreeHandle(SQL_HANDLE_DBC, self.connection_handle)

    def autocommit(self, autocommit):
        if autocommit:
            SQLSetConnectAttr(self.connection_handle, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_ON, SQL_IS_INTEGER)
        else:
            SQLSetConnectAttr(self.connection_handle, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF, SQL_IS_INTEGER)

    def commit(self):
        SQLEndTran(SQL_HANDLE_DBC, self.connection_handle, SQL_COMMIT)

    def rollback(self):
        SQLEndTran(SQL_HANDLE_DBC, self.connection_handle, SQL_ROLLBACK)

    def cursor(self):
        return Cursor(self)

    def xid(self, format_id, global_transaction_id, branch_qualifier):
        raise self.NotSupportedError("WORK IN PROGRESS")

    def tpc_begin(self, xid):
        raise self.NotSupportedError("WORK IN PROGRESS")

    def tpc_prepare(self):
        raise self.NotSupportedError("WORK IN PROGRESS")

    def tpc_commit(self, xid = None):
        raise self.NotSupportedError("WORK IN PROGRESS")

    def tpc_rollback(self, xid = None):
        raise self.NotSupportedError("WORK IN PROGRESS")

    def tpc_recover(self):
        raise self.NotSupportedError("WORK IN PROGRESS")

class Cursor:
    def __init__(self, connection):
        self.description = ""
        self.rowcount = 0
        self.arraysize = 0
        self.rownumber = 0
        self.connection = connection
        self.messages = []
        self.lastrowid = 0
        self.errorhandler = self.connection.errorhandler

        self.statement_handle = SQLHANDLE()

        if self.connection.connection_handle == SQL_NULL_HDBC:
            raise self.InterfaceError("BAD CONNECTION")

        sr = SQLAllocHandle(SQL_HANDLE_STMT, self.connection.connection_handle, byref(self.statement_handle))

        if (not sr == SQL_SUCCESS) and (not sr == SQL_SUCCESS_WITH_INFO):
            raise self.InterfaceError("UNABLE TO ALLOC STATEMENT")

        self.scroll_modes = {"absolute" : self.scroll_absolute,
                             "relative" : self.scroll_relative}

        self.sql_type_map = {SQL_DECIMAL : SQL_C_LONG,
                             SQL_INTEGER : SQL_C_LONG,
                             SQL_CHAR : SQL_C_CHAR,
                             SQL_VARCHAR : SQL_C_CHAR,
                             SQL_LONGVARCHAR : SQL_C_CHAR,
                             SQL_WCHAR : SQL_C_CHAR,
                             SQL_WVARCHAR : SQL_C_CHAR,
                             SQL_WLONGVARCHAR : SQL_C_CHAR,
                             SQL_BINARY : SQL_C_BINARY,
                             SQL_VARBINARY : SQL_C_BINARY,
                             SQL_LONGVARBINARY : SQL_C_BINARY,
                             SQL_BIGINT : SQL_C_SBIGINT,
                             SQL_TINYINT : SQL_C_TINYINT,
                             SQL_SMALLINT : SQL_C_SHORT,
                             SQL_BIT : SQL_C_BIT,
                             SQL_REAL : SQL_C_FLOAT,
                             SQL_DOUBLE : SQL_C_DOUBLE,
                             SQL_FLOAT : SQL_C_DOUBLE,
                             SQL_NUMERIC : SQL_C_NUMERIC,
                             SQL_TYPE_DATE : SQL_C_TYPE_DATE,
                             SQL_TYPE_TIME : SQL_C_TYPE_TIME,
                             SQL_TYPE_TIMESTAMP : SQL_C_TYPE_TIMESTAMP}
        self.sql_type_map = {SQL_DECIMAL : SQL_C_LONG,
                             SQL_INTEGER : SQL_C_LONG,
                             SQL_CHAR : SQL_C_CHAR,
                             SQL_VARCHAR : SQL_C_CHAR,
                             SQL_LONGVARCHAR : SQL_C_CHAR,
                             SQL_WCHAR : SQL_C_CHAR,
                             SQL_WVARCHAR : SQL_C_CHAR,
                             SQL_WLONGVARCHAR : SQL_C_CHAR,
                             SQL_BINARY : SQL_C_CHAR,
                             SQL_VARBINARY : SQL_C_CHAR,
                             SQL_LONGVARBINARY : SQL_C_CHAR,
                             SQL_BIGINT : SQL_C_SBIGINT,
                             SQL_TINYINT : SQL_C_TINYINT,
                             SQL_SMALLINT : SQL_C_SHORT,
                             SQL_BIT : SQL_C_BIT,
                             SQL_REAL : SQL_C_FLOAT,
                             SQL_DOUBLE : SQL_C_DOUBLE,
                             SQL_FLOAT : SQL_C_DOUBLE,
                             SQL_NUMERIC : SQL_C_CHAR,
                             SQL_TYPE_DATE : SQL_C_CHAR,
                             SQL_TYPE_TIME : SQL_C_CHAR,
                             SQL_TYPE_TIMESTAMP : SQL_C_CHAR}

        self.buffer_creator = {SQL_C_SSHORT : create_fixed_type_buffer_type(SQLSMALLINT),
                               SQL_C_USHORT : create_fixed_type_buffer_type(SQLUSMALLINT),
                               SQL_C_SHORT : create_fixed_type_buffer_type(SQLSMALLINT),
                               SQL_C_SLONG : create_fixed_type_buffer_type(SQLINTEGER),
                               SQL_C_ULONG : create_fixed_type_buffer_type(SQLUINTEGER),
                               SQL_C_LONG : create_fixed_type_buffer_type(SQLINTEGER),
                               SQL_C_FLOAT : create_fixed_type_buffer_type(SQLREAL),
                               SQL_C_DOUBLE : create_fixed_type_buffer_type(SQLDOUBLE),
                               SQL_C_BIT : create_fixed_type_buffer_type(SQLCHAR),
                               SQL_C_STINYINT : create_fixed_type_buffer_type(SQLSCHAR),
                               SQL_C_UTINYINT : create_fixed_type_buffer_type(SQLCHAR),
                               SQL_C_TINYINT : create_fixed_type_buffer_type(SQLCHAR),
                               SQL_C_SBIGINT : create_fixed_type_buffer_type(SQLBIGINT),
                               SQL_C_UBIGINT : create_fixed_type_buffer_type(SQLUBIGINT),
                               SQL_C_TYPE_DATE : string_buffer,
                               SQL_C_TYPE_TIME : string_buffer,
                               SQL_C_TYPE_TIMESTAMP : string_buffer,
                               SQL_C_NUMERIC : string_buffer,
                               SQL_C_CHAR : string_buffer,
                               SQL_C_WCHAR : string_buffer,
                               SQL_C_BINARY : string_buffer,
                               SQL_C_GUID : string_buffer}

        self.parameter_buffers = None
        self.result_buffers = None

    def __iter__(self):
        row = self.fetchone()

        while row is not None:
            yield row
            row = self.fetchone()

    def callproc(self, procname, *parameters):
        return self

    def close(self):
        SQLFreeHandle(SQL_HANDLE_STMT, self.statement_handle)

    def create_buffer(self, c_type, size):
        return self.buffer_creator[c_type](size)

    def set_parameters(self, parameters):
        if parameters is None:
            return self

        parameter_count = max(len(parameters), len(self.parameter_buffers))

        for index in range(parameter_count):
            self.parameter_buffers[index][3].set_value(parameters[index])

    def bind_parameter_buffers_server_type(self):
        if self.parameter_buffers is not None:
            return self

        self.parameter_buffers = ()
        number_of_parameters = SQLSMALLINT()
        SQLNumParams(self.statement_handle, byref(number_of_parameters))

        data_type = SQLSMALLINT()
        parameter_size = SQLULEN()
        decimal_digits = SQLSMALLINT()
        nullable = SQLSMALLINT()

        for index in range(1, number_of_parameters.value + 1):
            data_type.value = 0
            parameter_size.value = 0
            decimal_digits.value = 0
            nullable.value = 0

            SQLDescribeParam(self.statement_handle, index,
                             byref(data_type),
                             byref(parameter_size),
                             byref(decimal_digits),
                             byref(nullable))

            sql_type = data_type.value
            c_type = self.sql_type_map[sql_type]
            size = parameter_size.value
            digits = decimal_digits.value
            buffer = self.create_buffer(c_type, size)
            self.parameter_buffers = self.parameter_buffers + ((c_type, sql_type, digits, buffer, ), )

            SQLBindParameter(self.statement_handle, index,
                             SQL_PARAM_INPUT,
                             c_type,
                             sql_type,
                             buffer.get_size(),
                             digits,
                             buffer.get_reference(),
                             buffer.get_size(),
                             buffer.get_length_reference())
        return self

    def bind_parameter_buffers_client_type(self, parameters):
        if parameters is None:
            return self

        if self.parameter_buffers is not None:
            return self

        self.parameter_buffers = ()
        number_of_parameters = len(parameters)

        for index in range(number_of_parameters):
            sql_type = SQL_CHAR
            c_type = self.sql_type_map[sql_type]
            size = 512
            digits = 0
            buffer = self.create_buffer(c_type, size)
            self.parameter_buffers = self.parameter_buffers + ((c_type, sql_type, digits, buffer, ), )

            SQLBindParameter(self.statement_handle, index + 1,
                             SQL_PARAM_INPUT,
                             c_type,
                             sql_type,
                             buffer.get_size(),
                             digits,
                             buffer.get_reference(),
                             buffer.get_size(),
                             buffer.get_length_reference())
        return self

    def bind_result_buffers(self):
        if self.result_buffers is not None:
            return self

        self.result_buffers = ()
        number_of_columns = SQLSMALLINT()
        SQLNumResultCols(self.statement_handle, byref(number_of_columns))

        column_name_size = 512;
        column_name = create_string_buffer(column_name_size)
        name_length = SQLSMALLINT()
        data_type = SQLSMALLINT()
        column_size = SQLULEN()
        decimal_digits = SQLSMALLINT()
        nullable = SQLSMALLINT()

        for index in range(1, number_of_columns.value + 1):
            name_length.value = 0
            data_type.value = 0
            column_size.value = 0
            decimal_digits.value = 0
            nullable.value = 0

            SQLDescribeCol(self.statement_handle, index,
                           cast(column_name, POINTER(SQLCHAR)), column_name_size, byref(name_length),
                           byref(data_type),
                           byref(column_size),
                           byref(decimal_digits),
                           byref(nullable))

            sql_type = data_type.value
            c_type = self.sql_type_map[sql_type]
            size = column_size.value
            digits = decimal_digits.value
            buffer = self.create_buffer(c_type, size)
            self.result_buffers = self.result_buffers + ((c_type, sql_type, digits, buffer, ), )

            SQLBindCol(self.statement_handle, index,
                       c_type,
                       buffer.get_reference(),
                       buffer.get_size(),
                       buffer.get_length_reference())

        return self

    def prepare(self, operation):
        SQLFreeStmt(self.statement_handle, SQL_CLOSE)
        SQLFreeStmt(self.statement_handle, SQL_UNBIND)
        SQLFreeStmt(self.statement_handle, SQL_RESET_PARAMS)
        self.parameter_buffers = None
        self.result_buffers = None
        sqlchar_operation = cast(create_string_buffer(str(operation).encode()), POINTER(SQLCHAR))
        SQLPrepare(self.statement_handle, sqlchar_operation, SQL_NTS)
        self.bind_parameter_buffers_server_type()
        return self

    def execute_prepared(self, parameters = None):
        SQLFreeStmt(self.statement_handle, SQL_CLOSE)
        self.set_parameters(parameters)
        SQLExecute(self.statement_handle)
        self.bind_result_buffers()
        return self

    def execute_language(self, operation, parameters = None):
        SQLFreeStmt(self.statement_handle, SQL_CLOSE)
        SQLFreeStmt(self.statement_handle, SQL_UNBIND)
        SQLFreeStmt(self.statement_handle, SQL_RESET_PARAMS)
        self.parameter_buffers = None
        self.result_buffers = None
        self.bind_parameter_buffers_client_type(parameters)
        self.set_parameters(parameters)
        sqlchar_operation = cast(create_string_buffer(str(operation).encode()), POINTER(SQLCHAR))
        SQLExecDirect(self.statement_handle, sqlchar_operation, SQL_NTS)
        self.bind_result_buffers()
        return self

    def execute(self, operation, parameters = None):
        return self.execute_language(operation, parameters)

    def executemany(self, operation, sequence_of_parameters = None):
        self.prepare(operation)

        for parameters in sequence_of_parameters:
            self.execute_prepared(parameters)

        return self

    def fetchone(self):
        sr = SQLFetch(self.statement_handle)

        if sr == SQL_NO_DATA:
            return None

        row = ()

        for column in self.result_buffers:
            row = row + (column[3].get_value(), )

        return row

    def fetchmany(self, size = None):
        if size is None:
            size = self.arraysize

        row_set = ()

        while size > 0:
            row = self.fetchone()

            if row is None:
                break

            row_set = row_set + (row, )

        return row_set

    def fetchall(self):
        row_set = ()

        row = self.fetchone()

        while row is not None:
            row_set = row_set + (row, )
            row = self.fetchone()

        return row_set

    def nextset(self):
        SQLMoreResults(self.statement_handle)
        return self

    def setinputsizes(self, sizes):
        return self

    def setoutputsize(self, size, column = None):
        return self

    def scroll_absolute(self, value):
        SQLFetchScroll(self.statement_handle, SQL_FETCH_ABSOLUTE, value)
        return self

    def scroll_relative(self, value):
        SQLFetchScroll(self.statement_handle, SQL_FETCH_RELATIVE, value)
        return self

    def scroll(self, value, mode = "relative"):
        return scroll_modes[mode](value)

    def next(self):
        row = self.fetchone()

        if row is None:
            raise StopIteration("END OF RESULT SET")

        return row

def Date(year, month, day):
    value = SQL_DATE_STRUCT()
    value.year = year
    value.month = month
    value.day = day
    return value

def Time(hour, minute, second):
    value = SQL_TIME_STRUCT
    value.hour = hour
    value.minute = minute
    value.second = second
    return value

def Timestamp(year, month, day, hour, minute, second):
    value = SQL_TIMESTAMP_STRUCT
    value.year = year
    value.month = month
    value.day = day
    value.hour = hour
    value.minute = minute
    value.second = second
    return value

def DateFromTicks(ticks):
    timestamp = time.localtime(ticks)
    return Date(timestamp.tm_year, timestamp.tm_mon, timestamp.tm_mday)

def TimeFromTicks(ticks):
    timestamp = time.localtime(ticks)
    return Time(timestamp.tm_hour, timestamp.tm_min, timestamp.tm_sec)

def TimestampFromTicks(ticks):
    timestamp = time.localtime(ticks)
    return Timestamp(timestamp.tm_year, timestamp.tm_mon, timestamp.tm_mday,
                     timestamp.tm_hour, timestamp.tm_min, timestamp.tm_sec)

def Binary(string):
    raise self.connection.NotSupportedError("WORK IN PROGRESS")

STRING = None

BINARY = None

NUMBER = None

DATETIME = None

ROWID = None

def create_fixed_type_buffer_type(fixed_type):
    class fixed_type_buffer_type:
        def __init__(self, size):
            self.buffer_size = sizeof(fixed_type)
            self.buffer = fixed_type()
            self.length = SQLLEN()

        def set_value(self, value):
            if value is None:
                self.length.value = SQL_NULL_DATA
            else:
                self.length.value = self.buffer_size
                self.buffer.value = value

        def get_value(self):
            if self.length.value == SQL_NULL_DATA:
                return None
            else:
                return self.buffer.value

        def get_size(self):
            return self.buffer_size

        def get_reference(self):
            return byref(self.buffer)

        def get_length_reference(self):
            return byref(self.length)

    return fixed_type_buffer_type

class string_buffer:
    def __init__(self, size):
        if size > 64:
            self.buffer_size = size
        else:
            self.buffer_size = 64

        self.buffer = create_string_buffer(size)
        self.length = SQLLEN()

    def set_value(self, value):
        if value is None:
            self.length.value = SQL_NULL_DATA
        else:
            encoded_value = str(value).encode()
            self.length.value = len(encoded_value)
            self.buffer.value = encoded_value

    def get_value(self):
        if self.length.value == SQL_NULL_DATA:
            return None
        else:
            return self.buffer.value.decode()

    def get_size(self):
        return self.buffer_size

    def get_reference(self):
        return byref(self.buffer)

    def get_length_reference(self):
        return byref(self.length)

