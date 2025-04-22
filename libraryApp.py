import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# Database connection
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ansh@810',  # Update if needed
            database='libraryDB'  # Ensure this matches your DB
        )
        return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None

# Book insertion
def insert_book():
    values = (
        entry_book_id.get(), entry_title.get(), entry_author.get(),
        entry_publisher.get(), entry_year.get(), entry_genre.get(), entry_quantity.get()
    )
    if not all(values):
        messagebox.showwarning("Input Error", "Please fill all book fields.")
        return
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Books (BookID, Title, Author, Publisher, Year, Genre, Quantity)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, values)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Book inserted.")
            clear_fields()
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Member insertion
def add_member():
    values = (
        entry_member_id.get(), entry_name.get(), entry_email.get(),
        entry_phone.get(), entry_address.get()
    )
    if not all(values):
        messagebox.showwarning("Input Error", "Please fill all member fields.")
        return
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Members (MemberID, Name, Email, Phone, Address, JoinDate)
                VALUES (%s, %s, %s, %s, %s, CURDATE())
            """, values)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Member added.")
            clear_fields()
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Issue book
def issue_book():
    book_id = entry_issue_book_id.get()
    member_id = entry_issue_member_id.get()
    if not all([book_id, member_id]):
        messagebox.showwarning("Input Error", "Provide both Book ID and Member ID.")
        return
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Quantity FROM Books WHERE BookID = %s", (book_id,))
            result = cursor.fetchone()
            if result and result[0] > 0:
                cursor.execute("""
                    INSERT INTO IssuedBooks (BookID, MemberID, IssueDate)
                    VALUES (%s, %s, CURDATE())
                """, (book_id, member_id))
                cursor.execute("UPDATE Books SET Quantity = Quantity - 1 WHERE BookID = %s", (book_id,))
                conn.commit()
                messagebox.showinfo("Success", "Book issued.")
                clear_fields()
            else:
                messagebox.showwarning("Unavailable", "Book is not available.")
            conn.close()
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Return book
def return_book():
    issue_id = entry_return_issue_id.get()
    if not issue_id:
        messagebox.showwarning("Input Error", "Provide Issue ID.")
        return
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE IssuedBooks SET ReturnDate = CURDATE(), Returned = TRUE
                WHERE IssueID = %s
            """, (issue_id,))
            cursor.execute("""
                UPDATE Books SET Quantity = Quantity + 1
                WHERE BookID = (SELECT BookID FROM IssuedBooks WHERE IssueID = %s)
            """, (issue_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Book returned.")
            clear_fields()
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Show available books
def show_available_books():
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Books WHERE Quantity > 0")
            books = cursor.fetchall()
            conn.close()
            text_output.delete(1.0, tk.END)
            if books:
                for book in books:
                    text_output.insert(tk.END, f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Qty: {book[6]}\n")
            else:
                text_output.insert(tk.END, "No available books.\n")
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Show issued books
def show_issued_books():
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT IB.IssueID, B.Title, M.Name, IB.IssueDate
                FROM IssuedBooks IB
                JOIN Books B ON IB.BookID = B.BookID
                JOIN Members M ON IB.MemberID = M.MemberID
                WHERE IB.Returned = FALSE
            """)
            rows = cursor.fetchall()
            conn.close()
            text_output.delete(1.0, tk.END)
            if rows:
                for row in rows:
                    text_output.insert(tk.END, f"IssueID: {row[0]}, Book: {row[1]}, Member: {row[2]}, Date: {row[3]}\n")
            else:
                text_output.insert(tk.END, "No books currently issued.\n")
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Clear all fields
def clear_fields():
    for entry in [
        entry_book_id, entry_title, entry_author, entry_publisher,
        entry_year, entry_genre, entry_quantity,
        entry_member_id, entry_name, entry_email, entry_phone, entry_address,
        entry_issue_book_id, entry_issue_member_id,
        entry_return_issue_id
    ]:
        entry.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("Library Management System")

# ---------- Book Form ----------
frame_book = tk.LabelFrame(root, text="Add Book", padx=10, pady=10)
frame_book.grid(row=0, column=0, padx=10, pady=5)

labels = ["Book ID", "Title", "Author", "Publisher", "Year", "Genre", "Quantity"]
entries = []
for i, label in enumerate(labels):
    tk.Label(frame_book, text=f"{label}:").grid(row=i, column=0)
    e = tk.Entry(frame_book)
    e.grid(row=i, column=1)
    entries.append(e)

entry_book_id, entry_title, entry_author, entry_publisher, entry_year, entry_genre, entry_quantity = entries
tk.Button(frame_book, text="Insert Book", command=insert_book).grid(row=7, columnspan=2, pady=5)

# ---------- Member Form ----------
frame_member = tk.LabelFrame(root, text="Add Member", padx=10, pady=10)
frame_member.grid(row=1, column=0, padx=10, pady=5)

labels = ["Member ID", "Name", "Email", "Phone", "Address"]
entries = []
for i, label in enumerate(labels):
    tk.Label(frame_member, text=f"{label}:").grid(row=i, column=0)
    e = tk.Entry(frame_member)
    e.grid(row=i, column=1)
    entries.append(e)

entry_member_id, entry_name, entry_email, entry_phone, entry_address = entries
tk.Button(frame_member, text="Add Member", command=add_member).grid(row=5, columnspan=2, pady=5)

# ---------- Issue Form ----------
frame_issue = tk.LabelFrame(root, text="Issue Book", padx=10, pady=10)
frame_issue.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_issue, text="Book ID:").grid(row=0, column=0)
entry_issue_book_id = tk.Entry(frame_issue)
entry_issue_book_id.grid(row=0, column=1)

tk.Label(frame_issue, text="Member ID:").grid(row=1, column=0)
entry_issue_member_id = tk.Entry(frame_issue)
entry_issue_member_id.grid(row=1, column=1)

tk.Button(frame_issue, text="Issue Book", command=issue_book).grid(row=2, columnspan=2, pady=5)

# ---------- Return Form ----------
frame_return = tk.LabelFrame(root, text="Return Book", padx=10, pady=10)
frame_return.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_return, text="Issue ID:").grid(row=0, column=0)
entry_return_issue_id = tk.Entry(frame_return)
entry_return_issue_id.grid(row=0, column=1)

tk.Button(frame_return, text="Return Book", command=return_book).grid(row=1, columnspan=2, pady=5)

# ---------- Display Output ----------
frame_display = tk.LabelFrame(root, text="Display Panel", padx=10, pady=10)
frame_display.grid(row=0, column=2, rowspan=2, padx=10, pady=5)

tk.Button(frame_display, text="Show Available Books", command=show_available_books).grid(row=0, column=0, sticky='ew')
tk.Button(frame_display, text="Show Issued Books", command=show_issued_books).grid(row=1, column=0, sticky='ew')

text_output = tk.Text(frame_display, width=50, height=25)
text_output.grid(row=2, column=0, padx=5, pady=5)

root.mainloop()
