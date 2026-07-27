# Task-Tracker-CLI
Cool Task Tracker for CLI made in Python using the language's native libraries for archive handling (JSON, pathlib) and creating commands (argparse)

Project URL: https://roadmap.sh/projects/task-tracker

Usage:

Create a JSON file named "storage.json" to your editor or within your local files 

# Add, Update, and Delete tasks

    task.py add --status choices["todo", "in-progress", "done"]
    task.py update id title
    task.py delete id

# Mark a task as in progress or done

    task.py mark-in-progress id
    task.py mark-done id

# List all tasks   

    task.py list 

# List all tasks that are done

    task.py list done

# List all tasks that are not done

    task.py list todo
    
# List all tasks that are in progress

    task.py list in-progress
