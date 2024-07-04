import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_program_details(search_query):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = "/usr/bin/google-chrome-stable"

    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    search_url = f"https://bangumi.org/search?q={search_query}&area_code=23"
    driver.get(search_url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li > a[href*='/tv_events/']"))
        )
    except TimeoutException:
        print("検索結果が見つかりませんでした。")
        driver.quit()
        return []

    program_links = driver.find_elements(By.CSS_SELECTOR, "li > a[href*='/tv_events/']")
    links = [link.get_attribute('href') for link in program_links]
    program_data = []

    for program_url in links[:3]:
        driver.get(program_url)
        
        try:
            program_title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'program_title'))
            ).text

            program_supplement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'program_supplement'))
            ).text

            cast_elements = driver.find_elements(By.CSS_SELECTOR, ".addition li h2.heading + p a")
            cast_names = [element.text for element in cast_elements if element.text != '']

            program_data.append({
                'url': program_url,
                'title': program_title,
                'supplement': program_supplement,
                'cast_names': cast_names
            })

        except (TimeoutException, NoSuchElementException) as e:
            print(f"エラーが発生しました: {e}")
            print("ページソースを出力します:")
            print(driver.page_source)
            driver.save_screenshot('debug_screenshot.png')

    driver.quit()
    return program_data

def get_program_details_from_scraper(program_id):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    search_url = f"https://bangumi.org/tv_events/{program_id}"
    driver.get(search_url)
    time.sleep(5)

    try:
        program_title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'program_title'))
        )
        program_title = program_title_element.text

        program_supplement_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'program_supplement'))
        )
        program_supplement = program_supplement_element.text

        cast_elements = driver.find_elements(By.CSS_SELECTOR, ".addition li h2.heading + p a")
        cast_names = [element.text for element in cast_elements if element.text != '']

        program_data = {
            'url': search_url,
            'title': program_title,
            'supplement': program_supplement,
            'cast_names': cast_names
        }

    except (TimeoutException, NoSuchElementException) as e:
        print(f"番組ID {program_id} の詳細を取得中にエラーが発生しました: {e}")
        print("ページソースを出力します:")
        print(driver.page_source)
        driver.save_screenshot('debug_screenshot.png')
        program_data = {
            'url': '',
            'title': f'Scraped Program {program_id}',
            'supplement': f'Scraped Details of Program {program_id}',
            'cast_names': []
        }

    driver.quit()
    return program_data

def main():
    st.title('TV Program Recommendation App')
    search_word = st.text_input("検索ワードを入力してください", st.session_state.get('search_word', ''))
    if st.button('検索'):
        st.session_state.search_word = search_word
        st.session_state.program_data = get_program_details(search_word)
    
    if 'program_data' in st.session_state:
        for program in st.session_state.program_data:
            st.write(program)

if __name__ == "__main__":
    main()
