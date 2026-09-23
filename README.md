E-Commerce Data Engineering Pipeline

An end-to-end local data-quality pipeline built with Python and Pandas. It ingests raw e-commerce CSV data, validates business rules and referential integrity, quarantines invalid records, and produces a curated orders dataset plus an auditable data-quality summary.

Project Goals

Preserve raw source data for traceability.

Validate order-level business rules before analytics.

Separate rejected records from trusted curated data.

Retain audit fields so cleaned values can be traced back to their source.

Create a repeatable foundation for the planned AWS S3, Glue, and Snowflake ELT implementation.

Pipeline Flow

Raw CSV files
  -> data-quality validation (Python/Pandas)
  -> rejects / quarantine CSV
  -> curated orders CSV
  -> data-quality summary CSV

Dataset

The project uses dummy e-commerce data with intentionally injected quality issues.

Dataset

Rows

Description

customers.csv

20,000

Customer master data

products.csv

100

Product master data

orders.csv

100,300

Transactional order data with quality issues

Data-Quality Checks

The pipeline performs the following checks:

Quantity validation: accepts only numeric integer quantities from 1 to 10.

Customer FK validation: classifies customer IDs as matched, missing, or orphaned.

Product FK validation: identifies product IDs that do not exist in the product master.

Date validation: identifies invalid and missing order dates.

Amount reconciliation: compares source amount with product_price × quantity after rounding to two decimals.

Amount reconstruction: reconstructs missing amounts only when product and quantity are valid.

Order-status standardization: removes whitespace and normalizes status casing.

Duplicate handling: removes exact full-row duplicates while retaining one canonical record.

Data-Quality Decisions

Scenario

Treatment

Invalid quantity

Quarantined with INVALID_QUANTITY

Amount mismatch

Quarantined with INVALID_AMOUNT

Missing source amount with valid product and quantity

Reconstructed and marked Reconstructed

Missing customer ID

Retained with an unmatched customer status

Orphan product ID

Flagged as a product data-quality issue

Exact duplicate order row

One copy retained; extra identical copy removed

Results

Metric

Count

Raw orders

100,300

Invalid quantity rows

502

Amount mismatch rows

166

Total rejected rows

668

Valid rows before deduplication

99,632

Exact duplicate rows removed

132

Final curated orders

99,500

Detailed metrics are generated in output/data_quality_summary.csv.

Repository Structure

ecommerce-data-pipeline/
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
├── src/
│   └── data_quality.py
├── output/
│   ├── curated/
│   │   └── orders_clean.csv
│   ├── rejects/
│   │   └── invalid_data.csv
│   └── data_quality_summary.csv
├── tests/
└── README.md

How to Run

Prerequisites

Python 3.x

Pandas

Execute the pipeline

Run this command from the repository root:

python src/data_quality.py

Outputs

File

Purpose

output/curated/orders_clean.csv

Trusted, cleaned, deduplicated orders for analytics

output/rejects/invalid_data.csv

Quarantined rows with rejection reasons

output/data_quality_summary.csv

Audit summary of pipeline validation metrics

Tech Stack

Python

Pandas

CSV

Git and GitHub

Planned Cloud Architecture

The local pipeline is complete. The following cloud phase is planned:

S3 RAW -> AWS Glue validation/preprocessing -> S3 CURATED
       -> Snowflake RAW -> Snowflake SQL ELT -> Star Schema -> Analytics

Planned curated model:

DIM_CUSTOMER

DIM_PRODUCT

FACT_ORDERS at one order per row grain

Key Learnings

Raw data should be retained for auditability and reprocessing.

Missing values and invalid values require different validation checks.

Row-level validation is safer than filtering by a business key when duplicate IDs exist.

Source values should be preserved separately from reconstructed analytical values.

Reject/quarantine datasets prevent bad records from silently entering analytics.