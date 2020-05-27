import pandas as pd

df = pd.read_csv("videoDB.csv", encoding="latin-1", index_col="ID")

df.index = df.index.str.replace("tt", '').str.strip().astype(int)
df["Duración"] = df["Duración"].str.replace("min", '').str.strip().astype(int) * 60

unique_genres = df["Género"].str.strip().str.split(", ").explode().unique()
unique_genres_idxs = pd.factorize(unique_genres)[0] + 1

values = ''
i = 0
for genre in unique_genres:
    values +=  "({}, '{}'),".format(unique_genres_idxs[i], genre)
    i += 1
print()
print("INSERT INTO Genre_Catalog(id, genre) VALUES {};".format(values[:-1]))

df_movies = df[df["ID Episodio"].isna()]
df_movies["Fecha"] = df_movies["Fecha"].astype(int)
df_movies = df_movies.drop(columns=["ID Episodio", "Título Episodio", "Temporada", "Episodio"])
df_movies_no_genre = df_movies.drop(columns=["Género"])
values = ''

for movie in df_movies_no_genre.itertuples():
    values +=  "({}, {}, {}, {}, '{}'),".format(movie[0], movie[3], movie[2], movie[4], movie[1])
print()
print("INSERT INTO Movie_Detail(id, rating, duration, year, name) VALUES {};".format(values[:-1]))


movies_genres_Serie = df_movies["Género"].str.strip().str.split(", ").explode()

movies_idxs = movies_genres_Serie.index
movies_genres_idxs = movies_genres_Serie.factorize()[0] + 1

values = ''
i = 0
for genre_idx in movies_genres_idxs:
    values += "({},{}),".format(movies_idxs[i], genre_idx)
    i += 1
print()
print("INSERT INTO MovieGenres_Master(movie_id, genre_id) VALUES {};".format(values[:-1]))

df_series = df[df["ID Episodio"].notna()]
df_series["ID Episodio"] = df_series["ID Episodio"].str.replace("tt", '').str.strip().astype(int)
df_series["Temporada"] = df_series["Temporada"].astype(int)
df_series["Episodio"] = df_series["Episodio"].astype(int)
df_series["Fecha"] = df_series["Fecha"].str.replace('\x96', '-')
df_series["Calificación"] = df_series["Calificación"].fillna(5.0)
df_unique_series_idxs = df_series["Título Serie o Película"].drop_duplicates().index

values = ''
for serie_idx in df_unique_series_idxs:
    serie = df_series.loc[serie_idx, :]

    fecha = serie["Fecha"][:1].values[0]
    year_start, year_end = fecha.split('-')

    if not year_end.isdigit():
        year_end = "NULL"
    else:
        year_end = int(year_end)

    year_start = int(year_start)

    name = serie["Título Serie o Película"][:1].values[0]

    values += "({}, {}, {}, '{}'),".format(serie_idx, year_start, year_end, name)

print()
print("INSERT INTO Serie_Detail(id, year_start, year_end, name) VALUES {};".format(values[:-1]))
#df_series["Fecha"]#.astype(str).str.split('\x96', '')
#df_series.loc[1135300, "Fecha"].str.replace('\x96', '-').str.split('-').explode()


for serie_idx in df_unique_series_idxs:
    serie_genres = df_series[df_series.index == serie_idx]["Género"].unique()[0].split(', ')
    for genre in serie_genres:
        print("CALL insertSerieGenre({}, '{}');".format(serie_idx, genre))


from math import isnan

df_series.head()

values = ''
for episode in df_series.itertuples():
    serie_id = episode[0]
    episode_id = episode[6]
    n_episode = episode[-1]
    n_season = episode[-2]
    rating = episode[4]
    duration = episode[2]
    name = episode[7]
    #if isnan(rating):
    #    print(episode)
    values += "({}, {}, {}, {}, {}, {}, '{}'),".format(episode_id, serie_id, n_episode, n_season, rating, duration, name.replace('\'','\\\''))
print()
print("INSERT INTO Episode_Detail(id, serie_id, n_episode, n_season, rating, duration, name) VALUES {};".format(values[:-1]))
