import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu
import pandas as pd

pd.set_option("display.float_format", "{:,.2f}".format)

# carregar o csv fornecido
df = pd.read_csv("./games_march2025_cleaned.csv")

# Reclassificar faixas etárias:
# "Livre" (0 anos) e "18+" (idade mínima de 17 anos)
df["faixa_etaria"] = df["required_age"].apply(
    lambda x: "Livre" if x == 0 else "Não livre"
)

# Filtrar apenas as duas categorias de interesse
df = df[df["faixa_etaria"].isin(["Livre", "Não livre"])].copy()

# Converter tempos para float e remover valores nulos
df["tempo_jogo"] = pd.to_numeric(df["average_playtime_forever"], errors="coerce")
df_filtrado = df.dropna(subset=["tempo_jogo"])[df["tempo_jogo"] > 0]

# Obter as duas amostras
nao_livre = df_filtrado[df_filtrado["faixa_etaria"] == "Não livre"]["tempo_jogo"]
livre = df_filtrado[df_filtrado["faixa_etaria"] == "Livre"]["tempo_jogo"]

print("Estatísticas descritivas:")
print("Livre:")
print(livre.describe())
print("\nNão livre:")
print(nao_livre.describe())

# Teste de Mann-Whitney U (unilateral: Não livre > Livre)
stat, p_val = mannwhitneyu(nao_livre, livre, alternative="greater")

print(f"\nEstatística U: {stat}")
print(f"P-valor (unilateral): {p_val:.50f}")

alpha = 0.05
if p_val < alpha:
    print(
        "Rejeitamos H0: Jogos não livres têm tempo de jogo significativamente maior (teste não paramétrico)."
    )
else:
    print(
        "Não rejeitamos H0: Não há evidência suficiente de que jogos não livres tenham tempo de jogo maior."
    )

plt.figure(figsize=(12, 6))
sns.boxplot(
    x="faixa_etaria", y="tempo_jogo", data=df_filtrado, palette=["green", "orange"]
)
plt.title("Tempo de Jogo por Faixa Etária (apenas jogos com tempo > 0)")
plt.xlabel("Faixa Etária")
plt.ylabel("Tempo de Jogo (minutos)")
plt.yscale("log")  # para facilitar visualização
plt.grid(True)
plt.show()
