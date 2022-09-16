import pandas as pd
import argparse
import datetime
from fredapi import Fred

file = open('src/data/fred_api_key.txt',)
key = file.readlines()[0]
file.close()
fred = Fred(api_key=key)

def clean_data(input_path, output_path) :
    """Function cleans the raw dataset. Needs path to input and to output datafile.

    Args:
        input_path (str): path to raw datafile
        output_path (str): path to clean datafile
        
    Output:
        cleaned data (csv)
    """
    
    df = pd.read_csv(input_path)

    df['currency'] = ""
    df.loc[df.price_sold_scraped.str.match("([0-9, ]*EUR)|(EUR)"), 'currency'] = "EUR"
    df.loc[df.price_sold_scraped.str.match("\$"), 'currency'] = "USD"
    df.loc[df.price_sold_scraped.str.match("£"), 'currency'] = "GBP"
    
    df.loc[:, 'price_sold_scraped'] = df.price_sold_scraped.str.replace("\$|EUR|CHF|£", "") # Getting rid of currency signs
    df.loc[df.shop_code.str.match("de|fr|it"), 'price_sold_scraped'] = df.price_sold_scraped.str.replace(",", ".")[df.shop_code.str.match("de|fr|it")] # swap delimiters
    df.loc[(df.price_sold_scraped.str.count('\.') > 1), 'price_sold_scraped'] = df.price_sold_scraped[(df.price_sold_scraped.str.count('\.') > 1)].replace("\.([0-9][0-9])$", ',\1') # swap delimiters
    df.loc[:, 'price_sold_scraped'] = df.price_sold_scraped.str.replace(r'([0-9 ]*)\.([0-9 ]*)\.([0-9 ]*)', r'\1\2.\3', regex = True) # still swap delimiters...
    
    # Some sellers add a range of prices, we will remove those listings
    df = df[df.price_sold_scraped.str.count("bis") == 0] # German website
    df = df[df.price_sold_scraped.str.count("to") == 0] # American website
    df = df[df.price_sold_scraped.str.count("a") == 0] # Italian website
    df = df[df.price_sold_scraped.str.count("à") == 0] # French website
    df = df.reset_index()
    
    df.price_sold_scraped = pd.to_numeric(df.price_sold_scraped, errors= 'coerce') # Convert to numeric var
 
    # convert final price to numeric
    today = datetime.date.today()
    lastmonth = today - datetime.timedelta(days=30)
    
    forex_per_usd = {
        'EUR' : fred.get_series('DEXUSEU', observation_start=lastmonth, observation_end=today).dropna()[-1],
        'GBP' : fred.get_series('DEXUSUK', observation_start=lastmonth, observation_end=today).dropna()[-1]
    }
    df.price_sold_scraped[df.currency == "EUR"] = df.price_sold_scraped[df.currency == "EUR"] / forex_per_usd['EUR']
    df.price_sold_scraped[df.currency == "GBP"] = df.price_sold_scraped[df.currency == "GBP"] / forex_per_usd['GBP']

    df.bids_n_scraped = df.bids_n_scraped.str.extract("([ 0-9]*)")
    df.bids_n_scraped = df.bids_n_scraped.str.replace(" ", "")
    df.bids_n_scraped = pd.to_numeric(df.bids_n_scraped, errors= 'coerce') # Converting to numeric var

    df.location_seller_scraped = df.location_seller_scraped.str.replace("([a-z]* )", "", n = 1)
    df.date_sale_scraped = df.date_sale_scraped.str.replace("([a-zA-Z]*  )", "")

    df.to_csv(output_path, index = False)
    

def main():
    """Main Function. Calls data cleaning function 'clean_data'. 
    """
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input_path",
        help = "Input path to raw data (csv) file. Default: ./data/raw/data_raw.csv", 
        default = "./data/raw/data_raw.csv",
        type = str
        )
    parser.add_argument(
        "--output_path",
        help = "output path to cleaned data (csv) file. Default: ./data/clean/data_clean.csv", 
        default = "./data/clean/data_clean.csv",
        type = str
        )
    args = parser.parse_args()

    clean_data(args.input_path, args.output_path)

if __name__ == "__main__":
    main()