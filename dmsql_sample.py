#!/usr/bin/env python3

from ctypes import *

from dmsql import *

class SampleException(Exception):
    pass

def check_sql_return(sql_return):
    if sql_return != SQL_SUCCESS and sql_return != SQL_SUCCESS_WITH_INFO:
        raise SampleException("sql_return : " +  str(sql_return))

dsn = cast(create_string_buffer(b"DSN"), POINTER(SQLCHAR))
username = cast(create_string_buffer(b"uid"), POINTER(SQLCHAR))
password = cast(create_string_buffer(b"pwd"), POINTER(SQLCHAR))

select = cast(create_string_buffer(b"SELECT @@VERSION"), POINTER(SQLCHAR))

environment_handle = SQLHANDLE()
connection_handle = SQLHANDLE()
statement_handle = SQLHANDLE()

check_sql_return(SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, byref(environment_handle)))
check_sql_return(SQLSetEnvAttr(environment_handle, SQL_ATTR_ODBC_VERSION, SQL_OV_ODBC3, SQL_IS_UINTEGER))
check_sql_return(SQLAllocHandle(SQL_HANDLE_DBC, environment_handle, byref(connection_handle)))
check_sql_return(SQLConnect(connection_handle, dsn, SQL_NTS, username, SQL_NTS, password, SQL_NTS))
check_sql_return(SQLAllocHandle(SQL_HANDLE_STMT, connection_handle, byref(statement_handle)))
check_sql_return(SQLPrepare(statement_handle, select, SQL_NTS))
check_sql_return(SQLExecute(statement_handle))

version_size = 512
version_length = SQLLEN()
version = create_string_buffer(version_size)

check_sql_return(SQLBindCol(statement_handle, 1, SQL_C_CHAR, version, version_size, byref(version_length)))

check_sql_return(SQLFetch(statement_handle))

print(version.value.decode())

