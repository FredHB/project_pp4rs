# project_pp4rs
A project to fulfil the requirements of the 2020 Programming Practices for Research Students course at UZH. We webscrape and analyze global eBay price data for selected used goods. 

# Description 
We webscrape price data from past auctions of used, undifferentiated goods sold in different Western countries by non-professional eBay sellers. Our focal good is the Apple iPhone X with 64 GB of storage. 

# Dependencies 
The workflow manager snakemake handles the installation of the required dependencies into a local virtual environment. 
The only external dependencies you need are:

1. Install [anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) based on your operating system
2. Install [snakemake](https://snakemake.github.io/), ideally in its own separate conda virtual environment:
   ```bash
   conda create -c conda-forge -c bioconda -n snakemake snakemake
   ```
     
# Compiling
The steps to build the project are described in its snakemake file. The project can be compiled from scratch by running the snakemake command in its root directory:
```bash
cd /path/to/project_pp4rs
conda activate snakemake
snakemake --cores all --use-conda --conda-frontend conda
```

# Output 
You can find the output with the main summary statistics and graphs of this analysis in ```project_pp4rs/index.html```.



