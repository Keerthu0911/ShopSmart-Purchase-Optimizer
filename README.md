💰 ShopSmart – Smart Purchase Optimizer
ShopSmart is a command-line utility built with Python designed to help users track their spending and gain valuable insights into their purchasing habits. By recording purchases with details like cost and category, the tool can generate crucial summary reports to optimize future spending.

This project demonstrates core Python skills including persistent data storage, input validation, and statistical calculation.

🚀 Features
The application is run entirely through the command line and offers the following features:

Option

Functionality

Core Concept Demonstrated

1

Add New Purchase Record

User Input & Data Structuring (Dictionaries)

2

View All Records

Data Retrieval & Formatting

3

Search/Filter Records

String Comparison & List Comprehension

4

Update Record Details

Record Modification & Input Validation

5

Delete Record

List Manipulation & ID Management

6

Generate Summary Report

Statistical Aggregation (Totals & Averages by Category)

0

Exit and Save

Persistent Data Storage (JSON File Handling)

🛠️ Technology Stack
Language: Python 3.x

Libraries: json, os, datetime (Standard Library)

Data Persistence: Records are saved locally in a purchases.json file.

💡 How to Run Locally
Clone the Repository:

git clone [gh repo clone Keerthu0911/ShopSmart-Purchase-Optimizer]
cd ShopSmart-Optimizer

Run the script:

python main.py

Follow the prompts in the console. When you exit (Option 0), the data will be saved to purchases.json and loaded the next time you run the script.

⚙️ Project Structure
The entire application logic resides within a single file, ensuring simplicity and focus on core Python concepts.

main.py: Contains the main application loop, all CRUD functions, file handling logic, and the core summarize_report() function.

purchases.json: Automatically created file used to store all purchase data persistently.
