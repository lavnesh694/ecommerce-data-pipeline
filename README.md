PROJECT_CONTEXT.md

HANDOFF PURPOSE

This file is the persistent context for Lavnesh's current 30-day job sprint and E-Commerce Data Engineering portfolio project.

When this file is pasted into a new ChatGPT conversation, treat it as the current project state. Do NOT make the user repeat the whole history.

If the new conversation later becomes too long, create/update a newer PROJECT_CONTEXT.md with the latest state and move to another chat. The newest file becomes the source of truth for project continuity.

Always distinguish:

COMPLETED = actually done/tested

IN PROGRESS = currently being worked on

PENDING/PLANNED = not done yet

Never describe a pending task as completed.

1. USER + CAREER GOAL

User

Lavnesh.

Immediate goal

Get a minimum ₹5 LPA Data/Tech job within about 1 month.

₹5 LPA is the minimum target/floor, not a guarantee.

Main target roles

Priority:

Junior Data Engineer / Data Engineer

Data Analyst

ETL / SQL-heavy Data roles

Secondary:

Data-focused SDE / software roles

Career context

B.Tech CSE/Data Science background.

Current/previous DataOps/Data Analyst-style experience at Innovaccer.

Strongest current professional/technical exposure is around SQL and data workflows.

Do NOT invent or exaggerate professional experience.

Portfolio project uses dummy data only and is separate from employer work.

Main strategy

Focus on the fastest realistic route to employability:

SQL

interview-usable Python

practical Data Engineering concepts

AWS S3 / Glue

Snowflake

one credible portfolio project

project deep-dive interview preparation

SQL/Python interview practice

job applications/referrals

2. HOW TO TEACH LAVNESH

Preferred style:

Hinglish.

Friendly but honest.

Practical, not unnecessarily theoretical.

One concept/task/question at a time.

Explain commands before asking him to run them.

Explain both WHAT and WHY.

Let him attempt interview questions before revealing the answer when appropriate.

Clearly separate conceptual mistakes from syntax/typing mistakes.

Do not dump giant code blocks without teaching them.

Use real examples from the project.

The goal is actual understanding and interview ability, not memorization.

If he asks “why?”, explain the underlying mechanism.

Do not ask for context already contained in this file.

Do not repeatedly restart the project from zero.

For every command, ideally explain:

What it does

Why we need it

What output to expect

Then ask him to run it

3. CURRENT SKILL ESTIMATE

Approximate coaching estimates based on the work done so far:

SQL: ~7.5–8/10

Python: ~4–5/10; weak exposure but improving quickly

Data modeling: ~4/10 and improving

AWS/Data Engineering: ~2–3/10

Logical reasoning: ~7/10

Strengths observed

Good SQL logic.

Can solve joins, CTEs, window functions, RANK/DENSE_RANK.

Understands boolean filtering after explanation.

Can reason about data-quality tradeoffs.

Good basic programming logic.

Learns quickly when concepts are explained clearly.

Weaknesses observed

Python exposure is low.

Data modeling is still new.

AWS S3/Glue/Snowflake need practical teaching.

Occasional syntax/typing mistakes.

Needs realistic interview practice.

Important coaching observation:
Lavnesh's logic is generally stronger than his Python syntax/exposure.

4. DEVELOPMENT ENVIRONMENT

The work is being done on an office laptop where installing Python and VS Code is not allowed.

Current environment:

GitHub Codespaces in browser

Python 3.14.2

pip 26.2.1

Pandas installed successfully

Do NOT ask him to install Python/VS Code locally for this project.

Git knowledge

Lavnesh is a Git beginner.

Already understood:

Git = version control

GitHub = online Git platform/repository

Codespaces = browser-based development environment

git status

branch main

Teach gradually:
git status → git add → git commit → git log → git push → git pull → branches later.

5. PROJECT

Project name

E-Commerce Data Engineering Pipeline

Why we are building it

To learn and demonstrate:

Python/Pandas

data profiling

data quality

ETL/ELT

AWS S3

AWS Glue

Snowflake

dimensional modeling

SQL analytics

pipeline troubleshooting

interview-ready Data Engineering explanations

Repository structure

ecommerce-data-pipeline/
│
├── PROJECT_CONTEXT.md
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
│
├── src/
│   └── data_quality.py
│
├── tests/
├── sql/
├── output/
│   ├── curated/
│   └── rejects/
└── README.md

