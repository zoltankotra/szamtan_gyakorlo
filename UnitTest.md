
# Manuális Tesztelés Dokumentáció

## Tesztelési Terv
- **Cél**: Ellenőrizni a webalkalmazás funkcióit különböző böngészőkben.
- **Tesztelt funkciók**: űrlapok, válasz ellenőrzése, böngészők közötti kompatibilitás.

## Tesztelés
### 1. Űrlap kitöltése
- **Lépések**:
  1. Nyisd meg a projektet (pl. Pycharmban).
  2. Navigálj az URL-re miután lefuttatjuk a terminálban "python app.py" paranccsal: http://localhost:5000
  3. Töltsd ki az űrlapot a válaszokkal.
  4. Kattints a "Küldés" gombra.
- **Elvárt eredmény**: A válasznak helyesnek kell lennie.

## Eredmények
- **Dátum**: 2024.09.29.
- **Böngészők**: Chrome, Firefox, Edge,Arc
- **Eredmények**: 
  - Chrome: Minden funkció működik.
  - Firefox: Minden funkció működik.
  - Edge: Minden funkció működik.
  -Arc: Nem működik sajnos. :(
## Hibák
- **Arcban nem fut le a projekt.**

## Összegzés
- A tesztelés viszonylag sikeresen zajlott, minden funkció jól működött a tesztelt böngészőkben,kivéve ar Arc-ban.
- **Következő lépések**: Rendszeres tesztelés a jövőbeli frissítések után.

