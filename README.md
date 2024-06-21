# MaWoX POS
Point of Sales System, fully developed with Python Flask, HTML, and CSS
This repo requires to include some dependencies which are not yet included.
The system described in the provided code is a web-based application for managing customers, accounts, deliveries, payments, special notes, and expenses. It uses Flask as the web framework and SQLAlchemy as the ORM (Object-Relational Mapping) tool for interacting with the database.

Key Components and Their Roles
Customers Management

Models:
Customer: Stores customer information such as name, contact details, address, and creation/update timestamps.
SpecialNote: Stores special notes related to a customer.
Routes:
Add_Customer: Adds or updates customer information.
Edit_Customer: Renders a form to edit customer details.
New_Customer: Renders a form to create a new customer.
Functions:
Save_Customer, Update_Customer, Get_Customers, Get_Customer_ByRef_Id: Functions likely responsible for interacting with the database to save, update, and retrieve customer details.
Accounts Management

Models:
Account: Represents financial accounts related to customers, including fields for account type, quantity, status, and related deliveries and payments.
Payment: Represents payment transactions related to accounts.
Delivery: Represents delivery information related to accounts.
Functions:
Save_Account, Update_Account, Get_Account_ById, etc.: Functions likely handle the saving, updating, and retrieving of account details.
Products Management

Models:
Product: Stores information about products available in the system, such as name and price.
Expenses Management

Models:
Expense: Represents various expenses recorded in the system, including transaction details, category, quantity, paid amount, and source.
Workflow and Usage
Customer Addition and Management:

When a new customer is added via the /customers/<ref_id> route, the system collects the form data, assigns a reference ID, checks for existing contact numbers to avoid duplicates, and saves the new customer information in the Customer model.
If the customer already exists, the system will flash a warning message and redirect to the customer search page.
The customer details can also be updated through the same route by checking if the form submission is for an update.
Editing Customer Details:

The /modify_customer/<ref_id> route renders a form pre-filled with the existing customer details to allow for editing.
Account and Delivery Management:

Each customer can have multiple accounts, and each account can have multiple deliveries and payments associated with it.
The system manages the relationship between customers and their accounts, and between accounts and their deliveries and payments, ensuring data integrity through foreign keys and relationships.
Expenses Tracking:

The Expense model is used to track and record various expenses, which can be categorized and detailed with quantities and paid amounts.
Key Features and Benefits
User Authentication: The use of flask_login indicates that the system supports user authentication, ensuring that only authorized users can manage customer and account data.
Data Integrity: Unique constraints and relationships between models ensure data integrity and consistency. For example, the Contact_No field in the Customer model is unique, preventing duplicate entries.
Automated Timestamps: Automatic handling of creation and update timestamps helps in tracking changes and maintaining an audit trail.
Extensible and Modular Design: The use of blueprints in Flask (e.g., customers = Blueprint('Customers', __name__)) indicates a modular design that can be easily extended with additional features or routes.
Form Handling and Validation: The system processes form data submitted via POST requests, including validation and handling of different form actions (e.g., SAVE, UPDATE).
Summary
The system is a comprehensive web application designed to manage customer relationships, financial accounts, product inventory, deliveries, payments, special notes, and expenses. It leverages Flask for the web framework, and SQLAlchemy for database interactions, and ensures data integrity and user authentication. The modular design and clear separation of concerns make the system scalable and maintainable.
