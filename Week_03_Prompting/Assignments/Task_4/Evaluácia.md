# Vyhodnotenie SQL generovania

Všetky tabuľky a grafy sú v excel súbore pod názvom Metriky.xlsx.

Keďže som pracoval s Github Copilot Student nemal som navýber model miesto toho mi Microsoft priradil GPT-5.6 Luna.
Urobil som len dve iterácie pre každý prompt keďže Github Copilot Student licencia má len 2OO kreditov na bezplanné použitie.

## 1. Evaluácia 
zo súboru Metriky.xlsx
Prompt	Čas (s)	Presnosť (%)	Priemerná dĺžka (SQL tokeny/dopyt)	Najkratší dopyt	Najdlhší dopyt
prime	159	25,16	28,96	8	54
react	99	21,94	30,13	13	73
rtf	118	20,65	30,51	9	56
Priemer	125,33	22,59	29,87	10,00	61,00

### Interpretácia

V prvej evaluácii dosiahol prompt prime najvyššiu presnosť 25,16%, ale zároveň aj najdlhší čas spracovania 159s. Prompt react bol najrýchlejší 99s a dosiahol presnosť 21,94%. Prompt rtf mal najnižšiu presnosť 20,65% a najvyššiu priemernú dĺžku SQL dopytov (30,51 tokenov).

Priemerná presnosť všetkých promptov bola 22,59% a priemerný čas spracovania 125,33s.

## 2. Evaluácia
zo súboru Metriky.xlsx
Prompt	Čas (s)	Presnosť (%)	Priemerná dĺžka (SQL tokeny/dopyt)	Najkratší dopyt	Najdlhší dopyt
prime	142	27,74	33,17	13	129
react	100	21,94	28,06	8	50
rtf	86	21,94	51,94	38	74
Priemer	109,33	23,87	37,72	19,67	84,33

### Interpretácia

V druhej evaluácii dosiahol prime najvyššiu presnosť 27,74%, pričom jeho čas spracovania klesol na 142s. Prompt rtf bol najrýchlejší 86s, no generoval najdlhšie SQL dopyty v priemere (51,94 tokenov). Prompt react dosiahol presnosť 21,94% a mal najkratšie priemerné SQL dopyty (28,06 tokenov). Njdlhši SQL dotaz mal prime.

V porovnaní s prvou evaluáciou sa priemerná presnosť zvýšila z 22,59% na 23,87% a priemerný čas sa skrátil zo 125,33s na 109,33s. Priemerná dĺžka SQL dopytov však vzrástla z 29,87 na 37,72 tokenov.

## Celkové vyhodnotenie
zo súboru Metriky.xlsx
Metrika	Celkový priemer
Čas spracovania (s)	117,33
Presnosť (%)	23,23
Priemerná dĺžka SQL dopytu (tokeny na dotaz)	33,80
Najkratší dopyt	14,83
Najdlhší dopyt	72,67

Celková priemerná presnosť bola 23,23% a priemerný čas spracovania 117,33s. Výsledky naznačujú mierne zlepšenie v druhej evaluácii pri presnosti, avšak zvýšila sa i počet SQL tokenov.

Avšak len z týchto dvoch evaluácii nevieme spolahlivo určiť, či sú tieto dáta štatistický signifikantné, alebo ide len o nádodnu zmenu.

zo súboru Metriky.xlsx
Zmena v presnoti modelov vyzerá nasledovne:
model	Accuracy
prime	2,58
react	-0,01
rtf	1,29

Vidíme, že prime prompt trval celkovo najviac a tiež na základe dvoch evaluácií dosiahol prompt prime najvyššiu presnosť v oboch prípadoch. Zatiaľ čo react a rtf sa striedali o prvenstvo v čase. V prvej evaluácii generoval najkratšie SQL dopyty prime (28,96 tokenov), zatiaľ čo najdlhšie mal rtf (30,51 tokenov). V druhej evaluácii bol najkratší react (28,06 tokenov) a najdlhší rtf (51,94 tokenov). Rtf generuje v druhej evaluácii výrazne dlhšie SQL. Prompt prime dosahuje stredné hodnoty dĺžky, ale má najvyššiu maximálnu dĺžku pre jeden dopyt (129 tokenov).
Najčastejšov presnosťou vyzerá byť 21,94%, ale ostatné hodnoty nie sú ďaleko. I keď prime mal celkovo najlepšiu presnosť, môže ísť len o šťastie, keďže hodnoty sa od celkového priemeru nelíšia viac než o 4%. Ostatné hodnoty ako čas alebo priemerný počet SQL tokenov mali vyšší rozsah, čo možno naznačuje väčšiu varianciu, ale môže ísť len o okrajové prípady. React vyzerá ako kompromis medzi rýchlosťou a dĺžkou generovaného SQL, zatiaľ čo rtf v druhej evaluácii dosiahol najkratší čas spracovania.
