# ENCODE_EpiRR_extraction_GSM
Scripts to extract and organize the GSM/GSE information from ENCODE links.


# Requiremets

```python > 3.0``` and ```create a env with requirements.txt```


### Usage

#### main_epirr_encode.py

```
Script to create a dataframe containing EpiRR, experiment_type, adn Link_sample_ENCODE columns from a list of EpiRR (web scraping)

Command line: 

python main_epirr_encode.py list_epirr.txt EpiRR_ENCODE_df.csv

```


#### extract_gsm_encode.py

```
Script to create a dataframe containing EpiRR, experiment_type, Link_sample_ENCODE, and External_resources (GSM/GSE) columns from a previous dataframe containing the Link_sample_ENCODE column (web scraping)

Command line: 

python extract_gsm_encode.py EpiRR_ENCODE_df.csv
```