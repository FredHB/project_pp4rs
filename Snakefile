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
        hist_price = "out/hist_price.png",
        hist_price_auction = "out/hist_price_auction.png",
        hist_price_storage = "out/hist_price_storage.png",
        graph_country_bids_price = "out/graph_country_bids_price.html",
        graph_world_map = "out/world_map.html"
    shell:
        '''
        python {input.script} \
        --input_path {input.data} \
        --output_path_hist_price {output.hist_price} \
        --output_path_hist_price_auction {output.hist_price_auction} \
        --output_path_hist_price_storage {output.hist_price_storage} \
        --output_path_graph_country_bids_price {output.graph_country_bids_price} \
        --output_path_world_map {output.graph_world_map} \
        --stor 64
        '''

rule prepare_data:
    input:
        script = "src/data/prepare-data.py"
    output:
        data = "data/raw/data_raw.csv"
    shell:
        "python {input.script} --output_path {output.data} --domain_list com de fr it --storage 64 128 256 512 --condition 3000 --auctions_list 0 1"

rule clean_data:
    #conda: "ak-date-prep"
    #conda: "envs/environment.yaml"
    input:
        script = "src/data/clean-data.py",
        data = "data/raw/data_raw.csv"
    output:
        data = "data/clean/data_clean.csv"
    shell:
        "python {input.script} --input_path {input.data} --output_path {output.data}"


# rule all_graphs:
#     input:
#         graph1 = "out/graph_country_bids_price.html"









