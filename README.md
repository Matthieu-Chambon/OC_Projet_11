# Projet 11 – Améliorez une application Web Python par des tests et du débogage

## 📚 Description

**Güdlft** est une plateforme de réservation de compétitions régionales de force athlétique. Initialement développée pour les grandes marques de vêtements de fitness, une version légère a été demandée pour répondre aux besoins des clubs locaux.

Cette application permet aux secrétaires de clubs :
- de se connecter à l’aide de leur adresse e-mail
- de visualiser les compétitions à venir
- d’utiliser leurs points pour inscrire des athlètes
- de visualiser le nombre de points disponibles pour chaque club

---

## 📥 Installation et exécution

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/Matthieu-Chambon/OC_Projet_11
cd OC_Projet_11
```

### 2️⃣ Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4️⃣ Lancer l’application

#### Windows Powershell :

```bash
$env:FLASK_APP = "server.py"
$env:FLASK_ENV = "development"
flask run
```

#### Windows CMD :

```cmd
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

#### macOS / Linux :

```bash
export FLASK_APP=server.py
export FLASK_ENV=development
flask run
```

Par défaut, l'application est accessible à l’adresse : [http://127.0.0.1:5000](http://127.0.0.1:5000)


---

## 🧪 Tests

### Structure des tests :

* `unit_tests/` : tests unitaires
* `integration_tests/` : tests d’intégration
* `functional_tests/` : tests fonctionnels
* `performance_tests/` : tests Locust

### Lancer tous les tests :

```bash
pytest
```

---

## 📊 Couverture de tests

Le projet utilise **pytest-cov** pour mesurer la couverture de code.

### Générer la couverture :

```bash
pytest --cov=. --cov-report html
```

### Voir le rapport HTML :

```bash
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS
```

---

## 📈 Tests de performance (Locust)

Locust permet de tester la performance de l’application avec plusieurs utilisateurs simultanés.

### Lancer Locust :

```bash
locust -f .\tests\performance_tests\locustfile.py
```

Puis ouvrez votre navigateur à [http://localhost:8089](http://localhost:8089)

### Résultats des tests de performance (Locust)

| Type | Endpoint | # Requests | # Fails | Average (ms) | Max (ms) |
|------|----------|------------|---------|--------------|----------|
| GET  | `/` | 96 | 0 | 3.99 | 19 |
| GET  | `/book/Spring%20Festival/Simply%20Lift` | 101 | 0 | 3.67 | 18 |
| GET  | `/pointsDisplay` | 82 | 0 | 3.17 | 19 |
| POST | `/purchasePlaces` | 252 | 0 | 3.83 | 20 |
| POST | `/showSummary` | 87 | 0 | 7.03 | 31 |
| **Total** | — | **618** | **0** | **4.19** | **31** |

Avec comme paramétrage :

* Nombre d’utilisateurs : 6
* Ramping rate : 1 utilisateur/s
* Host : http://127.0.0.1:5000
* Run time : 1m

---

## 🛠️ Technologies utilisées

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [pytest](https://docs.pytest.org/)
- [coverage](https://coverage.readthedocs.io/)
- [Locust](https://locust.io/)
- [Selenium](https://www.selenium.dev/)

---

## ✅ Conformité

* **TDD** (Test-Driven Development)
* **Nom des branches** : `error/nom`, `bug/nom`, `feature/nom`
* **Code requis** dans `QA` avant fusion dans `master`
* **Couverture cible** : 60% minimum (97% atteints dans ce projet 🎯)
* **Rapport Locust** : chargement des pages < 5 sec, mises à jour < 2 sec
