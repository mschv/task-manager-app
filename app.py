from flask import Flask,render_template,request,redirect,session,url_for
import database

app=Flask(__name__)
app.secret_key="supersecretkey" #Needed for session

#initialize the database
database.init_db()

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        user=database.get_user(username)

        if user and user[2]==password:  #user[2]=stored password
            session["user_id"]=user[0]
            session["username"]=user[1]
            return redirect("/dashboard")

        else:
            return "Invalid credentials",401
    
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        success=database.add_user(username,password)

        if success:
            return redirect("/login")
        else:
            return "Username already exists",409
    
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    filter_value = request.args.get("filter", "all")

    if filter_value == "completed":
        tasks = database.get_tasks_by_status(user_id, completed=True)
    elif filter_value == "pending":
        tasks = database.get_tasks_by_status(user_id, completed=False)
    else:
        tasks = database.get_tasks_by_user(user_id)

    print("DEBUG: tasks from DB:", tasks)
    return render_template("dashboard.html", tasks=tasks, username=session["username"], filter=filter_value)


@app.route("/add-task",methods=["POST"])
def add_task():
    if "user_id" not in session:
        return redirect("/login")

    title=request.form["title"]
    category=request.form["category"]
    deadline=request.form["deadline"]
    priority=request.form["priority"]

    database.add_task(session["user_id"],title,category,deadline,priority)
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    if "user_id" not in session:
        return redirect("/login")
    
    database.toggle_task_completion(task_id)
    return redirect("/dashboard")

@app.route("/delete/<int:task_id>",methods=["POST"])
def delete_task(task_id):
    if "user_id" not in session:
        return redirect("/login")
    
    database.delete_task(task_id)
    return redirect("/dashboard")

@app.route("/edit/<int:task_id>",methods=["GET","POST"])
def edit_task(task_id):
    if "user_id" not in session:
        return redirect("/login")

    if request.method=="POST":
        title=request.form["title"]
        category=request.form["category"]
        deadline=request.form["deadline"]
        priority=request.form["priority"]
        database.update_task(task_id,title,category,deadline,priority)
        return redirect("/dashboard")

    task=database.get_task_by_id(task_id)
    return render_template("edit_task.html",task=task)
if __name__=="__main__":
    app.run(debug=True)