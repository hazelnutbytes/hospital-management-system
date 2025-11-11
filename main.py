import mysql.connector

# MySQL connection function
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="ananya123",  
        database="mydb" 
    )
# register function
def register():
    print("\nRegister a new user")
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    role = input("Enter the role (admin/doctor/staff): ").lower()

    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                       (username, password, role))
        connection.commit()
        print("User registered successfully!")
    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        connection.close()
# login function
def login():
    print("\nLogin")
    username = input("Enter username: ")
    password = input("Enter password: ")

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    
    if result:
        print(f"Login successful! Welcome {username} ({result[0]})")
        return result[0]
    else:
        print("Invalid username or password.")
        return None
#admin functions
def newPatient():
    print("\nAdd a new Patient Record")
    patientid = input("Enter Patient ID: ")
    patientname = input("Enter Patient Name: ")
    cause = input("Enter Cause of Visit: ")
    fee = float(input("Enter Fee: "))
    doctorname = input("Enter Doctor's Name: ")

    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO patients (patientid, patientname, cause, fee, doctorname) VALUES (%s, %s, %s, %s, %s)", 
                       (patientid, patientname, cause, fee, doctorname))
        connection.commit()
        print("Patient Record Saved!")
    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        connection.close()

def searchPatient():
    print("\nSearch a Patient Record")
    patientid = input("Enter Patient ID to search: ")

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM patients WHERE patientid = %s", (patientid,))
    result = cursor.fetchone()
    
    if result:
        print(f"Patient ID: {result[0]}, Name: {result[1]}, Cause: {result[2]}, Fee: {result[3]}, Doctor: {result[4]}")
    else:
        print("Patient not found.")
    
    cursor.close()
    connection.close()

def editPatient():
    print("\nUpdate a Patient Record")
    patientid = input("Enter Patient ID to update: ")

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM patients WHERE patientid = %s", (patientid,))
    result = cursor.fetchone()

    if result:
        print("Current Record:", result)
        patientname = input("Enter new name (leave blank to keep current): ") or result[1]
        cause = input("Enter new cause (leave blank to keep current): ") or result[2]
        fee = input("Enter new fee (leave blank to keep current): ") or result[3]
        doctorname = input("Enter new doctor name (leave blank to keep current): ") or result[4]

        cursor.execute("""
            UPDATE patients 
            SET patientname=%s, cause=%s, fee=%s, doctorname=%s 
            WHERE patientid=%s
        """, (patientname, cause, fee, doctorname, patientid))
        connection.commit()
        print("Patient record updated!")
    else:
        print("Patient not found.")
    
    cursor.close()
    connection.close()

def delPatient():
    print("\nDelete a Patient Record")
    patientid = input("Enter Patient ID to delete: ")

    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Backup the patient data before deletion
        cursor.execute("SELECT * FROM patients WHERE patientid = %s", (patientid,))
        patient_record = cursor.fetchone()
        
        if patient_record:
            # Delete associated prescriptions first
            cursor.execute("DELETE FROM prescriptions WHERE patient_id = %s", (patientid,))
            connection.commit()

            # Delete associated appointments first
            cursor.execute("DELETE FROM appointments WHERE patient_id = %s", (patientid,))
            connection.commit()

            # Insert the record into the backup table
            cursor.execute("""
                INSERT INTO patients_backup (patientid, patientname, cause, fee, doctorname)
                VALUES (%s, %s, %s, %s, %s)
            """, (patient_record[0], patient_record[1], patient_record[2], patient_record[3], patient_record[4]))
            connection.commit()

            # Now delete the patient record
            cursor.execute("DELETE FROM patients WHERE patientid = %s", (patientid,))
            connection.commit()

            print(f"Patient record with ID {patientid} has been deleted and backed up.")
        else:
            print("Patient not found.")
    
    except mysql.connector.Error as e:
        print("Error:", e)
    
    finally:
        cursor.close()
        connection.close()


