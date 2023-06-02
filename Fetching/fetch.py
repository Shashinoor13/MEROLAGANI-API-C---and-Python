from requests_html import HTMLSession
import re
import json


# Initializing an empty array to store the data
data = {}
# Specify the file name
filename = "./JSON/shares.json"
# Initializing the session
session = HTMLSession()


# Getting the list of Companies from the table
r = session.get("https://merolagani.com/MarketSummary.aspx?type=turnovers")


# Checking is the conenction is Sucessfull
print(r.status_code)


# Rendering the page to get the dynamically loaded content
r.html.render(sleep=1, scrolldown=1)


# Getting the list of Companies from the table
table = r.html.xpath('//*[@id="ctl00_ContentPlaceHolder1_tblSummary"]', first=True)


# Looping through every item in the table that has an absolute link
# To get more inforamtion about the company
# Then extracting the NEPSE code from the name

for item in table.absolute_links:
    r = session.get(item)
    # Xpath to get the name and sector of the company
    name = r.html.xpath(
        '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_companyName"]', first=True
    ).text
    sector = r.html.xpath('//*[@id="accordion"]/tbody[1]/tr/td', first=True).text
    # Pattern Observed in the name to extract the NEPSE code
    pattern = r"\((.*?)\)"
    result = re.search(pattern, name)
    market_price = r.html.xpath(
        '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_lblMarketPrice"]', first=True
    ).text
    change = r.html.xpath(
        '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_lblChange"]', first=True
    ).text
    shares_outstanding = r.html.xpath(
        '//*[@id="accordion"]/tbody[2]/tr/td', first=True
    ).text
    last_traded_on = r.html.xpath(
        '//*[@id="accordion"]/tbody[5]/tr/td', first=True
    ).text

    if result:
        extracted_text = result.group(1)
        print(f"Name:{name}: ,Sector:{sector},Code:{extracted_text},Link:{item}")
        Info = {
            "name": name,
            "sector": sector,
            "code": extracted_text,
            "link": item,
            "market-price": market_price,
            "change": change,
            "shares-outstanding": shares_outstanding,
            "last-traded-on": last_traded_on,
        }
        data[extracted_text] = Info
    else:
        print(f"Name:{name}: ,Sector:{sector},Code:None")
        Info = {
            "name": name,
            "sector": sector,
            "code": "None",
            "link": item,
            "market-price": market_price,
            "change": change,
            "shares-outstanding": shares_outstanding,
            "last-traded-on": last_traded_on,
        }
        data[extracted_text] = Info

with open(filename, "w") as file:
    json.dump(data, file)  # Write the list of dictionaries as JSON

print("Data written to", filename)


session.close()
