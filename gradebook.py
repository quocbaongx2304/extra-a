import json
import os

FILE = "gradebook.json"


def load_data():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_course(data, course):
    for c in data:
        if c["code"] == course["code"]:
            return False
    data.append(course)
    save_data(data)
    return True


def update_course(data, code, new_info):
    for c in data:
        if c["code"] == code:
            c.update(new_info)
            save_data(data)
            return True
    return False


def delete_course(data, code):
    for c in data:
        if c["code"] == code:
            data.remove(c)
            save_data(data)
            return True
    return False


def calculate_gpa(data):
    if not data:
        return 0
    total = 0
    total_credits = 0
    for c in data:
        total += c["score"] * c["credits"]
        total_credits += c["credits"]
    return round(total / total_credits, 2) if total_credits else 0


def calculate_gpa_by_semester(data, semester):
    filtered = [c for c in data if c["semester"] == semester]
    return calculate_gpa(filtered)


def get_float(prompt, min_v=0, max_v=10):
    while True:
        try:
            v = float(input(prompt))
            if v < min_v or v > max_v:
                print("Score must be between 0–10.")
                continue
            return v
        except:
            print("Invalid input.")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except:
            print("Invalid input.")


def view_gradebook(data):
    if not data:
        print("\nNo courses found.")
        return
    print("\n======= GRADEBOOK =======")
    for c in data:
        print(f"{c['code']} | {c['name']} | {c['credits']} credits | Semester {c['semester']} | Score: {c['score']}")
    print("=========================")


def print_menu():
    print("\n===== Student Gradebook CLI =====")
    print("1. Add course")
    print("2. Update course")
    print("3. Delete course")
    print("4. View gradebook")
    print("5. Calculate GPA")
    print("6. GPA by semester")
    print("0. Exit")
    print("================================")


def main():
    data = load_data()

    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            code = input("Course code: ").strip()
            name = input("Course name: ").strip()
            credits = get_int("Credits: ")
            semester = get_int("Semester: ")
            score = get_float("Score (0–10): ")
            course = {
                "code": code,
                "name": name,
                "credits": credits,
                "semester": semester,
                "score": score
            }
            if add_course(data, course):
                print("Course added.")
            else:
                print("Course code already exists.")

        elif choice == "2":
            code = input("Course code to update: ").strip()
            print("Leave blank to keep current value.")
            new_name = input("New name: ").strip()
            new_credits = input("New credits: ").strip()
            new_sem = input("New semester: ").strip()
            new_score = input("New score: ").strip()
            new_info = {}
            if new_name:
                new_info["name"] = new_name
            if new_credits:
                new_info["credits"] = int(new_credits)
            if new_sem:
                new_info["semester"] = int(new_sem)
            if new_score:
                new_info["score"] = float(new_score)
            if update_course(data, code, new_info):
                print("Course updated.")
            else:
                print("Course not found.")

        elif choice == "3":
            code = input("Course code to delete: ").strip()
            if delete_course(data, code):
                print("Course deleted.")
            else:
                print("Course not found.")

        elif choice == "4":
            view_gradebook(data)

        elif choice == "5":
            print("Overall GPA:", calculate_gpa(data))

        elif choice == "6":
            sem = get_int("Enter semester: ")
            print("Semester GPA:", calculate_gpa_by_semester(data, sem))

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
