import argparse
import random
import json
import datetime


class Task:
    def __init__(self, desc, id, createdAt, updatedAt, status):
        self.desc = desc
        self.id = id
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.status = status


def task_to_dict(obj):
    if isinstance(obj, Task):
        return {"desc": obj.desc, "ID": obj.id, "createdAt": obj.createdAt.strftime("%Y-%m-%d %H:%M:%S"), "updatedAt": obj.updatedAt.strftime("%Y-%m-%d %H:%M:%S"),
                "status": obj.status}
    raise TypeError("Object Task is not JSON serializable")


def add_task(args):
    id = random.randint(10000, 99999)
    status = "To-Do"
    new_task = Task(args.desc, id, datetime.datetime.now(), datetime.datetime.now(), status)

    print("Done")

    try:
        with open("tasks.json", 'r') as json_file:
            tasks = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    # Append the new task
    tasks.append(task_to_dict(new_task))

    # Write the updated task list to the file
    with open("tasks.json", 'w') as json_file:
        print(f"Writing to tasks.json: {tasks}")  # Just before the `json.dump` call
        json.dump(tasks, json_file, indent=4)

    print(f"Task '{args.desc}' added with ID: {id}")


def rem_task(args):
    try:
        with open("tasks.json", 'r') as json_file:
            tasks = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []
    print(tasks)

    for i, item in enumerate(tasks):
        if item["desc"] == args.desc:
            tasks.pop(i)  # Pop the matching dictionary
            break  # Exit the loop once the item is found and popped

    with open("tasks.json", 'w') as json_file:
        print(f"Writing to tasks.json: {tasks}")  # Just before the `json.dump` call
        json.dump(tasks, json_file, indent=4)

    print(f"Task '{args.desc}' removed with ID: {id}")


def complete_task(args):
    try:
        with open("tasks.json", 'r') as json_file:
            tasks = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    # Iterate through the list and pop the dictionary that matches the description
    for i, item in enumerate(tasks):
        if item["desc"] == args.desc:
            item["status"] = "Done"
            item["updatedAt"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")# Pop the matching dictionary
            break  # Exit the loop once the item is found and popped

    with open("tasks.json", 'w') as json_file:
        print(f"Writing to tasks.json: {tasks}")  # Just before the `json.dump` call
        json.dump(tasks, json_file, indent=4)

    print(f"Task '{args.desc}' completed with ID: {id}")


def get_tasks(args):
    try:
        with open("tasks.json", 'r') as json_file:
            tasks = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    for i, item in enumerate(tasks):
        if item["status"] != "Done":
            description = item["desc"]
            created = item["createdAt"]
            updated = item['updatedAt']
            status = item["status"]
            print(f"Task: {description} \nCreated at: {created} \nUpdated at: {updated} \nStatus: {status} \n")


def update_tasks(args):
    try:
        with open("tasks.json", 'r') as json_file:
            tasks = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    for i, item in enumerate(tasks):
        if item["desc"] == args.desc and args.in_progress:
            item["status"] = 'In Progress'
            print("Task now in progress")
        elif item["desc"] == args.desc:
            item["desc"] = args.new_name
            print("Task name updated")


    with open("tasks.json", 'w') as json_file:
        json.dump(tasks, json_file, indent=4)

def finished_tasks(args):
    try:
        with open("tasks.json", 'r') as json_file:
            tasks = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    # Iterate through the list and pop the dictionary that matches the description
    for i, item in enumerate(tasks):
        if item["status"] == "Done":
            description = item["desc"]
            created = item["createdAt"]
            updated = item['updatedAt']
            status = item["status"]
            print(f"Task: {description} \nCreated at: {created} \nUpdated at: {updated} \nStatus: {status} \n")


if __name__ == "__main__":
    Tasks = argparse.ArgumentParser(description='A task manager CLI program')

    subparsers = Tasks.add_subparsers(dest="command")

    ##Add Subcommand
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("-d", "--desc", type=str, help="Name of the task", required=True)
    add_parser.set_defaults(func=add_task)

    ##Remove Subcommand
    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("-d", "--desc", type=str, help="Name of the task", required=True)
    remove_parser.set_defaults(func=rem_task)

    #Complete Subcommand
    complete_parser = subparsers.add_parser("complete", help="Completing a task")
    complete_parser.add_argument("-d", "--desc", type=str, help="Name of the task", required=True)
    complete_parser.set_defaults(func=complete_task)

    #Pull unfinished task list
    get_tasks_parser = subparsers.add_parser("get", help="Pull uncompleted list of tasks")
    get_tasks_parser.set_defaults(func=get_tasks)

    #Pull finished task list
    finished_tasks_parser = subparsers.add_parser("finished", help="Pull completed list of tasks")
    finished_tasks_parser.set_defaults(func=finished_tasks)

    #Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("-d", "--desc", type=str, help="Name of the task", required=True)
    update_parser.add_argument("-i", "--in_progress", help="Change status to In-progress")
    update_parser.add_argument("-n", "--new_name", type=str, help='New name for task')
    update_parser.set_defaults(func=update_tasks)

    args = Tasks.parse_args()

    if args.command:
        args.func(args)
    else:
        Tasks.print_help()


