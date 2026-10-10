import threading


class Database:
    """Thread-safe in-memory store for the academic platform."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_db()
            return cls._instance

    def _init_db(self):
        self.students = {}
        self.courses = {}
        self.enrollments = []
        self._seed()

    def _seed(self):
        self.students["S101"] = {"student_id": "S101", "name": "Alice Johnson",
                                 "email": "alice@university.edu", "credits": 0}
        self.students["S102"] = {"student_id": "S102", "name": "Bob Mehta",
                                 "email": "bob@university.edu", "credits": 0}
        courses = [
            ("C101", "Cloud Computing", 6, "MON-09"),
            ("C102", "DevOps Engineering", 6, "TUE-09"),
            ("C103", "Data Structures", 6, "WED-09"),
            ("C104", "Databases", 6, "MON-09"),
        ]
        for cid, title, credits, slot in courses:
            self.courses[cid] = {"course_id": cid, "title": title, "credits": credits,
                                 "slot": slot, "capacity": 30, "enrolled": 0}

    def reset(self):
        with self._lock:
            self.students.clear()
            self.courses.clear()
            self.enrollments.clear()
            self._seed()


db = Database()
