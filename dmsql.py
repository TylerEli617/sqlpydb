#!/usr/bin/env python3

import sys

import sql

DM_ODBC_DRIVER = sql.Driver(sql.DM_ODBC_NAME)

for sql_attribute in dir(DM_ODBC_DRIVER):
    if not sql_attribute.startswith("_"):
        setattr(sys.modules[__name__], sql_attribute, getattr(DM_ODBC_DRIVER, sql_attribute))
