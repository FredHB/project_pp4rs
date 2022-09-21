# Packages
import pandas as pd 
import numpy as np
import argparse

def clean(input_path, storage):
    df = pd.read_csv(input_path)
    df_stor = df[df.storage == storage]

    # First, need to convert location names to English (France, UK and US are safe)
    df_stor.loc[df.location_seller_scraped == 'Deutschland', "location_seller_scraped"] = 'Germany'
    df_stor.loc[df.location_seller_scraped == 'Italy', "location_seller_scraped"] = 'Italy'

    # Renaming and dealing with missings
    df_stor.loc[df.seller_auction == 0, "bids_n_scraped"] = np.nan
    df_stor.rename(columns = {'location_seller_scraped': 'Country', 'price_sold_scraped':'Sale Price', 'bids_n_scraped':'Number of bids in auctions', 'seller_auction': 'Share of auctions'}, inplace = True)

    # Get means and standard deviations per country
    df_by_country = df_stor.groupby('Country').agg(['mean', 'std'])[['Sale Price', 'Number of bids in auctions', 'Share of auctions']]

    # Get overall mean and standard deviation
    df_mean = df_stor[['Sale Price', 'Number of bids in auctions', 'Share of auctions']].mean()
    df_std = df_stor[['Sale Price', 'Number of bids in auctions', 'Share of auctions']].std()


    
    return df_by_country, df_mean, df_std


def create_table(output_path, df_by_country, df_mean, df_std):
    summary_stats = pd.DataFrame([[df_by_country.iloc[0,0], df_by_country.iloc[0,1], df_by_country.iloc[0,2], df_by_country.iloc[0,3], df_by_country.iloc[0,4], df_by_country.iloc[0,5]],
                    [df_by_country.iloc[1,0], df_by_country.iloc[1,1], df_by_country.iloc[1,2], df_by_country.iloc[1,3], df_by_country.iloc[1,4], df_by_country.iloc[1,5]],
                    [df_by_country.iloc[2,0], df_by_country.iloc[2,1], df_by_country.iloc[2,2], df_by_country.iloc[2,3], df_by_country.iloc[2,4], df_by_country.iloc[2,5]],
                    [df_by_country.iloc[3,0], df_by_country.iloc[3,1], df_by_country.iloc[3,2], df_by_country.iloc[3,3], df_by_country.iloc[3,4], df_by_country.iloc[3,5]],
                    [df_by_country.iloc[4,0], df_by_country.iloc[4,1], df_by_country.iloc[4,2], df_by_country.iloc[4,3], df_by_country.iloc[4,4], df_by_country.iloc[4,5]],
                    [df_mean.iloc[0], df_std.iloc[0], df_mean.iloc[1], df_std.iloc[1], df_mean.iloc[2], df_std.iloc[2]]],
                    index=pd.Index(['France', 'Germany', 'Italy', 'United Kingdom', 'United States', 'All'], name='Countries'),
                    columns=pd.MultiIndex.from_product([['Sale Price', 'Number of bids in auctions', 'Share of auctions'],['Mean', 'SD']]))

    summary_stats = summary_stats.style.format('{:.2f}').set_properties(**{'text-align': 'left', 'color': '#444', 'padding': '4px', 'width': '80px'})
    summary_stats = summary_stats.set_table_styles([dict(selector = 'th', props=[('text-align', 'left'), ('color', '#444'), ('font-size', '18px')])])

    with open(output_path, 'w') as f:
        f.write(summary_stats.render())


def main():
    """Main function"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input_path",
        help = "Input path to clean data (csv) file. Default: ./data/clean/data_clean.csv", 
        default = "./data/clean/data_clean.csv",
        type = str
        )

    parser.add_argument(
        "--output_path",
        help = "The path to the output file for the table. Default: ./out/summary_stats.html", 
        type = str, 
        default = "./out/summary_stats.html"
        )

    parser.add_argument(
        "--stor",
        help = "Storage chosen to filter the data on the table. Default: 64.",
        type = int, 
        default = 64
    )


    args = parser.parse_args()
    df_by_country, df_mean, df_std = clean(args.input_path, args.stor)
    create_table(args.output_path, df_by_country, df_mean, df_std)
    

if __name__ == "__main__":
    main()