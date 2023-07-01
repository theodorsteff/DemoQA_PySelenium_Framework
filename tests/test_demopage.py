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

    # Read the required text from the screen
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

    # Verify that the text item exists in all the required texts
    return all(text_item in text_elem for text_elem in required_texts)


def verify_displayed_progress_value(
    demopage_obj, log, object_type, expected_progress_value
):
    """
    Local method used to verify that the progress value is correctly displayed

    :param demopage_obj: the demopage class used to execute page operations
    :param log: the logging object used to log the messages
    :param object_type: (str) label for the type of value to be verified
    :param expected_progress_value: (str) text containing the expected value
    :return: (bool) verification result
    """

    # Read the displayed progress value
    if object_type == "slider":
        detected_label_value = demopage_obj.read_progress_label_value()
        detected_bar_value = demopage_obj.read_progress_bar_value()
        detected_progress_value = (detected_label_value, detected_bar_value)
    else:
        detected_option = demopage_obj.read_selected_option()
        detected_label_value = demopage_obj.read_meter_label_value()
        detected_meter_value = demopage_obj.read_meter_bar_value()
        detected_progress_value = (
            detected_option,
            detected_label_value,
            detected_meter_value,
        )
    log_msg = f"Detected value: {detected_progress_value}, expecting value: {expected_progress_value}"
    log.info(log_msg)

    # Verify that the detected and expected values match
    return detected_progress_value == expected_progress_value


