Tasks CRUD API with SQLite
A simple REST API for managing tasks, built with Python (Flask) and SQLite. This project is the continuation of an in-memory CRUD assignment — the array was replaced with a real database while keeping the exact same API.

The big idea: the API describes what the app does, the database describes where it stores data. The client can't tell the difference.

Why SQLite?
Serverless — no separate database server, installation, or configuration needed.
Single file — the entire database lives in one file: tasks.db.
Zero setup — the database and table are created automatically on the first run.
Standard SQL — everything learned here transfers directly to PostgreSQL or MySQL later.
Where is the data stored?
All tasks are stored in a file called tasks.db in the project root. It is created automatically the first time the server starts.

Want a fresh start? Just delete tasks.db and restart the server — the file, the table, and the three example tasks will be recreated.

Project Structure
.
├── main.py      # Flask app: API routes + database setup (all in one file)
├── tasks.db     # SQLite database file (auto-created, safe to delete)
└── README.md
How to Run
1. Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
2. Install dependencies
pip install flask
3. Start the server
python main.py
The database file tasks.db and the tasks table are created automatically, and three example tasks are inserted only on the first run.

4. Test the API
The server runs at http://127.0.0.1:5000.

Method	Endpoint	Description	Success	Error
GET	/tasks	Get all tasks	200	—
GET	/tasks/<id>	Get one task	200	404
POST	/tasks	Create a task { "title": "..." }	201	400 (missing title)
PUT	/tasks/<id>	Update a task { "title": "...", "done": true }	200	404
DELETE	/tasks/<id>	Delete a task	204	404
Example requests
# Get all tasks
curl http://127.0.0.1:5000/tasks

# Create a task
curl -X POST http://127.0.0.1:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'

# Update a task
curl -X PUT http://127.0.0.1:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete a task
curl -X DELETE http://127.0.0.1:5000/tasks/1
Database Schema
Column	Type	Description
id	INTEGER	Primary key, auto-incremented
title	TEXT	The task description (required)
done	BOOLEAN	Completion status (stored as 0/1)
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN DEFAULT 0
);
Exploring the Database
Open tasks.db with a SQLite viewer — DB Browser for SQLite is recommended.

Example query I executed
-- Show only completed tasks
SELECT * FROM tasks WHERE done = 1;
Other useful queries
SELECT * FROM tasks;              -- list every task
SELECT COUNT(*) FROM tasks;       -- count all tasks
UPDATE tasks SET done = 1;        -- mark every task as completed
DELETE FROM tasks WHERE done = 1; -- delete all completed tasks
Any change made directly in the viewer is immediately visible through the API — and vice versa — because both are reading and writing the same tasks.db file.

Screenshot
Database viewer screenshot

How the API Talks to the Database
Every endpoint runs a SQL query instead of touching an in-memory array:

Endpoint	SQL operation
GET /tasks	SELECT * FROM tasks
GET /tasks/<id>	SELECT * FROM tasks WHERE id = ?
POST /tasks	INSERT INTO tasks (title, done) VALUES (?, ?)
PUT /tasks/<id>	UPDATE tasks SET ... WHERE id = ?
DELETE /tasks/<id>	DELETE FROM tasks WHERE id = ?
Notes on safety and correctness:

Parameterized queries (? placeholders) are used everywhere to prevent SQL injection.
404 handling — the app checks a task exists (with a SELECT) before updating or deleting, because SQL UPDATE/DELETE on a missing row silently affects 0 rows.
Persistence — restarting the server no longer loses any data.
Assignment Requirements Checklist
 Same CRUD endpoints as the previous (in-memory) assignment
 Tasks stored in SQLite instead of memory
 Data survives server restarts
 Database file created automatically if missing
 tasks table created automatically if missing
 Three example tasks inserted only on the first run
 CRUD operations implemented with SQL queries
 Unknown ids return 404 { "error": "Task not found" }
 Invalid requests (missing title) return 400
Glossary
Term	Meaning
Database	A system that stores data permanently, even after a program stops running.
SQLite	A lightweight SQL database stored in a single file. No separate server required.
Table	A collection of related data organized into rows and columns.
Row	One record in a table — in this project, one task is one row.
Column	A property stored for every row, such as title or done.
SQL	Structured Query Language — used to create, read, update, and delete data.
Query	A SQL command sent to a database (SELECT, INSERT, UPDATE, DELETE).
Primary key	A column whose value uniquely identifies every row (id).
Persistence	Data remaining available after the application stops and starts again.
Schema	The structure of a database — its tables and columns.
