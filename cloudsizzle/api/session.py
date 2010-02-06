class Session(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.user_id = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def open(self):
        """Open a new session and log in with given username and password."""
        pass

    def close(self):
        """Close the current session and log out."""
        pass



    """
    Everything from there downwards will probably be stored in Django Model
    """


    def add_to_planned_courses(self, course_code):
        """Add a course to this user's planned courses."""
        pass

    def remove_from_planned_courses(self, course_code):
        """Remove a course from this user's planned courses."""
        pass

    def get_events(self):
        """Returns the events of this user."""
        pass

    def get_planned_courses(self):
        """Returns the planned courses of this user."""
        pass

    def get_completed_courses(self):
        """Returns the completed courses for this user """
        pass

    def is_planned_course(self, course_code):
        pass

    def is_completed_course(self, course_code):
        pass
