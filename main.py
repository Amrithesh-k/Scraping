from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd
from pathlib import Path

def Scraper(uname,passwd):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://www.texasgasservice.com/account")
            page.fill("input#txtusername", uname)
            page.fill("input#txtpassword", passwd)
            page.click('.btn-blue.full-width')

            # Additional click handling (if needed)
            try:
                page.click('.fsrButton.fsrButton__inviteDecline.fsrDeclineButton')
            except:
                pass
            
            page.wait_for_selector('span[_ngcontent-ng-c3434576881=""]')
            account_number_elements = page.query_selector_all('span[_ngcontent-ng-c3434576881=""]')
            account_numbers = [el.inner_text() for el in account_number_elements]
            acc_no = account_numbers[1]
            print(account_numbers)
            page.click('#ngb-nav-3')
            page.click('#ngb-nav-6')

            bill_row_elements = page.query_selector_all('div.bill-row')
            bill_rows = [el.inner_html() for el in bill_row_elements]

            cleaned_data = []
            for item in bill_rows:
                soup = bs(item, 'html.parser')
                text = soup.get_text(strip=True)
                cleaned_data.append(text)

            pTWM = cleaned_data[:12]

            cl_list = []
            for i in range(len(pTWM)):
                elm = pTWM[i].split()
                l = [elm[2].replace(",", ""), elm[4]]
                cl_list.append(l)

            nparr = np.array(cl_list)
            csv = ".csv"
            print(cl_list)
            folder_path = Path('AccountNum') / (acc_no + csv)
            col_names = ["BILL", "DATE"]
            df = pd.DataFrame(cl_list, columns=col_names)
            df.to_csv(folder_path, index=False)

            browser.close()
        return acc_no
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def finder(acc_no):
    try:
        csv=".csv"
        folder_path = Path('AccountNum')/(acc_no+csv)
        df=pd.read_csv(folder_path)
        return df
    except:
        return "Account Number Not Found"

if __name__ == "__main__":
    uname = input("Enter Username:")
    passwd = input("Enter Password:")
    acc_no=Scraper(uname,passwd)
    print(finder(acc_no))