The exact GitHub URL/repository name is not recorded. Do not invent it.

6. DATASETS

Claude generated three dummy datasets.

customers.csv

20,000 rows

clean by design

customer_id is intended primary key

unique/non-null customer IDs

columns:

customer_id

customer_name

email

city

state

signup_date

products.csv

100 rows

clean by design

product_id is intended primary key

columns:

product_id

product_name

category

price

orders.csv

100,300 rows

100,000 base + 300 duplicate-ID rows

columns:

order_id

customer_id

product_id

order_date

quantity

amount

order_status

Designed quality problems include:

missing customer_id

orphan customer IDs

orphan product IDs

invalid order dates

bad quantities

missing amounts

duplicate order IDs

inconsistent order_status casing/whitespace

IMPORTANT: the actual loaded data is more authoritative than the generated documentation.

7. ACTUAL DATA PROFILING RESULTS

After loading orders.csv into Pandas:

Actual dtypes

order_id       str
customer_id    str
product_id     str
order_date     str
quantity       str
amount         float64
order_status   str

Actual missing values

order_id          0
customer_id     500
product_id        0
order_date       33
quantity         77
amount          600
order_status      0

Actual quantity frequency results

1      43978
2      23900
3      12824
4       8097
5       4988
6       3019
8       1972
10      1014
-2       103
0         88
abc       85
-1        79
NaN       77
-5        68
9          4
7          2
11         2

Observed invalid quantity rows:

-5: 68

-2: 103

-1: 79

0: 88

abc: 85

NULL/NaN: 77

11: 2

Total = 502 invalid quantity rows.

The generated data dictionary said 500, but the actual data contains 502. Use the actual profile as truth.

Important lesson learned:
Missing-value checks do not catch invalid-but-present values such as abc or an impossible date.

8. DATA MODEL

Established keys:

CUSTOMERS

PK = customer_id

no FK

PRODUCTS

PK = product_id

no FK

ORDERS

intended/business PK = order_id

FK = customer_id → customers.customer_id

FK = product_id → products.product_id

Important:
Raw orders has 300 duplicate order IDs, so the raw source violates the intended uniqueness constraint.

9. FACT / DIMENSION MODEL

Lavnesh initially had almost no data-modeling knowledge but now understands the basic idea.

Mental model:

Fact = a business event / something that happened.

Dimension = descriptive context around the event.

For this project:

DIM_CUSTOMER = who the customer is

DIM_PRODUCT = what the product is

FACT_ORDERS = one order/business transaction

Expected fact grain:
one order per row

FACT_ORDERS core fields:

order_id

customer_id

product_id

order_date

quantity

amount

order_status

Possible audit/quality fields later:

amount_source

customer_match_status

date_quality_status

ingest_date

processed_at

Do not mix customer-level aggregated metrics into the one-order-per-row fact table.

10. AGREED PIPELINE ARCHITECTURE

Hybrid ETL/ELT:

SOURCE CSVs
    ↓
AWS S3 RAW / LANDING
    ↓
AWS Glue
(basic ingestion + validation + preprocessing)
    ↓
S3 CURATED
    ↓
Snowflake RAW
    ↓
Snowflake SQL transformations / ELT
    ↓
CURATED STAR SCHEMA
    ↓
ANALYTICS

Star schema:

DIM_CUSTOMER

DIM_PRODUCT

FACT_ORDERS

Reasoning:

User correctly observed that Snowflake supports ELT well.

We are NOT forcing all transformations into Glue.

Glue remains useful for managed cloud ingestion/preprocessing/validation and learning AWS Data Engineering.

Snowflake performs warehouse-side transformations and analytics.

Current cloud status:

S3 = NOT IMPLEMENTED

Glue = NOT IMPLEMENTED

Snowflake = NOT IMPLEMENTED

All cloud components are still pending.

11. AGREED DATA-QUALITY PRINCIPLES

RAW data

RAW must remain immutable.

Never silently modify/delete original source data.

Bad records can be copied to a reject/quarantine path with a reason.

Concept:

S3 RAW
  ↓
Glue
  ├── valid → CURATED
  └── invalid → REJECTS

Quantity

Valid if:

numeric

integer



0

<= 10

Invalid examples:

NULL

abc

0

negative



10

Project decision:
Invalid quantity → reject/quarantine.

