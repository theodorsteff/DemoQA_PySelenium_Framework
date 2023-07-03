# -*- coding: utf-8 -*-
#
# Demo Project: Selenium testing framework implementation with Python
# Showcase implementation by: Theodor-Stefan Baca
# Version 1.0
#

"""
Description:
This module reads the configuration data and returns the data sets
used for multiple executions of a single test.
"""

import sqlite3


class DemoPageData:
    """
    Class definition to handle data sets for multiple text executions.
    """

    @staticmethod
    def get_test_data(database_path):
        """
        Static method used to read the config file and the data sets.

        :return: (list) List of tuples consisting of the data sets.
        """
        demopage_db = sqlite3.connect(database_path)
        cursor_object = demopage_db.cursor()
        testcase_name = cursor_object.execute(f"SELECT * FROM repetitive_tests").fetchall()[0][0]
        data_sets = cursor_object.execute(f"SELECT * FROM {testcase_name}").fetchall()
        demopage_db.close()
        return data_sets
