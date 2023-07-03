# -*- coding: utf-8 -*-
#
# Demo Project: Selenium testing framework implementation with Python
# Showcase implementation by: Theodor-Stefan Baca
# Version 1.0
#

"""
Description:
This module defines the page objects and actions for the "demo page"
(e.g.: clicking a hovering menu, reading a text field, injecting
a string to a specific text box).
"""

import os
import sqlite3

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

database_path = "..\\testdata\\demopage_data.db"


class DemoPage:
    """
    Class definition for the demo page objects and actions.
    """

    def __init__(self, driver):
        """
        Constructor for the class, where the configuration file is read,
        the page objects are being initialized and the url is being opened.

        :param driver: (obj) the selenium driver to be used for accessing the URL
        """
        # Load the demopage_data database
        self.driver = driver
        self.driver.implicitly_wait(5)
        self.actions = ActionChains(self.driver)
        self.demopage_db = sqlite3.connect(database_path)
        self.cursor_object = self.demopage_db.cursor()
        query_result = self.cursor_object.execute("SELECT * FROM general").fetchone()
        self.demopage_url = query_result[0]
        self.debug_showcase = bool(query_result[1])
        self.local_demo_page = bool(query_result[2])

        # Load a local html file into the web browser
        if self.local_demo_page:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            par_path = os.path.abspath(os.path.join(dir_path, os.pardir))
            url_path = os.path.join(par_path, query_result[3])

        # Load a demo page into the web browser
        else:
            url_path = self.demopage_url
        self.driver.get(url_path)
        self.driver.maximize_window()

    def __del__(self):
        """
        De-constructor used to close the previously opened database
        """
        self.demopage_db.close()

    def retrieve_record_from_db(
        self, table_name, record_filter, record_name, field_name
    ):
        """
        Method used to retrieve record data from the sqlite database.

        :param table_name: (str) name of the table where the query has to be executed
        :param record_filter: (str) filter type to be used for finding the record
        :param record_name: (str) name of the record data to be found
        :param field_name: (str) name of the record's field to be retrieved
        :return: (obj) retrieved record data from the database
        """
        current_command = f"""
            SELECT {field_name} FROM {table_name} WHERE {record_filter}='{record_name}'
        """
        return self.cursor_object.execute(current_command)

    def __convert_record_to_dict__(self, query_data):
        keys_in_record = list()
        record_as_dict = dict()
        query_result = self.retrieve_record_from_db(*query_data)
        for column in query_result.description:
            keys_in_record.append(f"{column[0]}")
        query_result = self.retrieve_record_from_db(*query_data)
        record_data = query_result.fetchone()
        for key_index, key_name in enumerate(keys_in_record):
            record_as_dict[key_name] = record_data[key_index]
        return record_as_dict

    def get_debug_showcase(self):
        """
        Method used to return the debug showcase flag, used to display logging information.

        :return: (bool) debug_showcase member
        """
        return self.debug_showcase

    def __inject_text_in_box__(self, text_to_insert, box_in_focus):
        """
        Method used to inject text in a specific box on the screen.

        :param text_to_insert: (str) text string to be inserted
        :param box_in_focus: (dict) item of the box in focus
        """
        box_item = self.__locator_handler__(box_in_focus)
        if box_in_focus["clear_required"]:
            self.driver.find_element(*box_item).clear()
        self.driver.find_element(*box_item).send_keys(text_to_insert)

    def inject_text_input_field(self, text_to_insert):
        """
        Method used to inject text in the text input field box.

        :param text_to_insert: (str) text string to be inserted
        """
        query_data = ("text_fields", "name", "text_input_field", "*")
        text_input_field = self.__convert_record_to_dict__(query_data)
        self.__inject_text_in_box__(text_to_insert, text_input_field)

    def inject_text_pre_filled_field(self, text_to_insert):
        """
        Method used to inject text in the text input pre-filled box.

        :param text_to_insert: (str) text string to be inserted
        """
        query_data = ("text_fields", "name", "pre_filled_text_field", "*")
        pre_filled_text_field = self.__convert_record_to_dict__(query_data)
        self.__inject_text_in_box__(text_to_insert, pre_filled_text_field)

    def inject_text_placeholder_field(self, text_to_insert):
        """
        Method used to inject text in the text placeholder field box.

        :param text_to_insert: (str) text string to be inserted
        """
        query_data = ("text_fields", "name", "placeholder_text_field", "*")
        placeholder_text_field = self.__convert_record_to_dict__(query_data)
        placeholder_item = self.__locator_handler__(placeholder_text_field)
        placeholder_text = self.driver.find_element(*placeholder_item).get_property(
            "placeholder"
        )
        self.__inject_text_in_box__(text_to_insert, placeholder_text_field)
        return placeholder_text

    def inject_text_area(self, text_to_insert):
        """
        Method used to inject text in the text area box.

        :param text_to_insert: (str) text string to be inserted
        """
        query_data = ("text_fields", "name", "text_area", "*")
        text_area = self.__convert_record_to_dict__(query_data)
        self.__inject_text_in_box__(text_to_insert, text_area)

    def __read_item_text__(self, *readable_item):
        """
        Method used to read the text from a specific item.

        :param readable_item: (locator) Selenium locator for the item to be read
        :return text: (str) the text read from the box
        """
        return self.driver.find_element(*readable_item).text

    def read_dynamic_subhead(self):
        """
        Method used to read the text from the dynamic subhead of the page.
        """
        query_data = ("misc_items", "name", "dynamic_subhead", "*")
        dynamic_subhead = self.__convert_record_to_dict__(query_data)
        dynamic_subhead_item = self.__locator_handler__(dynamic_subhead)
        return self.__read_item_text__(*dynamic_subhead_item)

    def read_button(self):
        """
        Method used to read the text from the "Button" of the page.
        """
        query_data = ("misc_items", "name", "button", "*")
        button_elem = self.__convert_record_to_dict__(query_data)
        button_item = self.__locator_handler__(button_elem)
        return self.__read_item_text__(*button_item)

    def read_paragraph(self):
        """
        Method used to read the text from the paragraph of the page.
        """
        query_data = ("misc_items", "name", "paragraph_with_text", "*")
        paragraph_with_text = self.__convert_record_to_dict__(query_data)
        paragraph_item = self.__locator_handler__(paragraph_with_text)
        return self.__read_item_text__(*paragraph_item)

    def read_only_field(self):
        """
        Method used to read the text from the read only field of the page.

        :return text: the text value read from the read only field of the page.
        """
        query_data = ("misc_items", "name", "read_only_text_field", "*")
        read_only_text_field = self.__convert_record_to_dict__(query_data)
        read_only_item = self.__locator_handler__(read_only_text_field)
        return self.driver.find_element(*read_only_item).get_property("value")

    def hover_click_option(self):
        """
        Method used to click on a hovering menu option.

        :return: (str) The text for the hovering option selected.
        """
        query_data = ("misc_items", "name", "hover_dropdown", "*")
        hover_dropdown = self.__convert_record_to_dict__(query_data)
        hover_dropdown_item = self.__locator_handler__(hover_dropdown)
        self.actions.move_to_element(
            self.driver.find_element(*hover_dropdown_item)
        ).perform()
        query_data = ("misc_items", "name", "hover_option_text", "*")
        hover_option_text = self.__convert_record_to_dict__(query_data)
        hover_option_item = self.__locator_handler__(hover_option_text)
        self.actions.click(self.driver.find_element(*hover_option_item)).perform()
        return hover_option_text["locator_hook"]

    def get_select_dropdown_data(self):
        """
        Method used to retrieve the select dropdown data.

        :return: (dict) select dropdown data (locator, maximum width value)
        """
        query_data = ("slider_dropdown", "name", "select_dropdown", "*")
        return self.__convert_record_to_dict__(query_data)

    def __dropdown_select__(self):
        """
        Helper method used to select a dropdown menu.

        :return: (obj) the selected dropdown menu
        """
        query_data = ("slider_dropdown", "name", "select_dropdown", "*")
        select_dropdown = self.__convert_record_to_dict__(query_data)
        dropdown_element = self.__locator_handler__(select_dropdown)
        dropdown_item = self.driver.find_element(*dropdown_element)
        selected_dropdown = Select(dropdown_item)
        return selected_dropdown

    def select_click_option(self):
        """
        Method used to click on a select menu option.

        :return: (str) The text for the menu option selected.
        """
        query_data = ("bar_and_label_values", "name", "meter_label", "*")
        meter_label = self.__convert_record_to_dict__(query_data)
        option_to_select = meter_label["end_progress_value"]
        select_dropdown = self.__dropdown_select__()
        select_dropdown.select_by_value(option_to_select)
        return option_to_select

    def read_selected_option(self):
        """
        Method used to read the text from the selected menu option.

        :return: (str) the selected dropdown menu option text
        """
        select_dropdown = self.__dropdown_select__()
        return select_dropdown.first_selected_option.text

    def __click_item__(self, *clickable_item):
        """
        Method used to click on a clickable item from the page.

        :param clickable_item: (locator) Selenium locator for the clickable item.
        """
        self.driver.find_element(*clickable_item).click()

    def click_button(self):
        """
        Method used to click on the page's "Button".
        """
        query_data = ("misc_items", "name", "button", "*")
        button_elem = self.__convert_record_to_dict__(query_data)
        button_item = self.__locator_handler__(button_elem)
        self.__click_item__(*button_item)

    def click_checkbox(self):
        """
        Method used to click on the page's "CheckBox".
        """
        query_data = ("misc_items", "name", "checkbox", "*")
        checkbox_elem = self.__convert_record_to_dict__(query_data)
        checkbox_item = self.__locator_handler__(checkbox_elem)
        self.__click_item__(*checkbox_item)

    def click_html_svg_rect(self):
        """
        Method used to click on the HTML SVG rectangle.
        """
        query_data = ("html_svg_item", "name", "html_svg_rect", "*")
        html_svg_rect = self.__convert_record_to_dict__(query_data)
        html_svg_item = self.__locator_handler__(html_svg_rect)
        self.__click_item__(*html_svg_item)

    def get_html_svg_rect_data(self):
        """
        Method used to retrieve the HTML SVG rectangle data.

        :return: (dict) HTML SVG rectangle data (locator, maximum width value)
        """
        query_data = ("html_svg_item", "name", "html_svg_rect", "*")
        return self.__convert_record_to_dict__(query_data)

    def read_html_svg_rect_width(self):
        """
        Method used to read the width of the HTML SVG rectangle.

        :return: (str) HTML SVG rectangle width value
        """
        query_data = ("html_svg_item", "name", "html_svg_rect", "*")
        html_svg_rect = self.__convert_record_to_dict__(query_data)
        html_svg_rect_item = self.__locator_handler__(html_svg_rect)
        html_svg_rect_elem = self.driver.find_element(*html_svg_rect_item)
        return html_svg_rect_elem.value_of_css_property("width")

    def drag_and_drop_picture(self):
        """
        Method used to drag and drop an item on the page.
        :return: (bool, str) Verification that the draggable item is
        in the correct position
        """

        # Log messages list
        log_messages = list()

        # Read the locator hook for the element to be dragged
        query_data = ("misc_items", "name", "draggable_item", "*")
        draggable_data = self.__convert_record_to_dict__(query_data)
        draggable_item = self.__locator_handler__(draggable_data)

        # Set up a web driver wait procedure, based on the visibility of the element condition
        wait = WebDriverWait(self.driver, 3)
        wait.until(expected_conditions.visibility_of_element_located(draggable_item))

        # Identify the source and target zones
        query_data = ("misc_items", "name", "dropzone_1", "*")
        dropzone_1 = self.__convert_record_to_dict__(query_data)
        source_item = self.__locator_handler__(dropzone_1)
        source_zone = self.driver.find_element(*source_item)
        query_data = ("misc_items", "name", "dropzone_2", "*")
        dropzone_2 = self.__convert_record_to_dict__(query_data)
        target_item = self.__locator_handler__(dropzone_2)
        target_zone = self.driver.find_element(*target_item)

        # Identify the item to be dragged
        draggable_elem = self.driver.find_element(*draggable_item)

        # Verify that the item is located in the source zone
        verification_flag, verification_msg = self.__verify_draggable_item_position__(
            draggable_elem, source_zone
        )
        log_messages.append(verification_msg)

        # If the above verification results in a false flag, stop execution and return the result
        if not verification_flag:
            return verification_flag, log_messages

        self.driver.set_script_timeout(2)

        # Load the jQuery helper
        with open("..\\utilities\\jquery_load_helper.js") as f:
            load_jquery_js = f.read()
            f.close()
        with open("..\\utilities\\jquery_load_helper.js") as f:
            load_jquery_lines = f.readlines()
            f.close()
        jquery_url = ""
        for jquery_line in load_jquery_lines:
            if "jqueryUrl =" in jquery_line:
                jquery_url = jquery_line.split("= ")[-1].split(";")[0].replace("'", "")

        # Load the jQuery
        self.driver.execute_async_script(load_jquery_js, jquery_url)

        # Load the javascript drag and drop helper
        with open("..\\utilities\\drag_and_drop_helper.js") as f:
            drag_and_drop_js = f.read()

        # Perform the drag and drop action
        sim_drag_and_drop_str = "$('%s').simulateDragDrop({ dropTarget: '%s'});" % (
            draggable_data["locator_hook"],
            dropzone_2["locator_hook"],
        )
        self.driver.execute_script(drag_and_drop_js + sim_drag_and_drop_str)
        log_messages.append("Drag and drop action performed")

        # Identify the item to be dragged
        draggable_elem = self.driver.find_element(*draggable_item)

        # Verify that the item is located in the target zone
        verification_flag, verification_msg = self.__verify_draggable_item_position__(
            draggable_elem, target_zone
        )
        log_messages.append(verification_msg)

        # Return the result
        return verification_flag, log_messages

    def switch_to_iframes(self):
        """
        Method used to verify the switch to iFrames functionality
        :return: (bool, str) Verification that the iFrame switches succeeded
        """
        query_data = ("iframe_items", "name", "iframe2", "*")
        iframe2_dict = self.__convert_record_to_dict__(query_data)
        self.driver.switch_to.frame(iframe2_dict["iframe_name"])
        iframe2_item = self.__locator_handler__(iframe2_dict)
        iframe2_text = self.driver.find_element(*iframe2_item).text
        expected_text = iframe2_dict["expected_text"]
        if iframe2_text != expected_text:
            return (
                False,
                f"Detected iFrame text: {iframe2_text}, expected: {expected_text}",
            )
        self.driver.switch_to.default_content()
        query_data = ("iframe_items", "name", "iframe3", "*")
        iframe3_dict = self.__convert_record_to_dict__(query_data)
        self.driver.switch_to.frame(iframe3_dict["iframe_name"])
        iframe3_item = self.__locator_handler__(iframe3_dict)
        self.__click_item__(*iframe3_item)
        self.driver.switch_to.default_content()
        return True, "Detected iFrame2 text as expected, iFrame3 checkbox clicked"

    def get_progress_bar_data(self):
        """
        Method used to retrieve the progress bar data.

        :return: (dict) Progress bar data (locator, start & end expected values)
        """
        query_data = ("bar_and_label_values", "name", "progress_bar", "*")
        return self.__convert_record_to_dict__(query_data)

    def get_progress_label_data(self):
        """
        Method used to retrieve the progress label data.

        :return: (dict) Progress label data (locator, start & end expected values)
        """
        query_data = ("bar_and_label_values", "name", "progress_label", "*")
        return self.__convert_record_to_dict__(query_data)

    def get_meter_bar_data(self):
        """
        Method used to retrieve the meter bar data.

        :return: (dict) Progress meter data (locator, start & end expected values)
        """
        query_data = ("bar_and_label_values", "name", "meter_bar", "*")
        return self.__convert_record_to_dict__(query_data)

    def get_meter_label_data(self):
        """
        Method used to retrieve the meter label data.

        :return: (dict) Progress meter data (locator, start & end expected values)
        """
        query_data = ("bar_and_label_values", "name", "meter_label", "*")
        return self.__convert_record_to_dict__(query_data)

    def __read_bar_value__(self, *readable_bar):
        """
        Helper method used to retrieve the displayed bar value.

        :return: (str) The displayed bar value
        """
        return self.driver.find_element(*readable_bar).get_attribute("value")

    def read_progress_bar_value(self):
        """
        Method used to retrieve the displayed progress bar value.

        :return: (str) The displayed progress bar value
        """
        query_data = ("bar_and_label_values", "name", "progress_bar", "*")
        bar_value_item = self.__locator_handler__(
            self.__convert_record_to_dict__(query_data)
        )
        return self.__read_bar_value__(*bar_value_item)

    def read_meter_bar_value(self):
        """
        Method used to retrieve the displayed meter bar value.

        :return: (str) The displayed meter bar value
        """
        query_data = ("bar_and_label_values", "name", "meter_bar", "*")
        meter_value_item = self.__locator_handler__(
            self.__convert_record_to_dict__(query_data)
        )
        return self.__read_bar_value__(*meter_value_item)

    def __read_label_value__(self, *readable_label):
        """
        Helper method used to retrieve the displayed bar value.

        :return: (str) The displayed bar value
        """
        label_value = (
            self.driver.find_element(*readable_label)
            .text.split(": ")[-1]
            .replace("(", "")
            .replace(")", "")
        )
        return label_value

    def read_progress_label_value(self):
        """
        Method used to retrieve the displayed progress label value.

        :return: (str) The displayed progress label value
        """
        query_data = ("bar_and_label_values", "name", "progress_label", "*")
        label_value_item = self.__locator_handler__(
            self.__convert_record_to_dict__(query_data)
        )
        return self.__read_label_value__(*label_value_item)

    def read_meter_label_value(self):
        """
        Method used to retrieve the displayed progress label value.

        :return: (str) The displayed progress label value
        """
        query_data = ("bar_and_label_values", "name", "meter_label", "*")
        label_value_item = self.__locator_handler__(
            self.__convert_record_to_dict__(query_data)
        )
        return self.__read_label_value__(*label_value_item)

    def get_slider_data(self):
        """
        Method used to retrieve the slider object data.

        :return: (dict) slider object data.
        """
        query_data = ("slider_dropdown", "name", "input_slider_control", "*")
        return self.__convert_record_to_dict__(query_data)

    def move_slider_control(self):
        """
        Method used to verify the input slider control movement functionality.
        """
        query_data = ("slider_dropdown", "name", "input_slider_control", "*")
        input_slider_control = self.__convert_record_to_dict__(query_data)
        slider_item = self.__locator_handler__(input_slider_control)
        slider_elem = self.driver.find_element(*slider_item)
        self.actions.drag_and_drop_by_offset(
            slider_elem,
            xoffset=input_slider_control["custom_field1"],
            yoffset=input_slider_control["custom_field2"],
        ).perform()

    def __get_radio_button_data__(self, radio_button):
        """
        Method used to retrieve the radio button data.

        :return: (dict) radio button data
        """
        query_data = ("radio_buttons", "name", radio_button, "*")
        return self.__convert_record_to_dict__(query_data)

    def get_radio_button1_data(self):
        """
        Method used to retrieve the radio button1 data.

        :return: (dict) radio button1 data.
        """
        return self.__get_radio_button_data__("radio_button1")

    def get_radio_button2_data(self):
        """
        Method used to retrieve the radio button1 data.

        :return: (dict) radio button1 data.
        """
        return self.__get_radio_button_data__("radio_button2")

    def verify_radio_button_selected(self, radio_button):
        """
        Method used to verify if a radio button is selected.

        :param radio_button: (dict) the radio button for which the verification is done
        :return: (bool) verification result
        """
        radio_button_item = self.__locator_handler__(radio_button)
        radio_button_elem = self.driver.find_element(*radio_button_item)
        radio_button_selected = (
            radio_button_elem.is_displayed(),
            radio_button_elem.is_enabled(),
            radio_button_elem.is_selected(),
        )
        return radio_button_selected

    def click_radio_button(self, radio_button):
        """
        Method used to click on a specific radio button.

        :param radio_button: (dict) the radio button on which to click
        """
        radio_button_item = self.__locator_handler__(radio_button)
        self.__click_item__(*radio_button_item)

    @staticmethod
    def __verify_draggable_item_position__(draggable_item, expected_zone):
        """
        Method used to verify that the draggable item is within the expected zone range.

        :param draggable_item: the draggable item to be verified
        :param expected_zone: the expected zone where the item should be situated
        :return: (bool, str) the verification result
        """
        margin_tolerance = 10
        expected_range = range(
            expected_zone.location["x"], expected_zone.location["x"] + margin_tolerance
        )
        if draggable_item.location["x"] not in expected_range:
            return False, f"Draggable item not in the expected range: {expected_range}"
        return True, f"Draggable item in expected range: {expected_range}"

    @staticmethod
    def __locator_handler__(locator_element):
        """
        Helper method used to handle the locator in function of its type.

        :param locator_element: the locator to be handled
        :return: (locator_item) the constructed locator
        """
        # Depending on the locator type, return the constructed locator
        if locator_element["locator_type"] == "XPATH":
            locator_item = (By.XPATH, locator_element["locator_hook"])
        elif locator_element["locator_type"] == "LINK_TEXT":
            locator_item = (By.LINK_TEXT, locator_element["locator_hook"])
        elif locator_element["locator_type"] == "PARTIAL_LINK_TEXT":
            locator_item = (By.PARTIAL_LINK_TEXT, locator_element["locator_hook"])
        elif locator_element["locator_type"] == "NAME":
            locator_item = (By.NAME, locator_element["locator_hook"])
        elif locator_element["locator_type"] == "TAG_NAME":
            locator_item = (By.TAG_NAME, locator_element["locator_hook"])
        elif locator_element["locator_type"] == "CLASS_NAME":
            locator_item = (By.CLASS_NAME, locator_element["locator_hook"])
        elif locator_element["locator_type"] == "CSS_SELECTOR":
            locator_item = (By.CSS_SELECTOR, locator_element["locator_hook"])
        # The default locator type will be considered to be "ID"
        else:
            locator_item = (By.ID, locator_element["locator_hook"])
        return locator_item
