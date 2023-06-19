# -*- coding: utf-8 -*-
#
# Demo Project: Selenium testing framework implementation with Python
# Showcase implementation by: Theodor-Stefan Baca
#

"""
Description:
This module configures the testing framework.
"""

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Prototype definition and initialization of the driver as an empty object
driver = None


def pytest_addoption(parser):
    """
    PyTest's method used to add options to the parser
    (e.g.: browser to be used).
    """
    parser.addoption("--browser_name", action="store", default="chrome")


@pytest.fixture(scope="class")
def setup(request):
    """
    Setup method used when invoking the test class.
    """
    # Initialization of the driver as a global variable
    # to be used by the test class.
    global driver

    # Setting up the path for the selenium drivers to be used
    service_obj = Service(r"C:\SeleniumDrivers")

    # Setting up the browser to be used
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        driver = webdriver.Chrome(service=service_obj)
    elif browser_name == "firefox":
        driver = webdriver.Firefox(service=service_obj)

    # Passing the driver to the request parameters,
    # in order to be used by the test classes. The driver will be then
    # yielded until the test executions have ended.
    request.cls.driver = driver
    yield
    driver.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Method used to extend the PyTest Plugin to take
    and embed a screenshot in html report, whenever a test fails.
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = (
                    '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" '
                    'onclick="window.open(this.src)" align="right"/></div>' % file_name
                )
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    """
    Method used to capture page screenshots.
    """
    driver.get_screenshot_as_file(name)
