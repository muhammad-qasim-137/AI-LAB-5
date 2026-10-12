import csv
import os

filename = "patients.csv"
fields = ["id", "age", "bmi", "blood_pressure", "glucose", "diabetes"]

if not os.path.exists(filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows([
            {"id": "P101", "age": 45, "bmi": 28.4, "blood_pressure": 125, "glucose": 145, "diabetes": "positive"},
            {"id": "P102", "age": 32, "bmi": 23.1, "blood_pressure": 118, "glucose": 92, "diabetes": "negative"},
            {"id": "P103", "age": 57, "bmi": 31.2, "blood_pressure": 140, "glucose": 180, "diabetes": "positive"}
        ])


def read_patients():
    with open(filename, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def save_patients(patients):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(patients)


patients = read_patients()
print("Patient records:")
for patient in patients:
    print(patient)

positive = sum(p["diabetes"].lower() == "positive" for p in patients)
negative = sum(p["diabetes"].lower() == "negative" for p in patients)
threshold = float(input("Glucose threshold: "))

print("Positive cases:", positive)
print("Negative cases:", negative)
print("Patients above glucose threshold:")
for patient in patients:
    if float(patient["glucose"]) > threshold:
        print(patient)

if patients:
    print("Average BMI:", sum(float(p["bmi"]) for p in patients) / len(patients))
    print("Average glucose:", sum(float(p["glucose"]) for p in patients) / len(patients))

choice = input("Add or update a record? (add/update/no): ").strip().lower()
if choice == "add":
    patient_id = input("New patient ID: ").strip()
    if any(p["id"] == patient_id for p in patients):
        print("ID already exists.")
    else:
        patients.append({
            "id": patient_id,
            "age": input("Age: ").strip(),
            "bmi": input("BMI: ").strip(),
            "blood_pressure": input("Blood pressure: ").strip(),
            "glucose": input("Glucose: ").strip(),
            "diabetes": input("Diabetes (positive/negative): ").strip().lower()
        })
        save_patients(patients)
        print("Record added.")
elif choice == "update":
    patient_id = input("Patient ID to update: ").strip()
    found = False
    for p in patients:
        if p["id"] == patient_id:
            p["age"] = input("New age: ").strip()
            p["bmi"] = input("New BMI: ").strip()
            p["blood_pressure"] = input("New blood pressure: ").strip()
            p["glucose"] = input("New glucose: ").strip()
            p["diabetes"] = input("New diabetes label: ").strip().lower()
            found = True
            break
    if found:
        save_patients(patients)
        print("Record updated.")
    else:
        print("Patient ID not found.")
