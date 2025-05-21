import os
import json

def load_lessons():
    """Load all lessons from the data/lessons directory."""
    lessons_dir = os.path.join(os.path.dirname(__file__), 'lessons')
    lessons = {}

    for i, filename in enumerate(os.listdir(lessons_dir)):
        if filename.endswith('.json'):
            with open(os.path.join(lessons_dir, filename), 'r', encoding='utf-8') as file:
                lesson_data = json.load(file)
                # Użyj unikalnego ID, dodając indeks dla duplikatów
                lesson_id = os.path.splitext(filename)[0]  # Nazwa pliku (bez rozszerzenia)
                if " copy" in lesson_id:
                    # Zamień "example_lesson copy" na "example_lesson_copy" dla lepszej obsługi
                    lesson_id = lesson_id.replace(" copy", "_copy")
                if lesson_id in lessons:
                    # Jeśli ID już istnieje, dodaj indeks
                    lesson_id = f"{lesson_id}_{i}"
                lessons[lesson_id] = lesson_data

    return lessons