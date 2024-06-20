# Sistem de Jurnalizare: Journiary

## Descrierea aplicației

Aplicația Journiary este realizată folosind Django, un framework web pentru Python. Aplicația oferă posibilitatea de a crea subiecte, exemplu: " Viața profesională ", de a crea intrări pentru subiecte, exemplu: "Interviul tehnic ", " Prima zi la muncă ", selectarea emoției trăite cât și modificarea datelor precum titlului, conținutului și emoția unei intrări.

Pe lângă acestea, utilizatorul are opțiunea de a căuta în lista de subiecte și intrări atât după un interval calendaristic, cât și dupa titlu. Este prezent și un grafic cu totalitatea emoțiilor trăite pentru ușurarea procesului de introspecție a utilizatorului. 

## Codul sursă al aplicației - GitHub repository

Pentru a accesa codul sursă al aplicației faceți click [aici](https://github.com/Azetlex/Journiary/tree/master)


## Pentru rularea aplicației este necesară instalarea următoarelor:
   - Descărcați [Python](https://www.python.org/downloads/), iar în timpul instalării asigurați-vă că selectați “Add Python to PATH”. Aceasta va permite folosirea în terminal a comenzii " python ", comandă care va fi folosită anterior.
   - Cel mai probabil pip va fi instalat deodată cu Python, dar dacă nu, intrați [aici](https://bootstrap.pypa.io/), iar mai apoi click-dreapta pe " get-pip.py " urmat de " Save link as " și îl salvați în directorul unde s-a instalat Python 
   - Descărcați [Git](https://git-scm.com/download/win).
  

## Pașii de compilare ai aplicației
### Pentru această etapă, apăsați click-dreapta pe " licență2 " și selectați " Open Git Bash here ". După deschiderea terminalului, scrieți următoarele comenzi:

1. **Clonarea repository-ului**
   ```bash
   git clone https://github.com/Azetlex/Journiary.git
   cd Journiary
2.  **Crearea unui mediu virtual**

```bash
python -m venv venv
source venv\Scripts\activate
```
3. **Instalarea dependințelor**

```bash
cd ..     ## Până vă intoarceți în directorul " licență2 "
pip install -r requirements.txt
```
4. **Aplicarea migrațiilor pentru baza de date**

```bash
python manage.py migrate
```
## Pașii de lansare a aplicației

### 1. Crearea unui superuser pentru accesul la panoul de administrare

```bash
winpty python manage.py createsuperuser
```
### 2. Lansarea serverului de dezvoltare

```bash
python manage.py runserver
```
### 3.Accesarea aplicatiei
Deschideți browser-ul web și accesați următorul link http://127.0.0.1:8000 pentru a accesa aplicația de jurnal.
   