def listPatients():
    print("\nList of All Patients")
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM patients")
        results = cursor.fetchall()
        
        if results:
            for patient in results:
                print(f"Patient ID: {patient[0]}, Name: {patient[1]}, Cause: {patient[2]}, Fee: {patient[3]}, Doctor: {patient[4]}")
        else:
            print("No patients found.")
    
    except mysql.connector.Error as e:
        print("Error:", e)
    
    finally:
        cursor.close()
        connection.close()
# doctor menu functions
def addPrescription():
    print("\nAdd a New Prescription")
    
    patientid = input("Enter Patient ID: ")
    doctorname = input("Enter Doctor's Name: ")
    medication = input("Enter Medication Name: ")
    dosage = input("Enter Dosage Instructions: ")
    date = input("Enter Date (YYYY-MM-DD): ")
    
    # Establish connection to the database
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Insert prescription data into the prescriptions table
        cursor.execute("""
            INSERT INTO prescriptions (patient_id, doctor_name, medication, dosage, date)
            VALUES (%s, %s, %s, %s, %s)
        """, (patientid, doctorname, medication, dosage, date))
        
        # Commit the transaction
        connection.commit()
        print("Prescription added successfully!")
    
    except mysql.connector.Error as e:
        print("Error:", e)
    
    finally:
        cursor.close()
        connection.close()
        
def searchPrescription():
    print("\nSearch Prescriptions for a Patient")
    patientid = input("Enter Patient ID to search: ")

    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Query to fetch prescriptions for the given patient ID
        cursor.execute("SELECT * FROM prescriptions WHERE patient_id = %s", (patientid,))
        results = cursor.fetchall()
        
        if results:
            print(f"\nPrescriptions for Patient ID {patientid}:")
            for prescription in results:
                print(f"Prescription ID: {prescription[0]}")
                print(f"Doctor: {prescription[2]}")
                print(f"Medication: {prescription[3]}")
                print(f"Dosage: {prescription[4]}")
                print(f"Date: {prescription[5]}")
                print("-" * 40)
        else:
            print("No prescriptions found for this patient.")
    
    except mysql.connector.Error as e:
        print("Error:", e)
    
    finally:
        cursor.close()
        connection.close()
def updatePrescription():
    print("\nUpdate a Prescription")
    prescription_id = input("Enter Prescription ID to update: ")

    connection = get_connection()
    cursor = connection.cursor()

    try:
    
        cursor.execute("SELECT * FROM prescriptions WHERE id = %s", (prescription_id,))
        result = cursor.fetchone()

        if not result:
            print("Prescription not found.")
            return

        print("Current Prescription:", result)
        
 
        doctor_name = input("New Doctor's Name (leave blank to keep current): ") or result[2]
        medication = input("New Medication (leave blank to keep current): ") or result[3]
        dosage = input("New Dosage (leave blank to keep current): ") or result[4]
        date = input("New Date (YYYY-MM-DD, leave blank to keep current): ") or result[5]

        cursor.execute("""
            UPDATE prescriptions
            SET doctor_name = %s, medication = %s, dosage = %s, date = %s
            WHERE id = %s
        """, (doctor_name, medication, dosage, date, prescription_id))
        connection.commit()

        print("Prescription updated successfully!")
    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        connection.close()


# admin menu funtions
def updateAppointment():
    print("\nUpdate an Appointment")
    appointment_id = input("Enter Appointment ID to update: ")

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM appointments WHERE id = %s", (appointment_id,))
        result = cursor.fetchone()

        if not result:
            print("Appointment not found.")
            return

        print("Current Record:", result)
        updates = {
            "doctor_name": input("New Doctor's Name (leave blank to keep): ") or result[2],
            "appointment_date": input("New Date (YYYY-MM-DD, leave blank to keep): ") or result[3],
            "appointment_time": input("New Time (HH:MM:SS, leave blank to keep): ") or result[4],
            "reason": input("New Reason (leave blank to keep): ") or result[5]
        }

        cursor.execute("""
            UPDATE appointments
            SET doctor_name = %s, appointment_date = %s, appointment_time = %s, reason = %s
            WHERE id = %s
        """, (*updates.values(), appointment_id))
        connection.commit()

        print("Appointment updated successfully!")
    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        connection.close()

