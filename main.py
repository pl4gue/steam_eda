import pandas as pd
import math
import re
import string
import seaborn as sns
from collections import Counter
import matplotlib.pyplot as plt

# Functions for cleaning and formatting data


def clean_and_split(text):
    cleaned_text = [
        text_split.translate(str.maketrans("", "", string.punctuation.replace(",", "")))
        for text_split in text.split(sep="', '")
    ]
    return cleaned_text


def clean_and_split_dict(text):
    cleaned_text = text.strip("{}").replace(" ", "")
    pairs = cleaned_text.split(",")
    keys = [pair.split(":")[0].strip("'\"") for pair in pairs if ":" in pair]
    return keys


# Sorting functions


def sort_range(ranges):
    def extract_range(estimated_owners):
        if estimated_owners == "0 - 0":
            return 0
        else:
            start, end = map(int, estimated_owners.split(" - "))
            return (start + end) / 2

    return sorted(ranges.unique(), key=extract_range)


def sort_prices(prices):
    def extract_price(price_group):
        if price_group == "Free":
            return 0
        if price_group.startswith("<"):
            return int(price_group.lstrip("< ").rstrip("$"))
        if price_group.startswith(">"):
            return int(price_group.lstrip("> ").rstrip("$")) + 1
        else:
            return int(price_group.rstrip("$"))

    return sorted(prices.unique(), key=extract_price)


# Functions for plotting


def make_price_groups(price):
    for price_group in range(0, 80, 5):
        if float(price) == 0:
            return "Free"
        if price <= price_group:
            return "< " + str(price_group) + "$"

    return "> 80"


def get_notes_type(note):
    sex_words = [
        "sex",
        "erotic",
        "nake",
        "nud",
        "underwear",
        "butt",
        "cloth",
        "fetish",
        "girl",
        "kiss",
        "masturb",
        "femal",
    ]
    violence_words = [
        "violen",
        "blood",
        "shoot",
        "kill",
        "abus",
        "gore",
        "weapons",
        "destr",
        "monster",
        "fight",
    ]
    mature_words = [
        "matur",
        "mild",
        "shock",
        "all ages",
        "child",
        "nsfw",
        "languag",
        "suicid",
        "depression",
        "addiction",
        "smok",
        "alcoh",
    ]

    sex_pattern = "(?:{})".format("|".join(sex_words))
    violence_pattern = "(?:{})".format("|".join(violence_words))
    mature_pattern = "(?:{})".format("|".join(mature_words))
    none_pattern = "(?:{})".format("|".join(["none", "nan"]))

    patterns = [
        none_pattern,
        sex_pattern,
        violence_pattern,
        mature_pattern,
    ]
    game_types = [
        "all ages",
        "sexual content",
        "violent content",
        "mature content",
    ]

    new_note = str(note).lower()

    for pattern, game_type in zip(patterns, game_types):
        if bool(re.search(pattern, new_note)):
            return game_type


def make_histplot(
    feature,
    data,
    x_label,
    y_label="Number of games",
    rotation=0,
    title="",
    y_feature="",
    order=None,
):
    if y_feature == "":
        sns.histplot(data[feature])
    else:
        sns.barplot(data=data, x=feature, y=y_feature, gap=0, order=order)

    plt.xticks(rotation=rotation)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.tight_layout()
    plt.show()


def make_countplot(
    feature, data, x_label, order, y_label="Number of games", rotation=0, title=""
):
    sns.countplot(x=feature, data=data, order=order, hue=feature)
    plt.xticks(rotation=rotation)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.tight_layout()
    plt.show()


