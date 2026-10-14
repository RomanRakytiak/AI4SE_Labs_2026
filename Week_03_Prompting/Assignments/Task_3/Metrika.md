# Nová metrika
Idea novej metriky by mohla byť, že sa pozrieme na dĺžku SQL dotazov. Konkrétne by sme mohli merať použité SQL tokeny, prierná dĺžka na dotaz, min a max hodnoty. Pre zjednodušenie toho čo myslím pod SQL tokenom použijem tento jednoduchý regex [^\s,;.]+, ktorý hľada hľadá skupiny neprázdnych znakov. Myslím si že ako heuristika to stačí, keďže úplne presné SQL tokeny by potrebovali veľmi komplexný regex alebo parser.

Kód je v súbore evaluate_predicion_length.py, ktorý zobral štruktúru z evaluate_rretrieval_predictions.py.

Táto metrika je užitočná lebo nechceme príliš dlhé SQL dopyty, ale sama o sebe určite nestačí, keďže nehovorí nič o správnosti. Avšak môže slúžiť ako doplnok k metrike správnosti.

## Výsledky podľa promptov
data-prime/evaluate_prediction_length.py
Total queries: 155
Total sql tokens: 4489
Average sql tokens per query: 28.96
Minimum sql tokens per query: 8
Maximum sql tokens per query: 54

data-prime-2/evaluate_prediction_length.py
Total queries: 155
Total sql tokens: 5142
Average sql tokens per query: 33.17
Minimum sql tokens per query: 13
Maximum sql tokens per query: 129

data-react/evaluate_prediction_length.py
Total queries: 155
Total sql tokens: 4670
Average sql tokens per query: 30.13
Minimum sql tokens per query: 13
Maximum sql tokens per query: 73

data-react-2/evaluate_prediction_length.py
Total queries: 155
Total sql tokens: 4350
Average sql tokens per query: 28.06
Minimum sql tokens per query: 8
Maximum sql tokens per query: 50

data-rtf/evaluate_prediction_length.py
Total queries: 155
Total sql tokens: 4729
Average sql tokens per query: 30.51
Minimum sql tokens per query: 9
Maximum sql tokens per query: 56

data-rtf-2/evaluate_prediction_length.py
Total queries: 155
Total sql tokens: 8051
Average sql tokens per query: 51.94
Minimum sql tokens per query: 38
Maximum sql tokens per query: 74

V prvej evaluácii generoval najkratšie SQL dopyty prime (28,96 tokenov), zatiaľ čo najdlhšie mal rtf (30,51 tokenov). V druhej evaluácii bol najkratší react (28,06 tokenov) a najdlhší rtf (51,94 tokenov). Rtf generuje v druhej evaluácii výrazne dlhšie SQL. Prompt prime dosahuje stredné hodnoty dĺžky, ale má najvyššiu maximálnu dĺžku pre jeden dopyt (129 tokenov). Celkovo najviac SQL token  pre všetky dopyty použil rtf v druhej evaluácii až 8051 tokenov, zatiaľ čo ostatné mali len okolo 4000-5000.
