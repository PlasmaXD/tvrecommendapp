from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_program_details(search_query):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')  # 追加オプション
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    # service = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service, options=options)
    # driver = webdriver.Chrome(options=options)

    search_url = f"https://bangumi.org/search?q={search_query}&area_code=23"
    driver.get(search_url)
    time.sleep(5)
    
    program_data = []
    program_links = driver.find_elements(By.CSS_SELECTOR, "li > a[href*='/tv_events/']")
    links = [link.get_attribute('href') for link in program_links]

    for program_url in links[:3]:
        driver.get(program_url)
        time.sleep(5)
        program_title = driver.find_element(By.CLASS_NAME, 'program_title').text
        program_supplement = driver.find_element(By.CLASS_NAME, 'program_supplement').text
        cast_elements = driver.find_elements(By.CSS_SELECTOR, ".addition li h2.heading + p a")
        cast_names = [element.text for element in cast_elements if element.text != '']
        program_data.append({
            'url': program_url,
            'title': program_title,
            'supplement': program_supplement,
            'cast_names': cast_names
        })
    
    driver.quit()
    return program_data
def get_program_details_from_scraper(program_id):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    # service = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(options=options)

    # 検索URLを構築
    # search_url = f"https://bangumi.org/search?q={program_id}&area_code=23"
    search_url = f"https://bangumi.org/tv_events/{program_id}"
    driver.get(search_url)
    time.sleep(5)  # ページが読み込まれるまで待機

    try:
        # 検索結果の最初のリンクを取得
        program_links = driver.find_elements(By.CSS_SELECTOR, "li > a[href*='/tv_events/']")
        if not program_links:
            raise ValueError("番組リンクが見つかりませんでした。")
        
        program_url = program_links[0].get_attribute('href')
        driver.get(program_url)
        time.sleep(5)  # ページが読み込まれるまで待機

        # 番組タイトルを取得
        program_title_element = driver.find_element(By.CLASS_NAME, 'program_title')
        program_title = program_title_element.text if program_title_element else 'Unknown Title'
        
        # 番組の補足情報を取得
        program_supplement_element = driver.find_element(By.CLASS_NAME, 'program_supplement')
        program_supplement = program_supplement_element.text if program_supplement_element else 'No Supplement'
        
        # 番組キャスト情報を取得
        cast_elements = driver.find_elements(By.CSS_SELECTOR, ".addition li h2.heading + p a")
        cast_names = [element.text for element in cast_elements if element.text != '']

        program_data = {
            'url': program_url,
            'title': program_title,
            'supplement': program_supplement,
            'cast_names': cast_names
        }
    except Exception as e:
        print(f"Error scraping program details for {program_id}: {e}")
        program_data = {
            'url': '',
            'title': f'Scraped Program {program_id}',
            'supplement': f'Scraped Details of Program {program_id}',
            'cast_names': []
        }
    
    driver.quit()
    return program_data