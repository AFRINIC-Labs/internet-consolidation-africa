from bs4 import BeautifulSoup
import requests
import pandas

countries = []
base_url = 'https://www.telegeography.com/'
links = []
dates = []
companies = []
african_countries = []


def scrap_site():
    """
    This function scraps data from a website and saves to CSV document.
    :return: A CSV file containing scrapped data
    """
    with open('countries.txt', 'r') as txt:
        countries_buffer = txt.readlines()
        for country in countries_buffer:
            countries.append(country.replace('\n', ''))

    for country in countries:
        print('Processing ' + country)
        search_url = 'https://www.telegeography.com/products/commsupdate/articles/search/?words=country:(+' \
                     + country + ')AND tag:(Mergers/Acquisitions)'
        request = requests.get(search_url)
        dom = BeautifulSoup(request.content, 'html.parser')
        limit = dom.h3.get_text()
        try:
            limit = int(limit.split()[-2])
        except IndexError:
            continue

        if limit:
            for i in range(0, limit, 10):
                if limit <= 10:
                    find_elements(dom, country)

                else:
                    request = requests.get(search_url + '&o=' + str(i))
                    dom = BeautifulSoup(request.content, 'html.parser')
                    find_elements(dom, country)

            print('Done processing ' + country)

    for link in links:
        print('Visiting links')
        deal_companies = []
        request = requests.get(link)
        dom = BeautifulSoup(request.content, 'html.parser')
        for company in dom.select('.companies > a'):
            deal_companies.append(company.get_text())
        companies.append(deal_companies)

    print('Done processing links')
    write_csv()


def write_csv():
    print('About to write CSV')
    data = pandas.DataFrame({'Date': dates, 'Link': links, 'Companies': companies, 'Countries': african_countries})
    data.to_csv("Research.csv", encoding='utf-8', index=False)
    print('Done writing CSV')


def find_elements(dom: BeautifulSoup, country: str):

    for link in dom.select('div > h2 > a'):
        links.append(base_url + link.get('href'))
        african_countries.append(country)

    date: BeautifulSoup
    for date in dom.select('.search-result-date > a'):
        dates.append(date.get_text().trim())


if __name__ == "__main__":
    scrap_site()
