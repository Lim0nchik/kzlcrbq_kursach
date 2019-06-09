import pandas as pd
from pandas import DataFrame

data = DataFrame()
data_new = DataFrame()
suffer = DataFrame()
path_one = ""
path_second = ""


def load_dataframe(db_city_path, db_town_path):
    global data, path_one, path_second, suffer
    path_one = db_city_path
    path_second = db_town_path
    data = pd.read_csv(path_one)
    data_new = pd.read_csv(path_second)
    suffer = pd.merge(data, data_new, on='Key', how='left')


def get_records():
    return [el[1:] for el in suffer.iloc[:, 1:].itertuples()]


def _save_dataframe():
    # data.iloc[:, :4].to_csv(path_one, index=False)
    suffer[['Key', 'popular_movie', 'movie_score']]\
        .drop_duplicates(
            subset=['Key'],
            keep='first'
        )\
        .to_csv(
            path_second,
            index=False
        )
    suffer[['Key', 'Actor', 'year_of_birth', 'country', 'played_films']]\
        .drop_duplicates(
            subset=['Actor'],
            keep='first'
        )\
        .to_csv(
            path_one,
            index=False
        )


def insert_record(record):
    global suffer

    f = suffer[suffer.Actor == record['Actor']]
    k = suffer[suffer.popular_movie == record['popular_movie']]
    try:
        if list(f.Actor)[0] == record['Actor']:
            for key, value in record.items():
                suffer.replace(list(f[key])[0], value, inplace=True)
                suffer.popular_movie.replace(list(k.movie_score)[0], record['movie_score'], inplace=True)
    except IndexError:
        try:
            if list(k.popular_movie)[0] == record['popular_movie']:
                record['Key'] = list(k.Key)[0]
                merged = suffer.append(record, ignore_index=True)
                merged.movie_score.replace(list(k.movie_score)[0], record['movie_score'], inplace=True)
        except IndexError:
            record['Key'] = suffer['Key'][pd.Series(suffer['Key']).idxmax()] + 1
            suffer = suffer.append(record, ignore_index=True)
    #_save_dataframe()


def delete_record(index):
    global suffer
    suffer = suffer.drop(index).reset_index(drop=True)
   # _save_dataframe()


def update_record(index, record_list):
    data.iloc[index] = record_list
#    _save_dataframe()
