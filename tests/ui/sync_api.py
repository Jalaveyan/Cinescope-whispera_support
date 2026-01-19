
import re

from playwright.async_api import Page
from playwright.sync_api import expect


def test_expect(page: Page):
    page.goto("https://demoqa.com/radio-button")
    yes_radio = page.get_by_role("radio", name="Yes")
    impressive_radio = page.get_by_role("radio", name="Impressive")
    no_radio = page.get_by_role("radio", name="No")
    expect(no_radio).to_be_disabled()
    expect(yes_radio).to_be_enabled()
    expect(impressive_radio).to_be_enabled()
    page.locator('[for="yesRadio"]').click()
    expect(yes_radio).to_be_checked()
    expect(impressive_radio).not_to_be_checked()

def test_registration_form(page: Page):
    page.goto("https://demoqa.com/webtables")

    page.locator('#addNewRecordButton').click()

    expect(page.locator('.modal-header')).to_contain_text('Registration Form')

    # 3. Fill form
    page.fill('input[placeholder="First Name"]', 'Artyom')
    page.fill('#lastName', 'Aleks')
    page.fill('#userEmail', 'rtmnsnk@gmail.com')
    page.fill('#age', '22')
    page.fill('#salary', '250000')
    page.fill('#department', 'QA Auto')

    page.locator('#submit').click()

def test_registration_student(page: Page):

    page.goto("https://demoqa.com/automation-practice-form")

    page.fill('input[placeholder="First Name"]', 'Artyom')
    page.type('#firstName', 'Alex')
    page.fill('#userEmail', 'rtmnsnk@gmail.com')
    page.locator('label[for="gender-radio-2"]').click()  # Female
    page.locator('label[for="gender-radio-3"]').click()  # Other
    page.locator('label[for="gender-radio-1"]').click()  # Male
    page.type('#userNumber', "79881040000")
    page.get_attribute('#dateOfBirthInput', '15.01.2026')
    page.fill('#subjectsInput', 'Music')
    page.keyboard.press('Enter')
    page.locator('label[for="hobbies-checkbox-1"]').click()  # Sports
    page.locator('label[for="hobbies-checkbox-2"]').click()  # Reading
    page.locator('label[for="hobbies-checkbox-3"]').click()  # Music
    page.locator('#state .css-yk16xz-control').click()
    page.fill('#react-select-3-input', 'NCR')
    page.keyboard.press('Enter')
    page.locator('#city .css-yk16xz-control').click()
    page.fill('#react-select-4-input', 'Delhi')
    page.keyboard.press('Enter')
    footer_text = page.locator('footer span').inner_text()
    assert footer_text == "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED."


def test_radiobutton(page: Page):
    page.goto("https://demoqa.com/radio-button")

    page.is_enabled('#yesRadio')
    page.locator('label[for="yesRadio"]').click()
    page.is_enabled('#impressiveRadio')
    page.locator('label[for="impressiveRadio"]').click()
    page.locator('label[for="noRadio"]').is_disabled()

def test_checkbox(page: Page):
    page.goto("https://demoqa.com/checkbox")

    assert page.locator('label[for="tree-node-home"]').is_visible()

    page.locator('label[for="tree-node-home"]').click()

    page.locator('button.rct-option-expand-all').click()

    assert page.locator('label[for="tree-node-desktop"]').is_visible()

def test_dynamic_properties(page: Page):
    page.goto("https://demoqa.com/dynamic-properties")

    page.locator('#visibleAfter').is_visible()
    page.wait_for_selector('#enableAfter', state='visible')
    page.locator('#visibleAfter').is_visible()