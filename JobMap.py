""" Scrape Dice and yank all the zip codes """

import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main(city, job):
    """Given a city and a job produce a jobs.csv
    file that has the ZIP code, company and posotion
    """
    driver = webdriver.Firefox()
    driver.get('https://www.dice.com/')
    search_box = driver.find_element_by_id('search-field-keyword')
    search_box.send_keys(job)
    search_location = driver.find_element_by_id('search-field-location')
    search_location.clear()
    search_location.send_keys(city)
    driver.find_element_by_id('findTechJobs').click()

    with open('jobs.csv', 'w') as csvfile:
        jobs_writer = csv.writer(csvfile, dialect='excel')

        while True:
            pagination_count = driver.find_element_by_css_selector('.posiCount > span').get_attribute('innerText')
            start, end = tuple(map(int, pagination_count.replace(',', '').split('-')))
            positions = list(map(
                lambda i: driver.find_element_by_id('position' + str(i)).get_attribute('title'),
                range(end - start + 1)))

            companies = driver.find_elements_by_css_selector('.hidden-xs[itemprop="hiringOrganization"]')
            companies = list(c.get_attribute('title') for c in companies)

            postal_codes = driver.find_elements_by_css_selector(
                ' > '.join([
                    'div.serp-result-content',
                    'ul.list-inline.details.row',
                    'li.location.col-sm-3.col-xs-12.col-md-2.col-lg-3.margin-top-3.text-ellipsis',
                    'span:nth-child(2)',
                    'span:nth-child(2)',
                    'span:nth-child(2)']))
            postal_codes = list(p.get_attribute('innerText') for p in postal_codes)

            try:
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="Go to next page"]')))
                element.click()
            except Exception as exception:
                # must be done
                print(repr(exception))
                break

            jobs_writer.writerows(zip(postal_codes, companies, positions))

    driver.close()


if __name__ == '__main__':
    try:
        _script, city, job = sys.argv
    except ValueError:
        print('python JobMap.py <city name> <job title>')
    else:
        main(city, job)
