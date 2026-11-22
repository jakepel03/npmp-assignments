# Enoplastni fizično reverzibilni demultiplekser s sinhronimi izhodi v QCA

Skupina 21 (Tara Majkič, Jaka Pelko, Miha Vintar), NPMP 2026/27

Poročilo: [report.pdf](report.pdf) · predstavitev: [predstavitev.pptx](predstavitev.pptx)

Spodaj je opisano, kako ponovimo meritve iz poročila. Razlaga metod in rezultatov je v poročilu (razdelka *Metode* in *Rezultati*).

## Vsebina repozitorija

```
gradniki/                      osnovni gradniki (vodilo, negator, majoritetna vrata, AND, OR)
vezja/
  1_aswathy/                   ireverzibilni DEMUX Aswathyja in sod. (referenca)
  2_alharbi/                   fizično reverzibilni DEMUX Alharbija in sod. (izhodišče)
  3_enoplastni/                lastna enoplastna nesinhrona različica
  4_enoplastni_sinhroni/       vmesna sinhrona različica (ni v poročilu)
  5_enoplastni_sinhroni_5x5/   lastna enoplastna sinhrona različica (v poročilu »sinhroni«)
rezultati/
  energija.csv                 vse meritve energije
  diagrami.py                  izris grafov iz poročila
porocilo/                      izvorne datoteke LaTeX
patches/                       naši popravki QCADesigner-E
Dockerfile, docker-compose.yml, Makefile   prevajanje in zagon simulatorja
```

V mapah vezij 2–5 sta dve podmapi: `vezje/` vsebuje vezje brez testnega okolja (`<ime>.qca`), `testno_okolje/` pa isto vezje s testnim okoljem (`<ime>_to.qca`). Testno okolje doda pred vsak vhod in za vsak izhod 4 medpomnilniške celice z vklopljenim *Ignore Energy Dissipation*. Aswathyjevemu vezju testnega okolja ni mogoče dodati.

## 1. Zagon simulatorja

Potrebujemo Linux z grafičnim okoljem, Docker z Docker Compose in `make`. V mapi `assignment1/` zaženemo:

```bash
make run
```

Ob prvem zagonu Docker iz izvorne kode prevede [QCADesigner-E](https://github.com/FSillT/QCADesigner-E) (commit `3bc9030`) z našima popravkoma iz mape `patches/`. Prvi odpravi sesutja na Linuxu, drugi doda ukaz *Simulation → Reset Polarization*. Na izračun simulacije ne vplivata. Mapa `assignment1/` je v vsebniku vidna kot `/work`.

## 2. Nastavitve simulacije

Pri vseh meritvah uporabimo pogon **Coherence Vector (w/ Energy)** in način **Exhaustive Verification** z naslednjimi nastavitvami:

| parameter | vrednost |
|---|---|
| Temperature | 1 K |
| Relaxation Time / Time Step | 1e-15 s / 1e-16 s |
| Clock High / Clock Low | 9,8e-22 J / 3,8e-23 J |
| Clock Shift, oblika ure | 0, GAUSS |
| Radius of Effect | 80 nm |
| Relative Permittivity | 12,9 |
| Layer Separation | 11,5 nm |
| metoda | Euler |
| Randomize Simulation Order, Zeroing of Inputs | vklopljeno |

Vsako vezje simuliramo pri dveh hitrostih ure:

| hitrost | Clock Slope | Clock Period = Input Period | Total Simulation Time |
|---|---|---|---|
| 10 ps | 1e-11 s | 1e-10 s | 8e-10 s |
| 100 ps | 1e-10 s | 1e-9 s | 8e-9 s |

## 3. Postopek

1. V simulatorju odpremo datoteko `.qca` (*File → Open*, npr. `/work/vezja/2_alharbi/testno_okolje/alharbi_to.qca`).
2. *Simulation → Simulation Type Setup*: izberemo **Exhaustive Verification**.
3. *Simulation → Simulation Engine Setup*: izberemo **Coherence Vector (w/ Energy)** in v *Options* vnesemo nastavitve iz razdelka 2.
4. *Simulation → Start Simulation*. Po koncu se na dnu glavnega okna izpišeta Sum_Ebath in Avg_Ebath.

Glavne meritve v poročilu so s testnim okoljem (datoteke `_to.qca`). Meritve brez testnega okolja služijo primerjavi z Aswathyjem pod enakimi pogoji.

## 4. Pričakovani rezultati

Avg_Ebath v meV (vse meritve so tudi v [rezultati/energija.csv](rezultati/energija.csv)):

| vezje | s testnim okoljem, 10 ps | s testnim okoljem, 100 ps | brez, 10 ps | brez, 100 ps |
|---|---|---|---|---|
| Aswathy | – | – | 0,678 | 0,675 |
| Alharbi | 0,0704 | 0,00759 | 1,10 | 1,06 |
| enoplastni nesinhroni | 0,0555 | 0,00570 | 1,08 | 1,05 |
| enoplastni sinhroni (5×5) | 0,0764 | 0,00790 | 1,10 | 1,06 |

Landauerjeva meja pri 1 K je 0,0597 meV. Ker je vklopljen *Randomize Simulation Order*, se ponovljena simulacija od zgornjih vrednosti lahko razlikuje za nekaj desetink odstotka (ponovitev Alharbija pri 10 ps: 0,3 %).