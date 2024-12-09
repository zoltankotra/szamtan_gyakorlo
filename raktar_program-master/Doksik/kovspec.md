# Követelmény specifikációk
A program lényege egy letisztult raktár nyilvántartó, ami a termékek helyét/típusát/darabszámát továbbá a rendelések állapotát/megrendelő nevét listázza egy adatbázisból.

## Vízió
Több fülre osztott, minden fülről elérhető legyen minden másik fül.

 - Termékek fül: Új termék hozzáadása gomb (al-fül), termékek kilistázva. Törlés opció.
- Ügyfelek fül: Új ügyfél hozzáadása gomb (al-fül), ügyfelek és adataik kilistázva. Ügyfelek törlése.
- Megrendelések fül: Megrendelés hozzáadása gomb (al-fül), megrendelések kilistázva, lezárva/teljesítve státusz jelölő.
- Raktár fül: Raktári termékek hozzáadása gomb (al-fül), termékek kilistázva, törlés opció.

## Use Cases
| Modul | ID    | UC ID | Név | Kifejtés |
| --- | -------- | ------- | ------- | ------ |
| Adatbázisba való felvétel | 01 | M1 | Megrendelés hozzáadása | Lehet új megrendeléseket felvenni. |
| Adatbázisból való törlés | 02 | M2 | Megrendelés törlése | Lehet ú megrendeléseket törölni. |
| Bővebb innformáció | 03 | M3 | Rendelés információ | Meglehet tekinteni bővebb információt egy rendelésről. |
| Szűrő | 04 | M4 | Rendelések szűrése | Lehet a rendelések listájában szűrni bizonyos kritériumok alapján. |
| Lapozás | 13 | M5 | Rendelések oldal lapozása | Meg lehet adni hány rendelés szerepeljen per oldal, lehet lapozni az oldalak között. |
| Adatbázisba való felvétel | 05 | T1 | Termékek hozzáadása | Lehet új termékeket felvenni a raktárba. |
| Adatbázisból való törlés | 06 | T2 | Termékek törlése | Lehet törölni termékeket a raktárból. |
| Szűrő | 07 | T3 | Termékek szűrése | Lehet a termékek listájában szűrni bizonyos kritériumok alapján. |
| Lapozás | 08 | T4 | Termékek oldal lapozása | Meg lehet adni hány termék szerepeljen per oldal, lehet lapozni az oldalak között. |
| Adatbázisba való felvétel | 09 | Ü1 | Ügyfél hozzáadása | Lehet új ügyfeleket felvenni. |
| Adatbázisból való törlés | 10 | Ü2 | Ügyfél törlése | Lehet törölni ügyfelet a nyilvántartásból. |
| Szűrő | 11 | Ü3 | Ügyfelek szűrése | Lehet az ügyfelek listájában szűrni bizonyos kritériumok alapján. |
| Lapozás | 12 | Ü4 | Ügyfelek oldal lapozása | Meg lehet adni hány ügyfél szerepeljen per oldal, lehet lapozni az oldalak között. |
| Adatbázisba való felvétel | 14 | R1 | Raktárba való felvétel | Raktárba meglévő termék felvétele. |
| Adatbázisból való törlés | 15 | R2 | Raktárból való kivétel | Raktárból meglévő termék és felvett termék törlése. |
