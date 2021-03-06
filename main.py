from asyncio.windows_events import NULL
from json import JSONDecoder
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import sys


def get_chapters():
    print("Fetching all chapters...")
    data = requests.get('http://localhost:3000/chapters')
    print("Fetching all chapters... Done")

    return data.json()


def get_chapter(num):
    chapters = get_chapters()
    # find chapter.text contains `第${number}章`
    print(f"Finding chapter {num}...")
    for chapter in chapters:
        if '第' + str(num) + '章' in chapter['text']:
            print(f"Chapter {num} found")
            print(chapter)
            return chapter
    print(f"Chapter {num} not found")
    return None


def get_chapter_content(url):
    print(f"Fetching chapter content from {url}")
    data = requests.get("http://localhost:3000/chapter", json={
        "url": url,
    },)
    print(f"Fetching chapter content from {url}... Done")
    return data.json()


def main():

    start = int(sys.argv[1])
    end = int(sys.argv[2])

    print("Initiating...")
    # check if start and end are numbers
    if not start or not end:
        print('Arguments start and end must be provided')
        return

    driver = webdriver.Firefox()

    driver.get("https://www.deepl.com/translator")

    driver.implicitly_wait(10)

    # set input language to chinese
    lang_input_element = driver.find_element(
        by=By.CSS_SELECTOR, value="div.lmt__language_select--source>button")
    lang_input_element.click()

    lang_input_element = driver.find_element(
        by=By.CSS_SELECTOR, value="button[dl-test='translator-lang-option-zh']")
    lang_input_element.click()

    # set output language to english
    lang_input_element = driver.find_element(
        by=By.CSS_SELECTOR, value="div.lmt__language_select--target>button")
    lang_input_element.click()

    lang_input_element = driver.find_element(
        by=By.CSS_SELECTOR, value="button[dl-test='translator-lang-option-en-US']")
    lang_input_element.click()

    def get_translation(text, title):
        print(f"{title}: Translating...")

        input_textarea = driver.find_element(
            by=By.CSS_SELECTOR, value='textarea.lmt__source_textarea')

        input_textarea.clear()
        # driver.execute_script(f'arguments[0].value={text}', input_textarea)
        input_textarea.send_keys(text)

        # wait if lmt__progress_popup is visible
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.lmt__progress_popup")))
        # the loading is started, wait until it is finished
        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.lmt__progress_popup")))

        # Loading has ended

        output_textarea = driver.find_element(
            by=By.CSS_SELECTOR, value='#target-dummydiv')

        translated_text = output_textarea.get_attribute("innerHTML")
        print(f"{title}: Translating Done")

        # make a post request to http://localhost:3000/createBook
        # with the following data:
        print(f"{title}: Saving book...")
        requests.post("http://localhost:3000/createBook", json={
            "raw": text,
            "text": output_textarea.get_attribute("innerHTML"),
            "title": title,
            "author": "Momo",
            "imageUrl": "",
            "publisher": "Jet"
        },)
        print(f"{title}: Done!")

    def scrape_from_until(start, end, url):
        if(end == 0):
            return
        if(start != None):
            c = get_chapter(start)
            url = c['href']
        chapter = get_chapter_content(url)

        get_translation(chapter["content"], chapter["title"])

        scrape_from_until(None, end - 1, chapter["nextLink"])

    scrape_from_until(start, end, "")


main()
