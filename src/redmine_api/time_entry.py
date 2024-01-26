class TimeEntry:
    def __init__(self, parameters: dict):
        self.id = parameters.get("id")
        self.project = parameters.get("project")
        self.issue = parameters.get("issue")
        self.user = parameters.get("user")
        self.activity = parameters.get("activity")
        self.hours = parameters.get("hours")
        self.comments = parameters.get("comments")
        self.spent_on = parameters.get("spent_on")
        self.created_on = parameters.get("created_on")
        self.updated_on = parameters.get("updated_on")

    def __str__(self):
        time_entry = f"{self.project['name']:<21.20} "
        time_entry += f"{self.issue['id']:>6} "
        time_entry += f"{self.user['name']:<21.20} "
        time_entry += f"{self.activity['name']:<15.14} "
        time_entry += f"{self.spent_on:<11} "
        time_entry += f"{self.hours:>6} hours"

        return time_entry