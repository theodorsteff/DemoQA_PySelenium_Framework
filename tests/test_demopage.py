# -*- coding: utf-8 -*-
#
# Demo Project: Selenium testing framework implementation with Python
# Showcase implementation by: Theodor-Stefan Baca
#

"""
Description:
This module defines the class for the testcases to be executed.
"""

import logging
import time
import pytest

from testdata.demopage_data import DemoPageData
from pageobjects.demopage import DemoPage
from utilities.baseclass import BaseClass


def verify_text_in_all_items(demopage_obj, text_item, logger):
    """
    Local method used to verify that a specific text is present in
    all specified page objects.

    :param demopage_obj: the demopage class used to execute page operations
    :param text_item: the required text to be found in the specified objects
    :param logger: object for the test logger
    :return: (bool) verification result
    """
    required_texts = (
        demopage_obj.read_button(),
        demopage_obj.read_only_field(),
        demopage_obj.read_paragraph(),
    )
    logger.info(
        f"Button text: {required_texts[0]}, "
        f"Read only field text: {required_texts[1]}, "
        f"Paragraph text: {required_texts[2]}"
    )
    return all(text_item in text_elem for text_elem in required_texts)


def verify_displayed_progress_value(demopage, log, expected_value):
    detected_progress_value = demopage.read_progress_bar_value()
    expected_progress_value = expected_value
    log_msg = f"Detected value: {detected_progress_value}, expecting value: {expected_progress_value}"
    log.info(log_msg)
    return detected_progress_value == expected_progress_value


class TestDemoPage(BaseClass):
    """
    Class definition for the demo page tests.
    """

    def test_color_change_demo(self, get_data):
        """
        Test case used to verify the color changing functionality.

        :param get_data: data sets used for multiple executions
        """

        # Instantiate the logger and the DemoPage
        log = self.get_logger()
        log.info(f"Received data is: {get_data}")
        demopage = DemoPage(self.driver)

        # Set up the test data
        color_name, text_input, pre_filled_input, color_to_change = (
            get_data["color"],
            get_data["text_input"],
            get_data["pre_filled_input"],
            get_data["color_to_change"],
        )

        # Execute the text inject operations
        demopage.inject_text_input_field(f"{text_input}: for {color_name}")
        demopage.inject_text_pre_filled_field(pre_filled_input)
        if color_to_change:
            placeholder_input = "Color change will execute"
        else:
            placeholder_input = "Color change will skip"
        placeholder_text = demopage.inject_text_placeholder_field(placeholder_input)
        demopage.inject_text_area(f"{text_input}: {color_name}\n{pre_filled_input}")

        # Log the initial and the new placeholder text
        log.info(
            f"Initial placeholder text: {placeholder_text}, "
            f"New placeholder text: {placeholder_input}"
        )

        # If the debug_showcase flag is True, sleep for a few seconds
        if demopage.get_debug_showcase():
            time.sleep(2)

        # If the text in the "Button", "Read-Only Text Field"
        # and "Paragraph with Text" differs, click on "Button"
        if not verify_text_in_all_items(demopage, color_name, log):
            demopage.click_button()

        # If the text is still not matching in all the above fields,
        # assert the failure and log the error
        assert verify_text_in_all_items(demopage, color_name, log) is True, log.error(
            f"Failed to successfully change the color to {color_name}"
        )

        # If the debug_showcase flag is True, sleep for a few seconds
        if demopage.get_debug_showcase():
            time.sleep(3)

    def test_hover_select_by_text(self):
        """
        Test case used to verify the hover menu functionality.
        """

        # Instantiate the logger and the DemoPage
        log = self.get_logger()
        demopage = DemoPage(self.driver)

        # Hover on the menu and click on the required option
        selected_text = demopage.hover_click_option()

        # Read the page dynamic subhead
        dynamic_subhead = demopage.read_dynamic_subhead()

        # Log the selected hovering option and the subhead title
        log.info(
            f"Selected Option text: {selected_text}, Dynamic subhead title: {dynamic_subhead}"
        )

        # If the selected hovering option text is not found in the
        # subhead title, assert the failure and log the error
        assert selected_text in dynamic_subhead, log.error(
            f"Failed to successfully detext {selected_text} in {dynamic_subhead}"
        )

        # If the logging level is set to DEBUG, sleep for a few seconds
        if log.level == logging.DEBUG:
            time.sleep(3)

    @pytest.mark.xfail
    def test_drag_and_drop(self):
        """
        Test case used to verify the functionality of the CheckBox
        (revealing of the "Drag and Drop" fields on the page) and the
        "Drag and Drop" operation.
        (NOTE) Known issue: Java handler implementation required for this operation
        """

        # Instantiate the logger and the DemoPage
        log = self.get_logger()
        demopage = DemoPage(self.driver)

        # Click on the checkbox
        demopage.click_checkbox()

        # Verify the drag and drop result and assert an error if the operation fails
        verif_response, verif_msg = demopage.drag_and_drop_picture()
        log.info(verif_msg)
        if log.level == logging.DEBUG:
            time.sleep(3)
        assert verif_response is True, log.error(
            f"Response: {verif_msg}; Known Issue: Java handler implementation required for this operation"
        )

    def test_iframe_switch(self):
        """
        Test case used to verify the functionality of
        switching to another frame.
        """

        # Instantiate the logger and the DemoPage
        log = self.get_logger()
        demopage = DemoPage(self.driver)

        # Switch to the iFrame, read the body text and
        # assert if operation fails
        verification_response, verification_msg = demopage.switch_to_iframes()
        log.info(verification_msg)
        if log.level == logging.DEBUG:
            time.sleep(3)
        assert verification_response is True, log.error(verification_msg)

    def test_input_slider_control(self):
        """
        Test case used to verify the functionality of
        the input slider control.
        """

        # Instantiate the logger and the DemoPage
        log = self.get_logger()
        demopage = DemoPage(self.driver)

        # Retrieve the progress bar data
        progress_bar_data = demopage.get_progress_bar_data()
        expected_progress_value = progress_bar_data["start_progress_value"]
        progress_registered = verify_displayed_progress_value(
            demopage, log, expected_progress_value
        )
        assert progress_registered is True, log.error(
            f"Progress not correctly registered"
        )

        # Move the input slider control 
        demopage.move_slider_control()
        if log.level == logging.DEBUG:
            time.sleep(3)

        # Retrieve the progress bar data
        expected_progress_value = progress_bar_data["end_progress_value"]
        progress_registered = verify_displayed_progress_value(
            demopage, log, expected_progress_value
        )

        # If the registered progress value is not correct,
        # assert and log an error
        assert progress_registered is True, log.error(
            f"Progress not correctly registered"
        )

    @pytest.fixture(params=DemoPageData.get_test_data())
    def get_data(self, request):
        """
        Method used to retrieve test data to be used for multiple
        test executions.

        :param request: structure used by pytest to parse the data
        :return: parameters to be used for the multiple executions.
        """
        return request.param
