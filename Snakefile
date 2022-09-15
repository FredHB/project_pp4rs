rule graph_all:
    input:
        graph_country_bids_price = "out/graph_country_bids_price.html",
        graph_price_auction = "out/hist_price_auction.png",
        graph_price_storage = "out/hist_price_storage.png",
        graph_price = "out/hist_price.png",
        graph_map = "out/world_map.html"

rule graph_creator:
    #conda: "ak-data-prep"
    input:
        script = "src/figures/graph-creator.py",
        data = "data/clean/data_clean.csv"
    output:
        graph_country_bids_price = "out/graph_country_bids_price.html",
        graph_price_auction = "out/hist_price_auction.png",
        graph_price_storage = "out/hist_price_storage.png",
        graph_price = "out/hist_price.png",
        graph_map = "out/world_map.html"
    shell:
        "python {input.script}"

rule prepare_data:
    input:
        script = "src/data/prepare-data.py"
    output:
        data = "data/raw/data_raw.csv"
    shell:
        "python src/data/prepare-data.py"

rule clean_data:
    #conda: "ak-date-prep"
    #conda: "envs/environment.yaml"
    input:
        script = "src/data/clean-data.py",
        data = "data/raw/data_raw.csv"
    output:
        data = "data/clean/data_clean.csv"
    shell:
        "python {input.script}"


# rule all_graphs:
#     input:
#         graph1 = "out/graph_country_bids_price.html"









