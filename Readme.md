

````markdown
# 🥗 Health Simplified CLI

A clean, user-friendly command-line interface app to track your food intake, calorie goals, and meal plans — all backed by SQLite and SQLAlchemy.

---

## 🚀 Features

- Track food entries by user, calorie count, and date.
- Set daily and weekly calorie goals.
- Plan meals for specific weeks and days.
- Generate reports across custom date ranges.
- Built with **Typer** for a rich CLI experience and **SQLAlchemy** for robust database handling.

---

## 📦 Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd health-simplified-cli
````

### 2. Install Dependencies

Using **pip**:

```bash
pip install .
```

Or using **Pipenv**:

```bash
pipenv install
pipenv shell
```

---

## 🧑‍💻 Usage

Launch the CLI:

```bash
myapp --help
```

### 👥 User Management

```bash
myapp user create --name Alice
myapp user list
```

### 🍎 Food Entries

```bash
myapp entry add --user Alice --food Apple --calories 95 --date 2025-06-02
myapp entry list --user Alice
myapp entry update --id 1 --food Banana --calories 120
myapp entry delete --id 1
```

### 🎯 Goals

```bash
myapp goal set --user Alice --daily-calories 1500 --weekly-calories 10500
myapp goal list --user Alice
```

### 🥗 Meal Planning

```bash
myapp plan-meal --user Alice --week 1 --meals "Mon: Salad"
```

### 📊 Reporting

```bash
myapp report --user Alice --start-date 2025-06-01 --end-date 2025-06-07
```

---

## 🧪 Testing

Run tests with coverage:

```bash
pipenv run pytest --cov=health_tracker --cov-report=term-missing
```

---

## 📁 Project Structure

```
health-simplified-cli/
├── health_tracker/
│   ├── cli.py            # CLI commands
│   ├── database.py       # DB connection setup
│   └── models.py         # SQLAlchemy models
├── tests/
│   ├── test_cli.py
│   └── test_models.py
├── debug.py              # Script to test CLI functionality
├── Pipfile
├── pyproject.toml
└── README.md
```

---

## 📌 Requirements

* Python **3.11+**
* Dependencies:

  * `sqlalchemy`
  * `typer`
  * `pytest`

---



## 💬 Feedback

Found a bug or have a feature request?  write me an email 

https://elvisamonde.vercel.app/
