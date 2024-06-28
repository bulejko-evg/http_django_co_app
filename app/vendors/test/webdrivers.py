import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.chrome.service import Service as ChromeService

"""
Requires installation of chromedriver and geckodriver for usage

brew install geckodriver
brew install chromedriver
"""


@pytest.fixture(scope="module")
def safari_browser_instance(request):
    service = SafariService(executable_path="/usr/bin/safaridriver")
    options = webdriver.SafariOptions()
    browser = webdriver.Safari(service=service, options=options)
    yield browser
    browser.close()


@pytest.fixture(scope="module")
def firefox_browser_instance(request):
    service = FirefoxService(executable_path="./geckodriver")
    options = webdriver.FirefoxOptions()
    options.headless = False
    browser = webdriver.Firefox(service=service, options=options)
    yield browser
    browser.close()


@pytest.fixture(scope="module")
def chrome_browser_instance(request):
    service = ChromeService(executable_path="./chromedriver")
    options = webdriver.ChromeOptions()
    options.headless = False
    browser = webdriver.Chrome(service=service, options=options)
    yield browser
    browser.close()
