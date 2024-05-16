from playwright.sync_api import sync_playwright
import pandas as pd

def Scraper(uname, passwd):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            print('AEP: Successfully launched browser and created a new page.')

            # Task 1: Login to the website
            page.goto("https://www.texasgasservice.com/account")
            page.fill("input#txtusername", uname)
            page.fill("input#txtpassword", passwd)
            page.click('.btn-blue.full-width')
            print('AEP: Logged in successfully.')

            # Additional click handling (if needed)
            try:
                page.click('.fsrButton.fsrButton__inviteDecline.fsrDeclineButton')
            except:
                pass
            
            page.wait_for_selector('span[_ngcontent-ng-c3434576881=""]')
            account_number_elements = page.query_selector_all('span[_ngcontent-ng-c3434576881=""]')
            account_numbers = [el.inner_text() for el in account_number_elements]
            acc_no = account_numbers[1]
            print(acc_no)

            # Task 3: Navigate to the page with the table of bills
            page.click('#ngb-nav-3')
            page.click('#ngb-nav-6')

            # Task 4: Wait for bill rows to load
            page.wait_for_selector('div.bill-row')

            bill_row_elements =page.query_selector_all('div.bill-row')
            bill_rows = [el.inner_html() for el in bill_row_elements]
            twelvebills=bill_rows[:12]

            cleaned_data = [s.replace('<span _ngcontent-ng-c366551828="">', '').replace('</span>', '') for s in twelvebills]
            
            print(cleaned_data)

            cl_list = []
            
            for i in range(len(twelvebills)):
                elm = cleaned_data[i].split()
                l = [elm[2].replace(",", ""), elm[4]]
                cl_list.append(l)

            
            csv_file = f"AccountNum/{acc_no}.csv"
            col_names = ["BILL", "DATE"]
            df = pd.DataFrame(cl_list, columns=col_names)
            df.to_csv(csv_file, index=False)

            browser.close()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def finder(acc_no):
    try:
        csv_file = f"AccountNum/{acc_no}.csv"
        df = pd.read_csv(csv_file)
        return df
    except:
        return "Account Number Not Found"

if __name__ == "__main__":
    uname = input("Enter Username:")
    passwd = input("Enter Password:")
    acc_no = Scraper(uname, passwd)
    print(finder(acc_no))
