import re
from datetime import date


NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z\s'-]{1,49}$")
PHONE_PATTERN = re.compile(r"^(0[7-9][01]\d{8}|\+234[7-9][01]\d{8})$")
VALID_GENDERS = {"male", "female"}
MIN_AGE = 0
MAX_AGE = 90


class Patient:
    def __init__(self, mrn, name, date_of_birth, phone, gender):
        self.mrn = mrn
        self.name = name
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.gender = gender
        self.is_active = True

    def age(self):
        today = date.today()
        years = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            years -= 1
        return years

    def __str__(self):
        return f"{self.mrn} | {self.name} | Age: {self.age()} | Phone: {self.phone} | Gender: {self.gender}"


patients = []
next_mrn_number = 1


def generate_mrn():
    global next_mrn_number
    mrn = f"P{next_mrn_number:03d}"
    next_mrn_number += 1
    return mrn


def get_valid_date(prompt):
    while True:
        raw = input(prompt)
        parts = raw.split("-")
        try:
            if len(parts) != 3:
                raise ValueError
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            dob = date(year, month, day)
            if dob > date.today():
                print("Date of birth can't be in the future. Try again.")
                continue

            # NEW: enforce the age ceiling right here, since age depends on dob.
            today = date.today()
            years = today.year - dob.year
            if (today.month, today.day) < (dob.month, dob.day):
                years -= 1
            if years < MIN_AGE or years > MAX_AGE:
                print(f"Age must be between {MIN_AGE} and {MAX_AGE}. Try again.")
                continue

            return dob
        except ValueError:
            print("Invalid date. Use format YYYY-MM-DD, e.g. 1995-06-20.")


def get_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This can't be empty. Try again.")


def get_valid_name(prompt):
    while True:
        value = input(prompt).strip()
        if NAME_PATTERN.match(value):
            return value.title()
        print("Name must contain only letters, spaces, hyphens or apostrophes "
              "(2-50 characters). Try again.")


def get_valid_phone(prompt):
    while True:
        value = input(prompt).strip().replace(" ", "")
        if PHONE_PATTERN.match(value):
            return value
        print("Phone must be 11 digits starting with 0 (e.g. 08012345678) "
              "or +234 (e.g. +234801234567) followed by 10 digits. Try again.")


def get_valid_gender(prompt):
    while True:
        value = input(prompt).strip().lower()
        if value in VALID_GENDERS:
            return value.title()
        print(f"Gender must be one of: {', '.join(sorted(VALID_GENDERS))}. Try again.")




def add_patient():
    name = get_valid_name("Name: ")
    dob = get_valid_date("Date of birth (YYYY-MM-DD): ")
    phone = get_valid_phone("Phone (e.g. 08012345678): ")
    gender = get_valid_gender("Gender (Male/Female): ")
    mrn = generate_mrn()
    patients.append(Patient(mrn, name, dob, phone, gender))
    print(f"Added. MRN is {mrn}.")


def list_patients():
    active = [p for p in patients if p.is_active]
    if not active:
        print("No patients on file.")
        return
    for p in active:
        print(p)


def find_patient():
    query = input("Search by name or MRN: ").strip().lower()
    matches = [
        p for p in patients
        if p.is_active and (query == p.mrn.lower() or query in p.name.lower())
    ]
    if not matches:
        print("No matching patient found.")
        return None
    for p in matches:
        print(p)
    return matches


def update_phone():
    matches = find_patient()
    if not matches:
        return
    mrn = input("Enter MRN of the patient to update: ").strip().upper()
    for p in patients:
        if p.mrn == mrn and p.is_active:
            new_phone = get_valid_phone("New phone number (e.g. 08012345678): ")
            p.phone = new_phone
            print("Updated.")
            return
    print("MRN not found among matches.")


def remove_patient():
    mrn = input("Enter MRN to remove: ").strip().upper()
    for p in patients:
        if p.mrn == mrn and p.is_active:
            p.is_active = False  # soft delete: keep the record, just hide it
            print(f"{p.name} deactivated (record kept, not deleted).")
            return
    print("MRN not found.")


def main():
    menu = """
--- Patient Manager ---
1. Add patient
2. List patients
3. Search patient
4. Update phone number
5. Remove patient
6. Quit
"""
    while True:
        print(menu)
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_patient()
        elif choice == "2":
            list_patients()
        elif choice == "3":
            find_patient()
        elif choice == "4":
            update_phone()
        elif choice == "5":
            remove_patient()
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()