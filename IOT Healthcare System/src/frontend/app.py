import email

from backend.backendService import Service
from backend.sensor_runner import run_sensor_stream
import threading, queue

service = Service()

def menu():
    print("\nWhat do you want to do?")
    print("1 - Add a new patient")
    print("2 - See all patients")
    print("3 - See last 10 minutes of readings")
    print("4 - See all readings for a patient")
    print("5 - Quit")

def add_patient():
    print("\nAdding a new patient.")
    name = input("Patient name: ")
    age = input("Age: ").strip()
    if not age.isdigit():
        print("Age must be a valid number.")
        return
    email = input("Email: ").strip()
    if not email or "@" not in email:
        print("Please enter a valid email.")
        return
    try:
        service.add_patient(name, int(age), email)
        print(f"Done! {name} has been added.")
    except Exception as e:
        print(f"Something went wrong: {e}")

def list_patients():
    print("\nHere are all the patients:")
    patients = service.list_patients()
    if not patients:
        print("No patients in the system yet.")
        return
    for p in patients:
        print(f"  [{p[0]}] {p[1]} | Age: {p[2]} | Email: {p[3]}")

def view_all_readings():
    print("\nAll readings for a patient.")
    name = input("Patient name: ")
    patient = service.get_patient_by_name(name)
    if not patient:
        print(f"Could not find a patient named '{name}'.")
        return
    readings = service.get_all_readings(patient[0])
    if not readings:
        print("No readings found.")
        return
    print(f"\nAll readings for {name}:")
    for r in readings:
        print(f"  Heart Rate: {r[2]} bpm | Temp: {r[3]}°C | Blood O2: {r[4]}% | Time: {r[5]}")


def view_last_10_minutes_readings():
    print("\nLet's look up readings for a patient.")
    name = input("Patient name: ")
    patient = service.get_patient_by_name(name)
    if not patient:
        print(f"Could not find a patient named '{name}'.")
        return
    readings = service.get_last_10_min_readings(patient[0])
    if not readings:
        print("No readings found for this patient.")
        return
    print(f"\nReadings for {name}:")
    for r in readings:
        print(f"  Heart Rate: {r[2]} bpm | Temp: {r[3]}°C | Blood O2: {r[4]}% | Time: {r[5]}")

def printQueueElement(queue):
    if queue.empty():
        print("No alerts right now.")
        return
    while not queue.empty():
        print(queue.get())


alert_queue = queue.Queue();
patient_list = service.list_patients()
patient_names = []
for patient in patient_list:
    patient_names.append(patient[1])
sensors_thread = threading.Thread(target=run_sensor_stream, args=(patient_names, alert_queue), daemon=True)
sensors_thread.start()


while True:
    printQueueElement(alert_queue)
    menu()
    choice = input("\nYour choice: ")

    if choice == "1":
        add_patient()
    elif choice == "2":
        list_patients()
    elif choice == "3":
        view_last_10_minutes_readings()
    elif choice == "4":
        view_all_readings()
    elif choice == "5":
        print("\nGoodbye.")
        break
    else:
        print("That's not a valid option. Try again.")
