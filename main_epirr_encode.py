import sys
import pandas as pd
from tqdm import tqdm
import requests
from retry import retry
from time import sleep
from distutils.dir_util import mkpath
from utils.loggerinitializer import *
from json import JSONDecodeError
import logging
import os


mkpath(os.getcwd()+ "/logs/")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
initialize_logger(os.getcwd() + "/logs/", logger)


@retry(TimeoutError, tries=5, delay=3)
def get_json(file_n):
    '''Receives a txt file
    with a list of EpiRR and
    returns a df with EpiRR,
    Link_sample_Encode and
    target columns'''

    file_epi = open(file_n, 'r')
    dict_master = {}
    logger.info('Starting requests...')
    ctn = 0


    for line in tqdm(file_epi):
        
        line = line.strip()
        url = 'https://www.ebi.ac.uk/vg/epirr/view/'+str(line)+'?format=json' #ok
        ctn +=1
        sleep(3)

        try:
            dict_data = requests.get(url).json()
            
            for ele in dict_data['raw_data']: #accessing each dict (ele)
                master_key = ele.get('archive_url', ctn)
                dict_master[master_key] = {}
                dict_master[master_key]['EpiRR'] = line
                dict_master[master_key]['experiment_type'] = ele.get('experiment_type', '----')

        except JSONDecodeError as jd:
            logger.error("JSONDecodeError. Restart the program from: " + str(line) + " Something wrong with the url.")
            print(f'JSONDecodeError {jd}. Restart the program from {line}. Something wrong with the url')
            sys.exit(1)

        except requests.exceptions.Timeout:
            logger.error("Timeout! You should restart the program from: " + str(line))
            print(f'Timeout! You should restart the program from: {line}')
            sys.exit(1)

        except ConnectionAbortedError as cae:
            logger.error("Connection aborted error! You shold restart the program from: " + str(line))
            print(f"Error {cae}. You shold restart the program  from {line}")
            sys.exit(1)

        except ConnectionRefusedError as cre:
            logger.error("Connection aborted error! You shold restart the program from: " + str(line))
            print(f"Error {cre}. You shold restart the program  from {line}")
            sys.exit(1)

    logger.info('dict_master done!!') 
    
    return dict_master


def dict_to_df(dict_master):


    df = pd.DataFrame.from_dict(dict_master, orient='index')
    df['Link_Sample_ENCODE'] = df.index
    df.reset_index(drop=True, inplace=True) #getting all samples (including TF, Histone, Control, RNA-Seq)
    logger.info('Dataframe done!') 
    
    return df
    

def main():

    print('Starting...')
    dict_master = get_json(sys.argv[1]) #list of EpiRR
    df_final = dict_to_df(dict_master)
    df_final.to_csv(sys.argv[2], index=False) #output file name
    print('Df saved!')


if __name__ == "__main__":



    main()
