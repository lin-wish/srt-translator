from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import sys
import os


def main():
    srt_filepath = os.path.abspath(sys.argv[1])
    srt_filedir = os.path.dirname(srt_filepath)
    mine_type = 'plain/text'

    options = Options()
    options.add_argument('--headless')

    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', srt_filedir)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', mine_type)
    profile.set_preference('browser.helperApps.neverAsk.openFile', mine_type)
    profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    profile.set_preference("browser.download.manager.useWindow", False)
    profile.set_preference("browser.download.manager.focusWhenStarting", False)
    profile.set_preference(
        "browser.download.manager.showAlertOnComplete", False)
    profile.set_preference("browser.download.manager.closeWhenDone", True)

    driver = webdriver.Firefox(options=options, firefox_profile=profile)
    driver.get("https://translate-subtitles.com/")
    assert "Subtitles" in driver.title
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "file"))
    )
    select = Select(driver.find_element_by_class_name('goog-te-combo'))
    select.select_by_value('zh-CN')
    driver.find_element_by_id('file').send_keys(srt_filepath)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "download"))
    ).click()
    driver.close()


if __name__ == '__main__':
    if not sys.argv[1]:
        print("Please input srt file")
        sys.exit(1)
    else:
        main()
