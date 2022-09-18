# project_pp4rs
A project to fulfil the requirements of the 2020 Programming Practices for Research Students course at UZH. We webscrape and analyze global eBay price data for selected used goods. 

# Description 
We webscrape price data from past auctions of used, undifferentiated goods sold in different Western countries by non-professional eBay sellers. Our focal good is the Apple iPhone X with 64 GB of storage. 
# Output 
You can find the output with the main summary statistics and graphs of this analysis in ```project_pp4rs/index.html```.
# How to compile 
The workflow manager snakemake handles the installation of the required dependencies into a local virtual environment. The only external dependencies you need to install are [conda](https://docs.conda.io/en/latest/) and [snakemake](https://snakemake.github.io/). The first two can be installed using your preferred method. It is recommended to install snakemake in its own separate conda virtual environment (e.g. ```conda create -c conda-forge -c bioconda -n snakemake snakemake```).

The steps to build the project are described in its snakemake file. If snakemake is installed it can be compiled from scratch by running the snakemake command in its root directory:
```bash
    cd /path/to/project_pp4rs
    conda activate snakemake
    snakemake --cores N --use-conda
```
where `N` is the number of jobs you wish to run in parallel.



