# 🐈 ShantiCat Controller

**ShantiCat Controller** — это Python-приложение для приёма BLE Advertising-пакетов от умного ошейника **ShantiCat Collar**, их декодирования и подготовки данных для последующего хранения, анализа и визуализации.

Проект является частью экосистемы **ShantiCat**.


# Архитектура

```text
                  +------------------+
                  | ShantiCat Collar |
                  +--------+---------+
                           |
                    BLE Advertising
                           |
                           ▼
               +----------------------+
               | BLE Collector        |
               +----------+-----------+
                          |
                          ▼
               +----------------------+
               | Protocol Decoder     |
               +----------+-----------+
                          |
                          ▼
               +----------------------+
               | CollarMeasurement    |
               +----------+-----------+
                          |
                          ▼
                  Последующая обработка

            +------------------------------+
            | TimescaleDB                  |
            | Анализ активности            |
            | Telegram Bot                 |
            | Web API                      |
            +------------------------------+
```

---

# Установка

Клонируйте репозиторий:

```bash
git clone https://github.com/ShantiCat/ShantiCatController.git
cd ShantiCatController
```

Создайте виртуальное окружение:

```bash
python -m venv .venv
```

Активируйте его.

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Установите проект:

```bash
pip install -e .
```

---

# Запуск

```bash
python -m shanti_cat_controller
```