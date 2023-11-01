from playwright.sync_api import sync_playwright
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page1 = browser.new_page()
    page1.goto('https://www.dataprivacyframework.gov/s/participant-search')
    sleep(2)

    page1.locator('button.slds-button.slds-button_brand').click()
    page1.locator('button.slds-combobox__input.slds-input_faux.slds-combobox__input-value').first.click()
    sleep(2)
    page1.keyboard.press('ArrowDown')
    sleep(2)
    page1.keyboard.press('Enter')
    
    list_of_inactives = []
    page_num = 0
    sleep(4)
    while (True):
        page_num+=1
        print(f"page: {page_num}")

        selector = 'a.slds-text-heading_small.lgorg'
        elements = page1.locator('a.slds-text-heading_small.lgorg')
        print(elements.count(), 'links')

        for i in range(elements.count()):
            inactive = {}
            e = elements.nth(i)
            company = e.text_content()
            id = e.get_attribute('data-id')
            url = f"https://www.dataprivacyframework.gov/s/participant-search/participant-detail?id={id}&status=Inactive"
            #elements.nth(1).click()

            page2 = browser.new_page()
            page2.goto(url)

            sleep(3)
            infos_locator = page2.locator('div[part="body"].slds-card__body').last.locator('div.slds-col.slds-size_6-of-12.lginside')
            print(infos_locator.count())

            infos_part_1 = infos_locator.nth(0).locator('div').all()
            for q in infos_part_1:
                print(q.text_content())

            infos_part_2 = infos_locator.nth(1).locator('div').all()
            for w in infos_part_2:
                print(w.text_content())

            inactive['Company'] = company
            inactive['Name'] = infos_part_1[0].text_content()
            inactive['Title'] = infos_part_1[1].text_content()
            inactive['Email'] = infos_part_2[0].text_content()
            inactive['Address 1'] = infos_part_1[2].text_content()
            inactive['Address 2'] = infos_part_1[3].text_content()
            inactive['Address 3'] = infos_part_1[4].text_content()
            inactive['Phone'] = infos_part_2[1].text_content().replace("Phone: ", "")
            
            list_of_inactives.append(inactive)
            df = pd.DataFrame(list_of_inactives)
            df.to_excel('inactives.xlsx', index=False)

            page2.close()

        sleep(1)
        next_locator = page1.locator('button[type="button"][part="button"].slds-button.slds-button_neutral').last
        next_button_disabled = next_locator.get_attribute('aria-disabled')
        if next_button_disabled=='false':
            next_locator.click()
        else:
            break
    
    sleep(10)
    browser.close()
