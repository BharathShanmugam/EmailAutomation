# Email Automation System

## Overview

This project automates email extraction, validation, generation, and storage using FastAPI and SQLModel. It processes email data extracted from Excel files, standardizes fields, generates missing data, and logs all operations for accuracy and data integrity. This README outlines the API endpoints, services, and the data flow for better understanding and efficient usage.

## Project Structure

- `api.py`: Defines API endpoints for handling data extraction and processing.
- `service.py`: Contains services for email extraction, data standardization, generation, logging, and storage.
- `model.py`: Defines database models for storing extracted, sent, retry, and replied email data.
- `schema.py`: Provides data validation schemas for consistent data processing.

## Table of Contents
1. [Installation](#installation)
2. [Database Models](#database-models)
3. [API Endpoints](#api-endpoints)
4. [Service Functions](#service-functions)
5. [Data Flow](#data-flow)

---

## Installation

### Requirements
- Python 3.8+
- FastAPI
- SQLModel
- Pandas
- SQLAlchemy

### Setup
1. Clone the repository.
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database and models:
    ```bash
    # Example script for creating tables
    from sqlmodel import SQLModel, create_engine
    from models import ExcelExtract, SentEmail, RetryEmail, RepliedEmail, ExcelStoreTable, LogEntry

    engine = create_engine("sqlite:///emails.db")
    SQLModel.metadata.create_all(engine)
    ```

4. Run the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

---

## Database Models

### `ExcelExtract`
Stores completed and validated email data.
- **Fields**: `firstname`, `lastname`, `company`, `email`, `company_domain`, `role`.

### `SentEmail`
Stores details of emails that have been sent.
- **Fields**: `email`, `subject`, `replied`, `date_sent`.

### `RetryEmail`
Stores emails that need to be retried.
- **Fields**: `email`, `subject`, `reason`, `date_failed`.

### `RepliedEmail`
Stores replies received for sent emails.
- **Fields**: `email`, `subject`, `date_sent`, `date_replied`.

### `ExcelStoreTable`
Temporary storage for incomplete records, pending validation or missing data.
- **Fields**: `firstname`, `lastname`, `company`, `email`, `company_domain`, `role`.

### `LogEntry`
Logs operations and details of each data processing step.
- **Fields**: `operation`, `details`, `date_logged`.

---

## API Endpoints

### `/extract-data/` - POST
**Description**: Uploads an Excel file for data extraction and storage.

**Parameters**:
- `file`: `UploadFile`

**Returns**:
- `message`: Confirmation of data extraction and storage.

### `/extract-data-path/` - POST
**Description**: Extracts data from a predefined file path and processes it.

**Parameters**:
- None

**Returns**:
- `message`: Confirmation of data extraction and storage.

---

## Service Functions

### `extract_data_from_excel`
Reads an Excel file and standardizes field names to `firstname`, `lastname`, `company`, and `company_domain`. Supports variations like 'First Name', 'first name', 'Company Domain', etc.

### `generate_email`
Generates an email based on `firstname`, `lastname`, and `company`. If `company_domain` is provided, it is used instead of the `company` field.

### `extract_details_from_email`
Extracts `firstname`, `lastname`, and `company` from an email address if these fields are missing.

### `save_extracted_data`
Saves extracted and validated data into `ExcelExtract`. Incomplete records are stored in `ExcelStoreTable`. Logs the transfer, creation, and deletion of records for tracking.

### `create_log_entry`
Creates a log entry detailing each step in the data processing flow for traceability and debugging.

---

## Data Flow

### 1. Data Extraction and Standardization

- **Input**: An Excel file containing data with varied field names.
- **Process**:
  - `extract_data_from_excel` reads and processes the file.
  - Field names like `First Name`, `Last-name`, `Company Domain`, etc., are mapped to `firstname`, `lastname`, `company`, and `company_domain`.
  - Missing values are represented as `None`.

### 2. Email Generation and Data Completion

- **Input**: Standardized data from `extract_data_from_excel`.
- **Process**:
  - Checks if `firstname`, `lastname`, and `company` are available.
  - If `email` is missing, it generates one based on `firstname`, `lastname`, and `company_domain` (if available) or `company`.
  - Uses `extract_details_from_email` to derive missing data fields if `email` is present but fields are incomplete.

### 3. Data Validation and Storage

- **Input**: Completed data after validation.
- **Process**:
  - Stores completed records in `ExcelExtract`.
  - Incomplete records are stored in `ExcelStoreTable`.
  - Deletes records from `ExcelStoreTable` after successful transfer to `ExcelExtract`.
  - Logs each operation with `create_log_entry` to document actions for each record.

### 4. Logging

- **Purpose**: Tracks each step in the data handling process for troubleshooting and auditing.
- **Fields**:
  - `operation`: Description of the action performed.
  - `details`: Information about the record(s) processed.
  - `date_logged`: Timestamp of the log entry.

---

## Example Workflow

1. **File Upload**:
   - Upload an Excel file using the `/extract-data/` endpoint.
   - The file is processed, and data is standardized.

2. **Data Processing**:
   - Missing emails are generated.
   - Incomplete records are stored in `ExcelStoreTable` for future handling.

3. **Data Storage and Logging**:
   - Completed records are saved in `ExcelExtract`.
   - Logs are created for each record moved, added, or deleted.

4. **Retrieve Logs**:
   - Access logs from `LogEntry` for monitoring and validation.

---

## Conclusion

This project streamlines email data extraction, validation, generation, and storage for consistent data management and integrity. Logs provide traceability for effective monitoring and error handling.
