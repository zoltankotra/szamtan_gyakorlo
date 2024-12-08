# Funkcionális specifikációk

## User Story-k

### Kata, a precíz ügyfélszolgálati menedzser
Kata, a precíz ügyfélszolgálati menedzser, egy mozgalmas munkanap reggelén leült a számítógépe elé, hogy átnézze az ügyfélnyilvántartást. A cég folyamatosan bővülő ügyfélkörrel büszkélkedhetett, de Kata, a precíz ügyfélszolgálati menedzser észrevette, hogy néhány régi, már nem aktív ügyfél még mindig szerepel a rendszerben, ami zűrzavart okozott az ügyfélszolgálati folyamatokban. Elhatározta, hogy kitörli az elavult adatokat, és közben hozzáad egy új ügyfelet.
Az „Ügyfelek” opcióra kattintva megjelent a táblázat, amelyben az összes ügyfél adatai látszottak. Gyorsan kikereste a régi ügyfeleket, ellenőrizte az adatokat, majd minden régi ügyfelet kitörölt.
Ezután hozzáadott egy új ügyfelet, kitöltve az összes mezőt és megnyomva a „Hozzáadás” gombot. Az új rekord azonnal megjelent a táblázatban. Mielőtt befejezte volna, beállította, hogy több sor jelenjen meg a táblázatban, és átnézte az adatokat, hogy minden rendben legyen. Megkönnyebbülve látta, hogy az elavult ügyfél eltűnt, és az új ügyfél helyesen szerepel a rendszerben. Kata, a precíz ügyfélszolgálati menedzser elégedetten bezárta az alkalmazást, tudva, hogy a pontos adatkezelés elengedhetetlen a sikeres ügyfélkapcsolatokhoz.

### Anna, a mindig akkurátus logisztikai vezető
Anna, a mindig akkurátus logisztikai vezető, egy forgalmas péntek reggelen leült, hogy rendbe tegye a raktári nyilvántartást. A cégük épp egy nagy kampányra készül, és Anna tudta, hogy a pontos készletkezelés kulcsfontosságú. Először észrevette, hogy a régi „Vintage Kávéscsésze Szett” még mindig szerepel az adatbázisban, amit sürgősen törölni akart, hogy elkerülje a téves rendeléseket. Gyorsan megnyitotta a „Termékek” menüt, megkereste a terméket, majd törölte azt.
Ezután hozzáadott egy új terméket, a „Modern Kávéhabosítót”, amit a kampány részeként kínáltak. Kitöltötte az összes adatot, és mentette a terméket, amely azonnal megjelent a táblázatban. Anna még egy gyors ellenőrzést végzett, beállította, hogy egyszerre 100 sor jelenjen meg, és megbizonyosodott arról, hogy minden adat helyesen szerepel. Elégedetten zárta le a munkát, tudva, hogy a nyilvántartás készen áll a kampányra, és hozzájárult a cég sikeréhez.

### Tamás, a lelkiismeretes logisztikai koordinátor
Tamás, a lelkiismeretes logisztikai koordinátor, megnyitotta a raktárkezelő alkalmazást, hogy frissítse a megrendelések státuszát. A „Megrendelések” opcióra kattintva egy táblázat jelent meg előtte, amelyben azonosítók, megrendelők és státuszokat változtató mező szerepeltek. Észrevette, hogy néhány régi rendelést még nem zárt le, holott azok már teljesítve lettek. Gyorsan végig ment a táblázaton, és bepipálta a „lezárva” és „teljesítve” mezőket az érintett megrendeléseknél, ezzel biztosítva, hogy minden naprakész legyen.
Miután végzett, egy új megrendelést is rögzített. A „Új megrendelés hozzáadása” gombra kattintva megnyitotta az űrlapot, kitöltötte az ügyfél email címét, a termék cikkszámát és mennyiségét, majd mentette az adatokat. Az új rendelés azonnal megjelent a táblázatban. Tamás, a lelkiismeretes logisztikai koordinátor elégedetten állapította meg, hogy az összes rendelés pontosan rögzítve van, és készen állt további teendőire.

### Péter, a páratlan raktárvezető
Péter, a páratlan raktárvezető, épp a napi leltározás előtt állt, és frissíteni akarta a raktáron lévő termékek nyilvántartását. Belépett a rendszerbe, és a "Raktáron lévő termékek" menüpontra kattintott. A táblázatban látta a termékek cikkszámát, nevét, lokációját, mennyiségét és szabad mennyiségét. Péter, a páratlan raktárvezető észrevette, hogy egy termék mennyisége alacsonyan van, így rákattintott a "Új termék hozzáadása" gombra, és felvitte az új készletet a rendszerbe. Ezután beállította, hogy egyszerre 50 sor jelenjen meg, hogy könnyebben átnézhesse a raktárkészletet. Miután frissítette a nyilvántartást, elégedetten folytatta a munkát, biztosítva, hogy a készlet naprakész maradjon.

## "Főoldal" oldal
Navigációs gombokat szolgáltat amikkel oldalak között lehet navigálni oda-vissza.

## "Termékek" oldal
- Termékek adatait tartalmazza. Cikkszám, Termék neve, Ár, Súly, Kategória, Törlés

- Egy termék cikkszám alapján csak egyszer szerepelhet a táblázatban.

