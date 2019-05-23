#!/usr/bin/python
# encoding: utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def set_zd_url(query):
    import urllib

    query = urllib.quote(str(query))
    url = 'https://dict.baidu.com/s?wd=' + query + '&from=zici'

    return url


def get_web_response(url):
    # 构造浏览器，传入地址，返回页面
    from selenium import webdriver

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
    browser.get(url)

    return browser


def get_dict(browser):
    rt = {}
    word = browser.find_element_by_css_selector('#pinyin strong')
    pinyin = browser.find_element_by_css_selector('dt.pinyin')
    jieshis = browser.find_elements_by_css_selector('#basicmean-wrapper dd p')
    rt['word'] = word.text
    rt['pinyin'] = pinyin.text
    rt['jieshi'] = [x.text for x in jieshis]

    return rt


def get_web_data(query):
    url = set_zd_url(query)
    browser = get_web_response(url)
    # 加入判断条件，判断依据为页面关键词中是否包含查询词语
    keyword_of_page = browser.find_element_by_name('keywords')

    if (keyword_of_page.get_attribute('content') == query):
        # print u'直接命中！'
        rt = get_dict(browser)
    else:
        # 如果为汇总页面，则获取第一个条目的链接，然后获取信息
        target_href_object = browser.find_elements_by_css_selector('#data-container div a[href*="zici"]')
        url = target_href_object[0].get_attribute('href')
        browser = get_web_response(url)
        rt = get_dict(browser)
        # print target_href_object.__str__(), url

    browser.close()
    return rt


def main():
    rt = get_web_data(sys.argv[1])
    sys.stdout.write(rt.__str__())


if __name__ == '__main__':
    main()
