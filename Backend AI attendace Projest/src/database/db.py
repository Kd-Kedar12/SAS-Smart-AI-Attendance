import bcrypt
from src.database.config import supabase

SUPABASE_AVAILABLE = supabase is not None

# If Supabase isn't configured, provide a lightweight in-memory fallback
if not SUPABASE_AVAILABLE:
    print('Supabase not available — using in-memory database fallback.')
    _in_memory = {
        'students': [],
        'teachers': [],
        'subjects': [],
        'subject_students': [],
        'attendance_logs': []
    }

    def _next_id(collection):
        return len(_in_memory[collection]) + 1

    def _create_student_in_memory(new_name, face_embedding=None, voice_embedding=None):
        sid = _next_id('students')
        student = {
            'student_id': sid,
            'name': new_name,
            'face_embedding': face_embedding,
            'voice_embedding': voice_embedding
        }
        _in_memory['students'].append(student)
        return [student]

    def _get_all_students_in_memory():
        return list(_in_memory['students'])

    def _create_attendance_in_memory(logs):
        _in_memory['attendance_logs'].extend(logs)
        return logs

    def _get_student_subjects_in_memory(student_id):
        res = [ss for ss in _in_memory['subject_students'] if ss['student_id'] == student_id]
        # simulate join with subjects
        out = []
        for ss in res:
            subj = next((s for s in _in_memory['subjects'] if s['subject_id'] == ss['subject_id']), {})
            out.append({'subjects': subj})
        return out

    def _get_student_attendance_in_memory(student_id):
        return [log for log in _in_memory['attendance_logs'] if log.get('student_id') == student_id]

    def _enroll_student_in_memory(student_id, subject_id):
        _in_memory['subject_students'].append({'student_id': student_id, 'subject_id': subject_id})
        return [{'student_id': student_id, 'subject_id': subject_id}]

    def _unenroll_student_in_memory(student_id, subject_id):
        before = len(_in_memory['subject_students'])
        _in_memory['subject_students'] = [ss for ss in _in_memory['subject_students'] if not (ss['student_id']==student_id and ss['subject_id']==subject_id)]
        return []

    # Expose fallback names expected by the rest of the code
    def get_all_students():
        return _get_all_students_in_memory()

    def create_student(new_name, face_embedding=None, voice_embedding=None):
        return _create_student_in_memory(new_name, face_embedding, voice_embedding)

    def create_attendance(logs):
        return _create_attendance_in_memory(logs)

    def get_student_subjects(student_id):
        return _get_student_subjects_in_memory(student_id)

    def get_student_attendance(student_id):
        return _get_student_attendance_in_memory(student_id)

    def enroll_student_to_subject(student_id, subject_id):
        return _enroll_student_in_memory(student_id, subject_id)

    def unenroll_student_to_subject(student_id, subject_id):
        return _unenroll_student_in_memory(student_id, subject_id)

    # Teacher and subject fallbacks
    def check_teacher_exists(username):
        return any(t for t in _in_memory['teachers'] if t.get('username') == username)

    def create_teacher(username, password, name):
        tid = _next_id('teachers')
        teacher = {'teacher_id': tid, 'username': username, 'password': bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), 'name': name}
        _in_memory['teachers'].append(teacher)
        return [teacher]

    def teacher_login(username, password):
        teacher = next((t for t in _in_memory['teachers'] if t.get('username') == username), None)
        if teacher and bcrypt.checkpw(password.encode(), teacher['password'].encode()):
            return teacher
        return None

    def create_subject(subject_code, name, section, teacher_id):
        sid = _next_id('subjects')
        subject = {'subject_id': sid, 'subject_code': subject_code, 'name': name, 'section': section, 'teacher_id': teacher_id}
        _in_memory['subjects'].append(subject)
        return [subject]

    def get_teacher_subjects(teacher_id):
        # Return simple representation similar to Supabase response
        res = [s for s in _in_memory['subjects'] if s.get('teacher_id') == teacher_id]
        out = []
        for s in res:
            out.append({'subject_id': s['subject_id'], 'subject_code': s['subject_code'], 'name': s['name'], 'section': s['section'], 'total_students': len([ss for ss in _in_memory['subject_students'] if ss['subject_id']==s['subject_id']])})
        return out

    def get_attendance_for_teacher(teacher_id):
        # Return attendance logs for subjects of the teacher
        teacher_subject_ids = [s['subject_id'] for s in _in_memory['subjects'] if s.get('teacher_id')==teacher_id]
        return [log for log in _in_memory['attendance_logs'] if log.get('subject_id') in teacher_subject_ids]

# End in-memory fallback


if SUPABASE_AVAILABLE:

    def hash_pass(pwd):
        return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

    def check_pass(pwd, hashed):
        return bcrypt.checkpw(pwd.encode(), hashed.encode())

    def check_teacher_exists(username):
        # Check for unique username, returns true when username is already taken
        response = supabase.table("teachers").select("username").eq("username", username).execute()
        return len(response.data) > 0


    def create_teacher (username, password, name):

        data = {"username" : username, "password": hash_pass(password), "name" : name}
        response = supabase.table("teachers").insert(data).execute()
        return response.data


    def teacher_login(username, password):
        response = supabase.table("teachers").select("*").eq("username", username).execute()
        if response.data:
            teacher  = response.data[0]
            if check_pass(password, teacher['password']):
                return teacher
        return None

    def get_all_students():
        response = supabase.table("students").select('*').execute()
        return response.data

    def create_student(new_name, face_embedding = None, voice_embedding = None):
        data = {"name": new_name, "face_embedding": face_embedding, "voice_embedding": voice_embedding}
        response = supabase.table("students").insert(data).execute()
        return response.data

    def create_subject(subject_code, name, section, teacher_id):
        data = {'subject_code' : subject_code, 'name' : name, 'section' : section, 'teacher_id' : teacher_id}
        response = supabase.table("subjects").insert(data).execute()
        return response.data

    def get_teacher_subjects(teacher_id):
        response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
        subjects = response.data


        for sub in subjects:
            sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
            attendance = sub.get('attendance_logs', [])
            unique_sessions = len(set(log['timestamp'] for log in attendance))
            sub['total_classes'] = unique_sessions


            sub.pop('subject_student', None)
            sub.pop('attendance_logs', None)

        return subjects

    def  enroll_student_to_subject(student_id, subject_id):
        data = {'student_id': student_id, "subject_id": subject_id}
        response= supabase.table('subject_students').insert(data).execute()
        return response.data

    def  unenroll_student_to_subject(student_id, subject_id):
        response= supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
        return response.data

    def get_student_subjects(student_id):
        response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
        return response.data

    def get_student_attendance(student_id):
        response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
        return response.data

    def create_attendance(logs):
        response = supabase.table('attendance_logs').insert(logs).execute()
        return response.data

    def get_attendance_for_teacher(teacher_id):
        response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
        return response.data

else:
    # when supabase is not available we already exposed minimal fallback implementations above
    pass