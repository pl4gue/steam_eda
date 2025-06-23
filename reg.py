import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

pd.set_option("display.float_format", "{:,.4f}".format)

# carregar o csv fornecido
df = pd.read_csv("./games_march2025_cleaned.csv")
df["tags"] = df["tags"].apply(
    lambda text: [
        pair.split(":")[0].strip("'\"")
        for pair in text.strip("{}").replace(" ", "").split(",")
        if ":" in pair
    ]
)

df["preco"] = pd.to_numeric(df["price"], errors="coerce")
df["tempo_jogo"] = pd.to_numeric(df["median_playtime_forever"], errors="coerce")
df["indie"] = (
    df["tags"].apply(lambda tags: any("Indie" in tag for tag in tags)).astype(int)
)
df = df[df["tempo_jogo"] > 0]

df = df.dropna(subset=["preco", "tempo_jogo", "indie"])

print(df["preco"].describe())
print(df["tempo_jogo"].describe())
print(df["indie"].describe())

X = df[["tempo_jogo", "indie"]]
X = sm.add_constant(X)  # adiciona intercepto
y = df["preco"]

modelo = sm.OLS(y, X).fit()
print(modelo.summary())

sns.residplot(x=modelo.fittedvalues, y=modelo.resid, lowess=True, color="blue")
plt.axhline(0, linestyle="--", color="black")
plt.xlabel("Preço previsto")
plt.ylabel("Resíduos")
plt.title("Resíduos do modelo de regressão")
plt.tight_layout()
plt.show()
