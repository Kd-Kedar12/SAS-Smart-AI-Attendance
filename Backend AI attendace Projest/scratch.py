from src.database.db import _in_memory, _unenroll_student_in_memory

_in_memory['subject_students'] = [
    {'student_id': 1, 'subject_id': 10},
    {'student_id': 1, 'subject_id': 20},
    {'student_id': 2, 'subject_id': 10}
]
print("Before:", _in_memory['subject_students'])
_unenroll_student_in_memory(1, 10)
print("After:", _in_memory['subject_students'])
