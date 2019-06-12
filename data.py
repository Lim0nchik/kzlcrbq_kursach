import pandas as pd
import config


actor_columns = [
    'actor_name',
    'actor_year_of_birth',
    'actor_country',
    'actor_played_movies',
    'actor_best_movie_id'
]

movie_columns = [
    'movie_id',
    'movie_name',
    'movie_score'
]


def join_from_csv() -> pd.DataFrame:
    """
    Left-joined actors x movies dataframe
    """
    df_actors = pd.read_csv(config.path_csv_actor)
    df_movies = pd.read_csv(config.path_csv_movie)
    return df_actors.merge(
        df_movies,
        left_on='actor_best_movie_id',
        right_on='movie_id',
        how='left'
    )


def save_to_csv(df: pd.DataFrame) -> None:
    df[actor_columns]\
        .drop_duplicates()\
        .to_csv(config.path_csv_actor, index=False)
    df[movie_columns]\
        .drop_duplicates()\
        .to_csv(config.path_csv_movie, index=False)


def edit_record(df: pd.DataFrame, actor_values, movie_values) -> None:
    df.loc[df.actor_name == actor_values[0], actor_columns] = actor_values
    df.loc[df.movie_id == movie_values[0], movie_columns] = movie_values


def insert_record(df: pd.DataFrame, values: dict) -> pd.DataFrame:
    movie_id = df['movie_id'].max() + 1
    values['movie_id'] = movie_id
    values['actor_best_movie_id'] = movie_id
    return df.append(values, ignore_index=True)


def delete_record(df: pd.DataFrame, actor_name: str) -> None:
    df.drop(df[df.actor_name == actor_name].index, inplace=True)


if __name__ == '__main__':
    data = join_from_csv()
    edit_record(
        data,
        (
            'Josh Brolin',
            19680,
            'USA',
            1450,
            1
        ),
        (
            15,
            'Batman Forever',
            106.5
        )
    )
    print(data)
    save_to_csv(data)
