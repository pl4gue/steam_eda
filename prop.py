import matplotlib.pyplot as plt
import string
import seaborn as sns
from statsmodels.stats.proportion import proportions_ztest
import pandas as pd

pd.set_option("display.float_format", "{:,.4f}".format)

# Carregar dados
df = pd.read_csv("./games_march2025_cleaned.csv")

# Limpar valores ausentes
df = df.dropna(subset=["supported_languages"])

# Separar e limpar lista de idiomas
df["supported_languages"] = df["supported_languages"].apply(
    lambda text: [
        text_split.translate(str.maketrans("", "", string.punctuation.replace(",", "")))
        for text_split in text.split(sep="', '")
    ]
)

# Flags para idiomas
df["portugues"] = df["supported_languages"].apply(
    lambda langs: any("Portuguese" in lang for lang in langs)
)

df["brasil"] = df["supported_languages"].apply(
    lambda langs: any("Brazil" in lang for lang in langs)
)

# Totais
total = len(df)
com_portugues = df["portugues"].sum()
com_brasil = df["brasil"].sum()
proporcao_portugues = com_portugues / total
proporcao_brasil = com_brasil / total
proporcao_brasil_pt = com_brasil / com_portugues

# Resultados iniciais
print(f"Número total de jogos: {total}")
print(f"\nNúmero de jogos com suporte a português Brasil: {com_brasil}")
print(f"Proporção observada: {proporcao_brasil:.4f}")
print(
    f"\nNúmero de jogos com suporte a português (Brasil ou Portugal): {com_portugues}"
)
print(f"Proporção observada: {proporcao_portugues:.4f}")
print(
    f"\nProporção de jogos com português Brasil e o total com suporte a português: {proporcao_brasil_pt:.4f}"
)

# Teste 1: Brasil >= 15% do total
stat1, pval1 = proportions_ztest(
    count=com_brasil, nobs=total, value=0.15, alternative="larger"
)
print("\nTeste 1 – H0: p_brasil <= 0.15 | H1: p_brasil > 0.15")
print(f"Estatística Z: {stat1:.4f} | P-valor: {pval1:.4f}")
if pval1 < 0.05:
    print(
        "Rejeitamos H0: Proporção de jogos com português Brasil é significativamente maior que 15%."
    )
else:
    print("Não rejeitamos H0.")

# Teste 2: Português (Brasil ou Portugal) >= 20% do total
stat2, pval2 = proportions_ztest(
    count=com_portugues, nobs=total, value=0.20, alternative="larger"
)
print("\nTeste 2 – H0: p_total <= 0.20 | H1: p_total > 0.20")
print(f"Estatística Z: {stat2:.4f} | P-valor: {pval2:.4f}")
if pval2 < 0.05:
    print(
        "Rejeitamos H0: Proporção de jogos com português (qualquer variante) é significativamente maior que 20%."
    )
else:
    print("Não rejeitamos H0.")

# Teste 3: Brasil é mais de 75% dentre os jogos com português
stat3, pval3 = proportions_ztest(
    count=com_brasil, nobs=com_portugues, value=0.75, alternative="larger"
)
print(
    "\nTeste 3 – H0: p_brasil_dos_portugues <= 0.75 | H1: p_brasil_dos_portugues > 0.75"
)
print(f"Estatística Z: {stat3:.4f} | P-valor: {pval3:.4f}")
if pval3 < 0.05:
    print(
        "Rejeitamos H0: Entre os jogos com suporte a português, a maioria significativa é em português Brasil (>75%)."
    )
else:
    print("Não rejeitamos H0.")

# Comparação das proporções com os valores hipotéticos

plt.figure(figsize=(8, 6))
plt.bar(
    ["Português Brasil", "Português Total"],
    [com_brasil, com_portugues],
    color=["#00a65a", "#3c8dbc"],
)

# Linhas de referência para hipóteses (valores absolutos)
plt.axhline(
    total * 0.15,
    color="red",
    linestyle="--",
    label="Hipótese Brasil ≥ 15% (n ≈ {:.0f})".format(total * 0.15),
)
plt.axhline(
    total * 0.20,
    color="orange",
    linestyle="--",
    label="Hipótese Total ≥ 20% (n ≈ {:.0f})".format(total * 0.20),
)

plt.title("Número de jogos com suporte a português (Brasil e Total)")
plt.ylabel("Número de jogos")
plt.ylim(0, total * 0.4)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# Proporção de Português Brasil entre jogos com suporte a português
# Valores
so_portugal = com_portugues - com_brasil
nao_portugues = total - com_portugues

# Gráfico – barra única empilhada
plt.figure(figsize=(6, 6))

# Barra empilhada com Brasil e outros
plt.bar(
    "Jogos com suporte a português",
    com_brasil,
    color="#00a65a",
    label="Português Brasil",
)
plt.bar(
    "Jogos com suporte a português",
    so_portugal,
    bottom=com_brasil,
    color="orange",
    label="Apenas português de Portugal",
)

# Linha de referência: 75% dos jogos com português (não do total)
plt.axhline(
    com_portugues * 0.75,
    color="red",
    linestyle="--",
    label="Hipótese 75% Brasil entre PTs",
)

plt.title("Distribuição dos jogos com suporte a português\n(dentro do total de jogos)")
plt.ylabel("Número de jogos")
plt.ylim(0, total)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
