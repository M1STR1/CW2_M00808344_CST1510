📘 CST1510 Coursework — README (Week 7, Week 8, Week 9)
📅 Week 7 — Foundations & Planning

During Week 7, the focus was on preparing the structure and logic for the Multi-Domain Intelligence Platform. This included understanding the problem, planning system architecture, and organising the folders and modules needed for the full project.

Key Achievements

Analysed the three domains:

Cybersecurity

Data Science

IT Operations

Designed high-level system architecture:

Database layer

Logic/Backend layer

Streamlit UI layer

Planned CRUD operations and data flow

Created an organised project folder structure

Identified required tools: SQLite, Streamlit, bcrypt, pandas

Learning Outcome

Gained experience in software planning, breaking a multi-layer Python application into clear components and preparing for backend/database development.

📅 Week 8 — Database, CRUD & Backend Logic

Week 8 focused on building the backend and database systems that power the platform. You built a full SQLite database with all required tables and CRUD operations.

Database Schema

The following tables were created:

Users

username

password_hash

role

Cyber Incidents

Datasets Metadata

IT Tickets

Backend Implementations

SQLite database setup

Secure password hashing using bcrypt

Parameterised SQL queries (safe from injection)

CRUD functions for all three domains

Database connection and helper modules

Testing backend functions before connecting to the UI

Learning Outcome

You learned how to:

Design and create relational tables

Write SQL for INSERT, SELECT, UPDATE, DELETE

Use Python to interact with a database

Build secure and reusable backend modules

📅 Week 9 — Streamlit, Frontend UI & Integration

Week 9 involved building the entire web interface in Streamlit and connecting it to the backend created in Week 8.

Key Streamlit Features Completed
🔐 Authentication System

Login and registration pages

Session state (logged_in, username, role)

Redirects and page guards

Secure authentication using the database

🎨 User Interface & Layout

Multi-page Streamlit app using pages/

Clean layout using columns, tabs and expanders

Metrics using st.metric()

Data tables using st.dataframe()

Navigation via the sidebar

🗄️ CRUD UI Integration

Each domain now supports:

Adding entries

Viewing data

Editing entries

Deleting entries
All fully linked to the Week 8 database functions.

📊 Visualisation & Analytics

Created domain-specific charts:

Cybersecurity threats

Data science training metrics

IT operations usage trends

Used:

pandas DataFrames

Streamlit built-in charts (bar, line)

🤖 AI Integration (Preview)

Added an optional page using OpenAI API for automated analysis or natural language summaries.

Learning Outcome

Week 9 developed your ability to:

Build professional web apps in Python

Connect frontend UI to backend logic

Use session state for authentication

Create data visualisations

Structure and style multi-page apps

🎯 Summary (Weeks 7–9)
Week	Focus	Outcome
Week 7	Project Planning	Clear architecture & folder structure
Week 8	Database + CRUD	Fully working backend with secure authentication
Week 9	Streamlit UI	Complete multi-page frontend with charts + CRUD