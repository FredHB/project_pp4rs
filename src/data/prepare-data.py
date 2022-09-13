# Packages
import requests 
import bs4 
import pandas as pd
from datetime import datetime

# Get data using beautifulsoup 
def get_data(url):
    """Use website URL to get data using beautiful soup"""
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup

#url = "https://www.ebay.com/sch/i.html?_fsrp=1&_from=R40&_nkw=iphone+13+pro+max&_sacat=0&LH_Sold=1&rt=nc&LH_Auction=1"
#soup = get_data(url)

# Parsing and extracting all the relevant information
def parse(soup):
    """Parse data and obtain important info and append to dictionary"""
    all_listings = soup.find_all("div", class_ = "s-item__info clearfix")
    all_listings = all_listings[1:] # Element 0 is a weird one without any actual info that's causing me problems, so let me eliminate that

    data = []

    for product in all_listings:
        subtitles = product.find_all("div", class_ = "s-item__subtitle")[0].text.split(" · ")
        if len(the_list) == 4:
            title = product.find("div", class_ = "s-item__title s-item__title--has-tags").text
            price_sold = product.find("span", class_ = "s-item__price").text
            bids_n = product.find("span", class_ = "s-item__bids s-item__bidCount").text
            location_seller = product.find("span", class_ = "s-item__location s-item__itemLocation").text
            date_sale = product.find("div", class_ = "s-item__title--tagblock").find("span", class_ = "POSITIVE").text
            data.append({
                "title": title, 
                "price_sold": price_sold,
                "bids_n": bids_n,
                "location_seller": location_seller,
                "date_sale": date_sale,
                "condition": subtitles[0],
                "product": subtitles[1],
                "storage": subtitles[2],
                "locked": subtitles[3]
                })
    return data

# Create pandas data frame
def output(data):
    """Create pandas data frame based on dictionary"""
    df =  pd.DataFrame(data)
    return df

# Clean data set 
def clean(df):
    """Clean data set, by removing extra info and transforming data types"""
    df.price_sold = df.price_sold.str.replace("$", "") # Getting rid of dollar signs
    df.price_sold = pd.to_numeric(df.price_sold.str.replace(",", "")) # Converting to numeric var

    df.bids_n = df.bids_n.str.replace(" bids", "") # Getting rid of "bids"
    df.bids_n = df.bids_n.str.replace(" bid", "") # Getting rid of "bid"
    df.bids_n = pd.to_numeric(df.bids_n) # Converting to numeric var

    df.location_seller = df.location_seller.str.replace("from ", "")

    df.date_sale = df.date_sale.str.replace("Sold ", "")
    df.date_sale = pd.to_datetime(df.date_sale) # convert into date

    return df

def main():
    """Main function"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "output_path",
        help = "The path to the output file", 
        type = str
        )

    args = parser.parse_args()

    # url = "https://www.ebay.com/sch/i.html?_fsrp=1&_from=R40&_nkw=iphone+13+pro+max&_sacat=0&LH_Sold=1&rt=nc&LH_Auction=1"

    soup = get_data(url)
    data = parse(soup)
    df = output(data)
    df_clean = clean(df)

    df.to_csv(args.output_path, index = False)


if __name__ == "__main__":
    main()