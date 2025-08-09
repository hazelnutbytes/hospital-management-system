CREATE DATABASE HospitalDB;

USE HospitalDB;

CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50),
    role VARCHAR(20)
);
CREATE TABLE patients (
    patientid INT PRIMARY KEY,
    patientname VARCHAR(100),
    cause VARCHAR(100),
    fee FLOAT,
    doctorname VARCHAR(100)
);
CREATE TABLE prescriptions (
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_name VARCHAR(100),
    medication VARCHAR(255),
    dosage VARCHAR(100),
    date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(patientid)
);
CREATE TABLE appointments (

    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_name VARCHAR(100),
    appointment_date DATE,
    appointment_time TIME,
    reason VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES patients(patientid)
);
CREATE TABLE patients_backup (
    patientid INT PRIMARY KEY,
    patientname VARCHAR(100),
    cause VARCHAR(255),
    fee DECIMAL(10, 2),
    doctorname VARCHAR(100),
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);