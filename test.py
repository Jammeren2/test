from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select 
import pytest
import logging
import os

@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()
    
@pytest.mark.parametrize("num1, num2, operation, expected", [
    ("5", "3", "+", "8.0"),
    ("10", "2", "-", "8.0"),
    ("2", "10", "-", "-8.0"),
    ("4", "3", "*", "12.0"),
    ("8", "2", "/", "4.0"),
    ("2", "8", "/", "0.25"),
    ("2", "3", "**", "8.0"),
    ("5", "3", "max", "5.0"),
    ("3", "5", "max", "5.0"),
    ("5", "3", "min", "3.0"),
    ("3", "5", "min", "3.0"),
    ("5", "0", "/", "Ошибка: Деление на ноль")
])
def test_calculator_operations(driver, num1, num2, operation, expected):
    num1_field = driver.find_element(By.NAME, "num1")
    num2_field = driver.find_element(By.NAME, "num2")
    operation_select = Select(driver.find_element(By.NAME, "operation"))
    submit_button = driver.find_element(By.TAG_NAME, "button")

    num1_field.clear()
    num1_field.send_keys(num1)
    num2_field.clear()
    num2_field.send_keys(num2)
    operation_select.select_by_value(operation)
    submit_button.click()

    # Wait for result to appear
    result_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h3"))
    )

    result_text = result_element.text
    print(driver.page_source)  # Debugging output
    assert f"Результат: {expected}" in result_text
