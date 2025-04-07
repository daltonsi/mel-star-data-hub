# https://pypi.org/project/sas7bdat/

#
from sas7bdat import SAS7BDAT
import pandas as pd


DATA_FILE_PATH = "/Users/daltonsi/HILS/mel-star-data-hub/src/data_schemas/qol/dataverse_files/p1w1painsupplement.sas7bdat"


def load_sas7bday_to_df(sas7bdat_filepath : str):
	"""
		load_sas7bday_to_df
		:param: filepath to sas7bdat file
		:output: pandas dataframe
	"""


	with SAS7BDAT(sas7bdat_filepath) as reader:
	    
	    df = reader.to_data_frame()
	   
	return df


def summarize_dataframe(df : pd.DataFrame):

	num_respsones = len(df)

	data_fields = df.columns

	num_data_fields = len(data_fields)

	print(num_respsones)
	print(data_fields)
	print(num_data_fields)

	for col in data_fields:
		print(col)
		print(df[col].value_counts())
		print()



def main():

	df = load_sas7bday_to_df(DATA_FILE_PATH)


	summarize_dataframe(df)


if __name__ == "__main__":
	main()