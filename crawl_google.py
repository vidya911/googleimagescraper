import urllib
from selenium import webdriver
import csv
import sys
from bs4 import BeautifulSoup
from core import SITE_URL
from pyvirtualdisplay import Display


display = Display(visible=0, size=(800, 600))
display.start()


def visit_walk_google(search_string):
    """
    Open google.com and search for funny images
    """

    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(SITE_URL)
    driver.implicitly_wait(3)
    search_box = driver.find_element_by_name('q')
    search_box.send_keys(search_string)
    driver.find_element_by_name('btnG').click()
    get_inside_image_search_page(driver, search_string)


def get_inside_image_search_page(driver, search_string):
    """
    Get all search link from the main search page with desired images
    """

    # driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[4]/div[3]/div/div/div[1]/div/div/div[2]/a').click()
    all_header_menu = driver.find_elements_by_class_name('qs')
    for each in all_header_menu:
        if each.text == 'Images':
            each.click()
            break
    #_google_image_tab = [each_tab for each_tab in soup.findAll('div',{'class':'hdtb-mitem'}) if 'Images' in each_tab.text]
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    check_more_images(driver)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    all_image_soup = soup.findAll("a", {"class": "rg_l"})
    all_images_links = get_all_images_links(all_image_soup)
    filename = '-'.join(search_string.split(' ')) + '_images.txt'
    f = open(filename, 'wb')
    for each_image in all_images_links:
        f.write(each_image)
        f.write('\n')
    f.close()


def get_all_images_links(all_image_soup):
    image_urls = []
    for each_image in all_image_soup:
        try:
            image_unparsed_link = each_image.attrs.get('href')
            image_url = get_image_url(image_unparsed_link)
            image_extension = image_url.split('.')[-1]
            if image_extension.lower() in ['jpg', 'png', 'gif']:
                image_urls.append(image_url)
        except:
            pass
    return image_urls


def check_more_images(driver):
    try:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_id('smb').click()
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        check_more_images(driver)
    except:
        return  # driver


def get_image_url(image_unparsed_link):
    image_url = image_unparsed_link.split('imgurl=')[1].split('&')[0]
    return image_url

if __name__ == "__main__":
    search_string = sys.argv[1]
    visit_walk_google(search_string)

display.stop()
