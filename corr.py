import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import pearsonr, spearmanr

pd.set_option("display.float_format", "{:,.2f}".format)

# carregar o csv fornecido
df = pd.read_csv("./games_march2025_cleaned.csv")

df["owners_limpo"] = df["estimated_owners"].str.replace(",", "").str.strip()
df["owners_min"] = df["owners_limpo"].str.extract(r"^(\d+)").astype(int)
df["owners_max"] = df["owners_limpo"].str.extract(r"(\d+)$").astype(int)

# Calcular a média do intervalo
df["owners_medio"] = (df["owners_min"] + df["owners_max"]) / 2

# Filtrar dados com preço válido (> 0)
df["preco"] = pd.to_numeric(df["price"], errors="coerce")
df_filtrado = df.dropna(subset=["owners_medio", "preco"])
df_filtrado = df_filtrado[df_filtrado["owners_medio"] > 0]
df_filtrado = df_filtrado[df_filtrado["price"] <= 150]

print("Média de jogadores:", df_filtrado["owners_medio"].describe())
print("\nPreco:", df_filtrado["preco"].describe())

# Correlação de Pearson (linear)
# Pearson
pearson_corr, pearson_p = pearsonr(df_filtrado["preco"], df_filtrado["owners_medio"])
# Spearman
spearman_corr, spearman_p = spearmanr(df_filtrado["preco"], df_filtrado["owners_medio"])

# Resultados
print(f"Correlação de Pearson: {pearson_corr:.4f} | p-valor: {pearson_p:.4f}")
print(f"Correlação de Spearman: {spearman_corr:.4f} | p-valor: {spearman_p:.4f}")

plt.figure(figsize=(8, 6))
sns.scatterplot(y="owners_medio", x="preco", data=df_filtrado, alpha=0.4)
sns.regplot(y="owners_medio", x="preco", data=df_filtrado, scatter=False, color="red")
plt.yscale("log")  # porque o número de jogadores varia em ordens de grandeza
plt.ylabel("Número médio de jogadores (escala logarítmica)")
plt.xlabel("Preço (US$)")
plt.title("Correlação entre número de jogadores e preço")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
