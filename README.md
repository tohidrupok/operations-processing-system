# 📘 Operations Management System - ERP

A Django-based ERP-style system for managing **Companies, Suppliers, Workers, Projects, Memos, Payments, Banks, Loans**, and more — all in one place. This software is a Django-based Operations Management System designed for construction or project-based companies. It allows authorized staff to easily manage Companies, Suppliers, Workers (MenPower), Categories, Items, Projects, Memos, Payments, Bank Transactions, and Reports — all in one place. The system helps track project costs, supplier dues, worker payments, bank balances, loans, and overall profitability. It includes user authentication, admin permission control, and clear dashboards for smooth daily operations. With this system, businesses can streamline paperwork, reduce manual errors, and maintain a clear financial record.

---

## 🚀 Features

- ✅ **Company Management**: Add, edit, delete companies.
- ✅ **Supplier Management**: Manage supplier details and memo summaries.
- ✅ **MenPower Management**: Track workers and their payment memos.
- ✅ **Category & Item Management**: Organize project materials easily.
- ✅ **Project Tracking**: Create projects, close them, set final bills, and view cost/profit summary.
- ✅ **Memo System**: Record purchase memos for suppliers and workers.
- ✅ **Finance Module**: Handle bank accounts, transactions, loans, and payments.
- ✅ **Reports**: Client dues, supplier dues, debit/credit, and more.
- ✅ **Staff-Only Access**: Secured admin operations for staff users.

---

## 📂 Project Structure

- `views.py` – Contains all CRUD and business logic.
- `urls.py` – Cleanly maps every feature.
- `templates/` – Organized HTML templates for each module.
- `models.py` – Well-structured database models.

---

## ⚡ How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the server
python manage.py runserver

If you encounter any issues or need this software, feel free to contact me on WhatsApp at +8801622151055.
