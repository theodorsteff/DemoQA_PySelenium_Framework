# -*- coding: utf-8 -*-
#
# Demo Project: Selenium testing framework implementation with Python
# Showcase implementation by: Theodor-Stefan Baca
# Version 1.0
#

"""
Description:
This module defines the base class for the testcases.
"""

import inspect
import logging
import pytest


@pytest.mark.usefixtures("setup")
class BaseClass:
    """
    Class definition for the base class, used to set up and retrieve the logger.
    """

    @staticmethod
    def get_logger():
        """
        Method used to set up the logger's name, filename, format
        and level of logging (DEBUG, INFO, WARNING, ERROR, etc.)

        :return: (obj) the logger object used to log information in the tests.
        """
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        file_handler = logging.FileHandler("logfile.log")
        formatter = logging.Formatter(
            "%(asctime)s :%(levelname)s : %(name)s :%(message)s"
        )
        file_handler.setFormatter(formatter)

        # filehandler object
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
        return logger
