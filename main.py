import argparse
import json
import os

def load_tasks():
    if not os.path.exists("tasks.json"):
        return []
    try:
        with open("tasks.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False,indent=2)

def add_task(title):
    tasks = load_tasks()
    new_id = len(tasks) + 1
    tasks.append({"id": new_id, "title": title, "status": "未完成"})
    save_tasks(tasks)
    print(f"✔️ 已添加任务：{title}")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == len(new_tasks):
        print("😟 没找到该任务ID")
    else:
        save_tasks(new_tasks)
        print(f"✔️ 已删除任务 {task_id}")

def update_status(task_id, status):
    tasks = load_tasks()
    found = False
    for t in tasks:
        if task_id == t["id"]:
            t["status"] = status
            found = True
            break
    if found:
        save_tasks(tasks)
        print(f"🆕 已更新任务 {task_id} 状态为：{status}")
    else:
        print("😟 没找到该任务ID")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("😟 当前没有任务")
        return
    print("🍫 当前任务列表：")
    for t in tasks:
        print(f"{t['id']}. {t['title']}  {t['status']}")

def edit_title(task_id, new_title):
    tasks = load_tasks()
    found = False
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = new_title
            found = True
            break
    if found:
        save_tasks(tasks)
        print("更新完成")
    else:
        print("未找到任务id")

def main():
    parser = argparse.ArgumentParser(description="简单的任务管理器")
    parser.add_argument("command", help="操作：add, delete, list, done, edit")
    parser.add_argument("argument", nargs="?", help="命令的参数，比如任务名或ID")

    args = parser.parse_args()

    if args.command == "add":
        if not args.argument:
            print("❗ 请输入任务内容")
        else:
            add_task(args.argument)
    elif args.command == "delete":
        if not args.argument:
            print("❗ 请输入要删除的任务ID")
        else:
            delete_task(int(args.argument))
    elif args.command == "done":
        if not args.argument:
            print("❗ 请输入要更新的任务ID")
        else:
            update_status(int(args.argument), "已完成")
    elif args.command == "edit":
        if not args.argument:
            print("❗ 请输入要编辑的任务ID")
        else:
            edit_title(int(args.argument), input("请输入新的标题："))
    elif args.command == "list":
        list_tasks()
    else:
        print("❗ 未知命令，请输入 --help 查看用法")

if __name__ == "__main__":
    main()