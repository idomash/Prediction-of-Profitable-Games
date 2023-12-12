import json
import pandas as pd
import time


def convert_from_json_to_csv(json_file, output_name):
    json_data = pd.read_json(json_file)
    json_data.to_csv(f"{output_name}.csv")
    time.sleep(5)
    read_csv = pd.read_csv(f"{output_name}.csv")
    read_csv.dropna(thresh=2, axis=0)
    read_csv.to_csv(f'{output_name}_clean.csv')
    print("done")


def show_amount():
    with open("database.json", 'r') as data_json:
        json_data = json.load(data_json)
        print(len(json_data))


if __name__ == "__main__":
    convert_from_json_to_csv('database.json', 'data_csv')