- Lehet termékeket törölni. Üzenet mellé: Termék sikeresen törölve!

- Lehet sorrendbe helyezni az adatokat a oszlopnevekre kattintva növekvőbe, vagy akár csökkenőbe.

- Lehet új terméket hozzáadni. Ha egy cikkszám már létezik az adatbázisban akkor hibát ad nekünk: A cikkszám már létezik.  Nem lehet új terméket hozzáadni!
- Ellenkező esetben: Termék sikeresen hozzáadva!
 
 - Be lehet állítani hogy egy oldalon hány sor jelenjen meg a termékek táblából
 Oldalszám navigáció(|Előző| |1| |2| |3| |4| |Következő| |Utolsó oldal|)

## "Ügyfelek" oldal
- Ügyfelek adatait tartalmazza. Név, Irányítószám, Város, Utca, Házszám, Email, Törlés

- Egy ügyfél csak egyszer szerepelhet a táblázatban email alapján.

- Lehet ügyfeleket törölni. Üzenet mellé: Ügyfél sikeresen törölve!

- Lehet sorrendbe helyezni az adatokat a oszlopnevekre kattintva növekvőbe, vagy akár csökkenőbe.

- Lehet új ügyfelet hozzáadni. Email címre figyelni kell hogy egyszer ha már megvan a táblázatban akkor nem engedi hozzáadni.

- Az alábbi hibaüzenetet dobja: Ez az email cím már létezik!

- Ellenkező esetben: Ügyfél sikeresen hozzáadva!

- Be lehet állítani hogy egy oldalon hány sor jelenjen meg az ügyfelek táblából.
Oldalszám navigáció(|Előző| |1| |2| |3| |4| |Következő| |Utolsó oldal|)

## "Raktáron" oldal
- Raktáron lévő termékek adatait tartalmazza. Cikkszám, Termék, Lokáció, Mennyiség, Szabad mennyiség, Törlés.

- Egy terméket csak akkor tudunk hozzáadni ha az már létezik a termékek táblában cikkszám alapján. Ellenkező esetben az alábbi üzenetet dobja: Hibás cikkszám! Ez a termék nem létezik.

- Sikeres hozzáadáskor az üzenet:Új termék hozzáadva a raktárhoz!

- Egy termék többször is lehet a raktárban ugyebár mivel egy termék több lokáción is lehet.

- Ha egy meglévő lokációra ugyanazzal a cikkszámmal rendelkező terméket szeretnénk hozzáadni mint ami már van ott, akkor a mennyiséghez csak simán hozzáadódik a hozzáadni kívánt termék mennyisége. Az alábbi üzenetet dobja ekkor: A mennyiség frissítve lett!

- Lehet raktáron lévő termékeket törölni a törlés gombbal. Üzenet ekkor: A rekord sikeresen törölve lett!

- Be lehet állítani hogy egy oldalon hány sor jelenjen meg az raktáron lévő termékek táblából táblából.
Oldalszám navigáció(|Előző| |1| |2| |3| |4| |Következő| |Utolsó oldal|)

## "Megrendelések" oldal
- Megrendelésekről tartalmaz adatokat. Order_Id, Megrendelő neve, ÖsszMegrendelt termékek mennyisége, Súlya, Illetve lezárva/Teljesítve gombok.

- Lehet hozzáadni új megrendeléseket. Ez egy külön oldalon történik, ahol a rendelési szám random generálódik ha üresen hagyjuk. Ellenkező esetben ha egy már meglévő megrendelési számot adunk meg, akkor a megrendelés_ID-jára kattintva egy oldalra dob minket a hivatkozás, ahol a megrendelt termékek vannak összegezve az ügyfel és megrendelés adatokkal.

- Egy adott megrendeléshez csak a megrendelés nevén lévő ügyfél tud új terméket megvásárolni.

- Ha egy megrendeléshez két ügyfélnek akarjuk hozzáadni a megrendelését, akkor a hibát kapunk ami kiírja hogy a megrendelés nem létezik vagy már egy adott ügyfél nevén van.

- A megrendelésben lévő termékmennyiségek levonódnak a raktáron lévő szabad mennyiségből, de csak akkor vonódik le a teljes mennyiségből, ha már a megrendelés teljesült, azaz a futárcég elszállította.

- Ha már egy meglévő termék van a megrendelésben, akkor a megrendelésen belüli termék mennyisége csak simán frissül.

- Be lehet állítani hogy egy oldalon hány sor jelenjen meg a termékek táblából
Oldalszám navigáció(|Előző| |1| |2| |3| |4| |Következő| |Utolsó oldal|)

## "Rendelés részletei" oldal
Ez tartalmazza az ügyfélinformációkat, rendelésinformációkat összegezven, mint például teljes ár, teljes súly, és ezek alatt a termékekről az információkat külön táblázatban vannak megjelenítve. Alul található egy gomb ami visszavisz minket a megrendelések oldalra.



## Adatok hozzáadásának oldalai
- Az új adatok hozzáadása mindig egy új oldalon nyílik meg ahol meg lehet adni az adatokat.

- Minden oldalon, ahol egy termék megjelenik cikkszám alapján ott rá lehet kattintani a cikkszámra, ami minket egy oldalra visz ahol a termék adatai jelennek meg.