Missing amount

Project decision:

If product_id is valid and quantity is valid, calculate:
amount = product.price * quantity

Add an audit field such as amount_source = CALCULATED.

Existing amount

For valid product and quantity:

calculate expected amount

compare source amount vs expected amount

use mismatch as reconciliation/data-quality signal

Invalid order_date

Project decision:

do not guess a date

if business permits, keep the order with order_date = NULL

add a quality flag such as INVALID_DATE

Missing customer_id

Project decision:

keep order if otherwise useful

customer_id = NULL

flag as unmatched

Reason:
Order-level/product-level analytics can still be useful even without customer attribution.

Invalid/missing product_id

Project decision for this project:

reject/quarantine

Reason:
Reliable product context and trusted product price are needed for our downstream amount validation/model.

This is a project/business rule, not a universal rule.

Duplicate order_id

IMPORTANT:

Deduplication is PLANNED only.

It has NOT been implemented yet.

A canonical-record selection rule still needs to be designed and documented.

12. COMPLETED WORK — DO NOT REPEAT

Environment

COMPLETED:

GitHub Codespace created

Python available

Pandas installed

Project structure

COMPLETED:

data/

src/

tests/

sql/

output/curated/

output/rejects/

Data loaded

COMPLETED:

customers.csv

products.csv

orders.csv are present in data/

orders.csv loaded successfully with Pandas

Profiling

COMPLETED:

head()

shape

dtypes

isna().sum()

value_counts(dropna=False)

Quantity validation

COMPLETED:

created quantity_numeric

used pd.to_numeric(..., errors="coerce")

created invalid_quantity boolean Series

found 502 invalid quantity rows

learned Pandas boolean masking

learned ~ as NOT on boolean masks

split valid/invalid orders

created reject output

Reject output

COMPLETED:

output/rejects/invalid_data.csv successfully created

invalid rows were given reject_reason = INVALID_QUANTITY

raw orders.csv was not modified

13. PANDAS CONCEPTS USER UNDERSTANDS

User now understands:

DataFrame ≈ table

orders["column"] selects a column

pd.to_numeric(..., errors="coerce") converts numeric values and turns invalid strings into NaN

isna() checks missing values

| is element-wise OR for Pandas boolean conditions

a boolean mask is a Series aligned by DataFrame index

orders[mask] filters rows where the mask is True

orders[~mask] filters rows where the mask is False

.copy() creates an independent DataFrame copy

boolean_series.sum() counts True values

Important mental model:

DataFrame
   ↓
condition calculated row-by-row
   ↓
True/False Series with same index
   ↓
DataFrame[Series]
   ↓
matching rows selected

14. CURRENT CODE STATE

src/data_quality.py currently contains working quantity-validation logic similar to:

import pandas as pd

orders = pd.read_csv("data/orders.csv")

orders["quantity_numeric"] = pd.to_numeric(
    orders["quantity"],
    errors="coerce"
)

invalid_quantity = (
    orders["quantity_numeric"].isna()
    | (orders["quantity_numeric"] > 10)
    | (orders["quantity_numeric"] <= 0)
)

print("Invalid quantity rows:", invalid_quantity.sum())

invalid_orders = orders[invalid_quantity].copy()
valid_orders = orders[~invalid_quantity].copy()

invalid_orders["reject_reason"] = "INVALID_QUANTITY"

invalid_orders.to_csv(
    "output/rejects/invalid_data.csv",
    index=False
)

print("Valid orders:", len(valid_orders))
print("Invalid orders:", len(invalid_orders))
print("Reject file created successfully.")

This is only the quantity stage, not the full pipeline.

15. CURRENT EXACT PROJECT POSITION

CURRENT PHASE: Local Python/Pandas data-quality pipeline.

COMPLETED: quantity validation + invalid quantity reject output.

CURRENT NEXT TASK: Customer foreign-key validation using customers.csv.

Do not restart environment setup.
Do not repeat quantity validation unless needed for debugging.

16. NEXT TASK — CUSTOMER FK VALIDATION

Goal:
Check whether each non-null orders.customer_id exists in customers.customer_id.

Need to distinguish:

valid customer ID

missing customer ID

orphan customer ID (non-null but not found in customer table)

Project policy for missing customer ID:

keep order with NULL customer_id

mark it unmatched

For orphan customer IDs, design the exact handling based on the project rule and explain the reasoning.

