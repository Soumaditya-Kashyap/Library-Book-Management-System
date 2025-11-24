"""
Library Book Management System - GUI Version
A complete Tkinter-based application to manage library books using JSON storage.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from typing import List, Dict, Optional


# ==================== DATA MANAGEMENT FUNCTIONS ====================

DATA_FILE = "books.json"


def load_data() -> List[Dict]:
    """
    Load book data from JSON file.
    Returns an empty list if file doesn't exist or is empty.
    """
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data if data else []
        else:
            # Create empty JSON file
            save_data([])
            return []
    except json.JSONDecodeError:
        messagebox.showwarning("Warning", "JSON file is corrupted. Starting with empty data.")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Error loading data: {e}")
        return []


def save_data(books: List[Dict]) -> bool:
    """
    Save book data to JSON file.
    Returns True if successful, False otherwise.
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(books, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error saving data: {e}")
        return False


def generate_id(books: List[Dict]) -> int:
    """
    Generate a unique ID for a new book.
    Returns the next available ID.
    """
    if not books:
        return 1
    return max(book['id'] for book in books) + 1


def add_book(title: str, author: str, year: int) -> bool:
    """
    Add a new book to the library.
    Returns True if successful, False otherwise.
    """
    books = load_data()
    
    new_book = {
        "id": generate_id(books),
        "title": title,
        "author": author,
        "year": year,
        "available": True
    }
    
    books.append(new_book)
    return save_data(books)


def search_book(search_term: str) -> List[Dict]:
    """
    Search for books by title or author.
    Returns list of matching books.
    """
    books = load_data()
    search_term_lower = search_term.lower()
    
    results = [
        book for book in books
        if search_term_lower in book['title'].lower() or search_term_lower in book['author'].lower()
    ]
    
    return results


def issue_book(book_id: int) -> tuple:
    """
    Issue a book to a user.
    Returns (success: bool, message: str).
    """
    books = load_data()
    
    book = next((b for b in books if b['id'] == book_id), None)
    
    if not book:
        return False, f"Book with ID {book_id} not found!"
    
    if not book['available']:
        return False, f"Book '{book['title']}' is already issued!"
    
    book['available'] = False
    
    if save_data(books):
        return True, f"Book '{book['title']}' issued successfully!"
    else:
        return False, "Failed to save changes!"


def return_book(book_id: int) -> tuple:
    """
    Return a book to the library.
    Returns (success: bool, message: str).
    """
    books = load_data()
    
    book = next((b for b in books if b['id'] == book_id), None)
    
    if not book:
        return False, f"Book with ID {book_id} not found!"
    
    if book['available']:
        return False, f"Book '{book['title']}' is already available!"
    
    book['available'] = True
    
    if save_data(books):
        return True, f"Book '{book['title']}' returned successfully!"
    else:
        return False, "Failed to save changes!"


def delete_book(book_id: int) -> tuple:
    """
    Delete a book from the library.
    Returns (success: bool, message: str, book_title: str).
    """
    books = load_data()
    
    book = next((b for b in books if b['id'] == book_id), None)
    
    if not book:
        return False, f"Book with ID {book_id} not found!", ""
    
    book_title = book['title']
    books = [b for b in books if b['id'] != book_id]
    
    if save_data(books):
        return True, f"Book '{book_title}' deleted successfully!", book_title
    else:
        return False, "Failed to save changes!", book_title


# ==================== GUI APPLICATION ====================

class LibraryManagementApp:
    """Main application class for Library Management System GUI."""
    
    def __init__(self, root):
        """Initialize the main application window."""
        self.root = root
        self.root.title("Library Book Management System")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Create main UI
        self.create_header()
        self.create_button_panel()
        self.create_book_display()
        self.create_footer()
        
        # Load initial data
        self.refresh_book_display()
    
    def create_header(self):
        """Create the header section."""
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📚 Library Book Management System",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
    
    def create_button_panel(self):
        """Create the button panel with all operations."""
        button_frame = tk.Frame(self.root, bg="#ecf0f1", height=100)
        button_frame.pack(fill=tk.X, side=tk.TOP, padx=10, pady=10)
        
        # Button configurations
        buttons = [
            ("➕ Add Book", self.open_add_book_window, "#27ae60"),
            ("🔍 Search Book", self.open_search_window, "#3498db"),
            ("📤 Issue Book", self.open_issue_window, "#e67e22"),
            ("📥 Return Book", self.open_return_window, "#9b59b6"),
            ("🗑️ Delete Book", self.open_delete_window, "#e74c3c"),
            ("🔄 Refresh", self.refresh_book_display, "#16a085"),
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 11, "bold"),
                bg=color,
                fg="white",
                relief=tk.RAISED,
                bd=3,
                padx=15,
                pady=8,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=5)
    
    def create_book_display(self):
        """Create the Treeview for displaying books."""
        display_frame = tk.Frame(self.root, bg="#ecf0f1")
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Title
        title_label = tk.Label(
            display_frame,
            text="All Books in Library",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1"
        )
        title_label.pack(pady=5)
        
        # Create Treeview with scrollbar
        tree_frame = tk.Frame(display_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Title", "Author", "Year", "Status"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Title", width=300, anchor=tk.W)
        self.tree.column("Author", width=200, anchor=tk.W)
        self.tree.column("Year", width=80, anchor=tk.CENTER)
        self.tree.column("Status", width=100, anchor=tk.CENTER)
        
        # Configure row colors
        self.tree.tag_configure('available', background='#d5f4e6')
        self.tree.tag_configure('issued', background='#fadbd8')
        
        # Pack elements
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
    
    def create_footer(self):
        """Create the footer section."""
        footer_frame = tk.Frame(self.root, bg="#34495e", height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            footer_frame,
            text="Ready",
            font=("Arial", 10),
            bg="#34495e",
            fg="white"
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=10)
    
    def refresh_book_display(self):
        """Refresh the book display with current data."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load and display books
        books = load_data()
        
        if not books:
            self.status_label.config(text="No books in library")
            return
        
        for book in books:
            status = "✓ Available" if book['available'] else "✗ Issued"
            tag = 'available' if book['available'] else 'issued'
            
            self.tree.insert(
                "",
                tk.END,
                values=(book['id'], book['title'], book['author'], book['year'], status),
                tags=(tag,)
            )
        
        self.status_label.config(text=f"Total books: {len(books)}")
    
    # ==================== ADD BOOK WINDOW ====================
    
    def open_add_book_window(self):
        """Open window to add a new book."""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Book")
        add_window.geometry("400x350")
        add_window.resizable(False, False)
        add_window.grab_set()
        
        # Header
        header = tk.Label(
            add_window,
            text="📖 Add New Book",
            font=("Arial", 16, "bold"),
            bg="#27ae60",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Form frame
        form_frame = tk.Frame(add_window, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(form_frame, text="Book Title:", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky=tk.W, pady=10)
        title_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
        title_entry.grid(row=0, column=1, pady=10, padx=10)
        title_entry.focus()
        
        # Author
        tk.Label(form_frame, text="Author Name:", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky=tk.W, pady=10)
        author_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
        author_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Year
        tk.Label(form_frame, text="Publication Year:", font=("Arial", 11, "bold")).grid(row=2, column=0, sticky=tk.W, pady=10)
        year_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
        year_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Button frame
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def submit_book():
            """Validate and add book."""
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            year_str = year_entry.get().strip()
            
            # Validation
            if not title:
                messagebox.showerror("Error", "Title cannot be empty!", parent=add_window)
                return
            
            if not author:
                messagebox.showerror("Error", "Author name cannot be empty!", parent=add_window)
                return
            
            try:
                year = int(year_str)
                if year < 0 or year > 2100:
                    messagebox.showerror("Error", "Please enter a valid year!", parent=add_window)
                    return
            except ValueError:
                messagebox.showerror("Error", "Year must be a number!", parent=add_window)
                return
            
            # Add book
            if add_book(title, author, year):
                messagebox.showinfo("Success", f"Book '{title}' added successfully!", parent=add_window)
                self.refresh_book_display()
                add_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to add book!", parent=add_window)
        
        # Buttons
        submit_btn = tk.Button(
            btn_frame,
            text="✓ Add Book",
            command=submit_book,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="✗ Cancel",
            command=add_window.destroy,
            font=("Arial", 11, "bold"),
            bg="#95a5a6",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        add_window.bind('<Return>', lambda e: submit_book())
    
    # ==================== SEARCH BOOK WINDOW ====================
    
    def open_search_window(self):
        """Open window to search books."""
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Books")
        search_window.geometry("800x500")
        search_window.resizable(True, True)
        search_window.grab_set()
        
        # Header
        header = tk.Label(
            search_window,
            text="🔍 Search Books",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Search frame
        search_frame = tk.Frame(search_window, padx=20, pady=15)
        search_frame.pack(fill=tk.X)
        
        tk.Label(search_frame, text="Search by Title or Author:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 11), width=40)
        search_entry.pack(side=tk.LEFT, padx=10)
        search_entry.focus()
        
        # Results frame
        results_frame = tk.Frame(search_window, padx=10, pady=5)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for results
        vsb = ttk.Scrollbar(results_frame, orient="vertical")
        hsb = ttk.Scrollbar(results_frame, orient="horizontal")
        
        results_tree = ttk.Treeview(
            results_frame,
            columns=("ID", "Title", "Author", "Year", "Status"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        vsb.config(command=results_tree.yview)
        hsb.config(command=results_tree.xview)
        
        # Configure columns
        results_tree.heading("ID", text="ID")
        results_tree.heading("Title", text="Title")
        results_tree.heading("Author", text="Author")
        results_tree.heading("Year", text="Year")
        results_tree.heading("Status", text="Status")
        
        results_tree.column("ID", width=50, anchor=tk.CENTER)
        results_tree.column("Title", width=300, anchor=tk.W)
        results_tree.column("Author", width=200, anchor=tk.W)
        results_tree.column("Year", width=80, anchor=tk.CENTER)
        results_tree.column("Status", width=100, anchor=tk.CENTER)
        
        results_tree.tag_configure('available', background='#d5f4e6')
        results_tree.tag_configure('issued', background='#fadbd8')
        
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        results_tree.pack(fill=tk.BOTH, expand=True)
        
        # Status label
        status_label = tk.Label(search_window, text="", font=("Arial", 10, "italic"))
        status_label.pack(pady=5)
        
        def perform_search():
            """Search and display results."""
            # Clear previous results
            for item in results_tree.get_children():
                results_tree.delete(item)
            
            search_term = search_entry.get().strip()
            
            if not search_term:
                messagebox.showwarning("Warning", "Please enter a search term!", parent=search_window)
                return
            
            results = search_book(search_term)
            
            if not results:
                status_label.config(text=f"No books found matching '{search_term}'", fg="red")
                return
            
            for book in results:
                status = "✓ Available" if book['available'] else "✗ Issued"
                tag = 'available' if book['available'] else 'issued'
                
                results_tree.insert(
                    "",
                    tk.END,
                    values=(book['id'], book['title'], book['author'], book['year'], status),
                    tags=(tag,)
                )
            
            status_label.config(text=f"Found {len(results)} book(s)", fg="green")
        
        search_btn = tk.Button(
            search_frame,
            text="🔍 Search",
            command=perform_search,
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        search_window.bind('<Return>', lambda e: perform_search())
    
    # ==================== ISSUE BOOK WINDOW ====================
    
    def open_issue_window(self):
        """Open window to issue a book."""
        issue_window = tk.Toplevel(self.root)
        issue_window.title("Issue Book")
        issue_window.geometry("700x500")
        issue_window.resizable(True, True)
        issue_window.grab_set()
        
        # Header
        header = tk.Label(
            issue_window,
            text="📤 Issue Book",
            font=("Arial", 16, "bold"),
            bg="#e67e22",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Available books frame
        tk.Label(issue_window, text="Available Books:", font=("Arial", 12, "bold")).pack(pady=10)
        
        books_frame = tk.Frame(issue_window, padx=10, pady=5)
        books_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for available books
        vsb = ttk.Scrollbar(books_frame, orient="vertical")
        hsb = ttk.Scrollbar(books_frame, orient="horizontal")
        
        books_tree = ttk.Treeview(
            books_frame,
            columns=("ID", "Title", "Author", "Year"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        vsb.config(command=books_tree.yview)
        hsb.config(command=books_tree.xview)
        
        books_tree.heading("ID", text="ID")
        books_tree.heading("Title", text="Title")
        books_tree.heading("Author", text="Author")
        books_tree.heading("Year", text="Year")
        
        books_tree.column("ID", width=50, anchor=tk.CENTER)
        books_tree.column("Title", width=300, anchor=tk.W)
        books_tree.column("Author", width=200, anchor=tk.W)
        books_tree.column("Year", width=80, anchor=tk.CENTER)
        
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        books_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load available books
        available_books = [b for b in load_data() if b['available']]
        
        for book in available_books:
            books_tree.insert(
                "",
                tk.END,
                values=(book['id'], book['title'], book['author'], book['year'])
            )
        
        # Input frame
        input_frame = tk.Frame(issue_window, padx=20, pady=15)
        input_frame.pack(fill=tk.X)
        
        tk.Label(input_frame, text="Enter Book ID to Issue:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
        id_entry = tk.Entry(input_frame, font=("Arial", 11), width=20)
        id_entry.pack(side=tk.LEFT, padx=10)
        id_entry.focus()
        
        def submit_issue():
            """Issue the selected book."""
            book_id_str = id_entry.get().strip()
            
            try:
                book_id = int(book_id_str)
            except ValueError:
                messagebox.showerror("Error", "Book ID must be a number!", parent=issue_window)
                return
            
            success, message = issue_book(book_id)
            
            if success:
                messagebox.showinfo("Success", message, parent=issue_window)
                self.refresh_book_display()
                issue_window.destroy()
            else:
                messagebox.showerror("Error", message, parent=issue_window)
        
        issue_btn = tk.Button(
            input_frame,
            text="✓ Issue Book",
            command=submit_issue,
            font=("Arial", 11, "bold"),
            bg="#e67e22",
            fg="white",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        issue_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        issue_window.bind('<Return>', lambda e: submit_issue())
        
        if not available_books:
            messagebox.showinfo("Info", "No available books to issue!", parent=issue_window)
    
    # ==================== RETURN BOOK WINDOW ====================
    
    def open_return_window(self):
        """Open window to return a book."""
        return_window = tk.Toplevel(self.root)
        return_window.title("Return Book")
        return_window.geometry("700x500")
        return_window.resizable(True, True)
        return_window.grab_set()
        
        # Header
        header = tk.Label(
            return_window,
            text="📥 Return Book",
            font=("Arial", 16, "bold"),
            bg="#9b59b6",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Issued books frame
        tk.Label(return_window, text="Issued Books:", font=("Arial", 12, "bold")).pack(pady=10)
        
        books_frame = tk.Frame(return_window, padx=10, pady=5)
        books_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for issued books
        vsb = ttk.Scrollbar(books_frame, orient="vertical")
        hsb = ttk.Scrollbar(books_frame, orient="horizontal")
        
        books_tree = ttk.Treeview(
            books_frame,
            columns=("ID", "Title", "Author", "Year"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        vsb.config(command=books_tree.yview)
        hsb.config(command=books_tree.xview)
        
        books_tree.heading("ID", text="ID")
        books_tree.heading("Title", text="Title")
        books_tree.heading("Author", text="Author")
        books_tree.heading("Year", text="Year")
        
        books_tree.column("ID", width=50, anchor=tk.CENTER)
        books_tree.column("Title", width=300, anchor=tk.W)
        books_tree.column("Author", width=200, anchor=tk.W)
        books_tree.column("Year", width=80, anchor=tk.CENTER)
        
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        books_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load issued books
        issued_books = [b for b in load_data() if not b['available']]
        
        for book in issued_books:
            books_tree.insert(
                "",
                tk.END,
                values=(book['id'], book['title'], book['author'], book['year'])
            )
        
        # Input frame
        input_frame = tk.Frame(return_window, padx=20, pady=15)
        input_frame.pack(fill=tk.X)
        
        tk.Label(input_frame, text="Enter Book ID to Return:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
        id_entry = tk.Entry(input_frame, font=("Arial", 11), width=20)
        id_entry.pack(side=tk.LEFT, padx=10)
        id_entry.focus()
        
        def submit_return():
            """Return the selected book."""
            book_id_str = id_entry.get().strip()
            
            try:
                book_id = int(book_id_str)
            except ValueError:
                messagebox.showerror("Error", "Book ID must be a number!", parent=return_window)
                return
            
            success, message = return_book(book_id)
            
            if success:
                messagebox.showinfo("Success", message, parent=return_window)
                self.refresh_book_display()
                return_window.destroy()
            else:
                messagebox.showerror("Error", message, parent=return_window)
        
        return_btn = tk.Button(
            input_frame,
            text="✓ Return Book",
            command=submit_return,
            font=("Arial", 11, "bold"),
            bg="#9b59b6",
            fg="white",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        return_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        return_window.bind('<Return>', lambda e: submit_return())
        
        if not issued_books:
            messagebox.showinfo("Info", "No issued books to return!", parent=return_window)
    
    # ==================== DELETE BOOK WINDOW ====================
    
    def open_delete_window(self):
        """Open window to delete a book."""
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Book")
        delete_window.geometry("700x500")
        delete_window.resizable(True, True)
        delete_window.grab_set()
        
        # Header
        header = tk.Label(
            delete_window,
            text="🗑️ Delete Book",
            font=("Arial", 16, "bold"),
            bg="#e74c3c",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)
        
        # All books frame
        tk.Label(delete_window, text="All Books:", font=("Arial", 12, "bold")).pack(pady=10)
        
        books_frame = tk.Frame(delete_window, padx=10, pady=5)
        books_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for all books
        vsb = ttk.Scrollbar(books_frame, orient="vertical")
        hsb = ttk.Scrollbar(books_frame, orient="horizontal")
        
        books_tree = ttk.Treeview(
            books_frame,
            columns=("ID", "Title", "Author", "Year", "Status"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        vsb.config(command=books_tree.yview)
        hsb.config(command=books_tree.xview)
        
        books_tree.heading("ID", text="ID")
        books_tree.heading("Title", text="Title")
        books_tree.heading("Author", text="Author")
        books_tree.heading("Year", text="Year")
        books_tree.heading("Status", text="Status")
        
        books_tree.column("ID", width=50, anchor=tk.CENTER)
        books_tree.column("Title", width=280, anchor=tk.W)
        books_tree.column("Author", width=180, anchor=tk.W)
        books_tree.column("Year", width=70, anchor=tk.CENTER)
        books_tree.column("Status", width=90, anchor=tk.CENTER)
        
        books_tree.tag_configure('available', background='#d5f4e6')
        books_tree.tag_configure('issued', background='#fadbd8')
        
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        books_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load all books
        all_books = load_data()
        
        for book in all_books:
            status = "Available" if book['available'] else "Issued"
            tag = 'available' if book['available'] else 'issued'
            books_tree.insert(
                "",
                tk.END,
                values=(book['id'], book['title'], book['author'], book['year'], status),
                tags=(tag,)
            )
        
        # Input frame
        input_frame = tk.Frame(delete_window, padx=20, pady=15)
        input_frame.pack(fill=tk.X)
        
        tk.Label(input_frame, text="Enter Book ID to Delete:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
        id_entry = tk.Entry(input_frame, font=("Arial", 11), width=20)
        id_entry.pack(side=tk.LEFT, padx=10)
        id_entry.focus()
        
        def submit_delete():
            """Delete the selected book."""
            book_id_str = id_entry.get().strip()
            
            try:
                book_id = int(book_id_str)
            except ValueError:
                messagebox.showerror("Error", "Book ID must be a number!", parent=delete_window)
                return
            
            # Confirmation dialog
            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this book?\nThis action cannot be undone!",
                parent=delete_window
            )
            
            if not confirm:
                return
            
            success, message, title = delete_book(book_id)
            
            if success:
                messagebox.showinfo("Success", message, parent=delete_window)
                self.refresh_book_display()
                delete_window.destroy()
            else:
                messagebox.showerror("Error", message, parent=delete_window)
        
        delete_btn = tk.Button(
            input_frame,
            text="✗ Delete Book",
            command=submit_delete,
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        delete_window.bind('<Return>', lambda e: submit_delete())
        
        if not all_books:
            messagebox.showinfo("Info", "No books available to delete!", parent=delete_window)


# ==================== MAIN EXECUTION ====================

def main():
    """Main function to run the application."""
    # Initialize data file if it doesn't exist
    if not os.path.exists(DATA_FILE):
        # Create sample data
        sample_books = [
            {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960, "available": True},
            {"id": 2, "title": "1984", "author": "George Orwell", "year": 1949, "available": True},
            {"id": 3, "title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813, "available": False},
            {"id": 4, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925, "available": True},
            {"id": 5, "title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "year": 1997, "available": True},
            {"id": 6, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951, "available": False},
            {"id": 7, "title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "available": True},
            {"id": 8, "title": "Fahrenheit 451", "author": "Ray Bradbury", "year": 1953, "available": True},
        ]
        save_data(sample_books)
    
    # Create and run the application
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
