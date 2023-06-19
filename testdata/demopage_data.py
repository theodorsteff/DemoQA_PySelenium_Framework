# -*- coding: utf-8 -*-
#
# Demo Project: Selenium testing framework implementation with Python
# Showcase implementation by: Theodor-Stefan Baca
#

"""
Description:
This module reads the configuration data and returns the data sets
used for multiple executions of a single test.
"""

from testdata.read_config_file import ReadConfigFiles


class DemoPageData:
    """
    Class definition to handle data sets for multiple text executions.
    """

    @staticmethod
    def get_test_data():
        """
        Static method used to read the config file and the data sets.

        :return: (list) List of dictionaries consisting of the data sets.
        """
        data_sets_reader = ReadConfigFiles()
        data_structure = data_sets_reader.get_test_data_sets()
        return data_structure["data_sets"]
