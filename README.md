# test2
Testovacie Python zadanie - verzia 2.0

## Požiadavky na spustenie:
- Python 3 + zoznam modulov je v súbore requirements.txt

## Pokyny k spusteniu (pre windows) : 
Stiahnite si repozitár. V priečinku Test_AMCEF si otvorte konzolu a vytvorte si virtuálne prostredie pre našu aplikáciu.

**python3 -m venv virtual**, prípadne **python -m venv virtual**

Virtuálne prostredie sa bude nachádzať v priečinku **virtual**. 
Teraz musíme prostredie aktivovať. V konzole sa presunieme do priečinka virtual a následne do priečinka Scripts
**cd virtual/Scripts** a prostredie aktivujeme príkazom **activate** , ktorý zadáme tiež do konzoly.

Pred cestou aktuálneho adresára v konzole by sa nám malo zobrazovať **(virtual)**.

Vrátime sa do priečinka Test_AMCEF 2x zadaním príkazu **cd ..** .

V priečinku Test_AMCEF si nainštalujeme všetky potrebné knižnice (Django,requests...), ktorých zoznam nájdeme v súbore **requirements.txt**.

**pip install -r requirements.txt**.

Po nainštalovaní všetkých knižníc môžeme spustiť (lokálny) server príkazom **python manage.py runserver**.

V konzole by sa mala zobraziť adresa servera (**127.0.0.1:8000**), ktorú stačí zadať do prehliadača.
Zoznam všetkých dostupných adries a použiteľných metód nájdete v API dokumentácii (openapi.yaml).


Súhrn všetkých príkazov : 
- **python -m venv virtual** 
- **cd virtual/Scripts**
- **activate**
- **cd ..**
- **cd ..**
- **pip install -r requirements.txt**
- **python manage.py runserver**.
