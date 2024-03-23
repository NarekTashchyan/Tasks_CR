import csv
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By



def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestsWarning as e:
        print(e)


def extract_job_info(job):
    job_name = job.find('p', class_='font_bold').get_text(strip=True)
    company = job.find('p', class_='job_list_company_title').get_text(strip=True)
    deadline = job.find('div', class_='badge_deadline_block').get_text(strip=True)
    location = job.find('p', class_='job_location').get_text(strip=True)
    return {'Job Name': job_name, 'Company': company, 'Deadline': deadline, 'Location': location}


def scrape_jobs(html):
    soup = BeautifulSoup(html, 'html.parser')
    jobs = soup.find_all('div', class_='right_radius_change')
    return [extract_job_info(job) for job in jobs]


def scrape_all_pages(driver, url):
    driver.get(url)
    driver.find_element(By.ID, 'w1').find_element(By.CLASS_NAME, "hs_nav_link").click()
    jobs = scrape_jobs(driver.page_source)
    next_button = driver.find_element(By.CLASS_NAME, 'pagination').find_element(By.CLASS_NAME, 'next')
    while True:
        jobs += scrape_jobs(driver.page_source)
        if 'disabled' in next_button.get_attribute('class'):
            break
        next_button.click()
        time.sleep(1)
        next_button = driver.find_element(By.CLASS_NAME, 'pagination').find_element(By.CLASS_NAME, 'next')
    return jobs


def save_to_csv(jobs):
    with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Job Name', 'Company', 'Deadline', 'Location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)


def main():
    url = "https://staff.am/en"
    driver = webdriver.Chrome()
    jobs = scrape_all_pages(driver, url)
    save_to_csv(jobs)
    driver.quit()
    print("Scraped job data saved successfully to Data.csv")

main()



