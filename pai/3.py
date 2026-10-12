import json
import os

filename = "model_results.json"

if not os.path.exists(filename):
    initial_results = [
        {"model": "Random Forest", "accuracy": 0.91, "precision": 0.89, "recall": 0.90, "f1_score": 0.895},
        {"model": "Neural Network", "accuracy": 0.94, "precision": 0.92, "recall": 0.91, "f1_score": 0.915},
        {"model": "SVM", "accuracy": 0.88, "precision": 0.86, "recall": 0.87, "f1_score": 0.865}
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(initial_results, file, indent=4)


def load_results():
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_results(results):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)


results = load_results()
if results:
    print("Highest accuracy:", max(results, key=lambda x: x["accuracy"]))
    print("Highest F1-score:", max(results, key=lambda x: x["f1_score"]))

while True:
    print("\n1 Display  2 Add  3 Update  4 Remove  5 Exit")
    choice = input("Choose: ").strip()

    if choice == "1":
        print(json.dumps(load_results(), indent=4))
    elif choice == "2":
        results = load_results()
        name = input("Model name: ").strip()
        if any(r["model"].lower() == name.lower() for r in results):
            print("Model already exists.")
        else:
            results.append({
                "model": name,
                "accuracy": float(input("Accuracy: ")),
                "precision": float(input("Precision: ")),
                "recall": float(input("Recall: ")),
                "f1_score": float(input("F1-score: "))
            })
            save_results(results)
            print("Model result added.")
    elif choice == "3":
        results = load_results()
        name = input("Model name to update: ").strip()
        found = False
        for r in results:
            if r["model"].lower() == name.lower():
                r["accuracy"] = float(input("New accuracy: "))
                r["precision"] = float(input("New precision: "))
                r["recall"] = float(input("New recall: "))
                r["f1_score"] = float(input("New F1-score: "))
                found = True
                break
        if found:
            save_results(results)
            print("Result updated.")
        else:
            print("Model not found.")
    elif choice == "4":
        results = load_results()
        name = input("Model name to remove: ").strip()
        updated = [r for r in results if r["model"].lower() != name.lower()]
        if len(updated) == len(results):
            print("Model not found.")
        else:
            save_results(updated)
            print("Result removed.")
    elif choice == "5":
        break
    else:
        print("Invalid choice.")
