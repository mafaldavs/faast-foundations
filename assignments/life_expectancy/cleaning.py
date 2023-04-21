"""This module does data cleaning."""
import argparse
import pandas as pd

PATH='../life_expectancy/data/eu_life_expectancy_raw.tsv'

def clean_data(input_data = PATH, region = "PT"):
    """This function cleans the eu_life_expectancy data."""
    df_input = pd.read_table(input_data , header=0, sep='\t')
    split_cols = df_input['unit,sex,age,geo\\time'].str.split(',', expand=True)
    df_input[['unit', 'sex', 'age', 'region']] = split_cols

    df_input = df_input.drop(columns=['unit,sex,age,geo\\time'])

    df_long = pd.melt(df_input, id_vars=['unit', 'sex', 'age', 'region']
                            ,var_name='year'
                            ,value_name='value')

    df_long['year'] = df_long['year'].astype('int64')

    df_long['value'] = df_long['value'].str.replace(r'[: e p be b]+', '', regex=True)
    df_long = df_long[df_long['value'] != '']
    df_long['value'] = df_long['value'].astype('float64')

    df_long = df_long[df_long['region'] == region ]

    return df_long.to_csv('../life_expectancy/data/pt_life_expectancy.csv', index = False)




if __name__ == '__main__':  # pylint: disable=no-value-for-parameter
    parser = argparse.ArgumentParser()
    parser.add_argument("-region"
                        , action = 'store'
                        , help = 'Filters the dataset for the selected region'
                        , dest='region'
                        , default = 'PT'
                        , type = str)
    args = parser.parse_args()

    clean_data(input_data = '../life_expectancy/data/eu_life_expectancy_raw.tsv'
                ,region = args.region) # pylint: disable=no-value-for-parameter




