#!/usr/bin/env python3

import ctypes
import enum
import os

if os.name == "nt":
    DM_ODBC_NAME = "odbc32.dll"
else:
    DM_ODBC_NAME = "libodbc.so"

def UnimplementedSQLFunction(*args):
    raise NotImplementedError("This SQL function is not implemented")

class Driver:
    def __init__(self, odbc_driver_name = DM_ODBC_NAME, size_of_long = 8, unicode = True, legacy = True):
        self.ODBC_DRIVER_NAME = odbc_driver_name
        self.SIZE_OF_LONG = size_of_long
        self.UNICODE = unicode
        self.LEGACY = legacy

        self.ODBC_DRIVER = ctypes.CDLL(self.ODBC_DRIVER_NAME)

        self.UnimplementedSQLFunction = UnimplementedSQLFunction

        ####----------------------------------------------------------------------------
        ####This section mimics iodbcunix.h---------------------------------------------
        ####----------------------------------------------------------------------------
        self.TRUE = 1
        self.FALSE = 0

        ################################################################################
        ####Windows style typedefs######################################################
        ################################################################################
        self.BYTE = ctypes.c_ubyte
        self.WORD = ctypes.c_ushort
        self.DWORD = ctypes.c_uint
        self.LPSTR = ctypes.c_char_p
        self.LPCSTR = ctypes.c_char_p
        self.LPWSTR = ctypes.c_wchar_p
        self.LPCWSTR = ctypes.c_wchar_p
        self.LPDWORD = ctypes.POINTER(self.DWORD,)
        self.BOOL = ctypes.c_int

        ####----------------------------------------------------------------------------
        ####This section mimics sqltypes.h----------------------------------------------
        ####----------------------------------------------------------------------------
        ################################################################################
        ####ODBC Specification##########################################################
        ################################################################################
        self.ODBCVER = 0x0351

        ################################################################################
        ####ODBC Types##################################################################
        ################################################################################
        self.SQLCHAR = ctypes.c_ubyte
        self.SQLSMALLINT = ctypes.c_short
        self.SQLUSMALLINT = ctypes.c_ushort

        if self.SIZE_OF_LONG == 8:
            self.SQLINTEGER = ctypes.c_int
            self.SQLUINTEGER = ctypes.c_uint
        else:
            self.SQLINTEGER = ctypes.c_long
            self.SQLUINTEGER = ctypes.c_ulong

        self.SQLPOINTER = ctypes.c_void_p
        self.SQLSCHAR = ctypes.c_char
        self.SQLDATE = ctypes.c_ubyte
        self.SQLDECIMAL = ctypes.c_ubyte
        self.SQLNUMERIC = ctypes.c_ubyte
        self.SQLDOUBLE = ctypes.c_double
        self.SQLFLOAT = ctypes.c_double
        self.SQLREAL = ctypes.c_float
        self.SQLTIME = ctypes.c_ubyte
        self.SQLTIMESTAMP = ctypes.c_ubyte
        self.SQLVARCHAR = ctypes.c_ubyte
        self.SQLBIGINT = ctypes.c_longlong
        self.SQLUBIGINT = ctypes.c_ulonglong
        self.SQLWCHAR = ctypes.c_ushort

        if self.UNICODE:
            self.SQLTCHAR = self.SQLWCHAR
        else:
            self.SQLTCHAR = self.SQLCHAR

        if self.LEGACY:
            self.SQLLEN = ctypes.c_int
            self.SQLULEN = ctypes.c_uint
            self.SQLSETPOSIROW = ctypes.c_ushort
        else:
            self.SQLLEN = ctypes.c_long
            self.SQLULEN = ctypes.c_ulong
            self.SQLSETPOSIROW = ctypes.c_ushort

        ################################################################################
        ####Backward Compatibility with older platform SDKs#############################
        ################################################################################
        self.SQLROWCOUNT = self.SQLULEN
        self.SQLROWSETSIZE = self.SQLULEN
        self.SQLTRANSID = self.SQLULEN
        self.SQLROWOFFSET = self.SQLLEN

        ################################################################################
        ####Generic Pointer Types#######################################################
        ################################################################################
        self.PTR = ctypes.c_void_p
        self.SQLHANDLE = ctypes.c_void_p

        ################################################################################
        ####Handles#####################################################################
        ################################################################################
        self.HENV = ctypes.c_void_p
        self.HDBC = ctypes.c_void_p
        self.HSTMT = ctypes.c_void_p

        self.SQLHENV = self.SQLHANDLE
        self.SQLHDBC = self.SQLHANDLE
        self.SQLHSTMT = self.SQLHANDLE
        self.SQLHDESC = self.SQLHANDLE

        self.HWND = self.SQLPOINTER
        self.SQLHWND = self.SQLPOINTER

        ################################################################################
        ####Portable Types##############################################################
        ################################################################################
        self.UCHAR = ctypes.c_ubyte
        self.SCHAR = ctypes.c_char
        self.SWORD = ctypes.c_short
        self.UWORD = ctypes.c_ushort
        self.SDWORD = ctypes.c_long
        self.UDWORD = ctypes.c_ulong
        self.SSHORT = ctypes.c_short
        self.USHORT = ctypes.c_ushort
        self.SLONG = ctypes.c_long
        self.ULONG = ctypes.c_ulong
        self.SFLOAT = ctypes.c_float
        self.SDOUBLE = ctypes.c_double
        self.LDOUBLE = ctypes.c_double
        self.ODBCINT64 = ctypes.c_longlong
        self.ODBCUINT64 = ctypes.c_ulonglong

        ################################################################################
        ####Return Types################################################################
        ################################################################################
        self.RETCODE = ctypes.c_short
        self.SQLRETURN = self.RETCODE

        ################################################################################
        ####Portable Types:DATA, TIME, TIMESTAMO, BOOKMARK##############################
        ################################################################################
        self.BOOKMARK = self.SQLULEN
        class DATE_STUCT_DEFINITION(ctypes.Structure):
            _fields_ = [("year", self.SQLSMALLINT),
                        ("month", self.SQLUSMALLINT),
                        ("day", self.SQLUSMALLINT)]
        self.DATE_STRUCT = DATE_STUCT_DEFINITION
        self.SQL_DATE_STRUCT = self.DATE_STRUCT
        class TIME_STRUCT_DEFINITION(ctypes.Structure):
            _fields_ = [("hour", self.SQLUSMALLINT),
                        ("minute", self.SQLUSMALLINT),
                        ("second", self.SQLUSMALLINT)]
        self.TIME_STRUCT = TIME_STRUCT_DEFINITION
        self.SQL_TIME_STRUCT = self.TIME_STRUCT
        class TIMESTAMP_STRUCT_DEFINITION(ctypes.Structure):
            _fields_ = [("year", self.SQLSMALLINT),
                        ("month", self.SQLUSMALLINT),
                        ("day", self.SQLUSMALLINT),
                        ("hour", self.SQLUSMALLINT),
                        ("minute", self.SQLUSMALLINT),
                        ("second", self.SQLUSMALLINT),
                        ("fraction", self.SQLUINTEGER)]
        self.TIMESTAMP_STRUCT = TIMESTAMP_STRUCT_DEFINITION
        self.SQL_TIMESTAMP_STRUCT = self.TIMESTAMP_STRUCT

        ################################################################################
        ####enumeration for DATETIME_INTERVAL_SUBCODE###################################
        ################################################################################
        self.SQLINTERVAL = ctypes.c_int
        self.SQL_IS_YEAR = 1
        self.SQL_IS_MONTH = 2
        self.SQL_IS_DAY = 3
        self.SQL_IS_HOUR = 4
        self.SQL_IS_MINUTE = 5
        self.SQL_IS_SECOND = 6
        self.SQL_IS_YEAR_TO_MONTH = 7
        self.SQL_IS_DAY_TO_HOUR  = 8
        self.SQL_IS_DAY_TO_MINUTE = 9
        self.SQL_IS_DAY_TO_SECOND = 10
        self.SQL_IS_HOUR_TO_MINUTE = 11
        self.SQL_IS_HOUR_TO_SECOND = 12
        self.SQL_IS_MINUTE_TO_SECOND = 13

        class SQL_YEAR_MONTH_STRUCT_DEFINITION(ctypes.Structure):
            _fields_ = [("year", self.SQLUINTEGER),
                        ("month", self.SQLUINTEGER)]
        self.SQL_YEAR_MONTH_STRUCT = SQL_YEAR_MONTH_STRUCT_DEFINITION
        class SQL_DAY_SECOND_STRUCT_DEFINITION(ctypes.Structure):
            _fields_ = [("day", self.SQLUINTEGER),
                        ("hour", self.SQLUINTEGER),
                        ("minute", self.SQLUINTEGER),
                        ("second", self.SQLUINTEGER),
                        ("fraction", self.SQLUINTEGER)]
        self.SQL_DAY_SECOND_STRUCT = SQL_DAY_SECOND_STRUCT_DEFINITION
        class SQL_INTERVAL_UNION_DEFINITION(ctypes.Union):
            _fields_ = [("year_month", self.SQL_YEAR_MONTH_STRUCT),
                        ("day_second", self.SQL_DAY_SECOND_STRUCT)]
        self.SQL_INTERVAL_UNION = SQL_INTERVAL_UNION_DEFINITION
        class SQL_INTERVAL_STRUCT_DEFINITION(ctypes.Structure):
            _fields_ = [("interval_type", self.SQLINTERVAL),
                        ("interval_sign", self.SQLSMALLINT),
                        ("intval", self.SQL_INTERVAL_UNION)]
        self.SQL_INTERVAL_STRUCT = SQL_INTERVAL_STRUCT_DEFINITION

        ################################################################################
        ####Numeric Data Type###########################################################
        ################################################################################
        self.SQL_MAX_NUMERIC_LEN = 16
        class SQL_NUMERIC_STRUCT_DEFINITION(ctypes.Structure):
            _fields_ = [("precision", self.SQLCHAR),
                        ("scale", self.SQLSCHAR),
                        ("sign", self.SQLCHAR),
                        ("val", self.SQLCHAR * self.SQL_MAX_NUMERIC_LEN)]
        self.SQL_NUMERIC_STRUCT = SQL_NUMERIC_STRUCT_DEFINITION

        ################################################################################
        ################################################################################
        ################################################################################
        class SQLGUID_DEFINITION(ctypes.Structure):
            _fields_ = [("Data1", ctypes.c_uint),
                        ("Data2", ctypes.c_ushort),
                        ("Data3", ctypes.c_ushort),
                        ("Data4", ctypes.c_char * 8)]
        self.SQLGUID = SQLGUID_DEFINITION

        ####----------------------------------------------------------------------------
        ####This section mimics sql.h---------------------------------------------------
        ####----------------------------------------------------------------------------
        ################################################################################
        ####Useful Constans#############################################################
        ################################################################################
        self.SQL_MAX_MESSAGE_LENGTH = 512

        ################################################################################
        ####Handle Types################################################################
        ################################################################################
        self.SQL_HANDLE_ENV = 1
        self.SQL_HANDLE_DBC = 2
        self.SQL_HANDLE_STMT = 3
        self.SQL_HANDLE_DESC = 4

        ################################################################################
        ####Function return codes#######################################################
        ################################################################################
        self.SQL_SUCCESS = 0
        self.SQL_SUCCESS_WITH_INFO = 1
        self.SQL_STILL_EXECUTING = 2
        self.SQL_ERROR = -1
        self.SQL_INVALID_HANDLE = -2
        self.SQL_NEED_DATA = 99
        self.SQL_NO_DATA = 100

        ################################################################################
        ####Test for success############################################################
        ################################################################################
        def SQL_SUCCEEDED_DEFINITION(return_code):
            return (return_code & ~1) == 0
        self.SQL_SUCCEEDED = SQL_SUCCEEDED_DEFINITION

        ################################################################################
        ####Special length vlaues#######################################################
        ################################################################################
        self.SQL_NULL_DATA = -1
        self.SQL_DATA_AT_EXEC = -2

        ################################################################################
        ####Flags for null-terminated strings###########################################
        ################################################################################
        self.SQL_NTS = -3
        self.SQL_NTSL = -3

        ################################################################################
        ####Standard SQL datatypes######################################################
        ################################################################################
        self.SQL_UNKNOWN_TYPE = 0
        self.SQL_CHAR = 1
        self.SQL_NUMERIC = 2
        self.SQL_DECIMAL = 3
        self.SQL_INTEGER = 4
        self.SQL_SMALLINT = 5
        self.SQL_FLOAT = 6
        self.SQL_REAL = 7
        self.SQL_DOUBLE = 8
        self.SQL_DATETIME = 9
        self.SQL_VARCHAR = 12

        ################################################################################
        ####SQLGetTypeInfo request for all data types###################################
        ################################################################################
        self.SQL_ALL_TYPES = 0

        ################################################################################
        ####Statement attribute values for date/time data types#########################
        ################################################################################
        self.SQL_TYPE_DATE = 91
        self.SQL_TYPE_TIME = 92
        self.SQL_TYPE_TIMESTAMP = 93

        ################################################################################
        ####Date/Time constants#########################################################
        ################################################################################
        self.SQL_DATE_LEN = 10
        self.SQL_TIME_LEN = 8
        self.SQL_TIMESTAMP_LEN = 19

        ################################################################################
        ####Null status constants#######################################################
        ################################################################################
        self.SQL_NO_NULLS = 0
        self.SQL_NULLABLE = 1
        self.SQL_NULLABLE_UNKNOWN = 2

        ################################################################################
        ####NULL Handles################################################################
        ################################################################################
        self.SQL_NULL_HENV = self.SQLHANDLE()
        self.SQL_NULL_HDBC = self.SQLHANDLE()
        self.SQL_NULL_HSTMT = self.SQLHANDLE()
        self.SQL_NULL_HDESC = self.SQLHANDLE()

        self.SQL_NULL_SQLLEN = ctypes.POINTER(self.SQLLEN)()
        self.SQL_NULL_SQLULEN = ctypes.POINTER(self.SQLULEN)()

        self.SQL_NULL_SQLSMALLINT = ctypes.POINTER(self.SQLSMALLINT)()
        self.SQL_NULL_SQLUSMALLINT = ctypes.POINTER(self.SQLUSMALLINT)()

        self.SQL_NULL_SQLINTEGER = ctypes.POINTER(self.SQLINTEGER)()
        self.SQL_NULL_SQLUINTEGER = ctypes.POINTER(self.SQLUINTEGER)()

        self.SQL_NULL_SQLCHAR = ctypes.POINTER(self.SQLCHAR)()
        self.SQL_NULL_SQLWCHAR = ctypes.POINTER(self.SQLWCHAR)()
        self.SQL_NULL_SQLTCHAR = ctypes.POINTER(self.SQLTCHAR)()

        ################################################################################
        ####Null parent for self.SQLHENV#####################################################
        ################################################################################
        self.SQL_NULL_HANDLE = self.SQLHANDLE(0)

        ################################################################################
        ####CLI option values###########################################################
        ################################################################################
        self.SQL_FALSE = 0
        self.SQL_TRUE = 1

        ################################################################################
        ####Default conversion code#####################################################
        ################################################################################
        self.SQL_DEFAULT = 99

        ################################################################################
        ####SQLDataSources/SQLFetchScroll - FetchOrientation############################
        ################################################################################
        self.SQL_FETCH_NEXT = 1
        self.SQL_FETCH_FIRST = 2

        ################################################################################
        ####SQLFetchScroll - FetchOrientation###########################################
        ################################################################################
        self.SQL_FETCH_LAST = 3
        self.SQL_FETCH_PRIOR = 4
        self.SQL_FETCH_ABSOLUTE = 5
        self.SQL_FETCH_RELATIVE = 6

        ################################################################################
        ####SQLFreeStmt#################################################################
        ################################################################################
        self.SQL_CLOSE = 0
        self.SQL_DROP = 1
        self.SQL_UNBIND = 2
        self.SQL_RESET_PARAMS = 3

        ################################################################################
        ####SQLGetConnectAttr - connection attributes###################################
        ################################################################################
        self.SQL_ATTR_AUTO_IPD = 10001
        self.SQL_ATTR_METADATA_ID = 10014

        ################################################################################
        ####SQLGetData code indicating that the application row descriptor##############
        ####specifies the data type#####################################################
        ################################################################################
        self.SQL_ARD_TYPE = -99

        ################################################################################
        ####SQLGetDescField - identifiers of fields in the SQL descriptor###############
        ################################################################################
        self.SQL_DESC_COUNT = 1001
        self.SQL_DESC_TYPE = 1002
        self.SQL_DESC_LENGTH = 1003
        self.SQL_DESC_OCTET_LENGTH_PTR = 1004
        self.SQL_DESC_PRECISION = 1005
        self.SQL_DESC_SCALE = 1006
        self.SQL_DESC_DATETIME_INTERVAL_CODE = 1007
        self.SQL_DESC_NULLABLE = 1008
        self.SQL_DESC_INDICATOR_PTR = 1009
        self.SQL_DESC_DATA_PTR = 1010
        self.SQL_DESC_NAME = 1011
        self.SQL_DESC_UNNAMED = 1012
        self.SQL_DESC_OCTET_LENGTH = 1013
        self.SQL_DESC_ALLOC_TYPE = 1099

        ################################################################################
        ####SQLGetDescField - SQL_DESC_ALLOC_TYPE#######################################
        ################################################################################
        self.SQL_DESC_ALLOC_AUTO = 1
        self.SQL_DESC_ALLOC_USER = 2

        ################################################################################
        ####SQLGetDescField - SQL_DESC_DATETIME_INTERVAL_CODE###########################
        ################################################################################
        self.SQL_CODE_DATE = 1
        self.SQL_CODE_TIME = 2
        self.SQL_CODE_TIMESTAMP = 3

        ################################################################################
        ####SQLGetDescField - SQL_DESC_UNNAMED##########################################
        ################################################################################
        self.SQL_NAMED = 0
        self.SQL_UNNAMED = 1

        ################################################################################
        ####SQLGetDiagField - identifiers of fields in the diagnostics area#############
        ################################################################################
        self.SQL_DIAG_RETURNCODE = 1
        self.SQL_DIAG_NUMBER = 2
        self.SQL_DIAG_ROW_COUNT = 3
        self.SQL_DIAG_SQLSTATE = 4
        self.SQL_DIAG_NATIVE = 5
        self.SQL_DIAG_MESSAGE_TEXT = 6
        self.SQL_DIAG_DYNAMIC_FUNCTION = 7
        self.SQL_DIAG_CLASS_ORIGIN = 8
        self.SQL_DIAG_SUBCLASS_ORIGIN = 9
        self.SQL_DIAG_CONNECTION_NAME = 10
        self.SQL_DIAG_SERVER_NAME = 11
        self.SQL_DIAG_DYNAMIC_FUNCTION_CODE = 12

        ################################################################################
        ####SQLGetDiagField - SQL_DIAG_DYNAMIC_FUNCTION_CODE############################
        ################################################################################
        self.SQL_DIAG_ALTER_DOMAIN = 3
        self.SQL_DIAG_ALTER_TABLE = 4
        self.SQL_DIAG_CALL = 7
        self.SQL_DIAG_CREATE_ASSERTION = 6
        self.SQL_DIAG_CREATE_CHARACTER_SET = 8
        self.SQL_DIAG_CREATE_COLLATION = 10
        self.SQL_DIAG_CREATE_DOMAIN = 23
        self.SQL_DIAG_CREATE_INDEX = -1
        self.SQL_DIAG_CREATE_SCHEMA = 64
        self.SQL_DIAG_CREATE_TABLE = 77
        self.SQL_DIAG_CREATE_TRANSLATION = 79
        self.SQL_DIAG_CREATE_VIEW = 84
        self.SQL_DIAG_DELETE_WHERE = 19
        self.SQL_DIAG_DROP_ASSERTION = 24
        self.SQL_DIAG_DROP_CHARACTER_SET = 25
        self.SQL_DIAG_DROP_COLLATION = 26
        self.SQL_DIAG_DROP_DOMAIN = 27
        self.SQL_DIAG_DROP_INDEX = -2
        self.SQL_DIAG_DROP_SCHEMA = 31
        self.SQL_DIAG_DROP_TABLE = 32
        self.SQL_DIAG_DROP_TRANSLATION = 33
        self.SQL_DIAG_DROP_VIEW = 36
        self.SQL_DIAG_DYNAMIC_DELETE_CURSOR = 38
        self.SQL_DIAG_DYNAMIC_UPDATE_CURSOR = 81
        self.SQL_DIAG_GRANT = 48
        self.SQL_DIAG_INSERT = 50
        self.SQL_DIAG_REVOKE = 59
        self.SQL_DIAG_SELECT_CURSOR = 85
        self.SQL_DIAG_UNKNOWN_STATEMENT = 0
        self.SQL_DIAG_UPDATE_WHERE = 82

        ################################################################################
        ####SQLGetEnvAttr - environment attribute#######################################
        ################################################################################
        self.SQL_ATTR_OUTPUT_NTS = 10001

        ################################################################################
        ####SQLGetFunctions#############################################################
        ################################################################################
        self.SQL_API_SQLALLOCCONNECT = 1
        self.SQL_API_SQLALLOCENV = 2
        self.SQL_API_SQLALLOCHANDLE = 1001
        self.SQL_API_SQLALLOCSTMT = 3
        self.SQL_API_SQLBINDCOL = 4
        self.SQL_API_SQLBINDPARAM = 1002
        self.SQL_API_SQLCANCEL = 5
        self.SQL_API_SQLCLOSECURSOR = 1003
        self.SQL_API_SQLCOLATTRIBUTE = 6
        self.SQL_API_SQLCOLUMNS = 40
        self.SQL_API_SQLCONNECT = 7
        self.SQL_API_SQLCOPYDESC = 1004
        self.SQL_API_SQLDATASOURCES = 57
        self.SQL_API_SQLDESCRIBECOL = 8
        self.SQL_API_SQLDISCONNECT = 9
        self.SQL_API_SQLENDTRAN = 1005
        self.SQL_API_SQLERROR = 10
        self.SQL_API_SQLEXECDIRECT = 11
        self.SQL_API_SQLEXECUTE = 12
        self.SQL_API_SQLFETCH = 13
        self.SQL_API_SQLFETCHSCROLL = 1021
        self.SQL_API_SQLFREECONNECT = 14
        self.SQL_API_SQLFREEENV = 15
        self.SQL_API_SQLFREEHANDLE = 1006
        self.SQL_API_SQLFREESTMT = 16
        self.SQL_API_SQLGETCONNECTATTR = 1007
        self.SQL_API_SQLGETCONNECTOPTION = 42
        self.SQL_API_SQLGETCURSORNAME = 17
        self.SQL_API_SQLGETDATA = 43
        self.SQL_API_SQLGETDESCFIELD = 1008
        self.SQL_API_SQLGETDESCREC = 1009
        self.SQL_API_SQLGETDIAGFIELD = 1010
        self.SQL_API_SQLGETDIAGREC = 1011
        self.SQL_API_SQLGETENVATTR = 1012
        self.SQL_API_SQLGETFUNCTIONS = 44
        self.SQL_API_SQLGETINFO = 45
        self.SQL_API_SQLGETSTMTATTR = 1014
        self.SQL_API_SQLGETSTMTOPTION = 46
        self.SQL_API_SQLGETTYPEINFO = 47
        self.SQL_API_SQLNUMRESULTCOLS = 18
        self.SQL_API_SQLPARAMDATA = 48
        self.SQL_API_SQLPREPARE = 19
        self.SQL_API_SQLPUTDATA = 49
        self.SQL_API_SQLROWCOUNT = 20
        self.SQL_API_SQLSETCONNECTATTR = 1016
        self.SQL_API_SQLSETCONNECTOPTION = 50
        self.SQL_API_SQLSETCURSORNAME = 21
        self.SQL_API_SQLSETDESCFIELD = 1017
        self.SQL_API_SQLSETDESCREC = 1018
        self.SQL_API_SQLSETENVATTR = 1019
        self.SQL_API_SQLSETPARAM = 22
        self.SQL_API_SQLSETSTMTATTR = 1020
        self.SQL_API_SQLSETSTMTOPTION = 51
        self.SQL_API_SQLSPECIALCOLUMNS = 52
        self.SQL_API_SQLSTATISTICS = 53
        self.SQL_API_SQLTABLES = 54
        self.SQL_API_SQLTRANSACT = 23

        ################################################################################
        ####SQLGetInfo##################################################################
        ################################################################################
        self.SQL_MAX_DRIVER_CONNECTIONS = 0
        self.SQL_MAXIMUM_DRIVER_CONNECTIONS = self.SQL_MAX_DRIVER_CONNECTIONS
        self.SQL_MAX_CONCURRENT_ACTIVITIES = 1
        self.SQL_MAXIMUM_CONCURRENT_ACTIVITIES = self.SQL_MAX_CONCURRENT_ACTIVITIES
        self.SQL_DATA_SOURCE_NAME = 2
        self.SQL_FETCH_DIRECTION = 8
        self.SQL_SERVER_NAME = 13
        self.SQL_SEARCH_PATTERN_ESCAPE = 14
        self.SQL_DBMS_NAME = 17
        self.SQL_DBMS_VER = 18
        self.SQL_ACCESSIBLE_TABLES = 19
        self.SQL_ACCESSIBLE_PROCEDURES = 20
        self.SQL_CURSOR_COMMIT_BEHAVIOR = 23
        self.SQL_DATA_SOURCE_READ_ONLY = 25
        self.SQL_DEFAULT_TXN_ISOLATION = 26
        self.SQL_IDENTIFIER_CASE = 28
        self.SQL_IDENTIFIER_QUOTE_CHAR = 29
        self.SQL_MAX_COLUMN_NAME_LEN = 30
        self.SQL_MAXIMUM_COLUMN_NAME_LENGTH = self.SQL_MAX_COLUMN_NAME_LEN
        self.SQL_MAX_CURSOR_NAME_LEN = 31
        self.SQL_MAXIMUM_CURSOR_NAME_LENGTH = self.SQL_MAX_CURSOR_NAME_LEN
        self.SQL_MAX_SCHEMA_NAME_LEN = 32
        self.SQL_MAXIMUM_SCHEMA_NAME_LENGTH = self.SQL_MAX_SCHEMA_NAME_LEN
        self.SQL_MAX_CATALOG_NAME_LEN = 34
        self.SQL_MAXIMUM_CATALOG_NAME_LENGTH = self.SQL_MAX_CATALOG_NAME_LEN
        self.SQL_MAX_TABLE_NAME_LEN = 35
        self.SQL_SCROLL_CONCURRENCY = 43
        self.SQL_TXN_CAPABLE = 46
        self.SQL_TRANSACTION_CAPABLE = self.SQL_TXN_CAPABLE
        self.SQL_USER_NAME = 47
        self.SQL_TXN_ISOLATION_OPTION = 72
        self.SQL_TRANSACTION_ISOLATION_OPTION = self.SQL_TXN_ISOLATION_OPTION
        self.SQL_INTEGRITY = 73
        self.SQL_GETDATA_EXTENSIONS = 81
        self.SQL_NULL_COLLATION = 85
        self.SQL_ALTER_TABLE = 86
        self.SQL_ORDER_BY_COLUMNS_IN_SELECT = 90
        self.SQL_SPECIAL_CHARACTERS = 94
        self.SQL_MAX_COLUMNS_IN_GROUP_BY = 97
        self.SQL_MAXIMUM_COLUMNS_IN_GROUP_BY = self.SQL_MAX_COLUMNS_IN_GROUP_BY
        self.SQL_MAX_COLUMNS_IN_INDEX = 98
        self.SQL_MAXIMUM_COLUMNS_IN_INDEX = self.SQL_MAX_COLUMNS_IN_INDEX
        self.SQL_MAX_COLUMNS_IN_ORDER_BY = 99
        self.SQL_MAXIMUM_COLUMNS_IN_ORDER_BY = self.SQL_MAX_COLUMNS_IN_ORDER_BY
        self.SQL_MAX_COLUMNS_IN_SELECT = 100
        self.SQL_MAXIMUM_COLUMNS_IN_SELECT = self.SQL_MAX_COLUMNS_IN_SELECT
        self.SQL_MAX_COLUMNS_IN_TABLE = 101
        self.SQL_MAX_INDEX_SIZE = 102
        self.SQL_MAXIMUM_INDEX_SIZE = self.SQL_MAX_INDEX_SIZE
        self.SQL_MAX_ROW_SIZE = 104
        self.SQL_MAXIMUM_ROW_SIZE = self.SQL_MAX_ROW_SIZE
        self.SQL_MAX_STATEMENT_LEN = 105
        self.SQL_MAXIMUM_STATEMENT_LENGTH = self.SQL_MAX_STATEMENT_LEN
        self.SQL_MAX_TABLES_IN_SELECT = 106
        self.SQL_MAXIMUM_TABLES_IN_SELECT = self.SQL_MAX_TABLES_IN_SELECT
        self.SQL_MAX_USER_NAME_LEN = 107
        self.SQL_MAXIMUM_USER_NAME_LENGTH = self.SQL_MAX_USER_NAME_LEN
        self.SQL_OJ_CAPABILITIES = 115
        self.SQL_OUTER_JOIN_CAPABILITIES = self.SQL_OJ_CAPABILITIES
        self.SQL_XOPEN_CLI_YEAR = 10000
        self.SQL_CURSOR_SENSITIVITY = 10001
        self.SQL_DESCRIBE_PARAMETER = 10002
        self.SQL_CATALOG_NAME = 10003
        self.SQL_COLLATION_SEQ = 10004
        self.SQL_MAX_IDENTIFIER_LEN = 10005
        self.SQL_MAXIMUM_IDENTIFIER_LENGTH = self.SQL_MAX_IDENTIFIER_LEN

        ################################################################################
        ####SQLGetInfo - SQL_ALTER_TABLE################################################
        ################################################################################
        self.SQL_AT_ADD_COLUMN = 0x00000001
        self.SQL_AT_DROP_COLUMN = 0x00000002
        self.SQL_AT_ADD_CONSTRAINT = 0x00000008

        ################################################################################
        ####SQLGetInfo - SQL_ASYNC_MODE#################################################
        ################################################################################
        self.SQL_AM_NONE = 0
        self.SQL_AM_CONNECTION = 1
        self.SQL_AM_STATEMENT = 2

        ################################################################################
        ####SQLGetInfo - SQL_CURSOR_COMMIT_BEHAVIOR#####################################
        ################################################################################
        self.SQL_CB_DELETE = 0
        self.SQL_CB_CLOSE = 1
        self.SQL_CB_PRESERVE = 2

        ################################################################################
        ####SQLGetInfo - SQL_FETCH_DIRECTION############################################
        ################################################################################
        self.SQL_FD_FETCH_NEXT = 0x00000001
        self.SQL_FD_FETCH_FIRST = 0x00000002
        self.SQL_FD_FETCH_LAST = 0x00000004
        self.SQL_FD_FETCH_PRIOR = 0x00000008
        self.SQL_FD_FETCH_ABSOLUTE = 0x00000010
        self.SQL_FD_FETCH_RELATIVE = 0x00000020

        ################################################################################
        ####SQLGetInfo - SQL_GETDATA_EXTENSIONS#########################################
        ################################################################################
        self.SQL_GD_ANY_COLUMN = 0x00000001
        self.SQL_GD_ANY_ORDER = 0x00000002

        ################################################################################
        ####SQLGetInfo - SQL_IDENTIFIER_CASE############################################
        ################################################################################
        self.SQL_IC_UPPER = 1
        self.SQL_IC_LOWER = 2
        self.SQL_IC_SENSITIVE = 3
        self.SQL_IC_MIXED = 4

        ################################################################################
        ####SQLGetInfo - SQL_NULL_COLLATION#############################################
        ################################################################################
        self.SQL_NC_HIGH = 0
        self.SQL_NC_LOW = 1

        ################################################################################
        ####SQLGetInfo - SQL_OJ_CAPABILITIES############################################
        ################################################################################
        self.SQL_OJ_LEFT = 0x00000001
        self.SQL_OJ_RIGHT = 0x00000002
        self.SQL_OJ_FULL = 0x00000004
        self.SQL_OJ_NESTED = 0x00000008
        self.SQL_OJ_NOT_ORDERED = 0x00000010
        self.SQL_OJ_INNER = 0x00000020
        self.SQL_OJ_ALL_COMPARISON_OPS = 0x00000040

        ################################################################################
        ####SQLGetInfo - SQL_SCROLL_CONCURRENCY#########################################
        ################################################################################
        self.SQL_SCCO_READ_ONLY = 0x00000001
        self.SQL_SCCO_LOCK = 0x00000002
        self.SQL_SCCO_OPT_ROWVER = 0x00000004
        self.SQL_SCCO_OPT_VALUES = 0x00000008

        ################################################################################
        ####SQLGetInfo - SQL_TXN_CAPABLE################################################
        ################################################################################
        self.SQL_TC_NONE = 0
        self.SQL_TC_DML = 1
        self.SQL_TC_ALL = 2
        self.SQL_TC_DDL_COMMIT = 3
        self.SQL_TC_DDL_IGNORE = 4

        ################################################################################
        ####SQLGetInfo - SQL_TXN_ISOLATION_OPTION#######################################
        ################################################################################
        self.SQL_TXN_READ_UNCOMMITTED = 0x00000001
        self.SQL_TRANSACTION_READ_UNCOMMITTED = self.SQL_TXN_READ_UNCOMMITTED
        self.SQL_TXN_READ_COMMITTED = 0x00000002
        self.SQL_TRANSACTION_READ_COMMITTED = self.SQL_TXN_READ_COMMITTED
        self.SQL_TXN_REPEATABLE_READ = 0x00000004
        self.SQL_TRANSACTION_REPEATABLE_READ = self.SQL_TXN_REPEATABLE_READ
        self.SQL_TXN_SERIALIZABLE = 0x00000008
        self.SQL_TRANSACTION_SERIALIZABLE = self.SQL_TXN_SERIALIZABLE

        ################################################################################
        ####SQLGetStmtAttr - statement attributes#######################################
        ################################################################################
        self.SQL_ATTR_APP_ROW_DESC = 10010
        self.SQL_ATTR_APP_PARAM_DESC = 10011
        self.SQL_ATTR_IMP_ROW_DESC = 10012
        self.SQL_ATTR_IMP_PARAM_DESC = 10013
        self.SQL_ATTR_CURSOR_SCROLLABLE = -1
        self.SQL_ATTR_CURSOR_SENSITIVITY = -2

        ################################################################################
        ####SQLGetStmtAttr - SQL_ATTR_CURSOR_SCROLLABLE#################################
        ################################################################################
        self.SQL_NONSCROLLABLE = 0
        self.SQL_SCROLLABLE = 1

        ################################################################################
        ####SQLGetStmtAttr - SQL_ATTR_CURSOR_SENSITIVITY################################
        ################################################################################
        self.SQL_UNSPECIFIED = 0
        self.SQL_INSENSITIVE = 1
        self.SQL_SENSITIVE = 2

        ################################################################################
        ####SQLGetTypeInfo - SEARCHABLE#################################################
        ################################################################################
        self.SQL_PRED_NONE = 0
        self.SQL_PRED_CHAR = 1
        self.SQL_PRED_BASIC = 2

        ################################################################################
        ####SQLSpecialColumns - Column scopes###########################################
        ################################################################################
        self.SQL_SCOPE_CURROW = 0
        self.SQL_SCOPE_TRANSACTION = 1
        self.SQL_SCOPE_SESSION = 2

        ################################################################################
        ####SQLSpecialColumns - PSEUDO_COLUMN###########################################
        ################################################################################
        self.SQL_PC_UNKNOWN = 0
        self.SQL_PC_NON_PSEUDO = 1
        self.SQL_PC_PSEUDO = 2

        ################################################################################
        ####SQLSpecialColumns - IdentifierType##########################################
        ################################################################################
        self.SQL_ROW_IDENTIFIER = 1

        ################################################################################
        ####SQLStatistics - fUnique#####################################################
        ################################################################################
        self.SQL_INDEX_UNIQUE = 0
        self.SQL_INDEX_ALL = 1

        ################################################################################
        ####SQLStatistics - TYPE########################################################
        ################################################################################
        self.SQL_INDEX_CLUSTERED = 1
        self.SQL_INDEX_HASHED = 2
        self.SQL_INDEX_OTHER = 3

        ################################################################################
        ####SQLTransact/SQLEndTran######################################################
        ################################################################################
        self.SQL_COMMIT = 0
        self.SQL_ROLLBACK = 1

        ################################################################################
        ####Function Prototypes#########################################################
        ################################################################################
        if hasattr(self.ODBC_DRIVER, "SQLAllocConnect"):
            self.ODBC_DRIVER.SQLAllocConnect.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLAllocConnect.argtypes = (self.SQLHENV, ctypes.POINTER(self.SQLHDBC),)
            self.SQLAllocConnect = self.ODBC_DRIVER.SQLAllocConnect
        else:
            self.SQLAllocConnect = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLAllocEnv"):
            self.ODBC_DRIVER.SQLAllocEnv.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLAllocEnv.argtypes = (ctypes.POINTER(self.SQLHENV),)
            self.SQLAllocEnv = self.ODBC_DRIVER.SQLAllocEnv
        else:
            self.SQLAllocEnv = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLAllocHandle"):
            self.ODBC_DRIVER.SQLAllocHandle.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLAllocHandle.argtypes = (self.SQLSMALLINT, self.SQLHANDLE, ctypes.POINTER(self.SQLHANDLE),)
            self.SQLAllocHandle = self.ODBC_DRIVER.SQLAllocHandle
        else:
            self.SQLAllocHandle = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLAllocStmt"):
            self.ODBC_DRIVER.SQLAllocStmt.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLAllocStmt.argtypes = (self.SQLHDBC, ctypes.POINTER(self.SQLHSTMT),)
            self.SQLAllocStmt = self.ODBC_DRIVER.SQLAllocStmt
        else:
            self.SQLAllocStmt = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLBindCol"):
            self.ODBC_DRIVER.SQLBindCol.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLBindCol.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLSMALLINT, self.SQLPOINTER, self.SQLLEN, ctypes.POINTER(self.SQLLEN),)
            self.SQLBindCol = self.ODBC_DRIVER.SQLBindCol
        else:
            self.SQLBindCol = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLBindParam"):
            self.ODBC_DRIVER.SQLBindParam.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLBindParam.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLULEN, self.SQLSMALLINT, self.SQLPOINTER, ctypes.POINTER(self.SQLLEN),)
            self.SQLBindParam = self.ODBC_DRIVER.SQLBindParam
        else:
            self.SQLBindParam = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLCancel"):
            self.ODBC_DRIVER.SQLCancel.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLCancel.argtypes = (self.SQLHSTMT,)
            self.SQLCancel = self.ODBC_DRIVER.SQLCancel
        else:
            self.SQLCancel = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLCloseCursor"):
            self.ODBC_DRIVER.SQLCloseCursor.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLCloseCursor.argtypes = (self.SQLHSTMT,)
            self.SQLCloseCursor = self.ODBC_DRIVER.SQLCloseCursor
        else:
            self.SQLCloseCursor = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLColAttribute"):
            self.ODBC_DRIVER.SQLColAttribute.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLColAttribute.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLUSMALLINT, self.SQLPOINTER, self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLLEN),)
            self.SQLColAttribute = self.ODBC_DRIVER.SQLColAttribute
            self.SQLColAttribute = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLColumns"):
            self.ODBC_DRIVER.SQLColumns.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLColumns.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLColumns = self.ODBC_DRIVER.SQLColumns
        else:
            self.SQLColumns = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLConnect"):
            self.ODBC_DRIVER.SQLConnect.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLConnect.argtypes = (self.SQLHDBC, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLConnect = self.ODBC_DRIVER.SQLConnect
        else:
            self.SQLConnect = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLCopyDesc"):
            self.ODBC_DRIVER.SQLCopyDesc.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLCopyDesc.argtypes = (self.SQLHDESC, self.SQLHDESC,)
            self.SQLCopyDesc = self.ODBC_DRIVER.SQLCopyDesc
        else:
            self.SQLCopyDesc = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDataSources"):
            self.ODBC_DRIVER.SQLDataSources.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDataSources.argtypes = (self.SQLHENV, self.SQLUSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLDataSources = self.ODBC_DRIVER.SQLDataSources
        else:
            self.SQLDataSources = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDescribeCol"):
            self.ODBC_DRIVER.SQLDescribeCol.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDescribeCol.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLULEN), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLDescribeCol = self.ODBC_DRIVER.SQLDescribeCol
        else:
            self.SQLDescribeCol = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDisconnect"):
            self.ODBC_DRIVER.SQLDisconnect.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDisconnect.argtypes = (self.SQLHDBC,)
            self.SQLDisconnect = self.ODBC_DRIVER.SQLDisconnect
        else:
            self.SQLDisconnect = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLEndTran"):
            self.ODBC_DRIVER.SQLEndTran.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLEndTran.argtypes = (self.SQLSMALLINT, self.SQLHANDLE, self.SQLSMALLINT,)
            self.SQLEndTran = self.ODBC_DRIVER.SQLEndTran
        else:
            self.SQLEndTran = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLError"):
            self.ODBC_DRIVER.SQLError.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLError.argtypes = (self.SQLHENV, self.SQLHDBC, self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), ctypes.POINTER(self.SQLINTEGER), ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLError = self.ODBC_DRIVER.SQLError
        else:
            self.SQLError = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLExecDirect"):
            self.ODBC_DRIVER.SQLExecDirect.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLExecDirect.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLINTEGER,)
            self.SQLExecDirect = self.ODBC_DRIVER.SQLExecDirect
        else:
            self.SQLExecDirect = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLExecute"):
            self.ODBC_DRIVER.SQLExecute.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLExecute.argtypes = (self.SQLHSTMT,)
            self.SQLExecute = self.ODBC_DRIVER.SQLExecute
        else:
            self.SQLExecute = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLFetch"):
            self.ODBC_DRIVER.SQLFetch.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLFetch.argtypes = (self.SQLHSTMT,)
            self.SQLFetch = self.ODBC_DRIVER.SQLFetch
        else:
            self.SQLFetch = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLFetchScroll"):
            self.ODBC_DRIVER.SQLFetchScroll.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLFetchScroll.argtypes = (self.SQLHSTMT, self.SQLSMALLINT, self.SQLLEN,)
            self.SQLFetchScroll = self.ODBC_DRIVER.SQLFetchScroll
        else:
            self.SQLFetchScroll = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLFreeConnect"):
            self.ODBC_DRIVER.SQLFreeConnect.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLFreeConnect.argtypes = (self.SQLHDBC,)
            self.SQLFreeConnect = self.ODBC_DRIVER.SQLFreeConnect
        else:
            self.SQLFreeConnect = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLFreeEnv"):
            self.ODBC_DRIVER.SQLFreeEnv.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLFreeEnv.argtypes = (self.SQLHENV,)
            self.SQLFreeEnv = self.ODBC_DRIVER.SQLFreeEnv
        else:
            self.SQLFreeEnv = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLFreeHandle"):
            self.ODBC_DRIVER.SQLFreeHandle.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLFreeHandle.argtypes = (self.SQLSMALLINT, self.SQLHANDLE,)
            self.SQLFreeHandle = self.ODBC_DRIVER.SQLFreeHandle
        else:
            self.SQLFreeHandle = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLFreeStmt"):
            self.ODBC_DRIVER.SQLFreeStmt.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLFreeStmt.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT,)
            self.SQLFreeStmt = self.ODBC_DRIVER.SQLFreeStmt
        else:
            self.SQLFreeStmt = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetConnectAttr"):
            self.ODBC_DRIVER.SQLGetConnectAttr.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetConnectAttr.argtypes = (self.SQLHDBC, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLGetConnectAttr = self.ODBC_DRIVER.SQLGetConnectAttr
        else:
            self.SQLGetConnectAttr = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetConnectOption"):
            self.ODBC_DRIVER.SQLGetConnectOption.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetConnectOption.argtypes = (self.SQLHDBC, self.SQLUSMALLINT, self.SQLPOINTER,)
            self.SQLGetConnectOption = self.ODBC_DRIVER.SQLGetConnectOption
        else:
            self.SQLGetConnectOption = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetCursorName"):
            self.ODBC_DRIVER.SQLGetCursorName.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetCursorName.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetCursorName = self.ODBC_DRIVER.SQLGetCursorName
        else:
            self.SQLGetCursorName = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetData"):
            self.ODBC_DRIVER.SQLGetData.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetData.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLSMALLINT, self.SQLPOINTER, self.SQLLEN, ctypes.POINTER(self.SQLLEN),)
            self.SQLGetData = self.ODBC_DRIVER.SQLGetData
        else:
            self.SQLGetData = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetDescField"):
            self.ODBC_DRIVER.SQLGetDescField.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetDescField.argtypes = (self.SQLHDESC, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLPOINTER, self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLGetDescField = self.ODBC_DRIVER.SQLGetDescField
        else:
            self.SQLGetDescField = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetDescRec"):
            self.ODBC_DRIVER.SQLGetDescRec.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetDescRec.argtypes = (self.SQLHDESC, self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLLEN), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetDescRec = self.ODBC_DRIVER.SQLGetDescRec
        else:
            self.SQLGetDescRec = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetDiagField"):
            self.ODBC_DRIVER.SQLGetDiagField.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetDiagField.argtypes = (self.SQLSMALLINT, self.SQLHANDLE, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLPOINTER, self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetDiagField = self.ODBC_DRIVER.SQLGetDiagField
        else:
            self.SQLGetDiagField = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetDiagRec"):
            self.ODBC_DRIVER.SQLGetDiagRec.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetDiagRec.argtypes = (self.SQLSMALLINT, self.SQLHANDLE, self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), ctypes.POINTER(self.SQLINTEGER), ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetDiagRec = self.ODBC_DRIVER.SQLGetDiagRec
        else:
            self.SQLGetDiagRec = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetEnvAttr"):
            self.ODBC_DRIVER.SQLGetEnvAttr.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetEnvAttr.argtypes = (self.SQLHENV, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLGetEnvAttr = self.ODBC_DRIVER.SQLGetEnvAttr
        else:
            self.SQLGetEnvAttr = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetFunctions"):
            self.ODBC_DRIVER.SQLGetFunctions.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetFunctions.argtypes = (self.SQLHDBC, self.SQLUSMALLINT, ctypes.POINTER(self.SQLUSMALLINT),)
            self.SQLGetFunctions = self.ODBC_DRIVER.SQLGetFunctions
        else:
            self.SQLGetFunctions = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetInfo"):
            self.ODBC_DRIVER.SQLGetInfo.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetInfo.argtypes = (self.SQLHDBC, self.SQLUSMALLINT, self.SQLPOINTER, self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetInfo = self.ODBC_DRIVER.SQLGetInfo
        else:
            self.SQLGetInfo = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetStmtAttr"):
            self.ODBC_DRIVER.SQLGetStmtAttr.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetStmtAttr.argtypes = (self.SQLHSTMT, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLGetStmtAttr = self.ODBC_DRIVER.SQLGetStmtAttr
        else:
            self.SQLGetStmtAttr = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetStmtOption"):
            self.ODBC_DRIVER.SQLGetStmtOption.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetStmtOption.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLPOINTER,)
            self.SQLGetStmtOption = self.ODBC_DRIVER.SQLGetStmtOption
        else:
            self.SQLGetStmtOption = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetTypeInfo"):
            self.ODBC_DRIVER.SQLGetTypeInfo.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetTypeInfo.argtypes = (self.SQLHSTMT, self.SQLSMALLINT,)
            self.SQLGetTypeInfo = self.ODBC_DRIVER.SQLGetTypeInfo
        else:
            self.SQLGetTypeInfo = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLNumResultCols"):
            self.ODBC_DRIVER.SQLNumResultCols.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLNumResultCols.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLNumResultCols = self.ODBC_DRIVER.SQLNumResultCols
        else:
            self.SQLNumResultCols = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLParamData"):
            self.ODBC_DRIVER.SQLParamData.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLParamData.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLPOINTER),)
            self.SQLParamData = self.ODBC_DRIVER.SQLParamData
        else:
            self.SQLParamData = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLPrepare"):
            self.ODBC_DRIVER.SQLPrepare.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLPrepare.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLINTEGER,)
            self.SQLPrepare = self.ODBC_DRIVER.SQLPrepare
        else:
            self.SQLPrepare = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLPutData"):
            self.ODBC_DRIVER.SQLPutData.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLPutData.argtypes = (self.SQLHSTMT, self.SQLPOINTER, self.SQLLEN,)
            self.SQLPutData = self.ODBC_DRIVER.SQLPutData
        else:
            self.SQLPutData = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLRowCount"):
            self.ODBC_DRIVER.SQLRowCount.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLRowCount.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLLEN),)
            self.SQLRowCount = self.ODBC_DRIVER.SQLRowCount
        else:
            self.SQLRowCount = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetConnectAttr"):
            self.ODBC_DRIVER.SQLSetConnectAttr.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetConnectAttr.argtypes = (self.SQLHDBC, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER,)
            self.SQLSetConnectAttr = self.ODBC_DRIVER.SQLSetConnectAttr
        else:
            self.SQLSetConnectAttr = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetConnectOption"):
            self.ODBC_DRIVER.SQLSetConnectOption.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetConnectOption.argtypes = (self.SQLHDBC, self.SQLUSMALLINT, self.SQLULEN,)
            self.SQLSetConnectOption = self.ODBC_DRIVER.SQLSetConnectOption
        else:
            self.SQLSetConnectOption = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetCursorName"):
            self.ODBC_DRIVER.SQLSetCursorName.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetCursorName.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLSetCursorName = self.ODBC_DRIVER.SQLSetCursorName
        else:
            self.SQLSetCursorName = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetDescField"):
            self.ODBC_DRIVER.SQLSetDescField.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetDescField.argtypes = (self.SQLHDESC, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLPOINTER, self.SQLINTEGER,)
            self.SQLSetDescField = self.ODBC_DRIVER.SQLSetDescField
        else:
            self.SQLSetDescField = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetDescRec"):
            self.ODBC_DRIVER.SQLSetDescRec.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetDescRec.argtypes = (self.SQLHDESC, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLLEN, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLPOINTER, ctypes.POINTER(self.SQLLEN), ctypes.POINTER(self.SQLLEN),)
            self.SQLSetDescRec = self.ODBC_DRIVER.SQLSetDescRec
        else:
            self.SQLSetDescRec = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetEnvAttr"):
            self.ODBC_DRIVER.SQLSetEnvAttr.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetEnvAttr.argtypes = (self.SQLHENV, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER,)
            self.SQLSetEnvAttr = self.ODBC_DRIVER.SQLSetEnvAttr
        else:
            self.SQLSetEnvAttr = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetStmtAttr"):
            self.ODBC_DRIVER.SQLSetStmtAttr.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetStmtAttr.argtypes = (self.SQLHSTMT, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER,)
            self.SQLSetStmtAttr = self.ODBC_DRIVER.SQLSetStmtAttr
        else:
            self.SQLSetStmtAttr = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetStmtOption"):
            self.ODBC_DRIVER.SQLSetStmtOption.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetStmtOption.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLULEN,)
            self.SQLSetStmtOption = self.ODBC_DRIVER.SQLSetStmtOption
        else:
            self.SQLSetStmtOption = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSpecialColumns"):
            self.ODBC_DRIVER.SQLSpecialColumns.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSpecialColumns.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, self.SQLUSMALLINT, self.SQLUSMALLINT,)
            self.SQLSpecialColumns = self.ODBC_DRIVER.SQLSpecialColumns
        else:
            self.SQLSpecialColumns = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLStatistics"):
            self.ODBC_DRIVER.SQLStatistics.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLStatistics.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, self.SQLUSMALLINT, self.SQLUSMALLINT,)
            self.SQLStatistics = self.ODBC_DRIVER.SQLStatistics
        else:
            self.SQLStatistics = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLTables"):
            self.ODBC_DRIVER.SQLTables.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLTables.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLTables = self.ODBC_DRIVER.SQLTables
        else:
            self.SQLTables = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLTransact"):
            self.ODBC_DRIVER.SQLTransact.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLTransact.argtypes = (self.SQLHENV, self.SQLHDBC, self.SQLUSMALLINT,)
            self.SQLTransact = self.ODBC_DRIVER.SQLTransact
        else:
            self.SQLTransact = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetParam"):
            self.ODBC_DRIVER.SQLSetParam.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetParam.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLULEN, self.SQLSMALLINT, self.SQLPOINTER, ctypes.POINTER(self.SQLLEN),)
            self.SQLSetParam = self.ODBC_DRIVER.SQLSetParam
        else:
            self.SQLSetParam = self.UnimplementedSQLFunction

        ####----------------------------------------------------------------------------
        ####This section mimics sqlucode.h----------------------------------------------
        ####----------------------------------------------------------------------------
        ################################################################################
        ####SQL datatypes - Unicode#####################################################
        ################################################################################
        self.SQL_WCHAR = -8
        self.SQL_WVARCHAR = -9
        self.SQL_WLONGVARCHAR = -10
        self.SQL_C_WCHAR = self.SQL_WCHAR

        if self.UNICODE:
            self.SQL_C_TCHAR = self.SQL_C_WCHAR
        else:
            self.SQL_C_TCHAR = self.SQL_C_CHAR

        ################################################################################
        ####SQLTablesW##################################################################
        ################################################################################
        self.SQL_ALL_CATALOGSW = "%"
        self.SQL_ALL_SCHEMASW = "%"
        self.SQL_ALL_TABLE_TYPESW = "%"

        ################################################################################
        ####SQL_SQLSTATE_SIZEW##########################################################
        ################################################################################
        self.SQL_SQLSTATE_SIZEW = 10

        ################################################################################
        ####Function Prototypes - Unicode###############################################
        ################################################################################
        if hasattr(self.ODBC_DRIVER, "SQLColAttributeW"):
            self.ODBC_DRIVER.SQLColAttributeW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLColAttributeW.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLUSMALLINT, self.SQLPOINTER, self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLLEN),)
            self.SQLColAttributeW = self.ODBC_DRIVER.SQLColAttributeW
        else:
            self.SQLColAttributeW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLColAttributesW"):
            self.ODBC_DRIVER.SQLColAttributesW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLColAttributesW.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLUSMALLINT, self.SQLPOINTER, self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLLEN),)
            self.SQLColAttributesW = self.ODBC_DRIVER.SQLColAttributesW
        else:
            self.SQLColAttributesW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLConnectW"):
            self.ODBC_DRIVER.SQLConnectW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLConnectW.argtypes = (self.SQLHDBC, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT,)
            self.SQLConnectW = self.ODBC_DRIVER.SQLConnectW
        else:
            self.SQLConnectW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDescribeColW"):
            self.ODBC_DRIVER.SQLDescribeColW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDescribeColW.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLULEN), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLDescribeColW = self.ODBC_DRIVER.SQLDescribeColW
        else:
            self.SQLDescribeColW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLErrorW"):
            self.ODBC_DRIVER.SQLErrorW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLErrorW.argtypes = (self.SQLHENV, self.SQLHDBC, self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), ctypes.POINTER(self.SQLINTEGER), ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLErrorW = self.ODBC_DRIVER.SQLErrorW
        else:
            self.SQLErrorW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLExecDirectW"):
            self.ODBC_DRIVER.SQLExecDirectW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLExecDirectW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLINTEGER,)
            self.SQLExecDirectW = self.ODBC_DRIVER.SQLExecDirectW
        else:
            self.SQLExecDirectW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetConnectAttrW"):
            self.ODBC_DRIVER.SQLGetConnectAttrW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetConnectAttrW.argtypes = (self.SQLHDBC, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLGetConnectAttrW = self.ODBC_DRIVER.SQLGetConnectAttrW
        else:
            self.SQLGetConnectAttrW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetCursorNameW"):
            self.ODBC_DRIVER.SQLGetCursorNameW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetCursorNameW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetCursorNameW = self.ODBC_DRIVER.SQLGetCursorNameW
        else:
            self.SQLGetCursorNameW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetDescFieldW"):
            self.ODBC_DRIVER.SQLSetDescFieldW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetDescFieldW.argtypes = (self.SQLHDESC, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLPOINTER, self.SQLINTEGER,)
            self.SQLSetDescFieldW = self.ODBC_DRIVER.SQLSetDescFieldW
        else:
            self.SQLSetDescFieldW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetDescFieldW"):
            self.ODBC_DRIVER.SQLGetDescFieldW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetDescFieldW.argtypes = (self.SQLHDESC, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLPOINTER, self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLGetDescFieldW = self.ODBC_DRIVER.SQLGetDescFieldW
        else:
            self.SQLGetDescFieldW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetDescRecW"):
            self.ODBC_DRIVER.SQLGetDescRecW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetDescRecW.argtypes = (self.SQLHDESC, self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLLEN), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetDescRecW = self.ODBC_DRIVER.SQLGetDescRecW
        else:
            self.SQLGetDescRecW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetDiagFieldW"):
            self.ODBC_DRIVER.SQLGetDiagFieldW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetDiagFieldW.argtypes = (self.SQLSMALLINT, self.SQLHANDLE, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLPOINTER, self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetDiagFieldW = self.ODBC_DRIVER.SQLGetDiagFieldW
        else:
            self.SQLGetDiagFieldW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetDiagRecW"):
            self.ODBC_DRIVER.SQLGetDiagRecW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetDiagRecW.argtypes = (self.SQLSMALLINT, self.SQLHANDLE, self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), ctypes.POINTER(self.SQLINTEGER), ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetDiagRecW = self.ODBC_DRIVER.SQLGetDiagRecW
        else:
            self.SQLGetDiagRecW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLPrepareW"):
            self.ODBC_DRIVER.SQLPrepareW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLPrepareW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLINTEGER,)
            self.SQLPrepareW = self.ODBC_DRIVER.SQLPrepareW
        else:
            self.SQLPrepareW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetConnectAttrW"):
            self.ODBC_DRIVER.SQLSetConnectAttrW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetConnectAttrW.argtypes = (self.SQLHDBC, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER,)
            self.SQLSetConnectAttrW = self.ODBC_DRIVER.SQLSetConnectAttrW
        else:
            self.SQLSetConnectAttrW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetCursorNameW"):
            self.ODBC_DRIVER.SQLSetCursorNameW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetCursorNameW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT,)
            self.SQLSetCursorNameW = self.ODBC_DRIVER.SQLSetCursorNameW
        else:
            self.SQLSetCursorNameW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLColumnsW"):
            self.ODBC_DRIVER.SQLColumnsW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLColumnsW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT,)
            self.SQLColumnsW = self.ODBC_DRIVER.SQLColumnsW
        else:
            self.SQLColumnsW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetConnectOptionW"):
            self.ODBC_DRIVER.SQLGetConnectOptionW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetConnectOptionW.argtypes = (self.SQLHDBC, self.SQLUSMALLINT, self.SQLPOINTER,)
            self.SQLGetConnectOptionW = self.ODBC_DRIVER.SQLGetConnectOptionW
        else:
            self.SQLGetConnectOptionW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetInfoW"):
            self.ODBC_DRIVER.SQLGetInfoW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetInfoW.argtypes = (self.SQLHDBC, self.SQLUSMALLINT, self.SQLPOINTER, self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetInfoW = self.ODBC_DRIVER.SQLGetInfoW
        else:
            self.SQLGetInfoW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetTypeInfoW"):
            self.ODBC_DRIVER.SQLGetTypeInfoW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetTypeInfoW.argtypes = (self.SQLHSTMT, self.SQLSMALLINT,)
            self.SQLGetTypeInfoW = self.ODBC_DRIVER.SQLGetTypeInfoW
        else:
            self.SQLGetTypeInfoW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetConnectOptionW"):
            self.ODBC_DRIVER.SQLSetConnectOptionW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetConnectOptionW.argtypes = (self.SQLHDBC, self.SQLUSMALLINT, self.SQLULEN,)
            self.SQLSetConnectOptionW = self.ODBC_DRIVER.SQLSetConnectOptionW
        else:
            self.SQLSetConnectOptionW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSpecialColumnsW"):
            self.ODBC_DRIVER.SQLSpecialColumnsW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSpecialColumnsW.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, self.SQLUSMALLINT, self.SQLUSMALLINT,)
            self.SQLSpecialColumnsW = self.ODBC_DRIVER.SQLSpecialColumnsW
        else:
            self.SQLSpecialColumnsW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLStatisticsW"):
            self.ODBC_DRIVER.SQLStatisticsW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLStatisticsW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, self.SQLUSMALLINT, self.SQLUSMALLINT,)
            self.SQLStatisticsW = self.ODBC_DRIVER.SQLStatisticsW
        else:
            self.SQLStatisticsW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLTablesW"):
            self.ODBC_DRIVER.SQLTablesW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLTablesW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT,)
            self.SQLTablesW = self.ODBC_DRIVER.SQLTablesW
        else:
            self.SQLTablesW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDataSourcesW"):
            self.ODBC_DRIVER.SQLDataSourcesW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDataSourcesW.argtypes = (self.SQLHENV, self.SQLUSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLDataSourcesW = self.ODBC_DRIVER.SQLDataSourcesW
        else:
            self.SQLDataSourcesW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDriverConnectW"):
            self.ODBC_DRIVER.SQLDriverConnectW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDriverConnectW.argtypes = (self.SQLHDBC, self.SQLHWND, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), self.SQLUSMALLINT,)
            self.SQLDriverConnectW = self.ODBC_DRIVER.SQLDriverConnectW
        else:
            self.SQLDriverConnectW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLBrowseConnectW"):
            self.ODBC_DRIVER.SQLBrowseConnectW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLBrowseConnectW.argtypes = (self.SQLHDBC, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLBrowseConnectW = self.ODBC_DRIVER.SQLBrowseConnectW
        else:
            self.SQLBrowseConnectW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLColumnPrivilegesW"):
            self.ODBC_DRIVER.SQLColumnPrivilegesW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLColumnPrivilegesW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT,)
            self.SQLColumnPrivilegesW = self.ODBC_DRIVER.SQLColumnPrivilegesW
        else:
            self.SQLColumnPrivilegesW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetStmtAttrW"):
            self.ODBC_DRIVER.SQLGetStmtAttrW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetStmtAttrW.argtypes = (self.SQLHSTMT, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLGetStmtAttrW = self.ODBC_DRIVER.SQLGetStmtAttrW
        else:
            self.SQLGetStmtAttrW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetStmtAttrW"):
            self.ODBC_DRIVER.SQLSetStmtAttrW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetStmtAttrW.argtypes = (self.SQLHSTMT, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER,)
            self.SQLSetStmtAttrW = self.ODBC_DRIVER.SQLSetStmtAttrW
        else:
            self.SQLSetStmtAttrW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLForeignKeysW"):
            self.ODBC_DRIVER.SQLForeignKeysW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLForeignKeysW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT,)
            self.SQLForeignKeysW = self.ODBC_DRIVER.SQLForeignKeysW
        else:
            self.SQLForeignKeysW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLNativeSqlW"):
            self.ODBC_DRIVER.SQLNativeSqlW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLNativeSqlW.argtypes = (self.SQLHDBC, ctypes.POINTER(self.SQLWCHAR), self.SQLINTEGER, ctypes.POINTER(self.SQLWCHAR), self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLNativeSqlW = self.ODBC_DRIVER.SQLNativeSqlW
        else:
            self.SQLNativeSqlW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLPrimaryKeysW"):
            self.ODBC_DRIVER.SQLPrimaryKeysW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLPrimaryKeysW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT,)
            self.SQLPrimaryKeysW = self.ODBC_DRIVER.SQLPrimaryKeysW
        else:
            self.SQLPrimaryKeysW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLProcedureColumnsW"):
            self.ODBC_DRIVER.SQLProcedureColumnsW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLProcedureColumnsW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT,)
            self.SQLProcedureColumnsW = self.ODBC_DRIVER.SQLProcedureColumnsW
        else:
            self.SQLProcedureColumnsW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLProceduresW"):
            self.ODBC_DRIVER.SQLProceduresW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLProceduresW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT,)
            self.SQLProceduresW = self.ODBC_DRIVER.SQLProceduresW
        else:
            self.SQLProceduresW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLTablePrivilegesW"):
            self.ODBC_DRIVER.SQLTablePrivilegesW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLTablePrivilegesW.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT,)
            self.SQLTablePrivilegesW = self.ODBC_DRIVER.SQLTablePrivilegesW
        else:
            self.SQLTablePrivilegesW = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDriversW"):
            self.ODBC_DRIVER.SQLDriversW.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDriversW.argtypes = (self.SQLHENV, self.SQLUSMALLINT, ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLWCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLDriversW = self.ODBC_DRIVER.SQLDriversW
        else:
            self.SQLDriversW = self.UnimplementedSQLFunction

        ################################################################################
        ####Function prototypes - ANSI##################################################
        ################################################################################
        if hasattr(self.ODBC_DRIVER, "SQLColAttributeA"):
            self.ODBC_DRIVER.SQLColAttributeA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLColAttributeA.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLUSMALLINT, self.SQLPOINTER, self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLLEN),)
            self.SQLColAttributeA = self.ODBC_DRIVER.SQLColAttributeA
        else:
            self.SQLColAttributeA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLColAttributesA"):
            self.ODBC_DRIVER.SQLColAttributesA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLColAttributesA.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLUSMALLINT, self.SQLPOINTER, self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLLEN),)
            self.SQLColAttributesA = self.ODBC_DRIVER.SQLColAttributesA
        else:
            self.SQLColAttributesA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLConnectA"):
            self.ODBC_DRIVER.SQLConnectA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLConnectA.argtypes = (self.SQLHDBC, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLConnectA = self.ODBC_DRIVER.SQLConnectA
        else:
            self.SQLConnectA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDescribeColA"):
            self.ODBC_DRIVER.SQLDescribeColA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDescribeColA.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLULEN), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLDescribeColA = self.ODBC_DRIVER.SQLDescribeColA
        else:
            self.SQLDescribeColA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLErrorA"):
            self.ODBC_DRIVER.SQLErrorA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLErrorA.argtypes = (self.SQLHENV, self.SQLHDBC, self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), ctypes.POINTER(self.SQLINTEGER), ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLErrorA = self.ODBC_DRIVER.SQLErrorA
        else:
            self.SQLErrorA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLExecDirectA"):
            self.ODBC_DRIVER.SQLExecDirectA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLExecDirectA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLINTEGER,)
            self.SQLExecDirectA = self.ODBC_DRIVER.SQLExecDirectA
        else:
            self.SQLExecDirectA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetConnectAttrA"):
            self.ODBC_DRIVER.SQLGetConnectAttrA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetConnectAttrA.argtypes = (self.SQLHDBC, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLGetConnectAttrA = self.ODBC_DRIVER.SQLGetConnectAttrA
        else:
            self.SQLGetConnectAttrA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetCursorNameA"):
            self.ODBC_DRIVER.SQLGetCursorNameA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetCursorNameA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetCursorNameA = self.ODBC_DRIVER.SQLGetCursorNameA
        else:
            self.SQLGetCursorNameA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetDescFieldA"):
            self.ODBC_DRIVER.SQLSetDescFieldA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetDescFieldA.argtypes = (self.SQLHDESC, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLPOINTER, self.SQLINTEGER,)
            self.SQLSetDescFieldA = self.ODBC_DRIVER.SQLSetDescFieldA
        else:
            self.SQLSetDescFieldA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetDescFieldA"):
            self.ODBC_DRIVER.SQLGetDescFieldA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetDescFieldA.argtypes = (self.SQLHDESC, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLPOINTER, self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLGetDescFieldA = self.ODBC_DRIVER.SQLGetDescFieldA
        else:
            self.SQLGetDescFieldA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetDescRecA"):
            self.ODBC_DRIVER.SQLGetDescRecA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetDescRecA.argtypes = (self.SQLHDESC, self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLLEN), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetDescRecA = self.ODBC_DRIVER.SQLGetDescRecA
        else:
            self.SQLGetDescRecA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetDiagFieldA"):
            self.ODBC_DRIVER.SQLGetDiagFieldA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetDiagFieldA.argtypes = (self.SQLSMALLINT, self.SQLHANDLE, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLPOINTER, self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetDiagFieldA = self.ODBC_DRIVER.SQLGetDiagFieldA
        else:
            self.SQLGetDiagFieldA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetDiagRecA"):
            self.ODBC_DRIVER.SQLGetDiagRecA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetDiagRecA.argtypes = (self.SQLSMALLINT, self.SQLHANDLE, self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), ctypes.POINTER(self.SQLINTEGER), ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetDiagRecA = self.ODBC_DRIVER.SQLGetDiagRecA
        else:
            self.SQLGetDiagRecA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLPrepareA"):
            self.ODBC_DRIVER.SQLPrepareA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLPrepareA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLINTEGER,)
            self.SQLPrepareA = self.ODBC_DRIVER.SQLPrepareA
        else:
            self.SQLPrepareA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetConnectAttrA"):
            self.ODBC_DRIVER.SQLSetConnectAttrA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetConnectAttrA.argtypes = (self.SQLHDBC, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER,)
            self.SQLSetConnectAttrA = self.ODBC_DRIVER.SQLSetConnectAttrA
        else:
            self.SQLSetConnectAttrA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetCursorNameA"):
            self.ODBC_DRIVER.SQLSetCursorNameA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetCursorNameA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLSetCursorNameA = self.ODBC_DRIVER.SQLSetCursorNameA
        else:
            self.SQLSetCursorNameA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLColumnsA"):
            self.ODBC_DRIVER.SQLColumnsA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLColumnsA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLColumnsA = self.ODBC_DRIVER.SQLColumnsA
        else:
            self.SQLColumnsA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetConnectOptionA"):
            self.ODBC_DRIVER.SQLGetConnectOptionA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetConnectOptionA.argtypes = (self.SQLHDBC, self.SQLUSMALLINT, self.SQLPOINTER,)
            self.SQLGetConnectOptionA = self.ODBC_DRIVER.SQLGetConnectOptionA
        else:
            self.SQLGetConnectOptionA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetInfoA"):
            self.ODBC_DRIVER.SQLGetInfoA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetInfoA.argtypes = (self.SQLHDBC, self.SQLUSMALLINT, self.SQLPOINTER, self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLGetInfoA = self.ODBC_DRIVER.SQLGetInfoA
        else:
            self.SQLGetInfoA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetTypeInfoA"):
            self.ODBC_DRIVER.SQLGetTypeInfoA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetTypeInfoA.argtypes = (self.SQLHSTMT, self.SQLSMALLINT,)
            self.SQLGetTypeInfoA = self.ODBC_DRIVER.SQLGetTypeInfoA
        else:
            self.SQLGetTypeInfoA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetConnectOptionA"):
            self.ODBC_DRIVER.SQLSetConnectOptionA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetConnectOptionA.argtypes = (self.SQLHDBC, self.SQLUSMALLINT, self.SQLULEN,)
            self.SQLSetConnectOptionA = self.ODBC_DRIVER.SQLSetConnectOptionA
        else:
            self.SQLSetConnectOptionA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSpecialColumnsA"):
            self.ODBC_DRIVER.SQLSpecialColumnsA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSpecialColumnsA.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, self.SQLUSMALLINT, self.SQLUSMALLINT,)
            self.SQLSpecialColumnsA = self.ODBC_DRIVER.SQLSpecialColumnsA
        else:
            self.SQLSpecialColumnsA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLStatisticsA"):
            self.ODBC_DRIVER.SQLStatisticsA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLStatisticsA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, self.SQLUSMALLINT, self.SQLUSMALLINT,)
            self.SQLStatisticsA = self.ODBC_DRIVER.SQLStatisticsA
        else:
            self.SQLStatisticsA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLTablesA"):
            self.ODBC_DRIVER.SQLTablesA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLTablesA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLTablesA = self.ODBC_DRIVER.SQLTablesA
        else:
            self.SQLTablesA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDataSourcesA"):
            self.ODBC_DRIVER.SQLDataSourcesA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDataSourcesA.argtypes = (self.SQLHENV, self.SQLUSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLDataSourcesA = self.ODBC_DRIVER.SQLDataSourcesA
        else:
            self.SQLDataSourcesA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDriverConnectA"):
            self.ODBC_DRIVER.SQLDriverConnectA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDriverConnectA.argtypes = (self.SQLHDBC, self.SQLHWND, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), self.SQLUSMALLINT,)
            self.SQLDriverConnectA = self.ODBC_DRIVER.SQLDriverConnectA
        else:
            self.SQLDriverConnectA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLBrowseConnectA"):
            self.ODBC_DRIVER.SQLBrowseConnectA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLBrowseConnectA.argtypes = (self.SQLHDBC, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLBrowseConnectA = self.ODBC_DRIVER.SQLBrowseConnectA
        else:
            self.SQLBrowseConnectA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLColumnPrivilegesA"):
            self.ODBC_DRIVER.SQLColumnPrivilegesA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLColumnPrivilegesA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLColumnPrivilegesA = self.ODBC_DRIVER.SQLColumnPrivilegesA
        else:
            self.SQLColumnPrivilegesA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLGetStmtAttrA"):
            self.ODBC_DRIVER.SQLGetStmtAttrA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLGetStmtAttrA.argtypes = (self.SQLHSTMT, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLGetStmtAttrA = self.ODBC_DRIVER.SQLGetStmtAttrA
        else:
            self.SQLGetStmtAttrA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetStmtAttrA"):
            self.ODBC_DRIVER.SQLSetStmtAttrA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetStmtAttrA.argtypes = (self.SQLHSTMT, self.SQLINTEGER, self.SQLPOINTER, self.SQLINTEGER,)
            self.SQLSetStmtAttrA = self.ODBC_DRIVER.SQLSetStmtAttrA
        else:
            self.SQLSetStmtAttrA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLForeignKeysA"):
            self.ODBC_DRIVER.SQLForeignKeysA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLForeignKeysA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLForeignKeysA = self.ODBC_DRIVER.SQLForeignKeysA
        else:
            self.SQLForeignKeysA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLNativeSqlA"):
            self.ODBC_DRIVER.SQLNativeSqlA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLNativeSqlA.argtypes = (self.SQLHDBC, ctypes.POINTER(self.SQLCHAR), self.SQLINTEGER, ctypes.POINTER(self.SQLCHAR), self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLNativeSqlA = self.ODBC_DRIVER.SQLNativeSqlA
        else:
            self.SQLNativeSqlA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLPrimaryKeysA"):
            self.ODBC_DRIVER.SQLPrimaryKeysA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLPrimaryKeysA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLPrimaryKeysA = self.ODBC_DRIVER.SQLPrimaryKeysA
        else:
            self.SQLPrimaryKeysA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLProcedureColumnsA"):
            self.ODBC_DRIVER.SQLProcedureColumnsA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLProcedureColumnsA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLProcedureColumnsA = self.ODBC_DRIVER.SQLProcedureColumnsA
        else:
            self.SQLProcedureColumnsA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLProceduresA"):
            self.ODBC_DRIVER.SQLProceduresA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLProceduresA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLProceduresA = self.ODBC_DRIVER.SQLProceduresA
        else:
            self.SQLProceduresA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLTablePrivilegesA"):
            self.ODBC_DRIVER.SQLTablePrivilegesA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLTablePrivilegesA.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLTablePrivilegesA = self.ODBC_DRIVER.SQLTablePrivilegesA
        else:
            self.SQLTablePrivilegesA = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDriversA"):
            self.ODBC_DRIVER.SQLDriversA.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDriversA.argtypes = (self.SQLHENV, self.SQLUSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLDriversA = self.ODBC_DRIVER.SQLDriversA
        else:
            self.SQLDriversA = self.UnimplementedSQLFunction

        ################################################################################
        ####Mapping macros for Unicode##################################################
        ################################################################################
        #if self.UNICODE:
        #    self.SQLColAttribute = self.SQLColAttributeW
        #    self.SQLColAttributes = self.SQLColAttributesW
        #    self.SQLConnect = self.SQLConnectW
        #    self.SQLDescribeCol = self.SQLDescribeColW
        #    self.SQLError = self.SQLErrorW
        #    self.SQLExecDirect = self.SQLExecDirectW
        #    self.SQLGetConnectAttr = self.SQLGetConnectAttrW
        #    self.SQLGetCursorName = self.SQLGetCursorNameW
        #    self.SQLGetDescField = self.SQLGetDescFieldW
        #    self.SQLGetDescRec = self.SQLGetDescRecW
        #    self.SQLGetDiagField = self.SQLGetDiagFieldW
        #    self.SQLGetDiagRec = self.SQLGetDiagRecW
        #    self.SQLPrepare = self.SQLPrepareW
        #    self.SQLSetConnectAttr = self.SQLSetConnectAttrW
        #    self.SQLSetCursorName = self.SQLSetCursorNameW
        #    self.SQLSetDescField = self.SQLSetDescFieldW
        #    self.SQLSetStmtAttr = self.SQLSetStmtAttrW
        #    self.SQLGetStmtAttr = self.SQLGetStmtAttrW
        #    self.SQLColumns = self.SQLColumnsW
        #    self.SQLGetConnectOption = self.SQLGetConnectOptionW
        #    self.SQLGetInfo = self.SQLGetInfoW
        #    self.SQLGetTypeInfo = self.SQLGetTypeInfoW
        #    self.SQLSetConnectOption = self.SQLSetConnectOptionW
        #    self.SQLSpecialColumns = self.SQLSpecialColumnsW
        #    self.SQLStatistics = self.SQLStatisticsW
        #    self.SQLTables = self.SQLTablesW
        #    self.SQLDataSources = self.SQLDataSourcesW
        #    self.SQLDriverConnect = self.SQLDriverConnectW
        #    self.SQLBrowseConnect = self.SQLBrowseConnectW
        #    self.SQLColumnPrivileges = self.SQLColumnPrivilegesW
        #    self.SQLForeignKeys = self.SQLForeignKeysW
        #    self.SQLNativeSql = self.SQLNativeSqlW
        #    self.SQLPrimaryKeys = self.SQLPrimaryKeysW
        #    self.SQLProcedureColumns = self.SQLProcedureColumnsW
        #    self.SQLProcedures = self.SQLProceduresW
        #    self.SQLTablePrivileges = self.SQLTablePrivilegesW
        #    self.SQLDrivers = self.SQLDriversW
        #else:
        #    self.SQLColAttribute = self.SQLColAttributeA
        #    self.SQLColAttributes = self.SQLColAttributesA
        #    self.SQLConnect = self.SQLConnectA
        #    self.SQLDescribeCol = self.SQLDescribeColA
        #    self.SQLError = self.SQLErrorA
        #    self.SQLExecDirect = self.SQLExecDirectA
        #    self.SQLGetConnectAttr = self.SQLGetConnectAttrA
        #    self.SQLGetCursorName = self.SQLGetCursorNameA
        #    self.SQLGetDescField = self.SQLGetDescFieldA
        #    self.SQLGetDescRec = self.SQLGetDescRecA
        #    self.SQLGetDiagField = self.SQLGetDiagFieldA
        #    self.SQLGetDiagRec = self.SQLGetDiagRecA
        #    self.SQLPrepare = self.SQLPrepareA
        #    self.SQLSetConnectAttr = self.SQLSetConnectAttrA
        #    self.SQLSetCursorName = self.SQLSetCursorNameA
        #    self.SQLSetDescField = self.SQLSetDescFieldA
        #    self.SQLSetStmtAttr = self.SQLSetStmtAttrA
        #    self.SQLGetStmtAttr = self.SQLGetStmtAttrA
        #    self.SQLColumns = self.SQLColumnsA
        #    self.SQLGetConnectOption = self.SQLGetConnectOptionA
        #    self.SQLGetInfo = self.SQLGetInfoA
        #    self.SQLGetTypeInfo = self.SQLGetTypeInfoA
        #    self.SQLSetConnectOption = self.SQLSetConnectOptionA
        #    self.SQLSpecialColumns = self.SQLSpecialColumnsA
        #    self.SQLStatistics = self.SQLStatisticsA
        #    self.SQLTables = self.SQLTablesA
        #    self.SQLDataSources = self.SQLDataSourcesA
        #    self.SQLDriverConnect = self.SQLDriverConnectA
        #    self.SQLBrowseConnect = self.SQLBrowseConnectA
        #    self.SQLColumnPrivileges = self.SQLColumnPrivilegesA
        #    self.SQLForeignKeys = self.SQLForeignKeysA
        #    self.SQLNativeSql = self.SQLNativeSqlA
        #    self.SQLPrimaryKeys = self.SQLPrimaryKeysA
        #    self.SQLProcedureColumns = self.SQLProcedureColumnsA
        #    self.SQLProcedures = self.SQLProceduresA
        #    self.SQLTablePrivileges = self.SQLTablePrivilegesA
        #    self.SQLDrivers = self.SQLDriversW

        ####----------------------------------------------------------------------------
        ####This section mimics sqlext.h------------------------------------------------
        ####----------------------------------------------------------------------------
        ################################################################################
        ################################################################################
        ####Useful Constants############################################################
        ################################################################################
        self.SQL_SPEC_MAJOR = 3
        self.SQL_SPEC_MINOR = 52
        self.SQL_SPEC_STRING = "03.52"

        self.SQL_SQLSTATE_SIZE = 5
        self.SQL_MAX_DSN_LENGTH = 32
        self.SQL_MAX_OPTION_STRING_LENGTH = 256

        ################################################################################
        ####Handle types################################################################
        ################################################################################
        self.SQL_HANDLE_SENV = 5

        ################################################################################
        ####Function return codes#######################################################
        ################################################################################
        self.SQL_NO_DATA_FOUND = self.SQL_NO_DATA

        ################################################################################
        ####Special length values for attributes########################################
        ################################################################################
        self.SQL_IS_POINTER = -4
        self.SQL_IS_UINTEGER = -5
        self.SQL_IS_INTEGER = -6
        self.SQL_IS_USMALLINT = -7
        self.SQL_IS_SMALLINT = -8

        ################################################################################
        ####SQL extended datatypes######################################################
        ################################################################################
        self.SQL_DATE = 9
        self.SQL_INTERVAL = 10
        self.SQL_TIME = 10
        self.SQL_TIMESTAMP = 11
        self.SQL_LONGVARCHAR = -1
        self.SQL_BINARY = -2
        self.SQL_VARBINARY = -3
        self.SQL_LONGVARBINARY = -4
        self.SQL_BIGINT = -5
        self.SQL_TINYINT = -6
        self.SQL_BIT = -7
        self.SQL_GUID = -11

        ################################################################################
        ####SQL Interval datatypes######################################################
        ################################################################################
        self.SQL_CODE_YEAR = 1
        self.SQL_CODE_MONTH = 2
        self.SQL_CODE_DAY = 3
        self.SQL_CODE_HOUR = 4
        self.SQL_CODE_MINUTE = 5
        self.SQL_CODE_SECOND = 6
        self.SQL_CODE_YEAR_TO_MONTH = 7
        self.SQL_CODE_DAY_TO_HOUR = 8
        self.SQL_CODE_DAY_TO_MINUTE = 9
        self.SQL_CODE_DAY_TO_SECOND = 10
        self.SQL_CODE_HOUR_TO_MINUTE = 11
        self.SQL_CODE_HOUR_TO_SECOND = 12
        self.SQL_CODE_MINUTE_TO_SECOND = 13

        self.SQL_INTERVAL_YEAR = 100 + self.SQL_CODE_YEAR
        self.SQL_INTERVAL_MONTH = 100 + self.SQL_CODE_MONTH
        self.SQL_INTERVAL_DAY = 100 + self.SQL_CODE_DAY
        self.SQL_INTERVAL_HOUR = 100 + self.SQL_CODE_HOUR
        self.SQL_INTERVAL_MINUTE = 100 + self.SQL_CODE_MINUTE
        self.SQL_INTERVAL_SECOND = 100 + self.SQL_CODE_SECOND
        self.SQL_INTERVAL_YEAR_TO_MONTH = 100 + self.SQL_CODE_YEAR_TO_MONTH
        self.SQL_INTERVAL_DAY_TO_HOUR = 100 + self.SQL_CODE_DAY_TO_HOUR
        self.SQL_INTERVAL_DAY_TO_MINUTE = 100 + self.SQL_CODE_DAY_TO_MINUTE
        self.SQL_INTERVAL_DAY_TO_SECOND = 100 + self.SQL_CODE_DAY_TO_SECOND
        self.SQL_INTERVAL_HOUR_TO_MINUTE = 100 + self.SQL_CODE_HOUR_TO_MINUTE
        self.SQL_INTERVAL_HOUR_TO_SECOND = 100 + self.SQL_CODE_HOUR_TO_SECOND
        self.SQL_INTERVAL_MINUTE_TO_SECOND = 100 + self.SQL_CODE_MINUTE_TO_SECOND

        ################################################################################
        #### SQL unicode data types#####################################################
        ################################################################################
        self.SQL_UNICODE = self.SQL_WCHAR
        self.SQL_UNICODE_VARCHAR = self.SQL_WVARCHAR
        self.SQL_UNICODE_LONGVARCHAR = self.SQL_WLONGVARCHAR
        self.SQL_UNICODE_CHAR = self.SQL_WCHAR

        self.SQL_TYPE_DRIVER_START = self.SQL_INTERVAL_YEAR
        self.SQL_TYPE_DRIVER_END = self.SQL_UNICODE_LONGVARCHAR

        self.SQL_SIGNED_OFFSET = -20
        self.SQL_UNSIGNED_OFFSET = -22

        ################################################################################
        ####C datatype to SQL datatype mapping##########################################
        ################################################################################
        self.SQL_C_CHAR = self.SQL_CHAR
        self.SQL_C_LONG = self.SQL_INTEGER
        self.SQL_C_SHORT = self.SQL_SMALLINT
        self.SQL_C_FLOAT = self.SQL_REAL
        self.SQL_C_DOUBLE = self.SQL_DOUBLE
        self.SQL_C_NUMERIC = self.SQL_NUMERIC
        self.SQL_C_DEFAULT = 99

        self.SQL_C_DATE = self.SQL_DATE
        self.SQL_C_TIME = self.SQL_TIME
        self.SQL_C_TIMESTAMP = self.SQL_TIMESTAMP
        self.SQL_C_BINARY = self.SQL_BINARY
        self.SQL_C_BIT = self.SQL_BIT
        self.SQL_C_TINYINT = self.SQL_TINYINT
        self.SQL_C_SLONG = self.SQL_C_LONG+self.SQL_SIGNED_OFFSET
        self.SQL_C_SSHORT = self.SQL_C_SHORT+self.SQL_SIGNED_OFFSET
        self.SQL_C_STINYINT = self.SQL_TINYINT+self.SQL_SIGNED_OFFSET
        self.SQL_C_ULONG = self.SQL_C_LONG+self.SQL_UNSIGNED_OFFSET
        self.SQL_C_USHORT = self.SQL_C_SHORT+self.SQL_UNSIGNED_OFFSET
        self.SQL_C_UTINYINT = self.SQL_TINYINT+self.SQL_UNSIGNED_OFFSET
        self.SQL_C_TYPE_DATE = self.SQL_TYPE_DATE
        self.SQL_C_TYPE_TIME = self.SQL_TYPE_TIME
        self.SQL_C_TYPE_TIMESTAMP = self.SQL_TYPE_TIMESTAMP
        self.SQL_C_INTERVAL_YEAR = self.SQL_INTERVAL_YEAR
        self.SQL_C_INTERVAL_MONTH = self.SQL_INTERVAL_MONTH
        self.SQL_C_INTERVAL_DAY = self.SQL_INTERVAL_DAY
        self.SQL_C_INTERVAL_HOUR = self.SQL_INTERVAL_HOUR
        self.SQL_C_INTERVAL_MINUTE = self.SQL_INTERVAL_MINUTE
        self.SQL_C_INTERVAL_SECOND = self.SQL_INTERVAL_SECOND
        self.SQL_C_INTERVAL_YEAR_TO_MONTH = self.SQL_INTERVAL_YEAR_TO_MONTH
        self.SQL_C_INTERVAL_DAY_TO_HOUR = self.SQL_INTERVAL_DAY_TO_HOUR
        self.SQL_C_INTERVAL_DAY_TO_MINUTE = self.SQL_INTERVAL_DAY_TO_MINUTE
        self.SQL_C_INTERVAL_DAY_TO_SECOND = self.SQL_INTERVAL_DAY_TO_SECOND
        self.SQL_C_INTERVAL_HOUR_TO_MINUTE = self.SQL_INTERVAL_HOUR_TO_MINUTE
        self.SQL_C_INTERVAL_HOUR_TO_SECOND = self.SQL_INTERVAL_HOUR_TO_SECOND
        self.SQL_C_INTERVAL_MINUTE_TO_SECOND = self.SQL_INTERVAL_MINUTE_TO_SECOND
        self.SQL_C_SBIGINT = self.SQL_BIGINT+self.SQL_SIGNED_OFFSET
        self.SQL_C_UBIGINT = self.SQL_BIGINT+self.SQL_UNSIGNED_OFFSET
        self.SQL_C_BOOKMARK = self.SQL_C_UBIGINT
        self.SQL_C_VARBOOKMARK = self.SQL_C_BINARY

        self.SQL_C_GUID = self.SQL_GUID

        self.SQL_TYPE_NULL = 0

        self.SQL_TYPE_MIN = self.SQL_BIT
        self.SQL_TYPE_MAX = self.SQL_VARCHAR

        ################################################################################
        ####Level 1 Functions###########################################################
        ################################################################################

        ################################################################################
        ####SQLBindParameter############################################################
        ################################################################################
        self.SQL_DEFAULT_PARAM = -5
        self.SQL_IGNORE = -6
        self.SQL_COLUMN_IGNORE = self.SQL_IGNORE
        self.SQL_LEN_DATA_AT_EXEC_OFFSET = -100
        def SQL_LEN_DATA_AT_EXEC_DEFINITION(length):
            return (-length) + self.SQL_LEN_DATA_AT_EXEC_OFFSET
        self.SQL_LEN_DATA_AT_EXEC = SQL_LEN_DATA_AT_EXEC_DEFINITION

        ################################################################################
        ####binary length for driver specific attributes################################
        ################################################################################
        self.SQL_LEN_BINARY_ATTR_OFFSET = -100
        def SQL_LEN_BINARY_ATTR_DEFINITION(length):
            return (-length) + self.SQL_LEN_BINARY_ATTR_OFFSET
        self.SQL_LEN_BINARY_ATTR = SQL_LEN_BINARY_ATTR_DEFINITION

        ################################################################################
        ####SQLColAttributes - ODBC 2.x defines#########################################
        ################################################################################
        self.SQL_COLUMN_COUNT = 0
        self.SQL_COLUMN_NAME = 1
        self.SQL_COLUMN_TYPE = 2
        self.SQL_COLUMN_LENGTH = 3
        self.SQL_COLUMN_PRECISION = 4
        self.SQL_COLUMN_SCALE = 5
        self.SQL_COLUMN_DISPLAY_SIZE = 6
        self.SQL_COLUMN_NULLABLE = 7
        self.SQL_COLUMN_UNSIGNED = 8
        self.SQL_COLUMN_MONEY = 9
        self.SQL_COLUMN_UPDATABLE = 10
        self.SQL_COLUMN_AUTO_INCREMENT = 11
        self.SQL_COLUMN_CASE_SENSITIVE = 12
        self.SQL_COLUMN_SEARCHABLE = 13
        self.SQL_COLUMN_TYPE_NAME = 14
        self.SQL_COLUMN_TABLE_NAME = 15
        self.SQL_COLUMN_OWNER_NAME = 16
        self.SQL_COLUMN_QUALIFIER_NAME = 17
        self.SQL_COLUMN_LABEL = 18
        self.SQL_COLATT_OPT_MAX = self.SQL_COLUMN_LABEL
        self.SQL_COLUMN_DRIVER_START = 1000

        self.SQL_COLATT_OPT_MIN = self.SQL_COLUMN_COUNT

        ################################################################################
        ####SQLColAttributes - SQL_COLUMN_UPDATABLE#####################################
        ################################################################################
        self.SQL_ATTR_READONLY = 0
        self.SQL_ATTR_WRITE = 1
        self.SQL_ATTR_READWRITE_UNKNOWN = 2

        ################################################################################
        ####SQLColAttributes - SQL_COLUMN_SEARCHABLE####################################
        ################################################################################
        self.SQL_UNSEARCHABLE = 0
        self.SQL_LIKE_ONLY = 1
        self.SQL_ALL_EXCEPT_LIKE = 2
        self.SQL_SEARCHABLE = 3
        self.SQL_PRED_SEARCHABLE = self.SQL_SEARCHABLE

        ################################################################################
        ####SQLDataSources - additional fetch directions################################
        ################################################################################
        self.SQL_FETCH_FIRST_USER = 31
        self.SQL_FETCH_FIRST_SYSTEM = 32

        ################################################################################
        ####SQLDriverConnect############################################################
        ################################################################################
        self.SQL_DRIVER_NOPROMPT = 0
        self.SQL_DRIVER_COMPLETE = 1
        self.SQL_DRIVER_PROMPT = 2
        self.SQL_DRIVER_COMPLETE_REQUIRED = 3

        ################################################################################
        ####SQLGetConnectAttr - ODBC 2.x attributes#####################################
        ################################################################################
        self.SQL_ACCESS_MODE = 101
        self.SQL_AUTOCOMMIT = 102
        self.SQL_LOGIN_TIMEOUT = 103
        self.SQL_OPT_TRACE = 104
        self.SQL_OPT_TRACEFILE = 105
        self.SQL_TRANSLATE_DLL = 106
        self.SQL_TRANSLATE_OPTION = 107
        self.SQL_TXN_ISOLATION = 108
        self.SQL_CURRENT_QUALIFIER = 109
        self.SQL_ODBC_CURSORS = 110
        self.SQL_QUIET_MODE = 111
        self.SQL_PACKET_SIZE = 112

        ################################################################################
        ####SQLGetConnectAttr - ODBC 3.0 attributes#####################################
        ################################################################################
        self.SQL_ATTR_ACCESS_MODE = self.SQL_ACCESS_MODE
        self.SQL_ATTR_AUTOCOMMIT = self.SQL_AUTOCOMMIT
        self.SQL_ATTR_CONNECTION_TIMEOUT = 113
        self.SQL_ATTR_CURRENT_CATALOG = self.SQL_CURRENT_QUALIFIER
        self.SQL_ATTR_DISCONNECT_BEHAVIOR = 114
        self.SQL_ATTR_ENLIST_IN_DTC = 1207
        self.SQL_ATTR_ENLIST_IN_XA = 1208
        self.SQL_ATTR_LOGIN_TIMEOUT = self.SQL_LOGIN_TIMEOUT
        self.SQL_ATTR_ODBC_CURSORS = self.SQL_ODBC_CURSORS
        self.SQL_ATTR_PACKET_SIZE = self.SQL_PACKET_SIZE
        self.SQL_ATTR_QUIET_MODE = self.SQL_QUIET_MODE
        self.SQL_ATTR_TRACE = self.SQL_OPT_TRACE
        self.SQL_ATTR_TRACEFILE = self.SQL_OPT_TRACEFILE
        self.SQL_ATTR_TRANSLATE_LIB = self.SQL_TRANSLATE_DLL
        self.SQL_ATTR_TRANSLATE_OPTION = self.SQL_TRANSLATE_OPTION
        self.SQL_ATTR_TXN_ISOLATION = self.SQL_TXN_ISOLATION

        self.SQL_ATTR_CONNECTION_DEAD = 1209

        ################################################################################
        ####These options have no meaning for a 3.0 driver##############################
        ################################################################################
        self.SQL_CONN_OPT_MIN = self.SQL_ACCESS_MODE
        self.SQL_CONN_OPT_MAX = self.SQL_PACKET_SIZE
        self.SQL_CONNECT_OPT_DRVR_START = 1000

        ################################################################################
        ####SQLGetConnectAttr - SQL_ACCESS_MODE#########################################
        ################################################################################
        self.SQL_MODE_READ_WRITE = 0
        self.SQL_MODE_READ_ONLY = 1
        self.SQL_MODE_DEFAULT = self.SQL_MODE_READ_WRITE

        ################################################################################
        ####SQLGetConnectAttr - SQL_AUTOCOMMIT##########################################
        ################################################################################
        self.SQL_AUTOCOMMIT_OFF = 0
        self.SQL_AUTOCOMMIT_ON = 1
        self.SQL_AUTOCOMMIT_DEFAULT = self.SQL_AUTOCOMMIT_ON

        ################################################################################
        ####SQLGetConnectAttr - SQL_LOGIN_TIMEOUT#######################################
        ################################################################################
        self.SQL_LOGIN_TIMEOUT_DEFAULT = 15

        ################################################################################
        ####SQLGetConnectAttr - SQL_ODBC_CURSORS########################################
        ################################################################################
        self.SQL_CUR_USE_IF_NEEDED = 0
        self.SQL_CUR_USE_ODBC = 1
        self.SQL_CUR_USE_DRIVER = 2
        self.SQL_CUR_DEFAULT = self.SQL_CUR_USE_DRIVER

        ################################################################################
        ####SQLGetConnectAttr - SQL_OPT_TRACE###########################################
        ################################################################################
        self.SQL_OPT_TRACE_OFF = 0
        self.SQL_OPT_TRACE_ON = 1
        self.SQL_OPT_TRACE_DEFAULT = self.SQL_OPT_TRACE_OFF

        self.SQL_OPT_TRACE_FILE_DEFAULT = "odbc.log"
        self.SQL_OPT_TRACE_FILE_DEFAULTW = "odbc.log"

        ################################################################################
        ####SQLGetConnectAttr - SQL_ATTR_ANSI_APP#######################################
        ################################################################################
        self.SQL_AA_TRUE = 1
        self.SQL_AA_FALSE = 0

        ################################################################################
        ####SQLGetConnectAttr - SQL_ATTR_CONNECTION_DEAD################################
        ################################################################################
        self.SQL_CD_TRUE = 1
        self.SQL_CD_FALSE = 0

        ################################################################################
        ####SQLGetConnectAttr - SQL_ATTR_DISCONNECT_BEHAVIOR############################
        ################################################################################
        self.SQL_DB_RETURN_TO_POOL = 0
        self.SQL_DB_DISCONNECT = 1
        self.SQL_DB_DEFAULT = self.SQL_DB_RETURN_TO_POOL

        ################################################################################
        ####SQLGetConnectAttr - SQL_ATTR_ENLIST_IN_DTC##################################
        ################################################################################
        self.SQL_DTC_DONE = 0

        ################################################################################
        #### self.SQLGetConnectAttr - Unicode drivers########################################
        ################################################################################
        self.SQL_ATTR_ANSI_APP = 115

        ################################################################################
        ####SQLGetData##################################################################
        ################################################################################
        self.SQL_NO_TOTAL = -4

        ################################################################################
        ####SQLGetDescField - extended descriptor field#################################
        ################################################################################
        self.SQL_DESC_ARRAY_SIZE = 20
        self.SQL_DESC_ARRAY_STATUS_PTR = 21
        self.SQL_DESC_AUTO_UNIQUE_VALUE = self.SQL_COLUMN_AUTO_INCREMENT
        self.SQL_DESC_BASE_COLUMN_NAME = 22
        self.SQL_DESC_BASE_TABLE_NAME = 23
        self.SQL_DESC_BIND_OFFSET_PTR = 24
        self.SQL_DESC_BIND_TYPE = 25
        self.SQL_DESC_CASE_SENSITIVE = self.SQL_COLUMN_CASE_SENSITIVE
        self.SQL_DESC_CATALOG_NAME = self.SQL_COLUMN_QUALIFIER_NAME
        self.SQL_DESC_CONCISE_TYPE = self.SQL_COLUMN_TYPE
        self.SQL_DESC_DATETIME_INTERVAL_PRECISION = 26
        self.SQL_DESC_DISPLAY_SIZE = self.SQL_COLUMN_DISPLAY_SIZE
        self.SQL_DESC_FIXED_PREC_SCALE = self.SQL_COLUMN_MONEY
        self.SQL_DESC_LABEL = self.SQL_COLUMN_LABEL
        self.SQL_DESC_LITERAL_PREFIX = 27
        self.SQL_DESC_LITERAL_SUFFIX = 28
        self.SQL_DESC_LOCAL_TYPE_NAME = 29
        self.SQL_DESC_MAXIMUM_SCALE = 30
        self.SQL_DESC_MINIMUM_SCALE = 31
        self.SQL_DESC_NUM_PREC_RADIX = 32
        self.SQL_DESC_PARAMETER_TYPE = 33
        self.SQL_DESC_ROWS_PROCESSED_PTR = 34
        self.SQL_DESC_ROWVER = 35
        self.SQL_DESC_SCHEMA_NAME = self.SQL_COLUMN_OWNER_NAME
        self.SQL_DESC_SEARCHABLE = self.SQL_COLUMN_SEARCHABLE
        self.SQL_DESC_TYPE_NAME = self.SQL_COLUMN_TYPE_NAME
        self.SQL_DESC_TABLE_NAME = self.SQL_COLUMN_TABLE_NAME
        self.SQL_DESC_UNSIGNED = self.SQL_COLUMN_UNSIGNED
        self.SQL_DESC_UPDATABLE = self.SQL_COLUMN_UPDATABLE

        ################################################################################
        ####SQLGetDiagField - defines for diagnostics fields############################
        ################################################################################
        self.SQL_DIAG_CURSOR_ROW_COUNT = -1249
        self.SQL_DIAG_ROW_NUMBER = -1248
        self.SQL_DIAG_COLUMN_NUMBER = -1247

        ################################################################################
        ####SQLGetDiagField - SQL_DIAG_ROW_NUMBER and SQL_DIAG_COLUMN_NUMBER############
        ################################################################################
        self.SQL_NO_ROW_NUMBER = -1
        self.SQL_NO_COLUMN_NUMBER = -1
        self.SQL_ROW_NUMBER_UNKNOWN = -2
        self.SQL_COLUMN_NUMBER_UNKNOWN = -2

        ################################################################################
        ####SQLGetEnvAttr - Attributes##################################################
        ################################################################################
        self.SQL_ATTR_ODBC_VERSION = 200
        self.SQL_ATTR_CONNECTION_POOLING = 201
        self.SQL_ATTR_CP_MATCH = 202

        ################################################################################
        ####SQLGetEnvAttr - SQL_ATTR_ODBC_VERSION#######################################
        ################################################################################
        self.SQL_OV_ODBC2 = 2
        self.SQL_OV_ODBC3 = 3

        ################################################################################
        ####SQLGetEnvAttr - SQL_ATTR_CONNECTION_POOLING#################################
        ################################################################################
        self.SQL_CP_OFF = 0
        self.SQL_CP_ONE_PER_DRIVER = 1
        self.SQL_CP_ONE_PER_HENV = 2
        self.SQL_CP_DEFAULT = self.SQL_CP_OFF

        ################################################################################
        ####SQLGetEnvAttr - SQL_ATTR_CP_MATCH###########################################
        ################################################################################
        self.SQL_CP_STRICT_MATCH = 0
        self.SQL_CP_RELAXED_MATCH = 1
        self.SQL_CP_MATCH_DEFAULT = self.SQL_CP_STRICT_MATCH

        ################################################################################
        ####SQLGetFunctions - extensions to the X/Open specification####################
        ################################################################################
        self.SQL_API_SQLALLOCHANDLESTD = 73
        self.SQL_API_SQLBULKOPERATIONS = 24
        self.SQL_API_SQLBINDPARAMETER = 72
        self.SQL_API_SQLBROWSECONNECT = 55
        self.SQL_API_SQLCOLATTRIBUTES = 6
        self.SQL_API_SQLCOLUMNPRIVILEGES = 56
        self.SQL_API_SQLDESCRIBEPARAM = 58
        self.SQL_API_SQLDRIVERCONNECT = 41
        self.SQL_API_SQLDRIVERS = 71
        self.SQL_API_SQLEXTENDEDFETCH = 59
        self.SQL_API_SQLFOREIGNKEYS = 60
        self.SQL_API_SQLMORERESULTS = 61
        self.SQL_API_SQLNATIVESQL = 62
        self.SQL_API_SQLNUMPARAMS = 63
        self.SQL_API_SQLPARAMOPTIONS = 64
        self.SQL_API_SQLPRIMARYKEYS = 65
        self.SQL_API_SQLPROCEDURECOLUMNS = 66
        self.SQL_API_SQLPROCEDURES = 67
        self.SQL_API_SQLSETPOS = 68
        self.SQL_API_SQLSETSCROLLOPTIONS = 69
        self.SQL_API_SQLTABLEPRIVILEGES = 70

        ################################################################################
        ####These are not useful anymore as the X/Open specification defines############
        ####functions in the 10000 range################################################
        ################################################################################
        self.SQL_EXT_API_LAST = self.SQL_API_SQLBINDPARAMETER
        self.SQL_NUM_FUNCTIONS = 23
        self.SQL_EXT_API_START = 40
        self.SQL_NUM_EXTENSIONS = (self.SQL_EXT_API_LAST-self.SQL_EXT_API_START+1)

        ################################################################################
        ####SQLGetFunctions - ODBC version 2.x and earlier##############################
        ################################################################################
        self.SQL_API_ALL_FUNCTIONS = 0

        ################################################################################
        ####Loading by ordinal is not supported for 3.0 and above drivers###############
        ################################################################################
        self.SQL_API_LOADBYORDINAL = 199

        ################################################################################
        ####SQLGetFunctions - SQL_API_ODBC3_ALL_FUNCTIONS###############################
        ################################################################################
        self.SQL_API_ODBC3_ALL_FUNCTIONS = 999
        self.SQL_API_ODBC3_ALL_FUNCTIONS_SIZE = 250

        #TODO: Map self.SQL_FUNC_EXISTS macro
        self.SQL_FUNC_EXISTS = self.UnimplementedSQLFunction

        ################################################################################
        ####SQLGetInfo - ODBC 2.x extensions to the X/Open standard#####################
        ################################################################################
        self.SQL_INFO_FIRST = 0
        self.SQL_ACTIVE_CONNECTIONS = 0
        self.SQL_ACTIVE_STATEMENTS = 1
        self.SQL_DRIVER_HDBC = 3
        self.SQL_DRIVER_HENV = 4
        self.SQL_DRIVER_HSTMT = 5
        self.SQL_DRIVER_NAME = 6
        self.SQL_DRIVER_VER = 7
        self.SQL_ODBC_API_CONFORMANCE = 9
        self.SQL_ODBC_VER = 10
        self.SQL_ROW_UPDATES = 11
        self.SQL_ODBC_SAG_CLI_CONFORMANCE = 12
        self.SQL_ODBC_SQL_CONFORMANCE = 15
        self.SQL_PROCEDURES = 21
        self.SQL_CONCAT_NULL_BEHAVIOR = 22
        self.SQL_CURSOR_ROLLBACK_BEHAVIOR = 24
        self.SQL_EXPRESSIONS_IN_ORDERBY = 27
        self.SQL_MAX_OWNER_NAME_LEN = 32
        self.SQL_MAX_PROCEDURE_NAME_LEN = 33
        self.SQL_MAX_QUALIFIER_NAME_LEN = 34
        self.SQL_MULT_RESULT_SETS = 36
        self.SQL_MULTIPLE_ACTIVE_TXN = 37
        self.SQL_OUTER_JOINS = 38
        self.SQL_OWNER_TERM = 39
        self.SQL_PROCEDURE_TERM = 40
        self.SQL_QUALIFIER_NAME_SEPARATOR = 41
        self.SQL_QUALIFIER_TERM = 42
        self.SQL_SCROLL_OPTIONS = 44
        self.SQL_TABLE_TERM = 45
        self.SQL_CONVERT_FUNCTIONS = 48
        self.SQL_NUMERIC_FUNCTIONS = 49
        self.SQL_STRING_FUNCTIONS = 50
        self.SQL_SYSTEM_FUNCTIONS = 51
        self.SQL_TIMEDATE_FUNCTIONS = 52
        self.SQL_CONVERT_BIGINT = 53
        self.SQL_CONVERT_BINARY = 54
        self.SQL_CONVERT_BIT = 55
        self.SQL_CONVERT_CHAR = 56
        self.SQL_CONVERT_DATE = 57
        self.SQL_CONVERT_DECIMAL = 58
        self.SQL_CONVERT_DOUBLE = 59
        self.SQL_CONVERT_FLOAT = 60
        self.SQL_CONVERT_INTEGER = 61
        self.SQL_CONVERT_LONGVARCHAR = 62
        self.SQL_CONVERT_NUMERIC = 63
        self.SQL_CONVERT_REAL = 64
        self.SQL_CONVERT_SMALLINT = 65
        self.SQL_CONVERT_TIME = 66
        self.SQL_CONVERT_TIMESTAMP = 67
        self.SQL_CONVERT_TINYINT = 68
        self.SQL_CONVERT_VARBINARY = 69
        self.SQL_CONVERT_VARCHAR = 70
        self.SQL_CONVERT_LONGVARBINARY = 71
        self.SQL_ODBC_SQL_OPT_IEF = 73
        self.SQL_CORRELATION_NAME = 74
        self.SQL_NON_NULLABLE_COLUMNS = 75
        self.SQL_DRIVER_HLIB = 76
        self.SQL_DRIVER_ODBC_VER = 77
        self.SQL_LOCK_TYPES = 78
        self.SQL_POS_OPERATIONS = 79
        self.SQL_POSITIONED_STATEMENTS = 80
        self.SQL_BOOKMARK_PERSISTENCE = 82
        self.SQL_STATIC_SENSITIVITY = 83
        self.SQL_FILE_USAGE = 84
        self.SQL_COLUMN_ALIAS = 87
        self.SQL_GROUP_BY = 88
        self.SQL_KEYWORDS = 89
        self.SQL_OWNER_USAGE = 91
        self.SQL_QUALIFIER_USAGE = 92
        self.SQL_QUOTED_IDENTIFIER_CASE = 93
        self.SQL_SUBQUERIES = 95
        self.SQL_UNION = 96
        self.SQL_MAX_ROW_SIZE_INCLUDES_LONG = 103
        self.SQL_MAX_CHAR_LITERAL_LEN = 108
        self.SQL_TIMEDATE_ADD_INTERVALS = 109
        self.SQL_TIMEDATE_DIFF_INTERVALS = 110
        self.SQL_NEED_LONG_DATA_LEN = 111
        self.SQL_MAX_BINARY_LITERAL_LEN = 112
        self.SQL_LIKE_ESCAPE_CLAUSE = 113
        self.SQL_QUALIFIER_LOCATION = 114

        self.SQL_OJ_CAPABILITIES = 65003

        ################################################################################
        ####These values are not useful anymore as X/Open defines values in the#########
        ####10000 range#################################################################
        ################################################################################
        self.SQL_INFO_LAST = self.SQL_QUALIFIER_LOCATION
        self.SQL_INFO_DRIVER_START = 1000

        ################################################################################
        ####SQLGetInfo - ODBC 3.x extensions to the X/Open standard#####################
        ################################################################################
        self.SQL_ACTIVE_ENVIRONMENTS = 116
        self.SQL_ALTER_DOMAIN = 117

        self.SQL_SQL_CONFORMANCE = 118
        self.SQL_DATETIME_LITERALS = 119

        self.SQL_ASYNC_MODE = 10021
        self.SQL_BATCH_ROW_COUNT = 120
        self.SQL_BATCH_SUPPORT = 121
        self.SQL_CATALOG_LOCATION = self.SQL_QUALIFIER_LOCATION
        self.SQL_CATALOG_NAME_SEPARATOR = self.SQL_QUALIFIER_NAME_SEPARATOR
        self.SQL_CATALOG_TERM = self.SQL_QUALIFIER_TERM
        self.SQL_CATALOG_USAGE = self.SQL_QUALIFIER_USAGE
        self.SQL_CONVERT_WCHAR = 122
        self.SQL_CONVERT_INTERVAL_DAY_TIME = 123
        self.SQL_CONVERT_INTERVAL_YEAR_MONTH = 124
        self.SQL_CONVERT_WLONGVARCHAR = 125
        self.SQL_CONVERT_WVARCHAR = 126
        self.SQL_CREATE_ASSERTION = 127
        self.SQL_CREATE_CHARACTER_SET = 128
        self.SQL_CREATE_COLLATION = 129
        self.SQL_CREATE_DOMAIN = 130
        self.SQL_CREATE_SCHEMA = 131
        self.SQL_CREATE_TABLE = 132
        self.SQL_CREATE_TRANSLATION = 133
        self.SQL_CREATE_VIEW = 134
        self.SQL_DRIVER_HDESC = 135
        self.SQL_DROP_ASSERTION = 136
        self.SQL_DROP_CHARACTER_SET = 137
        self.SQL_DROP_COLLATION = 138
        self.SQL_DROP_DOMAIN = 139
        self.SQL_DROP_SCHEMA = 140
        self.SQL_DROP_TABLE = 141
        self.SQL_DROP_TRANSLATION = 142
        self.SQL_DROP_VIEW = 143
        self.SQL_DYNAMIC_CURSOR_ATTRIBUTES1 = 144
        self.SQL_DYNAMIC_CURSOR_ATTRIBUTES2 = 145
        self.SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1 = 146
        self.SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES2 = 147
        self.SQL_INDEX_KEYWORDS = 148
        self.SQL_INFO_SCHEMA_VIEWS = 149
        self.SQL_KEYSET_CURSOR_ATTRIBUTES1 = 150
        self.SQL_KEYSET_CURSOR_ATTRIBUTES2 = 151
        self.SQL_MAX_ASYNC_CONCURRENT_STATEMENTS = 10022
        self.SQL_ODBC_INTERFACE_CONFORMANCE = 152
        self.SQL_PARAM_ARRAY_ROW_COUNTS = 153
        self.SQL_PARAM_ARRAY_SELECTS = 154
        self.SQL_SCHEMA_TERM = self.SQL_OWNER_TERM
        self.SQL_SCHEMA_USAGE = self.SQL_OWNER_USAGE
        self.SQL_SQL92_DATETIME_FUNCTIONS = 155
        self.SQL_SQL92_FOREIGN_KEY_DELETE_RULE = 156
        self.SQL_SQL92_FOREIGN_KEY_UPDATE_RULE = 157
        self.SQL_SQL92_GRANT = 158
        self.SQL_SQL92_NUMERIC_VALUE_FUNCTIONS = 159
        self.SQL_SQL92_PREDICATES = 160
        self.SQL_SQL92_RELATIONAL_JOIN_OPERATORS = 161
        self.SQL_SQL92_REVOKE = 162
        self.SQL_SQL92_ROW_VALUE_CONSTRUCTOR = 163
        self.SQL_SQL92_STRING_FUNCTIONS = 164
        self.SQL_SQL92_VALUE_EXPRESSIONS = 165
        self.SQL_STANDARD_CLI_CONFORMANCE = 166
        self.SQL_STATIC_CURSOR_ATTRIBUTES1 = 167
        self.SQL_STATIC_CURSOR_ATTRIBUTES2 = 168

        self.SQL_AGGREGATE_FUNCTIONS = 169
        self.SQL_DDL_INDEX = 170
        self.SQL_DM_VER = 171
        self.SQL_INSERT_STATEMENT = 172
        self.SQL_UNION_STATEMENT = self.SQL_UNION

        self.SQL_DTC_TRANSITION_COST = 1750

        ################################################################################
        ####SQLGetInfo - SQL_AGGREGATE_FUNCTIONS########################################
        ################################################################################
        self.SQL_AF_AVG = 0x00000001
        self.SQL_AF_COUNT = 0x00000002
        self.SQL_AF_MAX = 0x00000004
        self.SQL_AF_MIN = 0x00000008
        self.SQL_AF_SUM = 0x00000010
        self.SQL_AF_DISTINCT = 0x00000020
        self.SQL_AF_ALL = 0x00000040

        ################################################################################
        ####SQLGetInfo - SQL_ALTER_DOMAIN###############################################
        ################################################################################
        self.SQL_AD_CONSTRAINT_NAME_DEFINITION = 0x00000001
        self.SQL_AD_ADD_DOMAIN_CONSTRAINT = 0x00000002
        self.SQL_AD_DROP_DOMAIN_CONSTRAINT = 0x00000004
        self.SQL_AD_ADD_DOMAIN_DEFAULT = 0x00000008
        self.SQL_AD_DROP_DOMAIN_DEFAULT = 0x00000010
        self.SQL_AD_ADD_CONSTRAINT_INITIALLY_DEFERRED = 0x00000020
        self.SQL_AD_ADD_CONSTRAINT_INITIALLY_IMMEDIATE = 0x00000040
        self.SQL_AD_ADD_CONSTRAINT_DEFERRABLE = 0x00000080
        self.SQL_AD_ADD_CONSTRAINT_NON_DEFERRABLE = 0x00000100

        ################################################################################
        ####SQLGetInfo - SQL_ALTER_TABLE################################################
        ################################################################################
        ################################################################################
        ####The following 5 bitmasks are defined in sql.h###############################
        ################################################################################
        ####SQL_AT_ADD_COLUMN = 0x00000001##############################################
        ####SQL_AT_DROP_COLUMN = 0x00000002#############################################
        ####SQL_AT_ADD_CONSTRAINT = 0x00000008##########################################
        ################################################################################
        self.SQL_AT_ADD_COLUMN_SINGLE = 0x00000020
        self.SQL_AT_ADD_COLUMN_DEFAULT = 0x00000040
        self.SQL_AT_ADD_COLUMN_COLLATION = 0x00000080
        self.SQL_AT_SET_COLUMN_DEFAULT = 0x00000100
        self.SQL_AT_DROP_COLUMN_DEFAULT = 0x00000200
        self.SQL_AT_DROP_COLUMN_CASCADE = 0x00000400
        self.SQL_AT_DROP_COLUMN_RESTRICT = 0x00000800
        self.SQL_AT_ADD_TABLE_CONSTRAINT = 0x00001000
        self.SQL_AT_DROP_TABLE_CONSTRAINT_CASCADE = 0x00002000
        self.SQL_AT_DROP_TABLE_CONSTRAINT_RESTRICT = 0x00004000
        self.SQL_AT_CONSTRAINT_NAME_DEFINITION = 0x00008000
        self.SQL_AT_CONSTRAINT_INITIALLY_DEFERRED = 0x00010000
        self.SQL_AT_CONSTRAINT_INITIALLY_IMMEDIATE = 0x00020000
        self.SQL_AT_CONSTRAINT_DEFERRABLE = 0x00040000
        self.SQL_AT_CONSTRAINT_NON_DEFERRABLE = 0x00080000

        ################################################################################
        ####SQLGetInfo - SQL_ASYNC_MODE#################################################
        ################################################################################
        self.SQL_AM_NONE = 0
        self.SQL_AM_CONNECTION = 1
        self.SQL_AM_STATEMENT = 2

        ################################################################################
        ####SQLGetInfo - SQL_BATCH_ROW_COUNT############################################
        ################################################################################
        self.SQL_BRC_PROCEDURES = 0x0000001
        self.SQL_BRC_EXPLICIT = 0x0000002
        self.SQL_BRC_ROLLED_UP = 0x0000004

        ################################################################################
        ####SQLGetInfo - SQL_BATCH_SUPPORT##############################################
        ################################################################################
        self.SQL_BS_SELECT_EXPLICIT = 0x00000001
        self.SQL_BS_ROW_COUNT_EXPLICIT = 0x00000002
        self.SQL_BS_SELECT_PROC = 0x00000004
        self.SQL_BS_ROW_COUNT_PROC = 0x00000008

        ################################################################################
        ####SQLGetInfo - SQL_BOOKMARK_PERSISTENCE#######################################
        ################################################################################
        self.SQL_BP_CLOSE = 0x00000001
        self.SQL_BP_DELETE = 0x00000002
        self.SQL_BP_DROP = 0x00000004
        self.SQL_BP_TRANSACTION = 0x00000008
        self.SQL_BP_UPDATE = 0x00000010
        self.SQL_BP_OTHER_HSTMT = 0x00000020
        self.SQL_BP_SCROLL = 0x00000040

        ################################################################################
        ####SQLGetInfo - SQL_CONCAT_NULL_BEHAVIOR#######################################
        ################################################################################
        self.SQL_CB_NULL = 0x0000
        self.SQL_CB_NON_NULL = 0x0001

        ################################################################################
        ####SQLGetInfo - SQL_CONVERT_* bitmask values###################################
        ################################################################################
        self.SQL_CVT_CHAR = 0x00000001
        self.SQL_CVT_NUMERIC = 0x00000002
        self.SQL_CVT_DECIMAL = 0x00000004
        self.SQL_CVT_INTEGER = 0x00000008
        self.SQL_CVT_SMALLINT = 0x00000010
        self.SQL_CVT_FLOAT = 0x00000020
        self.SQL_CVT_REAL = 0x00000040
        self.SQL_CVT_DOUBLE = 0x00000080
        self.SQL_CVT_VARCHAR = 0x00000100
        self.SQL_CVT_LONGVARCHAR = 0x00000200
        self.SQL_CVT_BINARY = 0x00000400
        self.SQL_CVT_VARBINARY = 0x00000800
        self.SQL_CVT_BIT = 0x00001000
        self.SQL_CVT_TINYINT = 0x00002000
        self.SQL_CVT_BIGINT = 0x00004000
        self.SQL_CVT_DATE = 0x00008000
        self.SQL_CVT_TIME = 0x00010000
        self.SQL_CVT_TIMESTAMP = 0x00020000
        self.SQL_CVT_LONGVARBINARY = 0x00040000
        self.SQL_CVT_INTERVAL_YEAR_MONTH = 0x00080000
        self.SQL_CVT_INTERVAL_DAY_TIME = 0x00100000
        self.SQL_CVT_WCHAR = 0x00200000
        self.SQL_CVT_WLONGVARCHAR = 0x00400000
        self.SQL_CVT_WVARCHAR = 0x00800000

        ################################################################################
        ####SQLGetInfo - SQL_CONVERT_FUNCTIONS##########################################
        ################################################################################
        self.SQL_FN_CVT_CONVERT = 0x00000001
        self.SQL_FN_CVT_CAST = 0x00000002

        ################################################################################
        ####SQLGetInfo - SQL_CORRELATION_NAME###########################################
        ################################################################################
        self.SQL_CN_NONE = 0x0000
        self.SQL_CN_DIFFERENT = 0x0001
        self.SQL_CN_ANY = 0x0002

        ################################################################################
        ####SQLGetInfo - SQL_CREATE_ASSERTION###########################################
        ################################################################################
        self.SQL_CA_CREATE_ASSERTION = 0x00000001
        self.SQL_CA_CONSTRAINT_INITIALLY_DEFERRED = 0x00000010
        self.SQL_CA_CONSTRAINT_INITIALLY_IMMEDIATE = 0x00000020
        self.SQL_CA_CONSTRAINT_DEFERRABLE = 0x00000040
        self.SQL_CA_CONSTRAINT_NON_DEFERRABLE = 0x00000080

        ################################################################################
        ####SQLGetInfo - SQL_CREATE_CHARACTER_SET#######################################
        ################################################################################
        self.SQL_CCS_CREATE_CHARACTER_SET = 0x00000001
        self.SQL_CCS_COLLATE_CLAUSE = 0x00000002
        self.SQL_CCS_LIMITED_COLLATION = 0x00000004

        ################################################################################
        ####SQLGetInfo - SQL_CREATE_COLLATION###########################################
        ################################################################################
        self.SQL_CCOL_CREATE_COLLATION = 0x00000001

        ################################################################################
        ####SQLGetInfo - SQL_CREATE_DOMAIN##############################################
        ################################################################################
        self.SQL_CDO_CREATE_DOMAIN = 0x00000001
        self.SQL_CDO_DEFAULT = 0x00000002
        self.SQL_CDO_CONSTRAINT = 0x00000004
        self.SQL_CDO_COLLATION = 0x00000008
        self.SQL_CDO_CONSTRAINT_NAME_DEFINITION = 0x00000010
        self.SQL_CDO_CONSTRAINT_INITIALLY_DEFERRED = 0x00000020
        self.SQL_CDO_CONSTRAINT_INITIALLY_IMMEDIATE = 0x00000040
        self.SQL_CDO_CONSTRAINT_DEFERRABLE = 0x00000080
        self.SQL_CDO_CONSTRAINT_NON_DEFERRABLE = 0x00000100

        ################################################################################
        ####SQLGetInfo - SQL_CREATE_SCHEMA##############################################
        ################################################################################
        self.SQL_CS_CREATE_SCHEMA = 0x00000001
        self.SQL_CS_AUTHORIZATION = 0x00000002
        self.SQL_CS_DEFAULT_CHARACTER_SET = 0x00000004

        ################################################################################
        ####SQLGetInfo - SQL_CREATE_TABLE###############################################
        ################################################################################
        self.SQL_CT_CREATE_TABLE = 0x00000001
        self.SQL_CT_COMMIT_PRESERVE = 0x00000002
        self.SQL_CT_COMMIT_DELETE = 0x00000004
        self.SQL_CT_GLOBAL_TEMPORARY = 0x00000008
        self.SQL_CT_LOCAL_TEMPORARY = 0x00000010
        self.SQL_CT_CONSTRAINT_INITIALLY_DEFERRED = 0x00000020
        self.SQL_CT_CONSTRAINT_INITIALLY_IMMEDIATE = 0x00000040
        self.SQL_CT_CONSTRAINT_DEFERRABLE = 0x00000080
        self.SQL_CT_CONSTRAINT_NON_DEFERRABLE = 0x00000100
        self.SQL_CT_COLUMN_CONSTRAINT = 0x00000200
        self.SQL_CT_COLUMN_DEFAULT = 0x00000400
        self.SQL_CT_COLUMN_COLLATION = 0x00000800
        self.SQL_CT_TABLE_CONSTRAINT = 0x00001000
        self.SQL_CT_CONSTRAINT_NAME_DEFINITION = 0x00002000

        ################################################################################
        ####SQLGetInfo - SQL_CREATE_TRANSLATION#########################################
        ################################################################################
        self.SQL_CTR_CREATE_TRANSLATION = 0x00000001

        ################################################################################
        ####SQLGetInfo - SQL_CREATE_VIEW################################################
        ################################################################################
        self.SQL_CV_CREATE_VIEW = 0x00000001
        self.SQL_CV_CHECK_OPTION = 0x00000002
        self.SQL_CV_CASCADED = 0x00000004
        self.SQL_CV_LOCAL = 0x00000008

        ################################################################################
        ####SQLGetInfo - SQL_DATETIME_LITERALS##########################################
        ################################################################################
        self.SQL_DL_SQL92_DATE = 0x00000001
        self.SQL_DL_SQL92_TIME = 0x00000002
        self.SQL_DL_SQL92_TIMESTAMP = 0x00000004
        self.SQL_DL_SQL92_INTERVAL_YEAR = 0x00000008
        self.SQL_DL_SQL92_INTERVAL_MONTH = 0x00000010
        self.SQL_DL_SQL92_INTERVAL_DAY = 0x00000020
        self.SQL_DL_SQL92_INTERVAL_HOUR = 0x00000040
        self.SQL_DL_SQL92_INTERVAL_MINUTE = 0x00000080
        self.SQL_DL_SQL92_INTERVAL_SECOND = 0x00000100
        self.SQL_DL_SQL92_INTERVAL_YEAR_TO_MONTH = 0x00000200
        self.SQL_DL_SQL92_INTERVAL_DAY_TO_HOUR = 0x00000400
        self.SQL_DL_SQL92_INTERVAL_DAY_TO_MINUTE = 0x00000800
        self.SQL_DL_SQL92_INTERVAL_DAY_TO_SECOND = 0x00001000
        self.SQL_DL_SQL92_INTERVAL_HOUR_TO_MINUTE = 0x00002000
        self.SQL_DL_SQL92_INTERVAL_HOUR_TO_SECOND = 0x00004000
        self.SQL_DL_SQL92_INTERVAL_MINUTE_TO_SECOND = 0x00008000

        ################################################################################
        ####SQLGetInfo - SQL_DDL_INDEX##################################################
        ################################################################################
        self.SQL_DI_CREATE_INDEX = 0x00000001
        self.SQL_DI_DROP_INDEX = 0x00000002

        ################################################################################
        ####SQLGetInfo - SQL_DROP_ASSERTION#############################################
        ################################################################################
        self.SQL_DA_DROP_ASSERTION = 0x00000001

        ################################################################################
        ####SQLGetInfo - SQL_DROP_CHARACTER_SET#########################################
        ################################################################################
        self.SQL_DCS_DROP_CHARACTER_SET = 0x00000001

        ################################################################################
        ####SQLGetInfo - SQL_DROP_COLLATION#############################################
        ################################################################################
        self.SQL_DC_DROP_COLLATION = 0x00000001

        ################################################################################
        ####SQLGetInfo - SQL_DROP_DOMAIN################################################
        ################################################################################
        self.SQL_DD_DROP_DOMAIN = 0x00000001
        self.SQL_DD_RESTRICT = 0x00000002
        self.SQL_DD_CASCADE = 0x00000004

        ################################################################################
        ####SQLGetInfo - SQL_DROP_SCHEMA################################################
        ################################################################################
        self.SQL_DS_DROP_SCHEMA = 0x00000001
        self.SQL_DS_RESTRICT = 0x00000002
        self.SQL_DS_CASCADE = 0x00000004

        ################################################################################
        ####SQLGetInfo - SQL_DROP_TABLE#################################################
        ################################################################################
        self.SQL_DT_DROP_TABLE = 0x00000001
        self.SQL_DT_RESTRICT = 0x00000002
        self.SQL_DT_CASCADE = 0x00000004

        ################################################################################
        ####SQLGetInfo - SQL_DROP_TRANSLATION###########################################
        ################################################################################
        self.SQL_DTR_DROP_TRANSLATION = 0x00000001

        ################################################################################
        ####SQLGetInfo - SQL_DROP_VIEW##################################################
        ################################################################################
        self.SQL_DV_DROP_VIEW = 0x00000001
        self.SQL_DV_RESTRICT = 0x00000002
        self.SQL_DV_CASCADE = 0x00000004

        ################################################################################
        ####SQLGetInfo - SQL_DTC_TRANSITION_COST########################################
        ################################################################################
        self.SQL_DTC_ENLIST_EXPENSIVE = 0x00000001
        self.SQL_DTC_UNENLIST_EXPENSIVE = 0x00000002

        ################################################################################
        ####SQLGetInfo - SQL_DYNAMIC_CURSOR_ATTRIBUTES1#################################
        ####SQLGetInfo - SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1############################
        ####SQLGetInfo - SQL_KEYSET_CURSOR_ATTRIBUTES1##################################
        ####SQLGetInfo - SQL_STATIC_CURSOR_ATTRIBUTES1##################################
        ################################################################################
        ################################################################################
        ####SQLFetchScroll - FetchOrientation###########################################
        ################################################################################
        self.SQL_CA1_NEXT = 0x00000001
        self.SQL_CA1_ABSOLUTE = 0x00000002
        self.SQL_CA1_RELATIVE = 0x00000004
        self.SQL_CA1_BOOKMARK = 0x00000008

        ################################################################################
        ####SQLSetPos - LockType########################################################
        ################################################################################
        self.SQL_CA1_LOCK_NO_CHANGE = 0x00000040
        self.SQL_CA1_LOCK_EXCLUSIVE = 0x00000080
        self.SQL_CA1_LOCK_UNLOCK = 0x00000100

        ################################################################################
        ####SQLSetPos Operations########################################################
        ################################################################################
        self.SQL_CA1_POS_POSITION = 0x00000200
        self.SQL_CA1_POS_UPDATE = 0x00000400
        self.SQL_CA1_POS_DELETE = 0x00000800
        self.SQL_CA1_POS_REFRESH = 0x00001000

        ################################################################################
        ####positioned updates and deletes##############################################
        ################################################################################
        self.SQL_CA1_POSITIONED_UPDATE = 0x00002000
        self.SQL_CA1_POSITIONED_DELETE = 0x00004000
        self.SQL_CA1_SELECT_FOR_UPDATE = 0x00008000

        ################################################################################
        ####SQLBulkOperations operations################################################
        ################################################################################
        self.SQL_CA1_BULK_ADD = 0x00010000
        self.SQL_CA1_BULK_UPDATE_BY_BOOKMARK = 0x00020000
        self.SQL_CA1_BULK_DELETE_BY_BOOKMARK = 0x00040000
        self.SQL_CA1_BULK_FETCH_BY_BOOKMARK = 0x00080000

        ################################################################################
        ####SQLGetInfo - SQL_DYNAMIC_CURSOR_ATTRIBUTES2#################################
        ####SQLGetInfo - SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES2############################
        ####SQLGetInfo - SQL_KEYSET_CURSOR_ATTRIBUTES2##################################
        ####SQLGetInfo - SQL_STATIC_CURSOR_ATTRIBUTES2##################################
        ################################################################################
        ################################################################################
        ####SQL_ATTR_SCROLL_CONCURRENCY#################################################
        ################################################################################
        self.SQL_CA2_READ_ONLY_CONCURRENCY = 0x00000001
        self.SQL_CA2_LOCK_CONCURRENCY = 0x00000002
        self.SQL_CA2_OPT_ROWVER_CONCURRENCY = 0x00000004
        self.SQL_CA2_OPT_VALUES_CONCURRENCY = 0x00000008

        ################################################################################
        ####sensitivity of the cursor to its own inserts, deletes, and updates##########
        ################################################################################
        self.SQL_CA2_SENSITIVITY_ADDITIONS = 0x00000010
        self.SQL_CA2_SENSITIVITY_DELETIONS = 0x00000020
        self.SQL_CA2_SENSITIVITY_UPDATES = 0x00000040

        ################################################################################
        ####SQL_ATTR_MAX_ROWS###########################################################
        ################################################################################
        self.SQL_CA2_MAX_ROWS_SELECT = 0x00000080
        self.SQL_CA2_MAX_ROWS_INSERT = 0x00000100
        self.SQL_CA2_MAX_ROWS_DELETE = 0x00000200
        self.SQL_CA2_MAX_ROWS_UPDATE = 0x00000400
        self.SQL_CA2_MAX_ROWS_CATALOG = 0x00000800
        self.SQL_CA2_MAX_ROWS_AFFECTS_ALL = self.SQL_CA2_MAX_ROWS_SELECT |\
                                            self.SQL_CA2_MAX_ROWS_INSERT |\
                                            self.SQL_CA2_MAX_ROWS_DELETE |\
                                            self.SQL_CA2_MAX_ROWS_UPDATE |\
                                            self.SQL_CA2_MAX_ROWS_CATALOG

        ################################################################################
        ####SQL_DIAG_CURSOR_ROW_COUNT###################################################
        ################################################################################
        self.SQL_CA2_CRC_EXACT = 0x00001000
        self.SQL_CA2_CRC_APPROXIMATE = 0x00002000

        ################################################################################
        ####the kinds of positioned statements that can be simulated####################
        ################################################################################
        self.SQL_CA2_SIMULATE_NON_UNIQUE = 0x00004000
        self.SQL_CA2_SIMULATE_TRY_UNIQUE = 0x00008000
        self.SQL_CA2_SIMULATE_UNIQUE = 0x00010000

        ################################################################################
        ####SQLGetInfo - SQL_FETCH_DIRECTION############################################
        ################################################################################
        self.SQL_FD_FETCH_RESUME = 0x00000040
        self.SQL_FD_FETCH_BOOKMARK = 0x00000080

        ################################################################################
        ####SQLGetInfo - SQL_FILE_USAGE#################################################
        ################################################################################
        self.SQL_FILE_NOT_SUPPORTED = 0x0000
        self.SQL_FILE_TABLE = 0x0001
        self.SQL_FILE_QUALIFIER = 0x0002
        self.SQL_FILE_CATALOG = self.SQL_FILE_QUALIFIER

        ################################################################################
        ####SQLGetInfo - SQL_GETDATA_EXTENSIONS#########################################
        ################################################################################
        self.SQL_GD_BLOCK = 0x00000004
        self.SQL_GD_BOUND = 0x00000008

        ################################################################################
        ####SQLGetInfo - SQL_GROUP_BY###################################################
        ################################################################################
        self.SQL_GB_NOT_SUPPORTED = 0x0000
        self.SQL_GB_GROUP_BY_EQUALS_SELECT = 0x0001
        self.SQL_GB_GROUP_BY_CONTAINS_SELECT = 0x0002
        self.SQL_GB_NO_RELATION = 0x0003
        self.SQL_GB_COLLATE = 0x0004

        ################################################################################
        ####SQLGetInfo - SQL_INDEX_KEYWORDS#############################################
        ################################################################################
        self.SQL_IK_NONE = 0x00000000
        self.SQL_IK_ASC = 0x00000001
        self.SQL_IK_DESC = 0x00000002
        self.SQL_IK_ALL = self.SQL_IK_ASC | self.SQL_IK_DESC

        ################################################################################
        ####SQLGetInfo - SQL_INFO_SCHEMA_VIEWS##########################################
        ################################################################################
        self.SQL_ISV_ASSERTIONS = 0x00000001
        self.SQL_ISV_CHARACTER_SETS = 0x00000002
        self.SQL_ISV_CHECK_CONSTRAINTS = 0x00000004
        self.SQL_ISV_COLLATIONS = 0x00000008
        self.SQL_ISV_COLUMN_DOMAIN_USAGE = 0x00000010
        self.SQL_ISV_COLUMN_PRIVILEGES = 0x00000020
        self.SQL_ISV_COLUMNS = 0x00000040
        self.SQL_ISV_CONSTRAINT_COLUMN_USAGE = 0x00000080
        self.SQL_ISV_CONSTRAINT_TABLE_USAGE = 0x00000100
        self.SQL_ISV_DOMAIN_CONSTRAINTS = 0x00000200
        self.SQL_ISV_DOMAINS = 0x00000400
        self.SQL_ISV_KEY_COLUMN_USAGE = 0x00000800
        self.SQL_ISV_REFERENTIAL_CONSTRAINTS = 0x00001000
        self.SQL_ISV_SCHEMATA = 0x00002000
        self.SQL_ISV_SQL_LANGUAGES = 0x00004000
        self.SQL_ISV_TABLE_CONSTRAINTS = 0x00008000
        self.SQL_ISV_TABLE_PRIVILEGES = 0x00010000
        self.SQL_ISV_TABLES = 0x00020000
        self.SQL_ISV_TRANSLATIONS = 0x00040000
        self.SQL_ISV_USAGE_PRIVILEGES = 0x00080000
        self.SQL_ISV_VIEW_COLUMN_USAGE = 0x00100000
        self.SQL_ISV_VIEW_TABLE_USAGE = 0x00200000
        self.SQL_ISV_VIEWS = 0x00400000

        ################################################################################
        ####SQLGetInfo - SQL_INSERT_STATEMENT###########################################
        ################################################################################
        self.SQL_IS_INSERT_LITERALS = 0x00000001
        self.SQL_IS_INSERT_SEARCHED = 0x00000002
        self.SQL_IS_SELECT_INTO = 0x00000004

        ################################################################################
        ####SQLGetInfo - SQL_LOCK_TYPES#################################################
        ################################################################################
        self.SQL_LCK_NO_CHANGE = 0x00000001
        self.SQL_LCK_EXCLUSIVE = 0x00000002
        self.SQL_LCK_UNLOCK = 0x00000004

        ################################################################################
        ####SQLGetInfo - SQL_POS_OPERATIONS#############################################
        ################################################################################
        self.SQL_POS_POSITION = 0x00000001
        self.SQL_POS_REFRESH = 0x00000002
        self.SQL_POS_UPDATE = 0x00000004
        self.SQL_POS_DELETE = 0x00000008
        self.SQL_POS_ADD = 0x00000010

        ################################################################################
        ####SQLGetInfo - SQL_NON_NULLABLE_COLUMNS#######################################
        ################################################################################
        self.SQL_NNC_NULL = 0x0000
        self.SQL_NNC_NON_NULL = 0x0001

        ################################################################################
        ####SQLGetInfo - SQL_NULL_COLLATION#############################################
        ################################################################################
        self.SQL_NC_START = 0x0002
        self.SQL_NC_END = 0x0004

        ################################################################################
        ####SQLGetInfo - SQL_NUMERIC_FUNCTIONS##########################################
        ################################################################################
        self.SQL_FN_NUM_ABS = 0x00000001
        self.SQL_FN_NUM_ACOS = 0x00000002
        self.SQL_FN_NUM_ASIN = 0x00000004
        self.SQL_FN_NUM_ATAN = 0x00000008
        self.SQL_FN_NUM_ATAN2 = 0x00000010
        self.SQL_FN_NUM_CEILING = 0x00000020
        self.SQL_FN_NUM_COS = 0x00000040
        self.SQL_FN_NUM_COT = 0x00000080
        self.SQL_FN_NUM_EXP = 0x00000100
        self.SQL_FN_NUM_FLOOR = 0x00000200
        self.SQL_FN_NUM_LOG = 0x00000400
        self.SQL_FN_NUM_MOD = 0x00000800
        self.SQL_FN_NUM_SIGN = 0x00001000
        self.SQL_FN_NUM_SIN = 0x00002000
        self.SQL_FN_NUM_SQRT = 0x00004000
        self.SQL_FN_NUM_TAN = 0x00008000
        self.SQL_FN_NUM_PI = 0x00010000
        self.SQL_FN_NUM_RAND = 0x00020000
        self.SQL_FN_NUM_DEGREES = 0x00040000
        self.SQL_FN_NUM_LOG10 = 0x00080000
        self.SQL_FN_NUM_POWER = 0x00100000
        self.SQL_FN_NUM_RADIANS = 0x00200000
        self.SQL_FN_NUM_ROUND = 0x00400000
        self.SQL_FN_NUM_TRUNCATE = 0x00800000

        ################################################################################
        ####SQLGetInfo - SQL_ODBC_API_CONFORMANCE#######################################
        ################################################################################
        self.SQL_OAC_NONE = 0x0000
        self.SQL_OAC_LEVEL1 = 0x0001
        self.SQL_OAC_LEVEL2 = 0x0002

        ################################################################################
        ####SQLGetInfo - SQL_ODBC_INTERFACE_CONFORMANCE#################################
        ################################################################################
        self.SQL_OIC_CORE = 1
        self.SQL_OIC_LEVEL1 = 2
        self.SQL_OIC_LEVEL2 = 3

        ################################################################################
        ####SQLGetInfo - SQL_ODBC_SAG_CLI_CONFORMANCE###################################
        ################################################################################
        self.SQL_OSCC_NOT_COMPLIANT = 0x0000
        self.SQL_OSCC_COMPLIANT = 0x0001

        ################################################################################
        ####SQLGetInfo - SQL_ODBC_SQL_CONFORMANCE#######################################
        ################################################################################
        self.SQL_OSC_MINIMUM = 0x0000
        self.SQL_OSC_CORE = 0x0001
        self.SQL_OSC_EXTENDED = 0x0002

        ################################################################################
        ####SQLGetInfo - SQL_OWNER_USAGE################################################
        ################################################################################
        self.SQL_OU_DML_STATEMENTS = 0x00000001
        self.SQL_OU_PROCEDURE_INVOCATION = 0x00000002
        self.SQL_OU_TABLE_DEFINITION = 0x00000004
        self.SQL_OU_INDEX_DEFINITION = 0x00000008
        self.SQL_OU_PRIVILEGE_DEFINITION = 0x00000010

        ################################################################################
        ####SQLGetInfo - SQL_PARAM_ARRAY_ROW_COUNTS#####################################
        ################################################################################
        self.SQL_PARC_BATCH = 1
        self.SQL_PARC_NO_BATCH = 2

        ################################################################################
        ####SQLGetInfo - SQL_PARAM_ARRAY_SELECTS########################################
        ################################################################################
        self.SQL_PAS_BATCH = 1
        self.SQL_PAS_NO_BATCH = 2
        self.SQL_PAS_NO_SELECT = 3

        ################################################################################
        ####SQLGetInfo - SQL_POSITIONED_STATEMENTS######################################
        ################################################################################
        self.SQL_PS_POSITIONED_DELETE = 0x00000001
        self.SQL_PS_POSITIONED_UPDATE = 0x00000002
        self.SQL_PS_SELECT_FOR_UPDATE = 0x00000004

        ################################################################################
        ####SQLGetInfo - SQL_QUALIFIER_LOCATION#########################################
        ################################################################################
        self.SQL_QL_START = 0x0001
        self.SQL_QL_END = 0x0002

        ################################################################################
        ####SQLGetInfo - SQL_CATALOG_LOCATION###########################################
        ################################################################################
        self.SQL_CL_START = self.SQL_QL_START
        self.SQL_CL_END = self.SQL_QL_END

        ################################################################################
        ####SQLGetInfo - SQL_QUALIFIER_USAGE############################################
        ################################################################################
        self.SQL_QU_DML_STATEMENTS = 0x00000001
        self.SQL_QU_PROCEDURE_INVOCATION = 0x00000002
        self.SQL_QU_TABLE_DEFINITION = 0x00000004
        self.SQL_QU_INDEX_DEFINITION = 0x00000008
        self.SQL_QU_PRIVILEGE_DEFINITION = 0x00000010

        ################################################################################
        ####SQLGetInfo - SQL_CATALOG_USAGE##############################################
        ################################################################################
        self.SQL_CU_DML_STATEMENTS = self.SQL_QU_DML_STATEMENTS
        self.SQL_CU_PROCEDURE_INVOCATION = self.SQL_QU_PROCEDURE_INVOCATION
        self.SQL_CU_TABLE_DEFINITION = self.SQL_QU_TABLE_DEFINITION
        self.SQL_CU_INDEX_DEFINITION = self.SQL_QU_INDEX_DEFINITION
        self.SQL_CU_PRIVILEGE_DEFINITION = self.SQL_QU_PRIVILEGE_DEFINITION

        ################################################################################
        ####SQLGetInfo - SQL_SCHEMA_USAGE###############################################
        ################################################################################
        self.SQL_SU_DML_STATEMENTS = self.SQL_OU_DML_STATEMENTS
        self.SQL_SU_PROCEDURE_INVOCATION = self.SQL_OU_PROCEDURE_INVOCATION
        self.SQL_SU_TABLE_DEFINITION = self.SQL_OU_TABLE_DEFINITION
        self.SQL_SU_INDEX_DEFINITION = self.SQL_OU_INDEX_DEFINITION
        self.SQL_SU_PRIVILEGE_DEFINITION = self.SQL_OU_PRIVILEGE_DEFINITION

        ################################################################################
        ####SQLGetInfo - SQL_SCROLL_OPTIONS#############################################
        ################################################################################
        self.SQL_SO_FORWARD_ONLY = 0x00000001
        self.SQL_SO_KEYSET_DRIVEN = 0x00000002
        self.SQL_SO_DYNAMIC = 0x00000004
        self.SQL_SO_MIXED = 0x00000008
        self.SQL_SO_STATIC = 0x00000010

        ################################################################################
        ####SQLGetInfo - SQL_SQL_CONFORMANCE############################################
        ################################################################################
        self.SQL_SC_SQL92_ENTRY = 0x00000001
        self.SQL_SC_FIPS127_2_TRANSITIONAL = 0x00000002
        self.SQL_SC_SQL92_INTERMEDIATE = 0x00000004
        self.SQL_SC_SQL92_FULL = 0x00000008

        ################################################################################
        ####SQLGetInfo - SQL_SQL92_DATETIME_FUNCTIONS###################################
        ################################################################################
        self.SQL_SDF_CURRENT_DATE = 0x00000001
        self.SQL_SDF_CURRENT_TIME = 0x00000002
        self.SQL_SDF_CURRENT_TIMESTAMP = 0x00000004

        ################################################################################
        ####SQLGetInfo - SQL_SQL92_FOREIGN_KEY_DELETE_RULE##############################
        ################################################################################
        self.SQL_SFKD_CASCADE = 0x00000001
        self.SQL_SFKD_NO_ACTION = 0x00000002
        self.SQL_SFKD_SET_DEFAULT = 0x00000004
        self.SQL_SFKD_SET_NULL = 0x00000008

        ################################################################################
        ####SQLGetInfo - SQL_SQL92_FOREIGN_KEY_UPDATE_RULE##############################
        ################################################################################
        self.SQL_SFKU_CASCADE = 0x00000001
        self.SQL_SFKU_NO_ACTION = 0x00000002
        self.SQL_SFKU_SET_DEFAULT = 0x00000004
        self.SQL_SFKU_SET_NULL = 0x00000008

        ################################################################################
        ####SQLGetInfo - SQL_SQL92_GRANT################################################
        ################################################################################
        self.SQL_SG_USAGE_ON_DOMAIN = 0x00000001
        self.SQL_SG_USAGE_ON_CHARACTER_SET = 0x00000002
        self.SQL_SG_USAGE_ON_COLLATION = 0x00000004
        self.SQL_SG_USAGE_ON_TRANSLATION = 0x00000008
        self.SQL_SG_WITH_GRANT_OPTION = 0x00000010
        self.SQL_SG_DELETE_TABLE = 0x00000020
        self.SQL_SG_INSERT_TABLE = 0x00000040
        self.SQL_SG_INSERT_COLUMN = 0x00000080
        self.SQL_SG_REFERENCES_TABLE = 0x00000100
        self.SQL_SG_REFERENCES_COLUMN = 0x00000200
        self.SQL_SG_SELECT_TABLE = 0x00000400
        self.SQL_SG_UPDATE_TABLE = 0x00000800
        self.SQL_SG_UPDATE_COLUMN = 0x00001000

        ################################################################################
        ####SQLGetInfo - SQL_SQL92_NUMERIC_VALUE_FUNCTIONS##############################
        ################################################################################
        self.SQL_SNVF_BIT_LENGTH = 0x00000001
        self.SQL_SNVF_CHAR_LENGTH = 0x00000002
        self.SQL_SNVF_CHARACTER_LENGTH = 0x00000004
        self.SQL_SNVF_EXTRACT = 0x00000008
        self.SQL_SNVF_OCTET_LENGTH = 0x00000010
        self.SQL_SNVF_POSITION = 0x00000020

        ################################################################################
        ####SQLGetInfo - SQL_SQL92_PREDICATES###########################################
        ################################################################################
        self.SQL_SP_EXISTS = 0x00000001
        self.SQL_SP_ISNOTNULL = 0x00000002
        self.SQL_SP_ISNULL = 0x00000004
        self.SQL_SP_MATCH_FULL = 0x00000008
        self.SQL_SP_MATCH_PARTIAL = 0x00000010
        self.SQL_SP_MATCH_UNIQUE_FULL = 0x00000020
        self.SQL_SP_MATCH_UNIQUE_PARTIAL = 0x00000040
        self.SQL_SP_OVERLAPS = 0x00000080
        self.SQL_SP_UNIQUE = 0x00000100
        self.SQL_SP_LIKE = 0x00000200
        self.SQL_SP_IN = 0x00000400
        self.SQL_SP_BETWEEN = 0x00000800
        self.SQL_SP_COMPARISON = 0x00001000
        self.SQL_SP_QUANTIFIED_COMPARISON = 0x00002000

        ################################################################################
        ####SQLGetInfo - SQL_SQL92_RELATIONAL_JOIN_OPERATORS############################
        ################################################################################
        self.SQL_SRJO_CORRESPONDING_CLAUSE = 0x00000001
        self.SQL_SRJO_CROSS_JOIN = 0x00000002
        self.SQL_SRJO_EXCEPT_JOIN = 0x00000004
        self.SQL_SRJO_FULL_OUTER_JOIN = 0x00000008
        self.SQL_SRJO_INNER_JOIN = 0x00000010
        self.SQL_SRJO_INTERSECT_JOIN = 0x00000020
        self.SQL_SRJO_LEFT_OUTER_JOIN = 0x00000040
        self.SQL_SRJO_NATURAL_JOIN = 0x00000080
        self.SQL_SRJO_RIGHT_OUTER_JOIN = 0x00000100
        self.SQL_SRJO_UNION_JOIN = 0x00000200

        ################################################################################
        ####SQLGetInfo - SQL_SQL92_REVOKE###############################################
        ################################################################################
        self.SQL_SR_USAGE_ON_DOMAIN = 0x00000001
        self.SQL_SR_USAGE_ON_CHARACTER_SET = 0x00000002
        self.SQL_SR_USAGE_ON_COLLATION = 0x00000004
        self.SQL_SR_USAGE_ON_TRANSLATION = 0x00000008
        self.SQL_SR_GRANT_OPTION_FOR = 0x00000010
        self.SQL_SR_CASCADE = 0x00000020
        self.SQL_SR_RESTRICT = 0x00000040
        self.SQL_SR_DELETE_TABLE = 0x00000080
        self.SQL_SR_INSERT_TABLE = 0x00000100
        self.SQL_SR_INSERT_COLUMN = 0x00000200
        self.SQL_SR_REFERENCES_TABLE = 0x00000400
        self.SQL_SR_REFERENCES_COLUMN = 0x00000800
        self.SQL_SR_SELECT_TABLE = 0x00001000
        self.SQL_SR_UPDATE_TABLE = 0x00002000
        self.SQL_SR_UPDATE_COLUMN = 0x00004000

        ################################################################################
        ####SQLGetInfo - SQL_SQL92_ROW_VALUE_CONSTRUCTOR################################
        ################################################################################
        self.SQL_SRVC_VALUE_EXPRESSION = 0x00000001
        self.SQL_SRVC_NULL = 0x00000002
        self.SQL_SRVC_DEFAULT = 0x00000004
        self.SQL_SRVC_ROW_SUBQUERY = 0x00000008

        ################################################################################
        ####SQLGetInfo - SQL_SQL92_STRING_FUNCTIONS#####################################
        ################################################################################
        self.SQL_SSF_CONVERT = 0x00000001
        self.SQL_SSF_LOWER = 0x00000002
        self.SQL_SSF_UPPER = 0x00000004
        self.SQL_SSF_SUBSTRING = 0x00000008
        self.SQL_SSF_TRANSLATE = 0x00000010
        self.SQL_SSF_TRIM_BOTH = 0x00000020
        self.SQL_SSF_TRIM_LEADING = 0x00000040
        self.SQL_SSF_TRIM_TRAILING = 0x00000080

        ################################################################################
        ####SQLGetInfo - SQL_SQL92_VALUE_EXPRESSIONS####################################
        ################################################################################
        self.SQL_SVE_CASE = 0x00000001
        self.SQL_SVE_CAST = 0x00000002
        self.SQL_SVE_COALESCE = 0x00000004
        self.SQL_SVE_NULLIF = 0x00000008

        ################################################################################
        ####SQLGetInfo - SQL_STANDARD_CLI_CONFORMANCE###################################
        ################################################################################
        self.SQL_SCC_XOPEN_CLI_VERSION1 = 0x00000001
        self.SQL_SCC_ISO92_CLI = 0x00000002

        ################################################################################
        ####SQLGetInfo - SQL_STATIC_SENSITIVITY#########################################
        ################################################################################
        self.SQL_SS_ADDITIONS = 0x00000001
        self.SQL_SS_DELETIONS = 0x00000002
        self.SQL_SS_UPDATES = 0x00000004

        ################################################################################
        ####SQLGetInfo - SQL_SUBQUERIES#################################################
        ################################################################################
        self.SQL_SQ_COMPARISON = 0x00000001
        self.SQL_SQ_EXISTS = 0x00000002
        self.SQL_SQ_IN = 0x00000004
        self.SQL_SQ_QUANTIFIED = 0x00000008
        self.SQL_SQ_CORRELATED_SUBQUERIES = 0x00000010

        ################################################################################
        ####SQLGetInfo - SQL_SYSTEM_FUNCTIONS###########################################
        ################################################################################
        self.SQL_FN_SYS_USERNAME = 0x00000001
        self.SQL_FN_SYS_DBNAME = 0x00000002
        self.SQL_FN_SYS_IFNULL = 0x00000004

        ################################################################################
        ####SQLGetInfo - SQL_STRING_FUNCTIONS###########################################
        ################################################################################
        self.SQL_FN_STR_CONCAT = 0x00000001
        self.SQL_FN_STR_INSERT = 0x00000002
        self.SQL_FN_STR_LEFT = 0x00000004
        self.SQL_FN_STR_LTRIM = 0x00000008
        self.SQL_FN_STR_LENGTH = 0x00000010
        self.SQL_FN_STR_LOCATE = 0x00000020
        self.SQL_FN_STR_LCASE = 0x00000040
        self.SQL_FN_STR_REPEAT = 0x00000080
        self.SQL_FN_STR_REPLACE = 0x00000100
        self.SQL_FN_STR_RIGHT = 0x00000200
        self.SQL_FN_STR_RTRIM = 0x00000400
        self.SQL_FN_STR_SUBSTRING = 0x00000800
        self.SQL_FN_STR_UCASE = 0x00001000
        self.SQL_FN_STR_ASCII = 0x00002000
        self.SQL_FN_STR_CHAR = 0x00004000
        self.SQL_FN_STR_DIFFERENCE = 0x00008000
        self.SQL_FN_STR_LOCATE_2 = 0x00010000
        self.SQL_FN_STR_SOUNDEX = 0x00020000
        self.SQL_FN_STR_SPACE = 0x00040000
        self.SQL_FN_STR_BIT_LENGTH = 0x00080000
        self.SQL_FN_STR_CHAR_LENGTH = 0x00100000
        self.SQL_FN_STR_CHARACTER_LENGTH = 0x00200000
        self.SQL_FN_STR_OCTET_LENGTH = 0x00400000
        self.SQL_FN_STR_POSITION = 0x00800000

        ################################################################################
        ####SQLGetInfo - SQL_TIMEDATE_ADD_INTERVALS#####################################
        ####SQLGetInfo - SQL_TIMEDATE_DIFF_INTERVALS####################################
        ################################################################################
        self.SQL_FN_TSI_FRAC_SECOND = 0x00000001
        self.SQL_FN_TSI_SECOND = 0x00000002
        self.SQL_FN_TSI_MINUTE = 0x00000004
        self.SQL_FN_TSI_HOUR = 0x00000008
        self.SQL_FN_TSI_DAY = 0x00000010
        self.SQL_FN_TSI_WEEK = 0x00000020
        self.SQL_FN_TSI_MONTH = 0x00000040
        self.SQL_FN_TSI_QUARTER = 0x00000080
        self.SQL_FN_TSI_YEAR = 0x00000100

        ################################################################################
        ####SQLGetInfo - SQL_TIMEDATE_FUNCTIONS#########################################
        ################################################################################
        self.SQL_FN_TD_NOW = 0x00000001
        self.SQL_FN_TD_CURDATE = 0x00000002
        self.SQL_FN_TD_DAYOFMONTH = 0x00000004
        self.SQL_FN_TD_DAYOFWEEK = 0x00000008
        self.SQL_FN_TD_DAYOFYEAR = 0x00000010
        self.SQL_FN_TD_MONTH = 0x00000020
        self.SQL_FN_TD_QUARTER = 0x00000040
        self.SQL_FN_TD_WEEK = 0x00000080
        self.SQL_FN_TD_YEAR = 0x00000100
        self.SQL_FN_TD_CURTIME = 0x00000200
        self.SQL_FN_TD_HOUR = 0x00000400
        self.SQL_FN_TD_MINUTE = 0x00000800
        self.SQL_FN_TD_SECOND = 0x00001000
        self.SQL_FN_TD_TIMESTAMPADD = 0x00002000
        self.SQL_FN_TD_TIMESTAMPDIFF = 0x00004000
        self.SQL_FN_TD_DAYNAME = 0x00008000
        self.SQL_FN_TD_MONTHNAME = 0x00010000
        self.SQL_FN_TD_CURRENT_DATE = 0x00020000
        self.SQL_FN_TD_CURRENT_TIME = 0x00040000
        self.SQL_FN_TD_CURRENT_TIMESTAMP = 0x00080000
        self.SQL_FN_TD_EXTRACT = 0x00100000

        ################################################################################
        ####SQLGetInfo - SQL_TXN_ISOLATION_OPTION#######################################
        ################################################################################
        self.SQL_TXN_VERSIONING = 0x00000010

        ################################################################################
        ####SQLGetInfo - SQL_UNION######################################################
        ################################################################################
        self.SQL_U_UNION = 0x00000001
        self.SQL_U_UNION_ALL = 0x00000002

        ################################################################################
        ####SQLGetInfo - SQL_UNION_STATEMENT############################################
        ################################################################################
        self.SQL_US_UNION = self.SQL_U_UNION
        self.SQL_US_UNION_ALL = self.SQL_U_UNION_ALL

        ################################################################################
        ####SQLGetStmtAttr - ODBC 2.x attributes########################################
        ################################################################################
        self.SQL_QUERY_TIMEOUT = 0
        self.SQL_MAX_ROWS = 1
        self.SQL_NOSCAN = 2
        self.SQL_MAX_LENGTH = 3
        self.SQL_ASYNC_ENABLE = 4
        self.SQL_BIND_TYPE = 5
        self.SQL_CURSOR_TYPE = 6
        self.SQL_CONCURRENCY = 7
        self.SQL_KEYSET_SIZE = 8
        self.SQL_ROWSET_SIZE = 9
        self.SQL_SIMULATE_CURSOR = 10
        self.SQL_RETRIEVE_DATA = 11
        self.SQL_USE_BOOKMARKS = 12
        self.SQL_GET_BOOKMARK = 13
        self.SQL_ROW_NUMBER = 14

        ################################################################################
        ####SQLGetStmtAttr - ODBC 3.x attributes########################################
        ################################################################################
        self.SQL_ATTR_ASYNC_ENABLE = 4
        self.SQL_ATTR_CONCURRENCY = self.SQL_CONCURRENCY
        self.SQL_ATTR_CURSOR_TYPE = self.SQL_CURSOR_TYPE
        self.SQL_ATTR_ENABLE_AUTO_IPD = 15
        self.SQL_ATTR_FETCH_BOOKMARK_PTR = 16
        self.SQL_ATTR_KEYSET_SIZE = self.SQL_KEYSET_SIZE
        self.SQL_ATTR_MAX_LENGTH = self.SQL_MAX_LENGTH
        self.SQL_ATTR_MAX_ROWS = self.SQL_MAX_ROWS
        self.SQL_ATTR_NOSCAN = self.SQL_NOSCAN
        self.SQL_ATTR_PARAM_BIND_OFFSET_PTR = 17
        self.SQL_ATTR_PARAM_BIND_TYPE = 18
        self.SQL_ATTR_PARAM_OPERATION_PTR = 19
        self.SQL_ATTR_PARAM_STATUS_PTR = 20
        self.SQL_ATTR_PARAMS_PROCESSED_PTR = 21
        self.SQL_ATTR_PARAMSET_SIZE = 22
        self.SQL_ATTR_QUERY_TIMEOUT = self.SQL_QUERY_TIMEOUT
        self.SQL_ATTR_RETRIEVE_DATA = self.SQL_RETRIEVE_DATA
        self.SQL_ATTR_ROW_BIND_OFFSET_PTR = 23
        self.SQL_ATTR_ROW_BIND_TYPE = self.SQL_BIND_TYPE
        self.SQL_ATTR_ROW_NUMBER = self.SQL_ROW_NUMBER
        self.SQL_ATTR_ROW_OPERATION_PTR = 24
        self.SQL_ATTR_ROW_STATUS_PTR = 25
        self.SQL_ATTR_ROWS_FETCHED_PTR = 26
        self.SQL_ATTR_ROW_ARRAY_SIZE = 27
        self.SQL_ATTR_SIMULATE_CURSOR = self.SQL_SIMULATE_CURSOR
        self.SQL_ATTR_USE_BOOKMARKS = self.SQL_USE_BOOKMARKS

        self.SQL_STMT_OPT_MAX = self.SQL_ROW_NUMBER
        self.SQL_STMT_OPT_MIN = self.SQL_QUERY_TIMEOUT

        ################################################################################
        ####SQLGetStmtAttr - SQL_ATTR_ASYNC_ENABLE######################################
        ################################################################################
        self.SQL_ASYNC_ENABLE_OFF = 0
        self.SQL_ASYNC_ENABLE_ON = 1
        self.SQL_ASYNC_ENABLE_DEFAULT = self.SQL_ASYNC_ENABLE_OFF

        ################################################################################
        ####SQLGetStmtAttr - SQL_ATTR_PARAM_BIND_TYPE###################################
        ################################################################################
        self.SQL_PARAM_BIND_BY_COLUMN = 0
        self.SQL_PARAM_BIND_TYPE_DEFAULT = self.SQL_PARAM_BIND_BY_COLUMN

        ################################################################################
        ####SQLGetStmtAttr - SQL_BIND_TYPE##############################################
        ################################################################################
        self.SQL_BIND_BY_COLUMN = 0
        self.SQL_BIND_TYPE_DEFAULT = self.SQL_BIND_BY_COLUMN

        ################################################################################
        ####SQLGetStmtAttr - SQL_CONCURRENCY############################################
        ################################################################################
        self.SQL_CONCUR_READ_ONLY = 1
        self.SQL_CONCUR_LOCK = 2
        self.SQL_CONCUR_ROWVER = 3
        self.SQL_CONCUR_VALUES = 4
        self.SQL_CONCUR_DEFAULT = self.SQL_CONCUR_READ_ONLY

        ################################################################################
        ####SQLGetStmtAttr - SQL_CURSOR_TYPE############################################
        ################################################################################
        self.SQL_CURSOR_FORWARD_ONLY = 0
        self.SQL_CURSOR_KEYSET_DRIVEN = 1
        self.SQL_CURSOR_DYNAMIC = 2
        self.SQL_CURSOR_STATIC = 3
        self.SQL_CURSOR_TYPE_DEFAULT = self.SQL_CURSOR_FORWARD_ONLY

        ################################################################################
        ####SQLGetStmtAttr - SQL_KEYSET_SIZE############################################
        ################################################################################
        self.SQL_KEYSET_SIZE_DEFAULT = 0

        ################################################################################
        ####SQLGetStmtAttr - SQL_MAX_LENGTH#############################################
        ################################################################################
        self.SQL_MAX_LENGTH_DEFAULT = 0

        ################################################################################
        ####SQLGetStmtAttr - SQL_MAX_ROWS###############################################
        ################################################################################
        self.SQL_MAX_ROWS_DEFAULT = 0

        ################################################################################
        ####SQLGetStmtAttr - SQL_NOSCAN#################################################
        ################################################################################
        self.SQL_NOSCAN_OFF = 0
        self.SQL_NOSCAN_ON = 1
        self.SQL_NOSCAN_DEFAULT = self.SQL_NOSCAN_OFF

        ################################################################################
        ####SQLGetStmtAttr - SQL_QUERY_TIMEOUT##########################################
        ################################################################################
        self.SQL_QUERY_TIMEOUT_DEFAULT = 0

        ################################################################################
        ####SQLGetStmtAttr - SQL_RETRIEVE_DATA##########################################
        ################################################################################
        self.SQL_RD_OFF = 0
        self.SQL_RD_ON = 1
        self.SQL_RD_DEFAULT = self.SQL_RD_ON

        ################################################################################
        ####SQLGetStmtAttr - SQL_ROWSET_SIZE############################################
        ################################################################################
        self.SQL_ROWSET_SIZE_DEFAULT = 1

        ################################################################################
        ####SQLGetStmtAttr - SQL_SIMULATE_CURSOR########################################
        ################################################################################
        self.SQL_SC_NON_UNIQUE = 0
        self.SQL_SC_TRY_UNIQUE = 1
        self.SQL_SC_UNIQUE = 2

        ################################################################################
        ####SQLGetStmtAttr - SQL_USE_BOOKMARKS##########################################
        ################################################################################
        self.SQL_UB_OFF = 0
        self.SQL_UB_ON = 1
        self.SQL_UB_DEFAULT = self.SQL_UB_OFF
        self.SQL_UB_FIXED = self.SQL_UB_ON
        self.SQL_UB_VARIABLE = 2

        ################################################################################
        ####SQLGetTypeInfo - SEARCHABLE#################################################
        ################################################################################
        self.SQL_COL_PRED_CHAR = self.SQL_LIKE_ONLY
        self.SQL_COL_PRED_BASIC = self.SQL_ALL_EXCEPT_LIKE

        ################################################################################
        ####SQLSetPos###################################################################
        ################################################################################
        self.SQL_ENTIRE_ROWSET = 0

        ################################################################################
        ####SQLSetPos - Operation#######################################################
        ################################################################################
        self.SQL_POSITION = 0
        self.SQL_REFRESH = 1
        self.SQL_UPDATE = 2
        self.SQL_DELETE = 3

        ################################################################################
        ####SQLBulkOperations - Operation###############################################
        ################################################################################
        self.SQL_ADD = 4
        self.SQL_SETPOS_MAX_OPTION_VALUE = self.SQL_ADD
        self.SQL_UPDATE_BY_BOOKMARK = 5
        self.SQL_DELETE_BY_BOOKMARK = 6
        self.SQL_FETCH_BY_BOOKMARK = 7

        ################################################################################
        ####SQLSetPos - LockType########################################################
        ################################################################################
        self.SQL_LOCK_NO_CHANGE = 0
        self.SQL_LOCK_EXCLUSIVE = 1
        self.SQL_LOCK_UNLOCK = 2
        self.SQL_SETPOS_MAX_LOCK_VALUE = self.SQL_LOCK_UNLOCK

        ################################################################################
        ####SQLSetPos macros############################################################
        ################################################################################
        #TODO: Map self.SQLSetPos macros
        self.SQL_POSITION_TO = self.UnimplementedSQLFunction
        self.SQL_LOCK_RECORD = self.UnimplementedSQLFunction
        self.SQL_REFRESH_RECORD = self.UnimplementedSQLFunction
        self.SQL_UPDATE_RECORD = self.UnimplementedSQLFunction
        self.SQL_DELETE_RECORD = self.UnimplementedSQLFunction
        self.SQL_ADD_RECORD = self.UnimplementedSQLFunction

        ################################################################################
        ####SQLSpecialColumns - Column types and scopes#################################
        ################################################################################
        self.SQL_BEST_ROWID = 1
        self.SQL_ROWVER = 2

        ################################################################################
        ####All the ODBC keywords#######################################################
        ################################################################################
        self.SQL_ODBC_KEYWORDS = ("ABSOLUTE,ACTION,ADA,ADD,ALL,ALLOCATE,ALTER,AND,ANY,ARE,AS,"
                                  "ASC,ASSERTION,AT,AUTHORIZATION,AVG,"
                                  "BEGIN,BETWEEN,BIT,BIT_LENGTH,BOTH,BY,CASCADE,CASCADED,CASE,CAST,CATALOG,"
                                  "CHAR,CHAR_LENGTH,CHARACTER,CHARACTER_LENGTH,CHECK,CLOSE,COALESCE,"
                                  "COLLATE,COLLATION,COLUMN,COMMIT,CONNECT,CONNECTION,CONSTRAINT,"
                                  "CONSTRAINTS,CONTINUE,CONVERT,CORRESPONDING,COUNT,CREATE,CROSS,CURRENT,"
                                  "CURRENT_DATE,CURRENT_TIME,CURRENT_TIMESTAMP,CURRENT_USER,CURSOR,"
                                  "DATE,DAY,DEALLOCATE,DEC,DECIMAL,DECLARE,DEFAULT,DEFERRABLE,"
                                  "DEFERRED,DELETE,DESC,DESCRIBE,DESCRIPTOR,DIAGNOSTICS,DISCONNECT,"
                                  "DISTINCT,DOMAIN,DOUBLE,DROP,"
                                  "ELSE,END,END-EXEC,ESCAPE,EXCEPT,EXCEPTION,EXEC,EXECUTE,"
                                  "EXISTS,EXTERNAL,EXTRACT,"
                                  "FALSE,FETCH,FIRST,FLOAT,FOR,FOREIGN,FORTRAN,FOUND,FROM,FULL,"
                                  "GET,GLOBAL,GO,GOTO,GRANT,GROUP,HAVING,HOUR,"
                                  "IDENTITY,IMMEDIATE,IN,INCLUDE,INDEX,INDICATOR,INITIALLY,INNER,"
                                  "INPUT,INSENSITIVE,INSERT,INT,INTEGER,INTERSECT,INTERVAL,INTO,IS,ISOLATION,"
                                  "JOIN,KEY,LANGUAGE,LAST,LEADING,LEFT,LEVEL,LIKE,LOCAL,LOWER,"
                                  "MATCH,MAX,MIN,MINUTE,MODULE,MONTH,"
                                  "NAMES,NATIONAL,NATURAL,NCHAR,NEXT,NO,NONE,NOT,NULL,NULLIF,NUMERIC,"
                                  "OCTET_LENGTH,OF,ON,ONLY,OPEN,OPTION,OR,ORDER,OUTER,OUTPUT,OVERLAPS,"
                                  "PAD,PARTIAL,PASCAL,PLI,POSITION,PRECISION,PREPARE,PRESERVE,"
                                  "PRIMARY,PRIOR,PRIVILEGES,PROCEDURE,PUBLIC,"
                                  "READ,REAL,REFERENCES,RELATIVE,RESTRICT,REVOKE,RIGHT,ROLLBACK,ROWS"
                                  "SCHEMA,SCROLL,SECOND,SECTION,SELECT,SESSION,SESSION_USER,SET,SIZE,"
                                  "SMALLINT,SOME,SPACE,SQL,SQLCA,SQLCODE,SQLERROR,SQLSTATE,SQLWARNING,"
                                  "SUBSTRING,SUM,SYSTEM_USER,"
                                  "TABLE,TEMPORARY,THEN,TIME,TIMESTAMP,TIMEZONE_HOUR,TIMEZONE_MINUTE,"
                                  "TO,TRAILING,TRANSACTION,TRANSLATE,TRANSLATION,TRIM,TRUE,"
                                  "UNION,UNIQUE,UNKNOWN,UPDATE,UPPER,USAGE,USER,USING,"
                                  "VALUE,VALUES,VARCHAR,VARYING,VIEW,WHEN,WHENEVER,WHERE,WITH,WORK,WRITE,"
                                  "YEAR,ZONE")

        ################################################################################
        ####Level 2 Functions###########################################################
        ################################################################################

        ################################################################################
        ####SQLExtendedFetch - fFetchType###############################################
        ################################################################################
        self.SQL_FETCH_BOOKMARK = 8

        ################################################################################
        ####SQLExtendedFetch - rgfRowStatus#############################################
        ################################################################################
        self.SQL_ROW_SUCCESS = 0
        self.SQL_ROW_DELETED = 1
        self.SQL_ROW_UPDATED = 2
        self.SQL_ROW_NOROW = 3
        self.SQL_ROW_ADDED = 4
        self.SQL_ROW_ERROR = 5
        self.SQL_ROW_SUCCESS_WITH_INFO = 6
        self.SQL_ROW_PROCEED = 0
        self.SQL_ROW_IGNORE = 1

        ################################################################################
        ####SQL_DESC_ARRAY_STATUS_PTR###################################################
        ################################################################################
        self.SQL_PARAM_SUCCESS = 0
        self.SQL_PARAM_SUCCESS_WITH_INFO = 6
        self.SQL_PARAM_ERROR = 5
        self.SQL_PARAM_UNUSED = 7
        self.SQL_PARAM_DIAG_UNAVAILABLE = 1

        self.SQL_PARAM_PROCEED = 0
        self.SQL_PARAM_IGNORE = 1

        ################################################################################
        ####SQLForeignKeys - UPDATE_RULE/DELETE_RULE####################################
        ################################################################################
        self.SQL_CASCADE = 0
        self.SQL_RESTRICT = 1
        self.SQL_SET_NULL = 2

        self.SQL_NO_ACTION = 3
        self.SQL_SET_DEFAULT = 4

        ################################################################################
        ####SQLForeignKeys - DEFERABILITY###############################################
        ################################################################################
        self.SQL_INITIALLY_DEFERRED = 5
        self.SQL_INITIALLY_IMMEDIATE = 6
        self.SQL_NOT_DEFERRABLE = 7

        ################################################################################
        ####SQLBindParameter - fParamType###############################################
        ####SQLProcedureColumns - COLUMN_TYPE###########################################
        ################################################################################
        self.SQL_PARAM_TYPE_UNKNOWN = 0
        self.SQL_PARAM_INPUT = 1
        self.SQL_PARAM_INPUT_OUTPUT = 2
        self.SQL_RESULT_COL = 3
        self.SQL_PARAM_OUTPUT = 4
        self.SQL_RETURN_VALUE = 5

        ################################################################################
        #### SQLProcedures - PROCEDURE_TYPE#############################################
        ################################################################################
        self.SQL_PT_UNKNOWN = 0
        self.SQL_PT_PROCEDURE = 1
        self.SQL_PT_FUNCTION = 2

        ################################################################################
        ####SQLSetParam to SQLBindParameter conversion##################################
        ################################################################################
        self.SQL_PARAM_TYPE_DEFAULT = self.SQL_PARAM_INPUT_OUTPUT
        self.SQL_SETPARAM_VALUE_MAX = -1

        ################################################################################
        ####SQLStatistics - fAccuracy###################################################
        ################################################################################
        self.SQL_QUICK = 0
        self.SQL_ENSURE = 1

        ################################################################################
        ####SQLStatistics - TYPE########################################################
        ################################################################################
        self.SQL_TABLE_STAT = 0

        ################################################################################
        ####SQLTables###################################################################
        ################################################################################
        self.SQL_ALL_CATALOGS = "%"
        self.SQL_ALL_SCHEMAS = "%"
        self.SQL_ALL_TABLE_TYPES = "%"

        ################################################################################
        ####SQLSpecialColumns - PSEUDO_COLUMN###########################################
        ################################################################################
        self.SQL_PC_NOT_PSEUDO = 1

        ################################################################################
        ####Deprecated defines from prior versions of ODBC##############################
        ################################################################################
        self.SQL_DATABASE_NAME = 16
        self.SQL_FD_FETCH_PREV = self.SQL_FD_FETCH_PRIOR
        self.SQL_FETCH_PREV = self.SQL_FETCH_PRIOR
        self.SQL_CONCUR_TIMESTAMP = self.SQL_CONCUR_ROWVER
        self.SQL_SCCO_OPT_TIMESTAMP = self.SQL_SCCO_OPT_ROWVER
        self.SQL_CC_DELETE = self.SQL_CB_DELETE
        self.SQL_CR_DELETE = self.SQL_CB_DELETE
        self.SQL_CC_CLOSE = self.SQL_CB_CLOSE
        self.SQL_CR_CLOSE = self.SQL_CB_CLOSE
        self.SQL_CC_PRESERVE = self.SQL_CB_PRESERVE
        self.SQL_CR_PRESERVE = self.SQL_CB_PRESERVE
        self.SQL_FETCH_RESUME = 7
        self.SQL_SCROLL_FORWARD_ONLY = 0
        self.SQL_SCROLL_KEYSET_DRIVEN = -1
        self.SQL_SCROLL_DYNAMIC = -2
        self.SQL_SCROLL_STATIC = -3

        ################################################################################
        ####Level 1 function prototypes#################################################
        ################################################################################
        if hasattr(self.ODBC_DRIVER, "SQLDriverConnect"):
            self.ODBC_DRIVER.SQLDriverConnect.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDriverConnect.argtypes = (self.SQLHDBC, self.SQLHWND, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), self.SQLUSMALLINT,)
            self.SQLDriverConnect = self.ODBC_DRIVER.SQLDriverConnect
        else:
            self.SQLDriverConnect = self.UnimplementedSQLFunction

        ################################################################################
        ####Level 2 function prototypes#################################################
        ################################################################################
        if hasattr(self.ODBC_DRIVER, "SQLBrowseConnect"):
            self.ODBC_DRIVER.SQLBrowseConnect.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLBrowseConnect.argtypes = (self.SQLHDBC, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLBrowseConnect = self.ODBC_DRIVER.SQLBrowseConnect
        else:
            self.SQLBrowseConnect = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLBulkOperations"):
            self.ODBC_DRIVER.SQLBulkOperations.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLBulkOperations.argtypes = (self.SQLHSTMT, self.SQLSMALLINT,)
            self.SQLBulkOperations = self.ODBC_DRIVER.SQLBulkOperations
        else:
            self.SQLBulkOperations = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLColAttributes"):
            self.ODBC_DRIVER.SQLColAttributes.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLColAttributes.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLUSMALLINT, self.SQLPOINTER, self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLLEN),)
            self.SQLColAttributes = self.ODBC_DRIVER.SQLColAttributes
        else:
            self.SQLColAttributes = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLColumnPrivileges"):
            self.ODBC_DRIVER.SQLColumnPrivileges.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLColumnPrivileges.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLColumnPrivileges = self.ODBC_DRIVER.SQLColumnPrivileges
        else:
            self.SQLColumnPrivileges = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDescribeParam"):
            self.ODBC_DRIVER.SQLDescribeParam.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDescribeParam.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLULEN), ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLDescribeParam = self.ODBC_DRIVER.SQLDescribeParam
        else:
            self.SQLDescribeParam = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLExtendedFetch"):
            self.ODBC_DRIVER.SQLExtendedFetch.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLExtendedFetch.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLLEN, ctypes.POINTER(self.SQLULEN), ctypes.POINTER(self.SQLUSMALLINT),)
            self.SQLExtendedFetch = self.ODBC_DRIVER.SQLExtendedFetch
        else:
            self.SQLExtendedFetch = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLForeignKeys"):
            self.ODBC_DRIVER.SQLForeignKeys.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLForeignKeys.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLForeignKeys = self.ODBC_DRIVER.SQLForeignKeys
        else:
            self.SQLForeignKeys = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLMoreResults"):
            self.ODBC_DRIVER.SQLMoreResults.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLMoreResults.argtypes = (self.SQLHSTMT,)
            self.SQLMoreResults = self.ODBC_DRIVER.SQLMoreResults
        else:
            self.SQLMoreResults = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLNativeSql"):
            self.ODBC_DRIVER.SQLNativeSql.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLNativeSql.argtypes = (self.SQLHDBC, ctypes.POINTER(self.SQLCHAR), self.SQLINTEGER, ctypes.POINTER(self.SQLCHAR), self.SQLINTEGER, ctypes.POINTER(self.SQLINTEGER),)
            self.SQLNativeSql = self.ODBC_DRIVER.SQLNativeSql
        else:
            self.SQLNativeSql = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLNumParams"):
            self.ODBC_DRIVER.SQLNumParams.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLNumParams.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLNumParams = self.ODBC_DRIVER.SQLNumParams
        else:
            self.SQLNumParams = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLParamOptions"):
            self.ODBC_DRIVER.SQLParamOptions.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLParamOptions.argtypes = (self.SQLHSTMT, self.SQLULEN, ctypes.POINTER(self.SQLULEN),)
            self.SQLParamOptions = self.ODBC_DRIVER.SQLParamOptions
        else:
            self.SQLParamOptions = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLPrimaryKeys"):
            self.ODBC_DRIVER.SQLPrimaryKeys.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLPrimaryKeys.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLPrimaryKeys = self.ODBC_DRIVER.SQLPrimaryKeys
        else:
            self.SQLPrimaryKeys = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLProcedureColumns"):
            self.ODBC_DRIVER.SQLProcedureColumns.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLProcedureColumns.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLProcedureColumns = self.ODBC_DRIVER.SQLProcedureColumns
        else:
            self.SQLProcedureColumns = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLProcedures"):
            self.ODBC_DRIVER.SQLProcedures.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLProcedures.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLProcedures = self.ODBC_DRIVER.SQLProcedures
        else:
            self.SQLProcedures = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLSetPos"):
            self.ODBC_DRIVER.SQLSetPos.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetPos.argtypes = (self.SQLHSTMT, self.SQLSETPOSIROW, self.SQLUSMALLINT, self.SQLUSMALLINT,)
            self.SQLSetPos = self.ODBC_DRIVER.SQLSetPos
        else:
            self.SQLSetPos = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLTablePrivileges"):
            self.ODBC_DRIVER.SQLTablePrivileges.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLTablePrivileges.argtypes = (self.SQLHSTMT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT,)
            self.SQLTablePrivileges = self.ODBC_DRIVER.SQLTablePrivileges
        else:
            self.SQLTablePrivileges = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLDrivers"):
            self.ODBC_DRIVER.SQLDrivers.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLDrivers.argtypes = (self.SQLHENV, self.SQLUSMALLINT, ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT), ctypes.POINTER(self.SQLCHAR), self.SQLSMALLINT, ctypes.POINTER(self.SQLSMALLINT),)
            self.SQLDrivers = self.ODBC_DRIVER.SQLDrivers
        else:
            self.SQLDrivers = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLBindParameter"):
            self.ODBC_DRIVER.SQLBindParameter.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLBindParameter.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLSMALLINT, self.SQLULEN, self.SQLSMALLINT, self.SQLPOINTER, self.SQLLEN, ctypes.POINTER(self.SQLLEN),)
            self.SQLBindParameter = self.ODBC_DRIVER.SQLBindParameter
        else:
            self.SQLBindParameter = self.UnimplementedSQLFunction

        ################################################################################
        ####Depreciated function prototypes#############################################
        ################################################################################
        if hasattr(self.ODBC_DRIVER, "SQLSetScrollOptions"):
            self.ODBC_DRIVER.SQLSetScrollOptions.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLSetScrollOptions.argtypes = (self.SQLHSTMT, self.SQLUSMALLINT, self.SQLLEN, self.SQLUSMALLINT,)
            self.SQLSetScrollOptions = self.ODBC_DRIVER.SQLSetScrollOptions
        else:
            self.SQLSetScrollOptions = self.UnimplementedSQLFunction

        if hasattr(self.ODBC_DRIVER, "SQLAllocHandleStd"):
            self.ODBC_DRIVER.SQLAllocHandleStd.restype = self.SQLRETURN
            self.ODBC_DRIVER.SQLAllocHandleStd.argtypes = (self.SQLSMALLINT, self.SQLHANDLE, ctypes.POINTER(self.SQLHANDLE),)
            self.SQLAllocHandleStd = self.ODBC_DRIVER.SQLAllocHandleStd
        else:
            self.SQLAllocHandleStd = self.UnimplementedSQLFunction

        ################################################################################
        ####Internal type subcodes######################################################
        ################################################################################
        self.SQL_YEAR = self.SQL_CODE_YEAR
        self.SQL_MONTH = self.SQL_CODE_MONTH
        self.SQL_DAY = self.SQL_CODE_DAY
        self.SQL_HOUR = self.SQL_CODE_HOUR
        self.SQL_MINUTE = self.SQL_CODE_MINUTE
        self.SQL_SECOND = self.SQL_CODE_SECOND
        self.SQL_YEAR_TO_MONTH = self.SQL_CODE_YEAR_TO_MONTH
        self.SQL_DAY_TO_HOUR = self.SQL_CODE_DAY_TO_HOUR
        self.SQL_DAY_TO_MINUTE = self.SQL_CODE_DAY_TO_MINUTE
        self.SQL_DAY_TO_SECOND = self.SQL_CODE_DAY_TO_SECOND
        self.SQL_HOUR_TO_MINUTE = self.SQL_CODE_HOUR_TO_MINUTE
        self.SQL_HOUR_TO_SECOND = self.SQL_CODE_HOUR_TO_SECOND
        self.SQL_MINUTE_TO_SECOND = self.SQL_CODE_MINUTE_TO_SECOND

