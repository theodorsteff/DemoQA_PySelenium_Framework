# QA Automation Framework Demo
## Selenium with Python integration

**Demo Project:** *Selenium testing framework implementation with Python (Version 1.0)*  
**Dependency packages installed:** **_pytest_, _pytest-html_ and _selenium_** *(including their automatically installed dependencies)*  
**Credits:** *The demo page used is provided by SeleniumBase (https://seleniumbase.io/demo_page)*

In order to install the required packages, please follow the *pip install* command structure, as showcased below.

### pytest
`» pip install pytest`

### pytest html plugin
`» pip install pytest-html`

### selenium
`» pip install selenium`  

The project uses the sqlite3 python extension module, in order to read from the "demopage_data" database. For a convenient way to visualize the content of the database, please use the "DB Browser for SQLite" available for download at the following link: https://sqlitebrowser.org/dl/    
    
For test suite execution, change the folder path to the "tests" folder of the project and use the pytest syntax, as shown below ("--html report.html" will generate a test report in the same folder as the location of the testcases).    
`» cd <DemoQA_PySelenium_Framework directory>\tests`  
`» py.test --html report.html` 
    
Main elements of the framework:
- utilities.baseclass -> **BaseClass**    
*Base class from which all test classes inherit; it's being used to instantiate the logging object.*
- testdata.demopage_data -> **DemoPageData**    
*Class used to handle multiple data sets for multiple executions of a single test.*
-  testdata.**demopage_data.db**    
*Database used to feed the required configuration and web objects localization data.*
- pageobjects.demopage -> **DemoPage**    
*Class used to handle the web objects and page interactions.*
- tests.**conftest**    
*Module used to configure pytest; it's also being used to instantiate the Selenium webdriver.*
- tests.test_demopage -> **TestDemoPage(BaseClass)**    
*Class used for the tests executions (derives from the base class).*
    
**Python version used:** *Python 3.11.0*
**Selenium library version used:** *selenium 4.18.1*
**Pytest library version used:** *pytest 8.0.1*
**Pytest html plugin version used:** *pytest-html 4.1.1*
**SQLite module version used:** *sqlite3*
