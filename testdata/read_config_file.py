# -*- coding: utf-8 -*-
#
# Demo Project: Selenium testing framework implementation with Python
# Showcase implementation by: Theodor-Stefan Baca
#

"""
Description:
This module reads and returns the configuration data
(e.g.: data sets, debug_showcase flag, Selenium locators for page objects)
"""

import json


class ReadConfigFiles:
    """
    Class definition for reading the configuration files.
    """

    def __init__(self):
        """
        Constructor reading the configuration file data and
        initialization of the data_structure member.
        """
        with open("..\\testdata\\demopage_data.json", "r") as data_file:
            data_structure = json.loads(data_file.read())
        self.data_structure = data_structure

    def get_debug_showcase(self):
        """
        Method used to retrieve the debug_showcase flag value.

        :return: (bool) debug_showcase value.
        """
        return self.data_structure["debug_showcase"]

    def get_demopage_url(self):
        """
        Method used to retrieve the demopage URL

        :return: (str) URL of the demopage
        """
        return self.data_structure["demopage_url"]

    def get_test_data_sets(self):
        """
        Method used to retrieve the data sets to be used for
        multiple test executions.

        :return: (dict) the data sets.
        """
        return {
            "testcase_name": self.data_structure["testcase_name"],
            "data_sets": self.data_structure["data_sets"],
        }

    def get_locators(self):
        """
        Method used to retrieve the locators for various page objects.

        :return: (dict) the data for the Selenium locators.
        """
        return self.data_structure["locators"]