def make_barplot(
    feature,
    data,
    x_label,
    y_label="Number of games",
    rotation=0,
    pre_counted=False,
    title="",
):
    sns.barplot(data=data, x=feature)

    plt.xticks(rotation=rotation)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def make_piechart(data, title=""):
    plt.figure(figsize=(8, 8))
    wedges, _, autotext = plt.pie(
        data,
        autopct="%1.1f%%",
        pctdistance=1.2,
        startangle=140,
        colors=plt.get_cmap("tab20").colors,
    )
    plt.gca().add_artist(plt.Circle((0, 0), 0.70, fc="white"))

    plt.legend(wedges, data.index, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.title(title)
    plt.tight_layout()
    plt.show()


def make_distplot(
    feature,
    data,
    x_label,
    y_label="Density",
    rotation=0,
    x_min=-math.inf,
    x_max=math.inf,
    title="",
):
    sns.kdeplot(data[feature][(data[feature] > x_min) & (data[feature] < x_max)])
    plt.xticks(rotation=rotation)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()
    plt.show()


# Cleaning and formatting the following columns

columns_to_process = [
    "supported_languages",
    "full_audio_languages",
    "categories",
    "genres",
    "developers",
    "publishers",
    "tags",
]


df = pd.read_csv("games_march2025_cleaned.csv")

df["notes_type"] = [get_notes_type(note) for note in df["notes"]]

# Limpa colunas inuteis
df = df.drop(
    [
        "appid",
        "header_image",
        "screenshots",
        "movies",
        "user_score",
        "average_playtime_2weeks",
        "median_playtime_2weeks",
        "score_rank",
        "notes",
        "metacritic_url",
        "website",
        "support_url",
        "support_email",
        "reviews",
        "detailed_description",
        "about_the_game",
        "short_description",
    ],
    axis=1,
)

for col in columns_to_process[:-1]:
    df[col] = df[col].apply(clean_and_split)

df["tags"] = df["tags"].apply(clean_and_split_dict)

df["release_date"] = pd.to_datetime(df["release_date"])

# Histograma jogos por data de lançamento

# make_histplot(
#     "release_date", df, "Release date", title="Distribution of games by release date"
# )
#
# # Histograma jogos por idade requerida
#
# make_histplot(
#     "required_age", df, "Required Age", title="Distribution of games by required age"
# )
#
# # Contagem jogos por idade requerida (excluindo jogos classíficados lívre)
#
# make_countplot(
#     "required_age",
#     df[df["required_age"] != 0],
#     "Required Age",
#     sorted(df["required_age"].unique())[1:],
#     title="Distribution of games by required age (excluding age free games)",
# )
#
# # Contagem de jogos por número estimado de jogadores
#
# make_countplot(
#     "estimated_owners",
#     df,
#     "Expected number of players",
#     sort_range(df["estimated_owners"]),
#     rotation=45,
#     title="Distribution of games by estimated number of players",
# )
#
# # Distribuição dos jogos por quantidade de conquistas (excluindo jogos de farming de conquista)
#
# make_distplot(
#     "achievements",
#     df[(df["achievements"] != 0) & (df["achievements"] < 1400)],
#     "Number of achievements in a game (excluding achievements farming games)",
# )
#
# # Distribuição dos jogos por quantidade de conquistas (excluindo o caso do PayDay 2)
#
# make_distplot(
#     "achievements",
#     df[(df["achievements"] != 0) & (df["achievements"] < 300)],
#     "Number of achievements",
#     title="Distribution of number of achievements (excluding achievement farming games and PayDay 2)",
# )
#
# # Histograma dos jogos por tipo de conteúdo.
#
# make_piechart(df["notes_type"].value_counts(), "Games by type of content")
#
# # Histograma preço por data de lançamento
#
# df["year"] = df["release_date"].dt.year
#
# price_by_year = df.groupby("year", as_index=False)["price"].mean()
#
# make_histplot(
#     feature="year",
#     y_feature="price",
#     data=price_by_year,
#     x_label="Release Year",
#     y_label="Average game price",
#     title="Average price of games across time.",
#     rotation=45,
# )

# Preço médio por quantidade de donos.

price_by_owner = df.groupby("estimated_owners", as_index=False)["price"].mean()

make_histplot(
    feature="estimated_owners",
    y_feature="price",
    data=price_by_owner,
    x_label="Estimated Owners",
    y_label="Average game price",
    title="Average price of games by number of estimated owners.",
    rotation=45,
    order=sort_range(df["estimated_owners"]),
)

# 10 linguagens mais comuns

language_counts = df.explode("supported_languages")[
    "supported_languages"
].value_counts()

make_barplot(
    None, language_counts.head(10), "Languages", title="10 most common languages"
)
