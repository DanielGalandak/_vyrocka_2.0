Doplnil jsem tvou poznámku o hlavní funkcionalitě (editace textu a tvorba grafů) a informaci, že role a oprávnění zatím nejsou plně implementovány, ale model i logika jsou připravené. Tady je upravený README:

---

# Django Redakční Systém – Reports Project

## Popis projektu

Tento projekt je víceaplikační Django řešení sloužící jako redakční systém pro tvorbu, správu a publikaci odborných reportů.
Hlavní funkcionalitou je možnost **editovat textový obsah (odstavce)** a **vytvářet grafy**.
Projekt obsahuje uživatelské role a oprávnění, které **zatím nejsou plně implementovány**, ale v databázovém modelu i logice (`profiles`) je připravena jejich podpora.

---

## Architektura projektu

Projekt je rozdělen do tří hlavních Django aplikací:

### **1. reports/**

* Správa reportů, sekcí a obsahových prvků.
* Modely: `Report`, `Section`, `Paragraph`, `Chart`, `Table`.
* Vrstva `repositories.py` pro ORM operace (CRUD).
* `services.py` obsahuje business logiku (publikace, schvalování, řazení obsahu).
* `utils.py` řeší validace a generování PDF.
* `views.py` – výpis publikovaných i rozpracovaných reportů.
* Obsahuje rozsáhlé jednotkové testy (`tests.py`).

### **2. profiles/**

* Správa uživatelských účtů a profilů (`UserProfile`).
* Implementace uživatelských rolí: **ADMIN**, **EDITOR**, **WRITER**, **READER** (logika připravena, propojení s views částečně chybí).
* Registrace a přihlášení uživatelů.
* `decorators.py` a `services.py` – kontrola oprávnění a autorizace.

### **3. data\_sources/**

* Evidence externích datových zdrojů (souborových i API).
* Modely: `DataSource` a `Data` (uložení obsahu do JSONField).
* Napojení na grafy a tabulky v reportech.

---

## Technologie

* **Python 3.10+**
* **Django 4+**
* **SQLite** (defaultní databáze)
* **ReportLab** – generování PDF
* HTML šablony (Django Templates) + základní CSS
* Testy psané pomocí `django.test.TestCase`

---

## Instalace a spuštění

1. **Naklonujte repozitář:**

   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```

2. **Vytvořte virtuální prostředí a aktivujte jej:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux / Mac
   venv\Scripts\activate     # Windows
   ```

3. **Nainstalujte závislosti:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Proveďte migrace databáze:**

   ```bash
   python manage.py migrate
   ```

5. **Vytvořte superuživatele:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Spusťte vývojový server:**

   ```bash
   python manage.py runserver
   ```

7. **Otevřete aplikaci v prohlížeči:**

   ```
   http://127.0.0.1:8000/
   ```

---

## Testování

Projekt obsahuje unit testy pro `reports`, `profiles` a `utils`.
Pro spuštění testů použijte:

```bash
python manage.py test
```

---

## Uživatelské role a oprávnění

* **ADMIN** – kompletní správa uživatelů, publikace reportů.
* **EDITOR** – schvalování a publikace obsahu.
* **WRITER** – vytváření a editace vlastních draftů.
* **READER** – přístup pouze k publikovaným reportům.

> **Poznámka:** Logika rolí je připravená v modelech a services, ale aktuální verze aplikace nemá plně implementované restrikce na úrovni views a šablon.

---

## Modely a struktura obsahu

Reporty jsou členěny do **sekcí** a ty obsahují různé **prvky obsahu** (`Paragraph`, `Chart`, `Table`).
Každý prvek má svůj **stav**: DRAFT → STAGED → APPROVED → PUBLISHED.

