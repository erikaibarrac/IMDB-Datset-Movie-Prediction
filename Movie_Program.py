# code to predict if a movie is a comedy or not
import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.preprocessing import MultiLabelBinarizer

""" This program will create the following files and sizes:
    Five_Actors_Orig_Meta = (7551, 6263)
    Five_Actors_New_Meta = (21028, 15585)
    Five_Actors_Income = (12196, 9532) """

def one_hot(df, col, k):
    """ col is a string """

    # Create new data frame to one hot encode col
    col_data_frame = df[[col]]
    col_data_frame.loc[:,col] = col_data_frame[col].str.split(", *")

    # Sklearn magic
    s = col_data_frame[col]
    mlb = MultiLabelBinarizer()
    unique_cols = pd.DataFrame(mlb.fit_transform(s), columns=mlb.classes_, index=col_data_frame.index)

    # If you set k = 1, you are looking to one hot encode everything, but if k > 1,
    # you are only looking to one hot encode the items that appear at least k times
    if k > 1:
        # This is all to create uniques which allows us to find not_serial_class
        col_data_frame = df[[col]]
        col_data_frame.loc[:,col] = col_data_frame[col].str.split(", *")
        col_data_frame = col_data_frame.explode(col)
        uniques = col_data_frame[col].value_counts()
        not_serial_col = []
        for item in uniques.index:
            if uniques[item] < k:
                not_serial_col.append(item)

        # Drop columns that are not serial class
        unique_cols = unique_cols.drop(columns=not_serial_col)

    # Rename columns to include column type
    unique_cols = unique_cols.rename(columns=lambda x: col + ("_") + x)

    return unique_cols


def create_data_frame():
    # This includes only the budgest adjusted to modern day dollars
    adjusted_budget = pd.read_csv("adjusted_budget.csv", index_col="imdb_title_id") # Generated by regularize_currency.ipynb
    # This includes only the incomes adjusted to modern day dollars
    adjusted_income = pd.read_csv("adjusted_income.csv", index_col="imdb_title_id") # Generated by regularize_currency.ipynb
    # This includes metascores for each movie including predicted metascores
    filled_metascores = pd.read_csv("filled_metascores.csv", index_col="imdb_title_id") # Generated by predict_meta_score.ipynb

    df = pd.read_csv("IMDB movies.csv")
    df = df.set_index("imdb_title_id")

    # Only include columns we want
    df = df[['genre', 'duration', 'director', 'writer', 'production_company', 'actors', 'avg_vote', 'votes', 'budget', 'worlwide_gross_income', 'metascore']]
    # Drop columns with important missing info
    df = df.dropna(subset=['genre', 'duration', 'director', 'writer', 'production_company', 'actors', 'avg_vote', 'votes', 'budget'])
    # Join the dataset with the adjusted_budget one and drop the rows that don't appear in adjusted_budget
    df = df.join(adjusted_budget, how="inner").drop(columns=["budget", "worlwide_gross_income"])

    # This dataset only has movies with a given metascore
    orig_meta = df.dropna(subset=["metascore"])
    # This dataset combines our dataset with the predicted metascores
    new_meta = df.join(filled_metascores, how="inner").drop(columns=["metascore"])
    # This dataset combines our dataset with the adjusted_income dataset to only include movies with a given adjusted income
    income = df.join(adjusted_income, how="inner").drop(columns=["metascore"])

    # One hot encode our categorical classes
    genre = one_hot(orig_meta, 'genre', 1)
    print("genre dataset = " + str(genre.shape))
    director = one_hot(orig_meta, 'director', 3)
    print("director dataset = " + str(director.shape))
    writer = one_hot(orig_meta, 'writer', 3)
    print("writer dataset = " + str(writer.shape))
    prod_comp = one_hot(orig_meta, 'production_company', 10)
    print("prod_comp dataset = " + str(prod_comp.shape))
    actors = one_hot(orig_meta, 'actors', 5)
    print("actors dataset = " + str(actors.shape))

    # Drop the old categorical columns
    orig_meta = orig_meta.drop(columns=['genre', 'director', 'writer', 'production_company', 'actors'])
    # Merge the dataframe to the one hot encoded dataframes
    orig_meta = orig_meta.join([genre, director, writer, prod_comp, actors])
    print("total = " + str(orig_meta.shape))
    orig_meta.to_csv("Five_Actors_Orig_Meta.csv")

    # One hot encode our categorical classes
    genre = one_hot(new_meta, 'genre', 1)
    print("genre dataset = " + str(genre.shape))
    director = one_hot(new_meta, 'director', 3)
    print("director dataset = " + str(director.shape))
    writer = one_hot(new_meta, 'writer', 3)
    print("writer dataset = " + str(writer.shape))
    prod_comp = one_hot(new_meta, 'production_company', 10)
    print("prod_comp dataset = " + str(prod_comp.shape))
    actors = one_hot(new_meta, 'actors', 5)
    print("actors dataset = " + str(actors.shape))

    # Drop the old categorical columns
    new_meta = new_meta.drop(columns=['genre', 'director', 'writer', 'production_company', 'actors'])
    # Merge the dataframe to the one hot encoded dataframes
    new_meta = new_meta.join([genre, director, writer, prod_comp, actors])
    print("total = " + str(new_meta.shape))
    new_meta.to_csv("Five_Actors_New_Meta.csv")

    # One hot encode our categorical classes
    genre = one_hot(income, 'genre', 1)
    print("genre dataset = " + str(genre.shape))
    director = one_hot(income, 'director', 3)
    print("director dataset = " + str(director.shape))
    writer = one_hot(income, 'writer', 3)
    print("writer dataset = " + str(writer.shape))
    prod_comp = one_hot(income, 'production_company', 10)
    print("prod_comp dataset = " + str(prod_comp.shape))
    actors = one_hot(income, 'actors', 5)
    print("actors dataset = " + str(actors.shape))

    # Drop the old categorical columns
    income = income.drop(columns=['genre', 'director', 'writer', 'production_company', 'actors'])
    # Merge the dataframe to the one hot encoded dataframes
    income = income.join([genre, director, writer, prod_comp, actors])
    print("total = " + str(income.shape))
    income.to_csv("Five_Actors_Income.csv")

    print(orig_meta.shape)
    print(new_meta.shape)
    print(income.shape)
    return

create_data_frame()
