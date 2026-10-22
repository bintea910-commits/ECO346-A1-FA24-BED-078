import pandas as pd, matplotlib.pyplot as plt
from pathlib import Path
import glob

# find csv
path = "data/pslm_person_subset.csv"
if not Path(path).exists():
    path = glob.glob("data/*.csv")[0]

df = pd.read_csv(path)
print("Columns:", df.columns.tolist())

# Variant 6 filter: Balochistan Rural 10-64
if 'prov_code' in df.columns:
    df = df[df['prov_code']==4]
if 'urban_rural' in df.columns:
    df = df[df['urban_rural']==1]
df = df[(df['age']>=10) & (df['age']<=64)]

wcol = 'hhweight' if 'hhweight' in df.columns else ('weight' if 'weight' in df.columns else None)
if wcol is None:
    df['_w']=1; wcol='_w'

bins=[10,15,20,25,30,35,40,45,50,55,60,65]
labels=['10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64']
df['age_band']=pd.cut(df['age'], bins=bins, labels=labels, right=False)

def w_mean(g):
    return (g['literate'] * g[wcol]).sum() / g[wcol].sum()

table = df.groupby(['age_band','sex'], observed=True).apply(w_mean).reset_index(name='lit_rate')
table['lit_rate']*=100
print(table)

plt.figure(figsize=(9,5))
for s in sorted(df['sex'].dropna().unique()):
    sub=table[table['sex']==s].sort_values('age_band')
    plt.plot(sub['age_band'], sub['lit_rate'], marker='o', label=f"Sex {s}")
plt.xlabel("Age Band"); plt.ylabel("Literacy Rate (%)")
plt.title("Q5 Python: Balochistan Rural")
plt.legend(); plt.xticks(rotation=45); plt.tight_layout()
Path("figures").mkdir(exist_ok=True)
plt.savefig("figures/q5_python.svg")
print("SAVED figures/q5_python.svg")