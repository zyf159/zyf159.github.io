import logging, time, requests, json, pandas as pd
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# 初始化浏览器
chrome_options = ChromeOptions()
chrome_options.add_argument('--disable-infobars')  # 禁用浏览器提示
chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 禁用自动化控制提示
chrome_options.add_argument('--allow-running-insecure-content')  # 允许运行不安全的网页
chrome_options.add_argument("--disable-features=ChromeDriverUpdater")  # 禁用ChromeDriver更新
# chrome_options.add_argument('--unsafely-treat-insecure-origin-as-secure=http://www.scio.gov.cn/')
driver_path = 'D:/python/chromedriver'
driver = Chrome(driver_executable_path=driver_path, options=chrome_options)
# driver = Chrome(options=chrome_options)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}

filePath = "./file.json"
excelPath = "./policy_data.xlsx"

def scrape_policy_list(pageContent: str) -> list:
    """刮取政策列表
    """
    soup = BeautifulSoup(pageContent, 'html.parser')

    policy_list = []

    if soup is not None:
        div = soup.find('div', class_='public-list1')
        if div is not None:
            li_list = div.find_all('li')[1: ]
            for li in li_list:
                policy_dict = {'city': '平顶山', 'isIndustry': True}

                title_link = li.find('a')
                policy_dict['title'] = title_link.text.strip().replace("\n", '')
                base_url = 'https://www.pds.gov.cn'
                policy_dict['url'] = urljoin(base_url, title_link['href'])
                policy_list.append(policy_dict)

        return policy_list

def crawl_policy_list():
    """爬取政策列表
    """
    url = 'https://www.pds.gov.cn/channels/31700.html'

    driver.get(url)

    # 等待页面加载
    time.sleep(10)

    all_policy_list = []

    if driver.page_source is not None:
        #  存储首页页面内容
        policy_list = scrape_policy_list(driver.page_source)

        logging.debug(f"写入数据：{policy_list}")

        if policy_list is not None and len(policy_list) > 0:
            all_policy_list.extend(policy_list)

        for i in range(1, 14):
            try:
                next_page_button = driver.find_element(By.XPATH,
                                                       "//span[@class='public-page-nav clear-float']/a[contains(text(), '下一页')]")

                if next_page_button:
                    next_page_button.click()

                    logging.info(f"Crawling page {i}")

                    # 等待页面加载
                    time.sleep(3)

                    if driver.page_source is not None:
                        #  存储首页页面内容
                        policy_list = scrape_policy_list(driver.page_source)

                        logging.debug(f"写入数据：{policy_list}")

                        if policy_list is not None and len(policy_list) > 0:
                            all_policy_list.extend(policy_list)
                else:
                    break
            except Exception as e:
                logging.error(f"Error clicking next page: {e}")
                break

    # 保存到JSON文件
    with open(filePath, 'w', encoding='utf-8') as f:
        json.dump(all_policy_list, f, ensure_ascii=False, indent=2)
    logging.info(f"Policy list saved to {filePath}")

def crawl_policy_content():
    """爬取政策内容
    """
    logging.info("Start to crawl data...")

    # 从JSON文件读取数据
    with open(filePath, 'r', encoding='utf-8') as f:
        policy_list = json.load(f)

    # 处理数据
    updated_policy_list = []
    for policy in policy_list:
        if 'content' not in policy:
            logging.info(f"crawl page: {policy['url']}")

            try:
                html = requests.get(policy['url'], headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
                html = html.content.decode('utf-8')

                soup = BeautifulSoup(html, 'html.parser')

                # 获取文档属性数据
                table = soup.find('div', class_='xxgk-table xgyd-xxgk-table')

                if table is not None:
                    ul_list = table.find_all('ul')

                    for ul in ul_list:
                        li = ul.find_all('li')
                        if len(li) > 5 and '发布日期' in li[4].text:
                            policy['release_date'] = li[5].text.strip()

                        if len(li) > 1:
                            if '发文字号' in li[0].text:
                                policy['file_number'] = li[1].text.strip()

                            if '主题分类' in li[0].text:
                                policy['category'] = li[1].text.strip()

                    policy['publisher'] = ''
                    policy['written_date'] = ''

                    div = soup.find('div', class_='article')
                    if div:
                        policy['content'] = div.text.strip()

                logging.info(f"写入数据：{policy}")
                time.sleep(3)
            except Exception as e:
                logging.error(f"Error crawling content: {e}")
        updated_policy_list.append(policy)

    # 保存更新后的数据到JSON文件
    with open(filePath, 'w', encoding='utf-8') as f:
        json.dump(updated_policy_list, f, ensure_ascii=False, indent=2)
    logging.info(f"Updated policy data saved to {filePath}")

def generate_excel():
    """生成Excel文件
    """
    # 从JSON文件读取数据
    with open(filePath, 'r', encoding='utf-8') as f:
        policy_list = json.load(f)

    # 转换为DataFrame
    df = pd.DataFrame(policy_list)

    # 保存到Excel文件
    df.to_excel(excelPath, index=False, engine='openpyxl')
    logging.info(f"Excel file generated at {excelPath}")


if __name__ == '__main__':
    # 爬取政策列表
    crawl_policy_list()
    # 爬取政策内容
    crawl_policy_content()
    # 生成Excel文件
    generate_excel()