Teaching approach:

Explain referential integrity in simple Hinglish.

Explain Pandas merge() or membership check.

Let user attempt a small example.

Implement the validation.

Add a customer-match status/flag.

Continue to product FK validation.

Do NOT jump to AWS yet.

17. REMAINING PROJECT WORK

Local Python/Pandas — PENDING

customer FK validation

product FK validation

date validation

amount reconstruction

amount reconciliation

status standardization

duplicate order_id handling

combined curated/reject pipeline

data-quality summary/report

tests

README/documentation

Cloud — PENDING

S3 RAW setup

upload datasets to S3

S3 folder structure

Glue crawler/schema discovery

Glue ETL job

Glue rejects/curated outputs

Snowflake database/schema/tables

Snowflake loading

Snowflake transformations

star schema

analytics SQL

pipeline troubleshooting exercises

Career — PENDING

SQL mock interviews

Python mock interviews

AWS/Snowflake interview questions

Data Engineering scenario questions

project deep-dive

resume alignment

application/referral sprint

18. GIT PLAN

User is a Git beginner.

Teach gradually:

git status

git add

git commit

git log

git push

git pull

branches later

Explain each command before use.

Use meaningful milestone commits later, for example:

project structure

quantity validation

customer validation

complete local pipeline

cloud pipeline

19. AI USAGE

User may use Claude and other AI tools.

Good division:

Claude can generate large dummy data.

ChatGPT acts as tutor, architect, debugger, and interviewer.

Rule:
AI-generated code should be explained and understood before being considered the user's own project knowledge.

Never put employer confidential/internal data, credentials, source code, or customer data into public AI tools.

20. INTERVIEW TARGET

Eventually Lavnesh should be able to explain:

Why S3 RAW?

Raw data is kept immutable for traceability, reprocessing, and auditability.

Why Glue?

Managed cloud processing/ingestion/validation where Glue adds value.

Why Snowflake transformations?

Snowflake is a cloud warehouse designed for scalable analytical processing, so warehouse-side ELT is practical.

Why not delete bad records?

Preserve source evidence; quarantine/reject separately and make failures traceable.

Why not reject every missing field?

Handling depends on field criticality, whether the value can be safely reconstructed, and downstream business requirements.

Duplicate handling

Answer must be based on the deduplication rule we actually implement later; do not invent a completed implementation now.

21. 30-DAY JOB SPRINT PRIORITIES

Priority order:

SQL — very high

Python — interview-usable fundamentals

Data Engineering concepts — high

S3 / Glue / Snowflake — practical

Project interview preparation — high

Mock interviews — high

Applications/referrals — high

Advanced DSA — secondary for the immediate Data-role target

The project supports the job search but does not replace applications or interviews.

22. FUTURE CHAT CONTINUATION PROTOCOL

When this file is pasted into a new chat, the user may simply say:

Continue from PROJECT_CONTEXT.md. Pick up from NEXT TASK. Don't repeat completed work.

The assistant should then:

Recognize the ₹5 LPA / ~1-month goal.

Recognize the E-Commerce Data Engineering Pipeline.

Recognize that Codespaces/Pandas setup is already done.

Recognize that quantity validation is completed.

Start at customer FK validation.

Avoid repeating completed setup/theory.

Continue one practical task at a time.

Keep COMPLETED vs PENDING accurate.

Update this file after major milestones when appropriate.

If the new chat becomes too long, produce a newer compact handoff file with the latest state.

The latest handoff file is the source of truth for continuity.

23. FINAL CURRENT STATE — ONE SCREEN SUMMARY

USER GOAL:
Minimum ₹5 LPA Data/Tech job in ~1 month.

CURRENT ENVIRONMENT:
GitHub Codespaces + Python 3.14.2 + Pandas.

PROJECT:
E-Commerce Data Engineering Pipeline.

DATA:
customers.csv (20k), products.csv (100), orders.csv (100,300).

COMPLETED:

setup

data loaded

profiling

quantity validation

502 invalid quantity rows identified

invalid quantity CSV written to output/rejects/

NOT COMPLETED:

customer FK validation

product FK validation

date/amount/status validation

dedupe

full curated dataset

AWS S3

AWS Glue

Snowflake

analytics

interview project deep-dive

NEXT:
Customer FK validation against customers.csv.

END OF PROJECT_CONTEXT.md