def verify_button_selection_values(
    demopage_obj, log, expected_button_values, radio_button
):
    """
    Method used to verify the selection values for a radio button

    :param demopage_obj: the demopage class used to execute page operations
    :param log: the logging object used to log the messages
    :param expected_button_values: the expected selection values for the radio button
    :param radio_button: the radio button for which the verification is done
    :return: (bool) verification result
    """

    # Retrieve the detected button selection values
    detected_button_values = demopage_obj.verify_radio_button_selected(radio_button)
    log.info(
        f"Detected button {radio_button['locator_hook']} selection values = (displayed: {detected_button_values[0]}, "
        f"enabled: {detected_button_values[1]}, selected: {detected_button_values[2]})"
    )
    return detected_button_values == expected_button_values


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
        assert verif_response is True, log.error(f"Wrong response: {verif_msg}")

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

        # Retrieve the initial progress label and bar valus=es
        object_data = demopage.get_slider_data()
        object_type = object_data["object_type"]
        progress_label_data = demopage.get_progress_label_data()
        expected_label_value = progress_label_data["start_progress_value"]
        progress_bar_data = demopage.get_progress_bar_data()
        expected_bar_value = progress_bar_data["start_progress_value"]

        # Verify that the initial values are correctly registered
        expected_value = (expected_label_value, expected_bar_value)
        progress_registered = verify_displayed_progress_value(
            demopage, log, object_type, expected_value
        )

        # If the registered progress value is not correct,
        # assert and log an error
        assert progress_registered is True, log.error(
            "Progress not correctly registered"
        )

        # Move the input slider control
        demopage.move_slider_control()

        # If the logging level is set to DEBUG, sleep for a few seconds
        if log.level == logging.DEBUG:
            time.sleep(3)

        # Retrieve the final progress label and bar values
        expected_label_value = progress_label_data["end_progress_value"]
        expected_bar_value = progress_bar_data["end_progress_value"]

        # Verify that the final values are correctly registered
        expected_value = (expected_label_value, expected_bar_value)
        progress_registered = verify_displayed_progress_value(
            demopage, log, object_type, expected_value
        )

        # If the registered progress value is not correct,
        # assert and log an error
        assert progress_registered is True, log.error(
            "Progress not correctly registered"
        )

    def test_select_dropdown_by_partial_text(self):
        """
        Test case used to verify the select dropdown menu functionality.
        """

        # Instantiate the logger and the DemoPage
        log = self.get_logger()
        demopage = DemoPage(self.driver)

        # Read the dropdown menu data and displayed selected option
        object_data = demopage.get_select_dropdown_data()
        object_type = object_data["object_type"]
        expected_dropdown_option = object_data["start_progress_value"]

        # Retrieve the initial meter label and bar values
        meter_label_data = demopage.get_meter_label_data()
        expected_label_value = meter_label_data["start_progress_value"]
        meter_bar_data = demopage.get_meter_bar_data()
        expected_bar_value = meter_bar_data["start_progress_value"]

        # Verify that the initial option and values are correctly registered
        expected_value = (
            expected_dropdown_option,
            expected_label_value,
            expected_bar_value,
        )
        progress_registered = verify_displayed_progress_value(
            demopage, log, object_type, expected_value
        )

        # If the registered progress value is not correct,
        # assert and log an error
        assert progress_registered is True, log.error(
            "Progress not correctly registered"
        )

        # If the logging level is set to DEBUG, sleep for a few seconds
        if log.level == logging.DEBUG:
            time.sleep(3)

        # Click on the select menu and choose on the required option
        selected_option = demopage.select_click_option()

        # If the logging level is set to DEBUG, sleep for a few seconds
        if log.level == logging.DEBUG:
            time.sleep(3)

        # Log the selected hovering option and the subhead title
        log.info(f"Selected Option value: {selected_option}")

        # Retrieve the final progress label and bar values
        expected_dropdown_option = object_data["end_progress_value"]
        expected_label_value = meter_label_data["end_progress_value"]
        expected_bar_value = meter_bar_data["end_progress_value"]

        # Verify that the final values are correctly registered
        expected_value = (
            expected_dropdown_option,
            expected_label_value,
            expected_bar_value,
        )
        progress_registered = verify_displayed_progress_value(
            demopage, log, object_type, expected_value
        )

        # If the registered progress value is not correct,
        # assert and log an error
        assert progress_registered is True, log.error(
            "Progress not correctly registered"
        )

    def test_html_svg_rectangle(self):
        """
        Test case used to verify the functionality of
        the HTML SVG rectangle responsiveness
        """

        # Instantiate the logger and the DemoPage
        log = self.get_logger()
        demopage = DemoPage(self.driver)

        # Retrieve the HTML SVG rectangle data
        html_svg_rect_data = demopage.get_html_svg_rect_data()
        max_width_px = float(html_svg_rect_data["max_width_px"].split("px")[0])
        log.info(f"Maximum HTML SVG rectangle width: {max_width_px}")

        # Wait 3s in order for the HTML SVG rectangle to reach max width
        time.sleep(3)
        html_svg_rect_width = float(demopage.read_html_svg_rect_width().split("px")[0])
        log.info(f"Initial HTML SVG rectangle width: {html_svg_rect_width}")
        assert html_svg_rect_width == max_width_px, log.error(
            f"HTML SVG failed to reach max width of {max_width_px}"
        )

        # Click the HTML SVG rectangle and verify its responsiveness by having its width changed
        demopage.click_html_svg_rect()
        html_svg_rect_width = float(demopage.read_html_svg_rect_width().split("px")[0])
        log.info(f"Modified HTML SVG rectangle width: {html_svg_rect_width}")
        assert html_svg_rect_width < max_width_px, log.error(
            "HTML SVG failed to change its width, responsiveness test failed"
        )

    def test_radio_button_selection(self):
        """
        Test case used to verify the radio button selection functionality.
        """

        # Instantiate the logger and the DemoPage
        log = self.get_logger()
        demopage = DemoPage(self.driver)

        # Retrieve the radio buttons data
        radio_button1 = demopage.get_radio_button1_data()
        radio_button2 = demopage.get_radio_button2_data()

        # Retrieve the initial expected button1 selection values
        expected_button1_values = (
            radio_button1["is_displayed"],
            radio_button1["is_enabled"],
            radio_button1["is_selected"],
        )
        radio_button_1_selected = verify_button_selection_values(
            demopage, log, expected_button1_values, radio_button1
        )
        assert radio_button_1_selected is True, log.error(
            f"Button {radio_button1['locator_hook']} selection expected: {expected_button1_values}"
        )

        # Retrieve the initial expected button2 selection values
        expected_button2_values = (
            radio_button2["is_displayed"],
            radio_button2["is_enabled"],
            radio_button2["is_selected"],
        )
        radio_button_2_deselected = verify_button_selection_values(
            demopage, log, expected_button2_values, radio_button2
        )
        assert radio_button_2_deselected is True, log.error(
            f"Button {radio_button2['locator_hook']} selection expected: {expected_button2_values}"
        )

        # If the logging level is set to DEBUG, sleep for a few seconds
        if log.level == logging.DEBUG:
            time.sleep(3)

        # Click on radio button2
        demopage.click_radio_button(radio_button2)

        # If the logging level is set to DEBUG, sleep for a few seconds
        if log.level == logging.DEBUG:
            time.sleep(3)

        # Retrieve the final expected button1 selection values
        expected_button1_values = (
            radio_button1["is_displayed"],
            radio_button1["is_enabled"],
            not radio_button1["is_selected"],
        )
        radio_button_1_deselected = verify_button_selection_values(
            demopage, log, expected_button1_values, radio_button1
        )
        assert radio_button_1_deselected is True, log.error(
            f"Button {radio_button1['locator_hook']} selection expected: {expected_button1_values}"
        )

        # Retrieve the initial expected button2 selection values
        expected_button2_values = (
            radio_button2["is_displayed"],
            radio_button2["is_enabled"],
            not radio_button2["is_selected"],
        )
        radio_button_2_selected = verify_button_selection_values(
            demopage, log, expected_button2_values, radio_button2
        )
        assert radio_button_2_selected is True, log.error(
            f"Button {radio_button2['locator_hook']} selection expected: {expected_button2_values}"
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
