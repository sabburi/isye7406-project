# ISYE7406 Data Mining ft. Dr. Lu

## Create and Activate the Environment

```
conda env create -f environment.yml
```

```
conda activate lu
```
If you use any more packages, add them to the `environments.yml` file

## Add new Data

Add your raw data to the `/data/raw` directory and then modify the `/src/preprocess.py` file in order to merge your data with the main dataset.

The idea is to have one Python script that merges all the datasets instead of 100 intermediate files. Code can also be easily merged when people are working in parallel.

