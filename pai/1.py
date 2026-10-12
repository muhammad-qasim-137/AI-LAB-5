def read_experiments(filename):
    experiments = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 5:
                    experiments.append({
                        "id": parts[0],
                        "model": parts[1],
                        "dataset": parts[2],
                        "learning_rate": parts[3],
                        "epochs": parts[4]
                    })
    except FileNotFoundError:
        pass
    return experiments


def save_experiments(filename, experiments):
    with open(filename, "w", encoding="utf-8") as file:
        for exp in experiments:
            file.write("|".join([
                exp["id"], exp["model"], exp["dataset"],
                exp["learning_rate"], exp["epochs"]
            ]) + "\n")


def display(experiments):
    if not experiments:
        print("No experiments found.")
    for exp in experiments:
        print(exp)


filename = "experiments.txt"

experiments = read_experiments(filename)
if not experiments:
    experiments = [
        {"id": "E101", "model": "CNN", "dataset": "CIFAR10", "learning_rate": "0.001", "epochs": "20"},
        {"id": "E102", "model": "LSTM", "dataset": "IMDB", "learning_rate": "0.01", "epochs": "10"}
    ]
    save_experiments(filename, experiments)

while True:
    print("\n1 Display  2 Search  3 Add  4 Update  5 Remove  6 Exit")
    choice = input("Choose: ").strip()

    if choice == "1":
        display(read_experiments(filename))
    elif choice == "2":
        exp_id = input("Experiment ID: ").strip()
        matches = [e for e in read_experiments(filename) if e["id"] == exp_id]
        display(matches)
    elif choice == "3":
        experiments = read_experiments(filename)
        exp_id = input("ID: ").strip()
        if any(e["id"] == exp_id for e in experiments):
            print("That ID already exists.")
        else:
            experiments.append({
                "id": exp_id,
                "model": input("Model name: ").strip(),
                "dataset": input("Dataset name: ").strip(),
                "learning_rate": input("Learning rate: ").strip(),
                "epochs": input("Epochs: ").strip()
            })
            save_experiments(filename, experiments)
            print("Experiment added.")
    elif choice == "4":
        experiments = read_experiments(filename)
        exp_id = input("ID to update: ").strip()
        found = False
        for exp in experiments:
            if exp["id"] == exp_id:
                exp["model"] = input("New model name: ").strip()
                exp["dataset"] = input("New dataset name: ").strip()
                exp["learning_rate"] = input("New learning rate: ").strip()
                exp["epochs"] = input("New epochs: ").strip()
                found = True
                break
        if found:
            save_experiments(filename, experiments)
            print("Experiment updated.")
        else:
            print("Experiment not found.")
    elif choice == "5":
        experiments = read_experiments(filename)
        exp_id = input("ID to remove: ").strip()
        updated = [e for e in experiments if e["id"] != exp_id]
        if len(updated) == len(experiments):
            print("Experiment not found.")
        else:
            save_experiments(filename, updated)
            print("Experiment removed.")
    elif choice == "6":
        break
    else:
        print("Invalid choice.")
