# Packages
from xml.etree.ElementTree import tostring
import requests 
import bs4 
import pandas as pd
import argparse

# Generate a scrape-able eBay search URL
def generate_search_url(params = {
                        "shop_code" : "de",
                        "local_listings" : 1, 
                        "search_key" : '"iphone x" -(defekt, defect, defunct, damaged)',
                        "model" : "Apple iPhone X",
                        "lock" : "Factory Unlocked",
                        "storage" : 64,
                        "condition" : 3000,
                        "sold" : 1,
                        "n_items_per_page" : 240,
                        "sell_auth" : 0,
                        "sell_store" : 0,
                        "sell_auction" : 1
                    }
    ) :
    
    """Function generates a valid search URL for eBay and a dictionary detailing the search request.

    Returns:
        str: URL string
    """
    
    # collect the full request in a dictionary
    search_prompt = {
        "shop" : ("https://www.ebay." + params['shop_code'] + "/sch/i.html?"), # ebay
        "cat" : "&_dcat=9355", # item category
        "ns1" : "&_fsrp=1&rt=nc&_from=R40", # not sure about these
        "ns2" : "&_fss=1", # dont know about this one yet 
        "ns3" : "&_sacat=0", # unknown, too
        "local_listings" : "&LH_PrefLoc="+str(params['local_listings']), # local ebay site only
        "search_key" : '&_nkw='+params['search_key'].replace(" ", "+"), # required search prompt, verbatim quotes
        "model" : "&Model=" + params['model'].replace(" ", "%2520"),  # model: iphone x
        "lock" : "&Lock%2520Status="+params['lock'].replace(" ", "%2520"), # band: factory unlocked
        "storage" : "&Storage%2520Capacity="+str(params['storage'])+"%2520GB",  # storage capacity: 64
        "condition" : "&LH_ItemCondition="+str(params['condition']), # condition: used
        "sold" : "&LH_Sold="+str(params['sold']), # sold items only
        "n_items" : "&LH_TitleDesc=0&_ipg="+str(params['n_items_per_page']), # items per page: 240
        "sell_auth" : "&LH_AS="+str(params['sell_auth']),  # no authorized sellers
        "sell_store" : "&LH_SellerWithStore="+str(params['sell_store']), # no sellers with store
        "sell_auction" : "&LH_Auction="+str(params['sell_auction']), # only search for auctions
    }
    
    # concatenate dictionary    
    url = ""
    for key in search_prompt.keys() :
        if not (key.startswith(("ns1", "ns2", "ns3"))) : 
            url = url + search_prompt[key]

    return url

# Get data using beautifulsoup 
def get_data(url):
    """Use website URL to get data using beautiful soup"""
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup

#url = "https://www.ebay.com/sch/i.html?_fsrp=1&_from=R40&_nkw=iphone+13+pro+max&_sacat=0&LH_Sold=1&rt=nc&LH_Auction=1"
#soup = get_data(url)

# Parsing and extracting all the relevant information
def parse(soup, search_params):
    """Parse data and obtain important info and append to dictionary"""
    
    all_listings = soup.find_all("div", class_ = "s-item__info clearfix")
    all_listings = all_listings[1:] # Element 0 is a weird one without any actual info that's causing me problems, so let me eliminate that
    
    data = []
    for product in all_listings:
        subtitles = product.find_all("div", class_ = "s-item__subtitle")[0].text.split(" · ")
        title = product.find("div", class_ = "s-item__title s-item__title--has-tags").text
        #print(title)
        price_sold = product.find("span", class_ = "s-item__price").text
        #print(price_sold)
        if str(search_params['sell_auction']) == '1' : 
            bids_n = product.find("span", class_ = "s-item__bids s-item__bidCount").text
            print(bids_n)
        else : bids_n = "0 bids"
        #print(bids_n)
        location_seller = product.find("span", class_ = "s-item__location s-item__itemLocation").text
        date_sale = product.find("div", class_ = "s-item__title--tagblock").find("span", class_ = "POSITIVE").text
        data.append({
            "title_scraped": title, 
            "price_sold_scraped": price_sold,
            "bids_n_scraped": bids_n,
            "product_scraped": subtitles,
            "location_seller_scraped": location_seller,
            "date_sale_scraped": date_sale,
            "shop_code": search_params['shop_code'],
            "condition": search_params['condition'], #subtitles[0],
            "storage": search_params['storage'], #subtitles[2],
            "locked": search_params['lock'], #subtitles[3]
            "model": search_params['model'], #subtitles[3]
            "seller_authorized": search_params['sell_auth'],
            "seller_hasstore": search_params['sell_store'],
            "seller_auction": search_params['sell_auction'] 
            })
    #print(data)
    return data

