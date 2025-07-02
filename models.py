class User:
    def __init__(self,username,password):
        self.username=username
        self._password=password
    
    def check_password(self,password):
        return self._password==password
    
    def __repr__(self):
        return f"User(username='{self.username}')"
    
class Task:
    def __init__(self,title,category,deadline,priority,completed=False):
        self.title=title
        self.category=category
        self.deadline=deadline
        self.priority=priority
        self.completed=completed

    def mark_complete(self):
        self.completed=True

    def __repr__(self):
        return f"Task('{self.title}','{self.category}','{self.deadline}','{self.priority}',completed={self.completed})"

if __name__=="__main__":
    user=User("marisu","secure123")
    print(user.check_password("wrong"))
    print(user.check_password("secure123"))

    task= Task("Finish project", "Work","2025-07-03","High")
    print(task)
    task.mark_complete()
    print(task)
