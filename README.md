# E-Authentication
## Overview  
The **E-AUthentication** is a Python-based application designed to streamline and secure the entry authentication process for students, faculty, and guests. Using barcode scanning and multi-tier OTP verification, it ensures only authorized individuals gain access, while maintaining a clean and modular backend architecture.

## Purpose & Use Cases  
- Automate and manage entry for educational institutions, workplaces, or gated facilities.  
- Enhance security by combining barcode-based identification and OTP-based verification.  
- Offer flexibility—guests can be registered manually if they don’t have a barcode or hashed ID.  
- Serve as a showcase for building modular, real-time Python applications with database connectivity and external API integration.

## Key Features & Capabilities  
- **Barcode & QR Code Authentication**: Uses `pyzbar` + OpenCV to scan and decode barcodes/QR codes live.  
- **OTP-Based Multi-Tier Verification**: Sends OTPs to email and mobile for second-factor authentication.  
- **Dynamic User Categories**: Supports three roles — Student, Faculty, and Guest — with distinct registration or login flows.  
- **Manual Guest Registration**: Allows entry via form when barcode scanning isn’t available.  
- **Backend Persistence**: Stores user and entry logs in MySQL for reliability and queryability.  
- **Asynchronous API Integration**: Uses external SMS API (via `requests`) and SMTP (via `smtplib`) for OTP delivery.  
- **Real-Time Operations**: Validates entries instantly, with timestamping using Python’s `datetime`.  
- **Robust Flow Control**: Gracefully handles invalid scans, network errors, timeouts, and unauthorized attempts.

## Technology Stack  
| Layer           | Technologies / Libraries                 |
|-----------------|------------------------------------------|
| Language        | Python                                   |
| GUI / Camera    | OpenCV, `pyzbar`, Tkinter or custom UI   |
| Database        | MySQL                                    |
| Email           | `smtplib`                                |
| SMS API         | `requests` (HTTP-based SMS gateway)      |
| OTP Generation  | `random` module                          |
| Time Handling   | `datetime`                               |

## Architecture & Design  
1. **Modular Classes for Each Role**  
   - `Student`, `Faculty`, `Guest`, and `Manual` modules handle respective workflows (scan → OTP → DB verification).  
2. **Decoupled Service Layer**  
   - Barcode scanning, OTP generation, API calls, email logic, and database operations are separated for maintainability.  
3. **Configuration & Constants**  
   - API credentials, email server settings, OTP settings, and DB connection strings are managed centrally.  
4. **Error Handling Strategy**  
   - Use `try/except` blocks around API calls, DB operations, and camera I/O to prevent crashes and provide user feedback.  
5. **Graceful Shutdown**  
   - Release camera resources and close DB connections properly when operations end or are aborted.

## Setup & Installation
### 1. Clone the Repository  
```bash
git clone https://github.com/Ramesh-Odde/E-Authentication.git
cd E-Authentication
```
### 2. Set Up Python Environment
```bash
python3 -m venv venv
source venv/bin/activate     # Linux / macOS
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```
### 3. Configure MySQL Database
- Ensure MySQL server is active.
- Create a database (e.g., entry_db).
- Update DB credentials in the configuration file (e.g., config.py).
- Example:
```sql
CREATE DATABASE entry_db;
```
- Ensure the connection URL matches:
```
mysql://username:password@localhost:3306/entry_db
```
### 4. Configure Email & SMS APIs
- Provide SMTP settings (hostname, port, login, TLS).
- Provide SMS API endpoint, headers, and API key in configuration.
### 5. Run the Application
```bash
python main.py
```
- The GUI should open (or camera feed start), enabling user interactions through barcode scanning or form input.
## API / Flow Examples & Testing
### Flow for Students / Faculty
1. Start camera → scan barcode → if valid → generate OTP
2. Send OTP to email & mobile
3. Prompt user to enter OTP
4. On matching the OTP, mark entry with timestamp in DB
### Guest / Manual Entry Flow
1. Present a form to capture name, mobile, email
2. Generate and send OTP
3. On correct OTP, save the record and mark entry
#### You can test by simulating scenarios:
1. Invalid barcode scan
2. OTP mismatches
3. API or network failures
4. Guests registering without barcode
## Error Handling & Validation
- Invalid barcode or no barcode detected → Retry prompt
- OTP expiration or mismatch → Deny access
- DB connectivity or insertion failures → Log and report errors
- API failures (SMS or email) → Fall back or notify user
- Graceful termination to release hardware (camera) and DB handles
## Future Enhancements & Contributions
- Add JWT-based login + session management
- Support batch guest registration and QR invitations
- Add entry logs and reporting dashboards
- Incorporate face recognition along with barcode
- Add role-based access or admin controls
- Dockerize the app for cross-machine deployment
- Allow SMS cost fallback (e.g., send only email if SMS fails)

## Contact & Maintainer
**Author:** Ramesh Odde  
**GitHub:** [Ramesh-Odde](https://github.com/Ramesh-Odde)  
**Email:** [ramesh.odde95@gmail.com](mailto:ramesh.odde95@gmail.com)
