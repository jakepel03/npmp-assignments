"""
python diagrami.py [pot/do/energija.csv]
"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, FixedLocator, NullLocator

CSV = sys.argv[1] if len(sys.argv) > 1 else "energija.csv"
df = pd.read_csv(CSV)

# --- skupne nastavitve --------------------------------------------------------
plt.rcParams.update({
    "font.family": "STIXGeneral",
    "mathtext.fontset": "stix",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.bbox": "tight",
})

# vrstni red in imena vezij (enaka v vseh diagramih in v besedilu)
VEZJA = [
    ("aswathy", "Aswathy"),
    ("alharbi", "Alharbi"),
    ("enoplastni", "enoplastni\nnesinhroni"),
    ("enoplastni_sinhroni_5x5", "enoplastni\nsinhroni"),
]
E_L = 0.0597  # Landauerjeva meja pri 1 K [meV]
B_TEMNA, B_SVETLA, B_SIVA = "#1f4e79", "#7fb2e5", "#9a9a9a"


def vejica(x, _=None):
    """Število z decimalno vejico, brez odvečnih ničel."""
    return f"{x:g}".replace(".", ",")


def avg(vezje, razl, ura):
    v = df[(df.vezje == vezje) & (df.razlicica == razl) & (df.ura == ura)
           & (df.zeroing == "da")
           & ~df.opomba.fillna("").str.contains("ponovitev")]
    return float(v.avg_ebath_meV.iloc[0])


def log_os(ax, ticks):
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(FixedLocator(ticks))
    ax.yaxis.set_major_formatter(FuncFormatter(vejica))
    ax.yaxis.set_minor_locator(NullLocator())
    ax.grid(axis="y", color="#e0e0e0", linewidth=0.6)
    ax.set_axisbelow(True)


def landauer(ax, x=1.01, ha="left", va="center"):
    """Črta Landauerjeve meje z vrednostjo ob črti (izračun: enačba v Metrikah)."""
    ax.axhline(E_L, color="black", linestyle=":", linewidth=1,
               label=r"Landauerjeva meja $E_\mathrm{L}$")
    ax.text(x, E_L, "0,0597", transform=ax.get_yaxis_transform(),
            ha=ha, va=va, fontsize=8)


def oznake(ax, bars, vrednosti):
    for b, v in zip(bars, vrednosti):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.08, f"{v:#.3g}".replace(".", ","),
                ha="center", va="bottom", fontsize=8)


x = np.arange(len(VEZJA))
w = 0.38
imena = [i for _, i in VEZJA]

# D1: poraba pri 10 in 100 ps
razl = lambda k: "brez_to" if k == "aswathy" else "to"
e10 = [avg(k, razl(k), "10ps") for k, _ in VEZJA]
e100 = [avg(k, razl(k), "100ps") for k, _ in VEZJA]

fig, ax = plt.subplots(figsize=(6.3, 3.4))
b1 = ax.bar(x - w / 2, e10, w, color=B_TEMNA, label=r"ura $10\,$ps")
b2 = ax.bar(x + w / 2, e100, w, color=B_SVETLA, label=r"ura $100\,$ps")
b1[0].set_hatch("///"); b2[0].set_hatch("///")
from matplotlib.patches import Patch
oznake(ax, b1, e10); oznake(ax, b2, e100)
landauer(ax)
log_os(ax, [0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1])
ax.set_ylim(0.003, 2)
ax.set_xticks(x, imena)
ax.set_ylabel(r"$\bar{E}$ [meV]")
from matplotlib.lines import Line2D
L_ROC = Line2D([], [], color="black", linestyle=":", linewidth=1)
L_IME = r"Landauerjeva meja $E_\mathrm{L}$"
ax.legend([Patch(color=B_TEMNA), Patch(color=B_SVETLA),
           Patch(facecolor="white", edgecolor="black", hatch="///"), L_ROC],
          [r"ura $10\,$ps", r"ura $100\,$ps", "brez testnega okolja", L_IME],
          frameon=False, fontsize=8, loc="upper right")
fig.savefig("D1_poraba.pdf")

# D2: s testnim okoljem in brez (10 ps)
brez = [avg(k, "brez_to", "10ps") for k, _ in VEZJA]
s_to = [np.nan] + [avg(k, "to", "10ps") for k, _ in VEZJA[1:]]

fig, ax = plt.subplots(figsize=(6.3, 3.4))
pos = np.r_[x[0], x[1:] + w / 2]  # Aswathy ima le en stolpec
b1 = ax.bar(pos, brez, w, color=B_SVETLA, hatch="///", edgecolor="black",
            linewidth=0, label="brez testnega okolja")
b2 = ax.bar(x[1:] - w / 2, s_to[1:], w, color=B_TEMNA, label="s testnim okoljem")
oznake(ax, b1, brez); oznake(ax, b2, s_to[1:])
landauer(ax)
log_os(ax, [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2])
ax.set_ylim(0.02, 6)
ax.set_xticks(x, imena)
ax.set_ylabel(r"$\bar{E}$ pri $10\,$ps [meV]")
ax.legend([Patch(color=B_TEMNA),
           Patch(facecolor=B_SVETLA, edgecolor="black", linewidth=0, hatch="///"), L_ROC],
          ["s testnim okoljem", "brez testnega okolja", L_IME],
          frameon=False, fontsize=8, loc="upper center", ncol=3)
fig.savefig("D2_testno_okolje.pdf")

# D3: poraba glede na število računanih celic (10 ps, s testnim okoljem)
CELICE = {"alharbi": 53, "enoplastni": 45, "enoplastni_sinhroni_5x5": 61}
kljuci = list(CELICE)
n = np.array([CELICE[k] for k in kljuci], float)
e = np.array([avg(k, "to", "10ps") for k in kljuci])
k_fit = float(n @ e / (n @ n))  # premica skozi izhodišče, metoda najmanjših kvadratov

fig, ax = plt.subplots(figsize=(6.3, 3.6))
xs = np.linspace(40, 65, 2)
ax.plot(xs, k_fit * xs, "--", color=B_SIVA, linewidth=1,
        label="premica skozi izhodišče")
landauer(ax)
ax.scatter(n, e, color=B_TEMNA, zorder=3)
ime = dict(VEZJA)
odmik = {"alharbi": (-8, 8, "right"), "enoplastni": (8, -12, "left"),
         "enoplastni_sinhroni_5x5": (-8, 8, "right")}
for k, ni, ei in zip(kljuci, n, e):
    dx, dy, ha = odmik[k]
    ax.annotate(f"{ime[k].replace(chr(10), ' ')}\n{vejica(ei)}", (ni, ei),
                xytext=(dx, dy), textcoords="offset points", ha=ha, fontsize=8)
ax.set_xlim(40, 65); ax.set_ylim(0.045, 0.085)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.3f}".replace(".", ",")))
ax.grid(color="#e0e0e0", linewidth=0.6); ax.set_axisbelow(True)
ax.set_xlabel(r"število računanih celic $N_\mathrm{r}$")
ax.set_ylabel(r"$\bar{E}$ pri $10\,$ps [meV]")
ax.legend(frameon=False, fontsize=8, loc="upper left")
fig.savefig("D3_celice.pdf")

# D4: zakasnitev po izhodih (v ciklih)
CONE = {"aswathy": (2, 2), "alharbi": (3, 5), "enoplastni": (2, 5),
        "enoplastni_sinhroni_5x5": (5, 5)}
y = np.arange(len(VEZJA))[::-1]
y0 = [CONE[k][0] / 4 for k, _ in VEZJA]
ost = [CONE[k][1] / 4 for k, _ in VEZJA]
h = 0.38

fig, ax = plt.subplots(figsize=(6.3, 2.8))
ax.barh(y + h / 2, y0, h, color=B_TEMNA, label=r"$Y_0$ (pri Aswathyju $Y_2$)")
ax.barh(y - h / 2, ost, h, color=B_SVETLA, label="ostali izhodi")
for yi, a, b in zip(y, y0, ost):
    ax.text(a + 0.02, yi + h / 2, vejica(a), va="center", fontsize=8)
    ax.text(b + 0.02, yi - h / 2, vejica(b), va="center", fontsize=8)
ax.set_yticks(y, [i.replace("\n", " ") for i in imena])
ax.set_xlim(0, 1.5)
ax.set_xticks(np.arange(0, 1.51, 0.25))  # mreža po urinih conah
ax.xaxis.set_major_formatter(FuncFormatter(vejica))
ax.set_xlabel("zakasnitev [urini cikli]")
ax.grid(axis="x", color="#e0e0e0", linewidth=0.6); ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=8, loc="upper right")
fig.savefig("D4_zakasnitev.pdf")

print(f"k = {k_fit:.4e} meV na celico")
