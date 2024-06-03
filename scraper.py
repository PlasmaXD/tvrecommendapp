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
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
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
