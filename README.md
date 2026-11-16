# Build a habit tracking application showcasing simple CLI and minimal GUI with Object oriented & Functional programming with Python.

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Pytest](https://img.shields.io/badge/Testing-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org)
[![Architecture](https://img.shields.io/badge/Architecture-Modular--4--Layer-orange?style=for-the-badge)](#-project-architecture--modules)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](#)


---

[Key Features](#-key-features) •
[Architecture](#-project-architecture--modules) •
[Quick Start](#-installation--setup) •
[Demo Workflow](#-interactive-demo-workflow) •
[Testing](#-automated-testing-suite)

---

Integrating new habits to daily life gradually impacts a human's overall health. Few determine to build good habits and break bad habits. Writing down the schedule of each habit is a no stranger method. But wanting to know the progress of it over a period of time is where this kind of approach lacks behind. This is when an application that can help in tracking habits comes into the play and lets you decide the flexiblity in type, periodicity, addition ,deletion and category . 



<img width="800" height="600" alt="VideoProject1-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/dbfc2252-1279-4b85-8ae7-f0c54e870d31" />





## Features of App

> Interact with just arrows and enter keys.

> No need to type each interaction.

>Gives you motivation by displaying a new quote each day.

>Provides **Daily** and **Weekly** habits.

>Add or delete habits flexibly.

> Provides **Build** and **Break** options for habits.

> Lets you build **streaks** based on your **consistency**.

> **Analyzes** habits and lets you know top performing and least performing habit.

> Lets you analyze each **individual habit** to see where you are progressing and lacking.

The foundation of project begins with designing the files in such a way that does not break at any level. The folder consists of python files namely habit, main, analytics, database, test_tracker, quotes, app_gui. Two database files of habits and test_habit_tracker. One UML diagram. 

##  Project Architecture & Modules
The application is structured into four core layers to ensure high maintainability, testability, and separation of concerns:
1. **User Interface (`main.py`):** Interactive Command Line Interface (CLI) managing user menus and commands.
2. **Core Domain Model (`habit.py`):** Object-Oriented Programming (OOP) class encapsulating habit attributes (`habit_id`, `name`, `periodicity`, `created_at`) and behavioral methods (`complete_task()`).
3. **Persistence Layer (`database.py`):** Acts as a habit manager. Manages SQLite relational database tables (`habits` and `tracker_logs`) with foreign key constraints, cascading deletions, and pre-loaded test fixtures.
4. **Analytics Engine (`analytics.py`):** Pure functional programming module calculating daily/weekly streaks, periodicity filters, and historical performance without side effects.Analytics acts as a heart of this project as it deals with calculating streaks ;one of the main reasons to build.


To create a virtual environment,
```
python -m venv venv
```

> It is important to activate the virtual environment after creating it. 

 **CLI**- Uses Questionary library. It ensures the user to have an effortless interaction with the application. It asks options in between to select like daily or weekly, checking-off habit from the habit list. The user interacts with the cli menu with Upward & Downward arrow, ,Enter keys. You don't need to type the whole input out there except while creating a habit.  Here's the command to launch the application CLI,
```
python main.py
```
**GUI**- Uses Pandas library. Streamlit was used to develop the graphical interface of the application. Here's the command to view it,

```
streamlit run app_gui.py
```

Here's the local host link 
```
http://localhost:8501
```

The following picture briefly shows the user flow on a technical note:

![alt text](<diagram uf .drawio.png>)

To install the dependencies, 
```
pip install -r requirements.txt
```

To run tests, 

```
pytest
```
**License MIT**
