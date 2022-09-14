import pandas as pd
import argparse

def clean_data(input_path, output_path) :
    """Function cleans the raw dataset. Needs path to input and to output datafile.

    Args:
        input_path (str): path to raw datafile
        output_path (str): path to clean datafile
        
    Output:
        cleaned data (csv)
    """
    
    df = pd.read_csv(input_path)

    df = df[df.price_sold_scraped.str.count(" ") == 1] # remove sellers with repeated sale of item
    df = df.reset_index()
    df['currency'] = ""
    df.currency[df.price_sold_scraped.str.match("EUR")] = "EUR"
    df.currency[df.price_sold_scraped.str.match("\$")] = "USD"
    df.currency[df.price_sold_scraped.str.match("£")] = "GBP"

    df.price_sold_scraped = df.price_sold_scraped.str.replace("\$|EUR|CHF|£", "") # Getting rid of currency signs
    df.price_sold_scraped[df.shop_code.str.match("de|fr|it")] = df.price_sold_scraped.str.replace(",", ".")[df.shop_code.str.match("de|fr|it")] # swap delimiters
    df.price_sold_scraped[(df.price_sold_scraped.str.count('\.') > 1)] = df.price_sold_scraped[(df.price_sold_scraped.str.count('\.') > 1)].replace("\.([0-9][0-9])$", ',\1') # swap delimiters
    df.price_sold_scraped = df.price_sold_scraped.str.replace(r'([0-9 ]*)\.([0-9 ]*)\.([0-9 ]*)', r'\1\2.\3', regex = True) # still swap delimiters...
    df.price_sold_scraped = pd.to_numeric(df.price_sold_scraped, errors= 'coerce') # Convert to numeric var

    df.bids_n_scraped = df.bids_n_scraped.str.extract("([ 0-9]*)")
    df.bids_n_scraped = df.bids_n_scraped.str.replace(" ", "")
    df.bids_n_scraped = pd.to_numeric(df.bids_n_scraped, errors= 'coerce') # Converting to numeric var

    df.location_seller_scraped = df.location_seller_scraped.str.replace("([a-z]* )", "")
    df.date_sale_scraped = df.date_sale_scraped.str.replace("([a-zA-Z]*  )", "")

    df.to_csv(output_path, index = False)
    

def main():
    """Main Function. Calls data cleaning function 'clean_data'. 
    """
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input_path",
        help = "Input path to raw data (csv) file.", 
        default = "./data/raw/data_raw.csv",
        type = str
        )
    parser.add_argument(
        "output_path",
        help = "output path to cleaned data (csv) file.", 
        default = "./data/clean/data_clean.csv",
        type = str
        )
    args = parser.parse_args()

    clean_data(args.input_path, args.output_path)

if __name__ == "__main__":
    main()