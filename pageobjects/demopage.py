# -*- coding: utf-8 -*-
#
# Demo Project: Selenium testing framework implementation with Python
# Showcase implementation by: Theodor-Stefan Baca
#

"""
Description:
This module defines the page objects and actions for the "demo page"
(e.g.: clicking a hovering menu, reading a text field, injecting
a string to a specific text box).
"""

import os

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from testdata.read_config_file import ReadConfigFiles


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
        self.local_demo_page = False
        self.driver = driver
        self.driver.implicitly_wait(5)
        self.actions = ActionChains(self.driver)
        self.locator_elements = ReadConfigFiles().get_locators()
        self.debug_showcase = ReadConfigFiles().get_debug_showcase()

        # Load a local html file into the web browser
        if self.local_demo_page:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            par_path = os.path.abspath(os.path.join(dir_path, os.pardir))
            url_path = os.path.join(par_path, "testdata\\demopage.html")

        # Load a demo page into the web browser
        else:
            url_path = "https://seleniumbase.io/demo_page/"
        self.driver.get(url_path)
        self.driver.maximize_window()

    def get_debug_showcase(self):
        """
        Method used to return the debug showcase flag, used to display logging information.

        :return: (bool) debug_showcase member
        """
        return self.debug_showcase

    def inject_text_in_box(self, text_to_insert, box_in_focus):
        """
        Method used to inject text in a specific box on the screen.

        :param text_to_insert: (str) text string to be inserted
        :param box_in_focus: (dict) item of the box in focus
        """
        if box_in_focus["locator_type"] == "CSS_SELECTOR":
            if box_in_focus["clear_required"]:
                self.driver.find_element(
                    By.CSS_SELECTOR, box_in_focus["locator_hook"]
                ).clear()
            self.driver.find_element(
                By.CSS_SELECTOR, box_in_focus["locator_hook"]
            ).send_keys(text_to_insert)
        elif box_in_focus["locator_type"] == "XPATH":
            if box_in_focus["clear_required"]:
                self.driver.find_element(By.XPATH, box_in_focus["locator_hook"]).clear()
            self.driver.find_element(By.XPATH, box_in_focus["locator_hook"]).send_keys(
                text_to_insert
            )

    def inject_text_input_field(self, text_to_insert):
        """
        Method used to inject text in the text input field box.

        :param text_to_insert: (str) text string to be inserted
        """
        self.inject_text_in_box(
            text_to_insert, self.locator_elements["text_input_field"]
        )

    def inject_text_pre_filled_field(self, text_to_insert):
        """
        Method used to inject text in the text input pre-filled box.

        :param text_to_insert: (str) text string to be inserted
        """
        self.inject_text_in_box(
            text_to_insert, self.locator_elements["pre_filled_text_field"]
        )

    def inject_text_placeholder_field(self, text_to_insert):
        """
        Method used to inject text in the text placeholder field box.

        :param text_to_insert: (str) text string to be inserted
        """
        placeholder_text = self.driver.find_element(
            By.CSS_SELECTOR,
            self.locator_elements["placeholder_text_field"]["locator_hook"],
        ).get_property("placeholder")
        self.inject_text_in_box(
            text_to_insert, self.locator_elements["placeholder_text_field"]
        )
        return placeholder_text

    def inject_text_area(self, text_to_insert):
        """
        Method used to inject text in the text area box.

        :param text_to_insert: (str) text string to be inserted
        """
        self.inject_text_in_box(text_to_insert, self.locator_elements["text_area"])

    def read_item_text(self, *readable_item):
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
        return self.read_item_text(
            By.CSS_SELECTOR, self.locator_elements["dynamic_subhead"]["locator_hook"]
        )

    def read_button(self):
        """
        Method used to read the text from the "Button" of the page.
        """
        return self.read_item_text(
            *(By.XPATH, self.locator_elements["button"]["locator_hook"])
        )

    def read_paragraph(self):
        """
        Method used to read the text from the paragraph of the page.
        """
        return self.read_item_text(
            *(By.XPATH, self.locator_elements["paragraph_with_text"]["locator_hook"])
        )

    def read_only_field(self):
        """
        Method used to read the text from the read only field of the page.

        :return text: the text value read from the read only field of the page.
        """
        return self.driver.find_element(
            By.XPATH, self.locator_elements["read_only_text_field"]["locator_hook"]
        ).get_property("value")

    def hover_click_option(self):
        """
        Method used to click on a hovering menu option.

        :return: (str) The text for the hovering option selected.
        """
        self.actions.move_to_element(
            self.driver.find_element(
                By.CSS_SELECTOR, self.locator_elements["hover_dropdown"]["locator_hook"]
            )
        ).perform()
        self.actions.click(
            self.driver.find_element(
                By.LINK_TEXT,
                self.locator_elements["hover_dropdown"]["hover_option_text"],
            )
        ).perform()
        return self.locator_elements["hover_dropdown"]["hover_option_text"]

    def click_item(self, *clickable_item):
        """
        Method used to click on a clickable item from the page.

        :param clickable_item: (locator) Selenium locator for the clickable item.
        """
        self.driver.find_element(*clickable_item).click()

    def click_button(self):
        """
        Method used to click on the page's "Button".
        """
        self.click_item(*(By.XPATH, self.locator_elements["button"]["locator_hook"]))

    def click_checkbox(self):
        """
        Method used to click on the page's "CheckBox".
        """
        self.click_item(
            *(By.CSS_SELECTOR, self.locator_elements["checkbox"]["locator_hook"])
        )

    def drag_and_drop_picture(self):
        """
        Method used to drag and drop an item on the page.
        :return: (bool, str) Verification that the draggable item is
        in the correct position
        """

        # Read the locator hook for the element to be dragged
        draggable_elem = self.locator_elements["draggable_item"]["locator_hook"]

        # Set up a web driver wait procedure, based on the visibility of the element condition
        wait = WebDriverWait(self.driver, 3)
        wait.until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, draggable_elem)
            )
        )

        # Identify the source and target zones
        source_elem = self.locator_elements["dropzone_1"]["locator_hook"]
        source_zone = self.driver.find_element(By.CSS_SELECTOR, source_elem)
        target_elem = self.locator_elements["dropzone_2"]["locator_hook"]
        target_zone = self.driver.find_element(By.CSS_SELECTOR, target_elem)

        # Identify the item to be dragged
        draggable_item = self.driver.find_element(By.CSS_SELECTOR, draggable_elem)

        # Verify that the item is located in the source zone
        verification_flag, verification_msg = self.verify_draggable_item_position(
            draggable_item, source_zone
        )

        # If the above verification results in a false flag, stop execution and return the result
        if not verification_flag:
            return verification_flag, verification_msg

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
            draggable_elem,
            target_elem,
        )
        self.driver.execute_script(drag_and_drop_js + sim_drag_and_drop_str)

        # Identify the item to be dragged
        draggable_item = self.driver.find_element(By.CSS_SELECTOR, draggable_elem)

        # Verify that the item is located in the target zone
        verification_flag, verification_msg = self.verify_draggable_item_position(
            draggable_item, target_zone
        )

        # Return the result
        return verification_flag, verification_msg

    def switch_to_iframes(self):
        """
        Method used to verify the switch to iFrames functionality
        :return: (bool, str) Verification that the iFrame switches succeeded
        """
        self.driver.switch_to.frame(self.locator_elements["iframe2"]["iframe_name"])
        iframe_text = self.driver.find_element(
            By.CSS_SELECTOR, self.locator_elements["iframe2"]["iframe_body"]
        ).text
        expected_text = self.locator_elements["iframe2"]["iframe_expected_text"]
        if iframe_text != expected_text:
            return (
                False,
                f"Detected iFrame text: {iframe_text}, expected: {expected_text}",
            )
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.locator_elements["iframe3"]["iframe_name"])
        self.click_item(
            *(By.CSS_SELECTOR, self.locator_elements["iframe3"]["iframe_checkbox"])
        )
        self.driver.switch_to.default_content()
        return True, "Detected iFrame2 text as expected, iFrame3 checkbox clicked"

    def get_progress_bar_data(self):
        """
        Method used to retrieve the progress bar data.

        :return: (dict) Progress bar data (locator, start & end expected values)
        """
        return self.locator_elements["progress_bar"]

    def read_progress_bar_value(self):
        """
        Method used to retrieve the displayed progress bar value.

        :return: (str) The displayed progress bar value
        """
        progress_value = self.driver.find_element(
            By.ID, self.locator_elements["progress_bar"]["locator_hook"]
        )
        return progress_value.text.split(": ")[-1].replace("(", "").replace(")", "")

    def move_slider_control(self):
        """
        Method used to verify the input slider control movement functionality.
        """
        slider_element = self.locator_elements["input_slider_control"]
        slider_item = self.driver.find_element(By.ID, slider_element["locator_hook"])
        self.actions.drag_and_drop_by_offset(
            slider_item,
            xoffset=slider_element["x_offset"],
            yoffset=slider_element["y_offset"],
        ).perform()

    @staticmethod
    def verify_draggable_item_position(draggable_item, expected_zone):
        margin_tolerance = 10
        expected_range = range(
            expected_zone.location["x"], expected_zone.location["x"] + margin_tolerance
        )
        if draggable_item.location["x"] not in expected_range:
            return False, f"Draggable item not in the expected range: {expected_range}"
        return True, "Item in correct position"