def addAppointment():
    print("\nAdd a New Appointment")
    
    patientid = input("Enter Patient ID: ")
    doctorname = input("Enter Doctor's Name: ")
    appointment_date = input("Enter Appointment Date (YYYY-MM-DD): ")
    appointment_time = input("Enter Appointment Time (HH:MM:SS): ")
    reason = input("Enter Reason for Appointment: ")
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_name, appointment_date, appointment_time, reason)
            VALUES (%s, %s, %s, %s, %s)
        """, (patientid, doctorname, appointment_date, appointment_time, reason))
            
        connection.commit()
        print("Appointment added successfully!")
    
    except mysql.connector.Error as e:
        print("Error:", e)
    
    finally:
        cursor.close()
        connection.close()

def searchAppointment():
    print("\nSearch a Patient's Appointment Record")
    patientid = input("Enter Patient ID to search: ")

    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Query appointments by patient ID
        cursor.execute("SELECT * FROM appointments WHERE patient_id = %s", (patientid,))
        result = cursor.fetchall()
        
        if result:
            print(f"\nAppointments for Patient ID {patientid}:")
            for appointment in result:
                print(f"Appointment ID: {appointment[0]}")
                print(f"Doctor: {appointment[2]}")
                print(f"Date: {appointment[3]}")
                print(f"Time: {appointment[4]}")
                print(f"Reason: {appointment[5]}")
                print("-" * 40)
        else:
            print("No appointments found for this patient.")
    
    except mysql.connector.Error as e:
        print("Error:", e)
    
    finally:
        cursor.close()
        connection.close()


    
    
#all menus
def staff_menu():
    while True:
        print("\n###########################")
        print("       Staff Menu")
        print("###########################")
        print("1. Add a new Patient Record")
        print("2. Update Existing Patient")
        print("3. Delete Existing Patient")
        print("4. Search a Patient")
        print("5. List all Patients") 
        print("6. Logout") 
        print('\n')
        choice = input("Enter your choice: ")

        if choice == '1':
            newPatient()
        elif choice == '2':
            editPatient()
        elif choice == '3':
            delPatient()
        elif choice == '4':
            searchPatient()
        elif choice == '5':
            listPatients()
        elif choice == '6':
            print("Exiting...")
            break

def doctor_menu():
    while True:
        print("\n###########################")
        print("        Doctor Menu")
        print("###########################")
        print("1. Search a Patient")
        print("2. List all Patients")
        print("3. Add a Prescription")
        print('4. Search Prescription for a patient')
        print('5. Update Prescription')
        print("6. Logout")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            searchPatient()
        elif choice == '2':
            listPatients()
        elif choice =='3':
            addPrescription()   
        elif choice =='4':
            searchPrescription()
        elif choice == '5':
            updatePrescription()
        elif choice == '6':
            print("Exiting...")
            break
        
def admin_menu():
    while True:
        print("\n###########################")
        print("        Admin Menu")
        print("###########################")
        print("1. Add a new Patient Record")
        print("2. Search a Patient")
        print("3. Add Appointment")
        print("4. Search Appointment")
        print("5. Update Appointment")
        print("6. Logout")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            newPatient()
        elif choice == '2':
            searchPatient()
        elif choice =='3':
            addAppointment()
        elif choice =='4' :
            searchAppointment()  
        elif choice == '5':
            updateAppointment()
        elif choice == '6':
            print("Exiting...")
            break
def main_menu():
    while True:
        print("\n|-------------------------------------------------------------|")
        print("             Welcome to the Hospital Management System")
        print("|-------------------------------------------------------------|")
        print("\n         Menu")
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("\nEnter your choice(1/2/3): ")

        if choice == '1':
            role = login()
            if role == "admin":
                admin_menu()
            elif role == "doctor":
                doctor_menu()
            elif role == "staff":
                staff_menu()
                
        elif choice == '2':
            register()
            
        elif choice == '3':
            print("Exiting...")
            break
main_menu()
