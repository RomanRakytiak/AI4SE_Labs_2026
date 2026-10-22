# Správa: Agentická sieť na rafináciu softvérových požiadaviek

##  Cieľ a prehľad riešenia

Sieť prijme adresár s textovými dokumentmi (.txt, .eml, .md, .rst, .csv, .json, .xml) a vyrobí jeden štruktúrovaný dokument softvérových požiadaviek v Markdowne. Cesta ku vstupu sa zadáva argumentom (python script.py <input_dir> --output requirements.md). Súbory sa hľadajú rekurzívne a do výstupu idú ako relatívne cesty, takže sieť funguje na hocikde.

Implementácia je v LangGraph (StateGraph) so zdieľaným stavom NetworkState.

## Graf 
START → load_documents → extract_candidates → consolidate_requirements
                                                  ↑            ↓
                                                  │     deterministic_validate
                                                  │            ↓
                                                  └─ revise ─ review_consistency
                                                                 ↓ finalize
                                                          finalize_document → END
### Uzly siete
load_documents	(deterministický)	
- Rekurzívne načíta podporované súbory, zachová relatívne cesty
extract_candidates	(LLM gpt-5.6-luna)	
- Po jednom dokumente extrahuje kandidátov so zdrojom, citátom, istotou a kvalitou
consolidate_requirements (LLM gpt-5.4-nano)
- Zlúči kandidátov do požiadaviek, určí priority, vyradí nepodložené položky
deterministic_validate	deterministický	
- Kontroluje povinné polia, platnosť priority, stopy a duplicitné názvy
review_consistency (LLM gpt-5-mini)
- chýbajúce stopy, rozpory, presné duplicity
finalize_document (deterministický)
- Pridelí ID REQ-001…, zostaví výstup a metadáta

## Návrhové rozhodnutia
Pri promptoch sa používa schéma RTF (Role, Task, Format).

Extrakcia je po každom dokumente zvlášť. Zdroj každého kandidáta je tak jednoznačný a nič sa nestratí v dlhom spoločnom kontexte. Kandidát nesie typ, citát z textu, ako si je istý (explicit/implied/uncertain) a kvalitu (valid/ambiguous/contradictory/nonsensical/unsupported/example-only).

Samostatná konsolidácia. Až tento krok vidí všetkých kandidátov naraz, a preto môže zlučovať duplicity naprieč dokumentmi. Prompt rozlišuje, čo sa smie zlúčiť (rovnaký aktér, akcia, dáta aj výsledok) a čo musí zostať samostatné (iný aktér, workflow, dáta, pravidlá, oprávnenia, akceptačný test). Pri ďalšom kole spätnej väzby sa už kandidáti neposielajú znova; model upravuje aktuálny návrh iba podľa konkrétnej spätnej väzby, aby sa počet požiadaviek nezvyšoval pri každej iterácii.

Deterministická validácia pred revíziou. Niečo, čo sa dá overiť kódom (povinné polia, platná priorita, neprázdne zdroje, zhodné názvy), kontroluje funkcia, nie model. 

Spätná väzba a slučka. Revízor hlási problémy (rozpory, duplicity s návrhom zlúčenia). Nálezy idú ako FEEDBACK späť do konsolidácie. Cyklus je ohraničený konštantou MAX_REVIEW_ROUNDS, aby nebeželi donekonečna. Prípadné nevyriešené problémy sa nezamlčia, ale vypíšu sa v závere dokumentu.


_json_response vyžaduje čistý JSON, odstraňuje zbytočnosti okolo a 3-krát opakuje volanie s inštrukciou. _normalise_model_lists a _normalise_sources zjednocujú tvar odpovede, aby nezáležalo na drobných odchýlkach. Zamietnuté a zlúčené položky sa kumulujú naprieč kolami (s deduplikáciou) a zapisujú do výstupu spolu s dôvodom a zdrojom.

## Špecifikácie
Sieť spĺňa požiadavku ANS1 na minimálne tri LLM uzly. Požiadavka ANS2 na minimálne jeden deterministický uzol. LOOP z ANS3 je implementovaná prepojením review_consistency <=> consolidate_requirements. Požiadavka ANS4 na použitie minimálne troch modelov gpt-5.6-luna, gpt-5.4-nano a gpt-5-mini. Požiadavka ANS5 na použitie frameworku LangGraph.

OS1 na vytvorenie jedného dokumentu je splnená tým, že funkcia render_markdown zostaví všetky časti do jedného súboru vo formáte .md. 
OS2 prideľuje požiadavkám identifikátory vo formáte REQ-001, REQ-002 a podobne.
OS3 na odstránenie duplicít je zabezpečená pravidlom  v konsolidačnom prompte, kontrolou zhodných názvov v uzle deterministic_validate. 
OS4 uvádzaním položky sources pri požiadavke.
OS5 na názov a vysvetľujúci odsek je zabezpečená definovaním formátu výstupu v konsolidačnom prompte a validáciou názvu. 
OS6 na prioritu a jej škálu je splnená povolením hodnôt Critical, High, Medium a Low, ktoré sú vynucované v prompte. Výstupný dokument zároveň obsahuje sekciu "Priority Scale".
OS7 na konzistentnosť je zabezpečená tým, že revízny uzol vyhľadáva rozpory a nejasné formulácie, konsolidačný uzol vyraďuje protichodné položky. 
OS8 na úplnosť je podporená extrakciou dokumentov po jednom súbore, zachovaním kandidátov so zdrojmi a revízorom, ktorý kontroluje chýbajúce schopnosti. Konsolidačný prompt zároveň zakazuje tiché zahodenie kandidáta: každý kandidát musí skončiť v požiadavke, merged_items alebo discarded. Keďže rozhodovanie vykonáva LLM, výsledok môže byť nedokonalý.
OS9 na vytvorenie blacklistu je splnená tým, že konsolidačný uzol presúva rozporné, nezmyselné, nepodložené a príkladové položky do zoznamu discarded, pričom ku každej uvádza dôvod vyradenia. História discarded_history tieto položky zbiera a vo výstupnom dokumente sa zobrazujú v "Blacklist".

## Spustenie

```powershell
pip install -r requirements.txt
$env:OPENAI_API_KEY = "your-key"
python network.py .\data\corpus --output requirements.md
```
