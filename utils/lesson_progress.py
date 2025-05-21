import json
import os
from datetime import datetime

def save_lesson_progress(username, lesson_id, step, notes=None):
    """Save user's progress in a lesson"""
    progress_file = 'lesson_progress.json'
    
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress_data = json.load(f)
    else:
        progress_data = {}
    
    if username not in progress_data:
        progress_data[username] = {}
    
    progress_data[username][str(lesson_id)] = {
        'current_step': step,
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'notes': notes or {},
        'bookmarks': progress_data.get(username, {}).get(str(lesson_id), {}).get('bookmarks', [])
    }
    
    with open(progress_file, 'w') as f:
        json.dump(progress_data, f)

def get_lesson_progress(username, lesson_id):
    """Get user's progress in a lesson"""
    if os.path.exists('lesson_progress.json'):
        with open('lesson_progress.json', 'r') as f:
            progress_data = json.load(f)
            
        if username in progress_data and str(lesson_id) in progress_data[username]:
            return progress_data[username][str(lesson_id)]
    
    return {
        'current_step': 'intro',
        'notes': {},
        'bookmarks': []
    }

def save_lesson_note(username, lesson_id, step, note):
    """Save a note for a specific part of the lesson"""
    progress = get_lesson_progress(username, lesson_id)
    if 'notes' not in progress:
        progress['notes'] = {}
    
    if step not in progress['notes']:
        progress['notes'][step] = []
    
    note_entry = {
        'text': note,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    progress['notes'][step].append(note_entry)
    
    save_lesson_progress(username, lesson_id, progress['current_step'], progress['notes'])

def add_bookmark(username, lesson_id, step, description):
    """Add a bookmark to a specific part of the lesson"""
    progress = get_lesson_progress(username, lesson_id)
    
    bookmark = {
        'step': step,
        'description': description,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if 'bookmarks' not in progress:
        progress['bookmarks'] = []
    
    progress['bookmarks'].append(bookmark)
    save_lesson_progress(username, lesson_id, progress['current_step'], progress.get('notes', {}))

def get_bookmarks(username, lesson_id):
    """Get all bookmarks for a lesson"""
    progress = get_lesson_progress(username, lesson_id)
    return progress.get('bookmarks', [])