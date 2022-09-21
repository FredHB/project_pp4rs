# Packages
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import country_converter as coco
import altair as alt
from vega_datasets import data
import argparse
import numpy as np

def clean(input_path, stor):
    """Cleaning data for graphs and creating new filtered data frames"""
    df = pd.read_csv(input_path)

    # First, need to convert location names to English (France, UK and US are safe)
    df.loc[df.location_seller_scraped == 'Deutschland', "location_seller_scraped"] = 'Germany'
    df.loc[df.location_seller_scraped == 'Italy', "location_seller_scraped"] = 'Italy'

    # Next, need to convert storage to a categorical variable to be able to use catplot 
    df['storage'] = df.storage.astype('category')

    # Martin, don't judge us but very annoying outliers are killing our nice figures, so we'll drop the max
    df = df.loc[df['price_sold_scraped']!=df['price_sold_scraped'].max()]

    # Create data frame with storage == 64, which will be the default for almost all graphs 
    df_stor = df[df.storage == stor]

    # Create data frame with storage == 64 and auction == 1
    df_stor_auction = df[(df.storage == stor) & (df.seller_auction == 1)]

    return df, df_stor, df_stor_auction

def hist_price(df, output_path_hist_price): 
    """Creating histogram of sale price"""
    n, bins, patches = plt.hist(x=df.price_sold_scraped, bins=50, color='#0504aa',
                            alpha=0.7, rwidth=0.85, density = True)
    plt.grid(False)
    plt.xlabel('Sale Price')
    plt.title("Distribution of Sale Price")

    plt.savefig(output_path_hist_price)
    plt.close()

def hist_price_auction(df, output_path_hist_price_auction):
    """Creating histogram of sale price by auction/non-auction"""
    hist_auction = sns.histplot(data=df, x="price_sold_scraped", 
                hue="seller_auction", bins = 50, alpha = .4, stat = 'density', palette = "Greys")

    hist_auction.set_xlabel("Sale Price")
    hist_auction.set_title("Distribution of Sale Price by Sale Format")
    hist_auction.legend(labels=["Direct Sale","Auction"])

    hist_auction.figure.savefig(output_path_hist_price_auction)
    plt.close()

def hist_price_storage(df, output_path_hist_price_storage):
    """Creating histogram of sale price by phone storage"""

    hist_storage = sns.FacetGrid(df, col="storage", col_wrap = 2, height = 5, aspect = 1.2)
    hist_storage.map(sns.histplot, "price_sold_scraped", stat = 'density', bins = 50)
    hist_storage.set_axis_labels("Sale Price ($)")
    hist_storage.set_titles(col_template="{col_name} GB")
    hist_storage.fig.subplots_adjust(top=0.9)
    hist_storage.fig.suptitle("Distribution of Sale Price by Storage")
    hist_storage.figure.savefig(output_path_hist_price_storage)

    plt.close()


def graph_country_bids_price(df_stor_auction, output_path_graph_country_bids_price):
    """Creating interactive graph of relationship between bids and price per country"""

    click = alt.selection_multi(encodings=['color'])

    scatter = alt.Chart(df_stor_auction).mark_point().encode(
        x=alt.X('price_sold_scraped:Q', title = "Sale Price"),
        y=alt.Y('bids_n_scraped:Q', title = "Number of bids"),
        color=alt.Color('location_seller_scraped:N', title = "Location")
    ).transform_filter(
        click
    )

    hist = alt.Chart(df_stor_auction).mark_bar().encode(
        x='count()',
        y=alt.Y('location_seller_scraped', title = "Location"),
        color=alt.condition(click, 'location_seller_scraped', alt.value('lightgray'))
    ).add_selection(
        click
    )

    chart = scatter & hist
    chart.save(output_path_graph_country_bids_price) # should save in html

def clean_country_data(df_stor):
    """Clean country data to map to json file"""
    cc = coco.CountryConverter()

    def get_iso_numeric_code(col):
        """Getting ISO numeric code from country name in order to match with json file"""
        try:
            iso_numeric_code =  cc.convert(names=col, to='ISOnumeric')
        except:
            iso_numeric_code = 'Unknown' 
        return iso_numeric_code

    df_stor.loc['code_numeric'] = df_stor['location_seller_scraped'].apply(get_iso_numeric_code)
    return df_stor

def world_map(df_stor, output_path_world_map):
    """Create world map with mean sale price for specific storage"""
    agg_df = df_stor.groupby('location_seller_scraped').mean().reset_index()

    source = alt.topo_feature(data.world_110m.url, "countries")

    background = alt.Chart(source).mark_geoshape(fill="white")

    foreground = (
        alt.Chart(source)
        .mark_geoshape(stroke="black", strokeWidth=0.15)
        .encode(
            color=alt.Color(
                "price_sold_scraped:N", scale=alt.Scale(scheme="lightgreyteal"), legend=None,
            ),
            tooltip=[
                alt.Tooltip("location_seller_scraped:N", title="Country"),
                alt.Tooltip("price_sold_scraped:Q", title="Mean Sale Price"),
            ],
        )
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(agg_df, "code_numeric", ["price_sold_scraped", "location_seller_scraped"]),
        )
    )

    final_map = (
        (background + foreground)
        .configure_view(strokeWidth=0)
        .properties(width=700, height=400)
        .project("naturalEarth1")
    )

    final_map.save(output_path_world_map)

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
        "--output_path_hist_price",
        help = "The path to the output file for the overall price histogram. Default: ./out/hist_price.png", 
        type = str, 
        default = "./out/hist_price.png"
        )

    parser.add_argument(
        "--output_path_hist_price_auction",
        help = "The path to the output file for the overall price histogram by auction. Default: ./out/hist_price_auction.png", 
        type = str, 
        default = "./out/hist_price_auction.png"
        )

    parser.add_argument(
        "--output_path_hist_price_storage",
        help = "The path to the output file for the overall price histogram by storage. Default: ./out/hist_price_storage.png",
        type = str,
        default = "./out/hist_price_storage.png"
        )

    parser.add_argument(
        "--output_path_graph_country_bids_price",
        help = "The path to the output file for the interactive graph of relationship between bids and price per country. Default: ./out/graph_country_bids_price.html",
        type = str,
        default = "./out/graph_country_bids_price.html"
    )

    parser.add_argument(
        "--output_path_world_map",
        help = "The path to the output file for the world map. Default: ./out/world_map.html",
        type = str,
        default = "./out/world_map.html"
    )

    parser.add_argument(
        "--stor",
        help = "Storage chosen to filter the graphs. Default: 64.",
        type = int, 
        default = 64
    )


    args = parser.parse_args()

    df, df_stor, df_stor_auction = clean(args.input_path, args.stor)
    hist_price(df, args.output_path_hist_price)
    hist_price_auction(df, args.output_path_hist_price_auction)  
    hist_price_storage(df, args.output_path_hist_price_storage)
    graph_country_bids_price(df_stor_auction, args.output_path_graph_country_bids_price)
    df_stor = clean_country_data(df_stor)
    world_map(df_stor, args.output_path_world_map)
    


if __name__ == "__main__":
    main()


    

