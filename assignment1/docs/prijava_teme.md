# NPMP: Prijava teme za seminar QCA in QC

**Skupina 21:** Miha Vintar, Tara Majkič, Jaka Pelko

**Naslov:** Enoplastni fizično reverzibilni demultiplekser s sinhronimi izhodi v QCA

**Opis:**
Fizično reverzibilen demultiplekser 1:2 (Alharbi in sod., [1]) porabi manj energije od Landauerjeve meje, vendar ima dve slabosti: uporablja večplastno križanje, ki ga je težko fizično realizirati, obenem pa njegova izhoda nista sinhrona (Y0 pride po 3 urinih conah, Y1 pa po 5). Zanima nas, ali omenjeno vezje lahko realiziramo v eni plasti in s sinhronimi izhodi, ne da bi se poraba energije povečala.

Pričakujemo, da se z drugačno postavitvijo levih majoritetnih vrat križanja lahko znebimo in pri tem porabimo manj energije, saj zmanjšamo število potrebnih celic. Sinhrono različico pa dobimo s podaljšanjem vodila oziroma povezave do izhoda Y0. Obe različici morata ostati fizično reverzibilni.

V simulatorju QCADesigner-E bomo implementirali Alharbijev demultiplekser (Slika 1) in za primerjavo še ireverzibilno izvedbo, nato pa obe izboljšavi. Vsa vezja bomo simulirali pod enakimi pogoji in primerjali po porabi energije, reverzibilnosti, zakasnitvi izhodov in strukturi.

![Alharbijev fizično reverzibilni demultiplekser 1:2](alharbi.png)

*Slika 1: Fizično reverzibilni demultiplekser 1:2 s trislojnim križanjem (vir: [1], slika 12).*

**Vir**

[1] M. Alharbi, G. Edwards, R. Stocker, »Design and Simulation of Reversible Time-Synchronized QCA Combinational Logic Circuits with Ultralow Energy Dissipation«, *International Transaction Journal of Engineering, Management, & Applied Sciences & Technologies* 13(12), 2022, doi:10.14456/itjemast.2022.240.