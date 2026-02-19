from __future__ import annotations

import sys
from pathlib import Path


def parse_log_line(line: str) -> dict:
    """
    Парсить один рядок логу у словник:
    {"date": "...", "time": "...", "level": "...", "message": "..."}.

    Якщо рядок має некоректний формат — повертає порожній dict.
    """
    line = line.strip()
    if not line:
        return {}

    parts = line.split(" ", 3)  # розбиваємо максимум на 4 частини
    if len(parts) < 4:
        return {}

    date, time, level, message = parts
    return {"date": date, "time": time, "level": level.upper(), "message": message}


def load_logs(file_path: str) -> list[dict]:
    """
    Завантажує лог-файл і повертає список словників-логів.
    Некоректні рядки ігноруються.
    """
    logs: list[dict] = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parsed = parse_log_line(line)
                if parsed:
                    logs.append(parsed)
    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}")
    except OSError as e:
        print(f"Помилка читання файлу: {e}")

    return logs


def filter_logs_by_level(logs: list[dict], level: str) -> list[dict]:
    """
    Повертає лише ті логи, де рівень збігається з level.
    level може бути у будь-якому регістрі (error/ERROR/Error).
    """
    level = level.upper()
    return list(filter(lambda log: log.get("level") == level, logs))


def count_logs_by_level(logs: list[dict]) -> dict[str, int]:
    """
    Рахує кількість записів для кожного рівня логування.
    """
    counts: dict[str, int] = {}
    for log in logs:
        lvl = log.get("level", "UNKNOWN")
        counts[lvl] = counts.get(lvl, 0) + 1
    return counts


def display_log_counts(counts: dict[str, int]) -> None:
    """
    Виводить таблицю з кількістю записів по рівнях логування.
    """
    print("Рівень логування | Кількість")
    print("-----------------|----------")

    # Сортуємо по назві рівня для стабільного виводу
    for level in sorted(counts.keys()):
        print(f"{level:<16} | {counts[level]}")


def display_log_details(logs: list[dict], level: str) -> None:
    """
    Виводить деталі логів для заданого рівня.
    Формат: YYYY-MM-DD HH:MM:SS - message
    """
    level = level.upper()
    print(f"\nДеталі логів для рівня '{level}':")

    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main() -> None:
    # Очікуємо: python task3.py /path/to/logfile.log [level]
    if len(sys.argv) < 2:
        print("Використання: python task3.py /path/to/logfile.log [level]")
        sys.exit(1)

    file_path = sys.argv[1]
    level_arg = sys.argv[2] if len(sys.argv) > 2 else None

    # Перевірка, що шлях існує і це файл
    path_obj = Path(file_path)
    if not path_obj.exists():
        print(f"Файл не знайдено: {file_path}")
        sys.exit(1)
    if not path_obj.is_file():
        print(f"Це не файл: {file_path}")
        sys.exit(1)

    logs = load_logs(file_path)
    if not logs:
        # якщо файл порожній або всі рядки некоректні — теж покажемо “порожню” статистику
        display_log_counts({})
        return

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level_arg:
        filtered = filter_logs_by_level(logs, level_arg)
        display_log_details(filtered, level_arg)


if __name__ == "__main__":
    main()