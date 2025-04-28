<h1>**🗂️ Task Manager CLI Project URL: (https://youtu.be/kpQI78TXtus)** </h1>

A simple and efficient Command-Line Interface (CLI) based Task Manager built using Python and SQLite. This tool provides users with the ability to manage their daily tasks in a structured, user-friendly environment — all within the terminal. Whether you're a beginner learning Python or someone who just needs a lightweight task manager, this project is an ideal fit.

🎯 Key Features 👤 User Authentication Login & Signup support for multiple users.

Each user's tasks are securely tied to their unique profile.

✅ Task Management Add new tasks with: A title A priority level (0–9) A deadline (must be a future date) Tasks are timestamped at the time of creation.

📋 Task Views Pending Tasks: Lists all uncompleted tasks in a tabular format. Completed Tasks: Separate view to track tasks marked as done. Mark Complete: Users can update task statuses to “done” with ease.

📊 Interactive Dashboard Upon successful login, a dashboard gives an instant overview: Total tasks Completed tasks Pending tasks Overdue tasks (missed deadlines)

🖥️ Clean CLI Display Clear screen transitions between each action (compatible with Windows, macOS, and Linux). Uses the tabulate library to present tasks in a clean and readable table format.

🧩 Database Schema This project uses SQLite for local data persistence with two tables:

Table: users Column Type Description id INTEGER Primary key (auto-incremented) name TEXT Username password TEXT Password (plain-text for demo purposes)

Table: tasks Column Type Description id INTEGER Primary key user_id INTEGER Foreign key referencing users.id task TEXT Task description/title priority INTEGER Priority level (0–9) deadline TEXT Deadline date (YYYY-MM-DD) created TEXT Timestamp when the task was created status INTEGER 0 = pending, 1 = completed

⚠️ Important Notes 🔐 Passwords are stored in plain text for simplicity. For real-world applications, hashing is essential. 📅 Deadlines must be set to a future date during task creation. 👥 Each user only sees their own tasks — there's no shared task visibility between users. 🧼 The interface clears the screen between actions for a smoother experience (compatible with both Windows and Unix-based systems). 💾 All data is saved locally using SQLite, making it lightweight and portable.

🙌 Credits This project was inspired by the need for a simple CLI-based productivity tool and serves as a great learning resource for Python beginners who want to work with: Databases (sqlite3) CLI interactions Date/time management User sessions and authentication External libraries (tabulate)
