import os
import glob

def list_logs():
    files = sorted(glob.glob(".github/prompts/prs_*.prompt.md"))
    for i, f in enumerate(files):
        print(f"[{i+1}] {f}")
    return files

def view_log(index):
    files = list_logs()
    if 0 <= index < len(files):
        print(open(files[index]).read())
    else:
        print("Invalid index.")

def search_logs(keyword):
    matches = []
    for f in glob.glob(".github/prompts/prs_*.prompt.md"):
        if keyword.lower() in open(f).read().lower():
            matches.append(f)
    for f in matches:
        print(f)

def main():
    while True:
        print("\n[PRS Memory CLI]")
        print("1. List logs")
        print("2. View a log")
        print("3. Search logs")
        print("4. Exit")
        choice = input("Choose: ")
        if choice == "1":
            list_logs()
        elif choice == "2":
            idx = int(input("Index: ")) - 1
            view_log(idx)
        elif choice == "3":
            kw = input("Keyword: ")
            search_logs(kw)
        elif choice == "4":
            break

if __name__ == "__main__":
    main()
