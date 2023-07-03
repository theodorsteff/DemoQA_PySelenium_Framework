# QA Automation Framework Demo
## Selenium with Python integration

**Demo Project:** *Selenium testing framework implementation with Python (Version 1.0)*  
**Dependency packages installed:** **_pytest_ and _selenium_** *(including their automatically installed dependencies)*  
**Credits:** *The demo page used is provided by SeleniumBase (https://seleniumbase.io/demo_page)*

In order to install the required packages, please follow the *pip install* command structure, as showcased below.

### pytest
`» pip install pytest`

### selenium
`» pip install selenium`  

The project uses the sqlite3 python extension module, in order to read from the "demopage_data" database. For a convenient way to visualize the content of the database, please use the "DB Browser for SQLite" available for download at the following link: https://sqlitebrowser.org/dl/    
    
For test suite execution, change the folder path to the "tests" folder of the project and use the pytest syntax, as shown below ("--html report.html" will generate a test report in the same folder as the location of the testcases).    
`» cd <DemoQA_PySelenium_Framework directory>\tests`  
`» py.test --html report.html` 

**Python version used:** *Python 3.11.0*  
**Selenium library version used:** *selenium 4.10.0*  
**Pytest library version used:** *pytest 7.3.1*  
**SQLite version used:** *sqlite3*
