from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import chromedriver_autoinstaller

def get_magalu(driver):
    findings = []
    try:
        # Navigate to Magazine Luiza's games section
        driver.get('https://www.magazineluiza.com.br/games/l/ga/')

        # Locate the search bar, enter 'Playstation 5' and hit Enter
        search_box = driver.find_element(By.ID, 'input-search')
        search_box.send_keys('Playstation 5')
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="product-list"]'))
        )

        # Find the element with data-testid="product-list"
        product_list_element = driver.find_element(By.CSS_SELECTOR, '[data-testid="product-list"]')

        # Find all <li> elements within the product list element
        li_elements = product_list_element.find_elements(By.TAG_NAME, 'li')

        # Print the text content of each <li> element
        for index, li in enumerate(li_elements[:3]):
            # product-title
            product_title_el = li.find_element(By.CSS_SELECTOR, '[data-testid="product-title"]')

            price_el = driver.find_element(By.CSS_SELECTOR, '[data-testid="price-value"]')
            item = {
                'source': 'Magazine Luiza',
                'title': product_title_el.text,
                'price': price_el.text
            }

            findings.append(item)
            print(item)
    except Exception as e:
        print(e)
    return findings

def get_kabum(driver):
    findings = []
    try:
        # Navigate to Kabum's gamer section
        driver.get('https://www.kabum.com.br/gamer')

        # Locate the search bar, enter 'Playstation 5' and hit Enter

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'input-busca'))
        )
        search_box = driver.find_element(By.ID, 'input-busca')
        search_box.send_keys('Playstation 5')
        search_box.send_keys(Keys.RETURN)

        # Wait for the results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="listing"]/div[3]/div/div/div[2]/div/main'))
        )


        # Find the element that contains the product list
        product_elements = driver.find_elements(By.XPATH, "//*[@id=\"listing\"]/div[3]/div/div/div[2]/div/main/article")

        # Extract and print the title and price of each product
        for index, product in enumerate(product_elements[:3]):
            title_element = product.find_element(By.CSS_SELECTOR, "span[class$='nameCard']") 
            price_element = product.find_element(By.CSS_SELECTOR, "span[class$='priceCard']") 

            findings.append({
                'source': 'Kabum',
                'title': title_element.text,
                'price': price_element.text
            })

            print(f'Product {index + 1}: {title_element.text} - {price_element.text}')
    except Exception as e:
        print(e)
    return findings


def run():
    chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                          # and if it doesn't exist, download it automatically,
                                          # then add chromedriver to path

    driver = webdriver.Chrome()

    input("Press Enter to start the search...")


    findings = []
    findings += get_magalu(driver)

    input("Press Enter to continue the search...")

    findings += get_kabum(driver)

    input("Press Enter to calculate the best price...")


    driver.quit()
    # get better price option
    findings = sorted(findings, key=lambda x: float(x['price'].replace('R$', '').replace('.', '').replace(',', '.')))

    print(f"Best price: {findings[0]['source']} - {findings[0]['title']} - {findings[0]['price']}")
    return findings

run()