# Create pandas data frame
def output(data):
    """Create pandas data frame based on dictionary"""
    df =  pd.DataFrame(data)
    return df

def main():
    """Main function"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output_path",
        help = "The path to the output file", 
        type = str, 
        default = "./data/raw/data_raw.csv"
        )
    parser.add_argument(
        "--domain_list",
        help = "List of eBay domains (string) corresponding to countries", 
        nargs = "*",
        default = ["com"]
    )
    parser.add_argument(
        "--search_key",
        help = "The search key to be used in the search request", 
        default = '"iphone x" -(defekt, defect, defunct, damaged)',
        type = str
        )
    parser.add_argument(
        "--model",
        help = "Model name of device in eBay.", 
        default = "Apple iPhone X",
        type = str
        )
    parser.add_argument(
        "--lock",
        help = "Device is factory locked/unlocked.", 
        default = "Factory Unlocked",
        type = str
        )
    parser.add_argument(
        "--storage_list",
        help = "Device storage.", 
        nargs = '*',
        default = [64],
        )
    parser.add_argument(
        "--condition",
        help = "Device condition (numeric, eBay specific. 3000 = 'used').", 
        default = [3000],
        nargs = '*',
        type = int
        )
    parser.add_argument(
        "--sold",
        help = "Only scrape data of sold listings.", 
        default = 1,
        type = int
        )
    parser.add_argument(
        "--n_items_per_page",
        help = "Scrape n items per page (attn: only first page is scraped anyways).", 
        default = 240,
        type = int
        )
    parser.add_argument(
        "--local_listings",
        help = "Only include listings local to the eBay shop in search request", 
        default = 1,
        type = int
    )
    parser.add_argument(
        "--sell_auth",
        help = "Whether to only include authorized sellers.", 
        default = 0,
        type = int
        )
    parser.add_argument(
        "--sell_store",
        help = "Whether to only include sellers with eBay shops.", 
        default = 0,
        type = int
        )
    parser.add_argument(
        "--auctions_list",
        help = "Whether to only include auctions. Numeric list to loop over.", 
        default = [0,1],
        nargs = '*'
        )

    args = parser.parse_args()

    df_main = pd.DataFrame()
    for condition in args.condition :
        for domain in args.domain_list:
            for storage in args.storage_list:
                for isauction in args.auctions_list:
                    
                    # collect all search parameters in a dictionary
                    search_params = {
                        "local_listings" : args.local_listings, # local ebay site only
                        "search_key" : args.search_key, # required search prompt, verbatim quotes
                        "model" : args.model,  # model: iphone x
                        "lock" : args.lock, # band: factory unlocked
                        "storage" : storage,  # storage capacity: eg 64, 128, 256
                        "condition" : condition, # condition: used (=3000)
                        "sold" : args.sold, # sold items only
                        "n_items_per_page" : args.n_items_per_page, # items per page: 240
                        "sell_auth" : args.sell_auth,  # no authorized sellers
                        "sell_store" : args.sell_store, # no sellers with store
                        "sell_auction" : isauction, # only search for auctions
                        "shop_code": domain
                    }
                    
                    [print(par, ": \n    ", search_params[par]) for par in search_params]
                    
                    url = generate_search_url(
                        params = search_params
                        )
                    
                    [print(par, ": \n    ", search_params[par]) for par in search_params]

                    print("\n\nThe search URL is: \n   ", url)

                    soup = get_data(url)
                    data = parse(soup, search_params)
                    df = output(data)
                    df_main = pd.concat([df_main, df])
                
    df_main.to_csv(args.output_path, index = False)

if __name__ == "__main__":
    main()