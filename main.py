"""
Library Book Management System
A complete console-based application to manage library books using JSON storage.
"""

import json
import os
from typing import List, Dict, Optional


# File path for JSON storage
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
            return []
    except json.JSONDecodeError:
        print("Warning: JSON file is corrupted. Starting with empty data.")
        return []
    except Exception as e:
        print(f"Error loading data: {e}")
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
        print(f"Error saving data: {e}")
        return False


def generate_id(books: List[Dict]) -> int:
    """
    Generate a unique ID for a new book.
    Returns the next available ID.
    """
    if not books:
        return 1
    return max(book['id'] for book in books) + 1


def add_book() -> None:
    """
    Add a new book to the library.
    Prompts user for book details and saves to JSON.
    """
    print("\n" + "="*50)
    print("ADD NEW BOOK")
    print("="*50)
    
    books = load_data()
    
    # Get book details from user
    title = input("Enter book title: ").strip()
    if not title:
        print("Error: Title cannot be empty!")
        return
    
    author = input("Enter author name: ").strip()
    if not author:
        print("Error: Author name cannot be empty!")
        return
    
    try:
        year = int(input("Enter publication year: ").strip())
        if year < 0 or year > 2100:
            print("Error: Invalid year!")
            return
    except ValueError:
        print("Error: Year must be a number!")
        return
    
    # Create new book entry
    new_book = {
        "id": generate_id(books),
        "title": title,
        "author": author,
        "year": year,
        "available": True
    }
    
    books.append(new_book)
    
    if save_data(books):
        print(f"\n✓ Book added successfully with ID: {new_book['id']}")
    else:
        print("\n✗ Failed to save book!")


def view_books() -> None:
    """
    Display all books in the library.
    Shows book details in a formatted table.
    """
    print("\n" + "="*50)
    print("ALL BOOKS IN LIBRARY")
    print("="*50)
    
    books = load_data()
    
    if not books:
        print("\nNo books available in the library.")
        return
    
    # Print header
    print(f"\n{'ID':<5} {'Title':<30} {'Author':<20} {'Year':<6} {'Status':<10}")
    print("-" * 71)
    
    # Print each book
    for book in books:
        status = "Available" if book['available'] else "Issued"
        print(f"{book['id']:<5} {book['title'][:29]:<30} {book['author'][:19]:<20} {book['year']:<6} {status:<10}")
    
    print(f"\nTotal books: {len(books)}")


def search_book() -> None:
    """
    Search for books by title or author.
    Displays matching books.
    """
    print("\n" + "="*50)
    print("SEARCH BOOK")
    print("="*50)
    
    books = load_data()
    
    if not books:
        print("\nNo books available in the library.")
        return
    
    search_term = input("Enter title or author to search: ").strip().lower()
    if not search_term:
        print("Error: Search term cannot be empty!")
        return
    
    # Find matching books
    results = [
        book for book in books
        if search_term in book['title'].lower() or search_term in book['author'].lower()
    ]
    
    if not results:
        print(f"\nNo books found matching '{search_term}'")
        return
    
    # Display results
    print(f"\nFound {len(results)} book(s):")
    print(f"\n{'ID':<5} {'Title':<30} {'Author':<20} {'Year':<6} {'Status':<10}")
    print("-" * 71)
    
    for book in results:
        status = "Available" if book['available'] else "Issued"
        print(f"{book['id']:<5} {book['title'][:29]:<30} {book['author'][:19]:<20} {book['year']:<6} {status:<10}")


def issue_book() -> None:
    """
    Issue a book to a user.
    Sets the book's available status to False.
    """
    print("\n" + "="*50)
    print("ISSUE BOOK")
    print("="*50)
    
    books = load_data()
    
    if not books:
        print("\nNo books available in the library.")
        return
    
    try:
        book_id = int(input("Enter book ID to issue: ").strip())
    except ValueError:
        print("Error: Book ID must be a number!")
        return
    
    # Find the book
    book = next((b for b in books if b['id'] == book_id), None)
    
    if not book:
        print(f"\nError: Book with ID {book_id} not found!")
        return
    
    if not book['available']:
        print(f"\nError: Book '{book['title']}' is already issued!")
        return
    
    # Issue the book
    book['available'] = False
    
    if save_data(books):
        print(f"\n✓ Book '{book['title']}' issued successfully!")
    else:
        print("\n✗ Failed to issue book!")


def return_book() -> None:
    """
    Return a book to the library.
    Sets the book's available status to True.
    """
    print("\n" + "="*50)
    print("RETURN BOOK")
    print("="*50)
    
    books = load_data()
    
    if not books:
        print("\nNo books available in the library.")
        return
    
    try:
        book_id = int(input("Enter book ID to return: ").strip())
    except ValueError:
        print("Error: Book ID must be a number!")
        return
    
    # Find the book
    book = next((b for b in books if b['id'] == book_id), None)
    
    if not book:
        print(f"\nError: Book with ID {book_id} not found!")
        return
    
    if book['available']:
        print(f"\nError: Book '{book['title']}' is already available in the library!")
        return
    
    # Return the book
    book['available'] = True
    
    if save_data(books):
        print(f"\n✓ Book '{book['title']}' returned successfully!")
    else:
        print("\n✗ Failed to return book!")


def delete_book() -> None:
    """
    Delete a book from the library.
    Permanently removes the book from storage.
    """
    print("\n" + "="*50)
    print("DELETE BOOK")
    print("="*50)
    
    books = load_data()
    
    if not books:
        print("\nNo books available in the library.")
        return
    
    try:
        book_id = int(input("Enter book ID to delete: ").strip())
    except ValueError:
        print("Error: Book ID must be a number!")
        return
    
    # Find the book
    book = next((b for b in books if b['id'] == book_id), None)
    
    if not book:
        print(f"\nError: Book with ID {book_id} not found!")
        return
    
    # Confirm deletion
    print(f"\nBook Details:")
    print(f"  Title: {book['title']}")
    print(f"  Author: {book['author']}")
    print(f"  Year: {book['year']}")
    
    confirm = input("\nAre you sure you want to delete this book? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("\nDeletion cancelled.")
        return
    
    # Delete the book
    books = [b for b in books if b['id'] != book_id]
    
    if save_data(books):
        print(f"\n✓ Book deleted successfully!")
    else:
        print("\n✗ Failed to delete book!")


def main_menu() -> None:
    """
    Display the main menu and handle user choices.
    Main loop of the application.
    """
    while True:
        print("\n" + "="*50)
        print("LIBRARY BOOK MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add new book")
        print("2. View all books")
        print("3. Search book by title or author")
        print("4. Issue book")
        print("5. Return book")
        print("6. Delete a book")
        print("7. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            search_book()
        elif choice == '4':
            issue_book()
        elif choice == '5':
            return_book()
        elif choice == '6':
            delete_book()
        elif choice == '7':
            print("\n" + "="*50)
            print("Thank you for using Library Management System!")
            print("Goodbye!")
            print("="*50)
            break
        else:
            print("\nError: Invalid choice! Please enter a number between 1 and 7.")
        
        # Wait for user to press Enter before showing menu again
        if choice in ['1', '2', '3', '4', '5', '6']:
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    # Welcome message
    print("\n" + "="*50)
    print("Welcome to Library Book Management System")
    print("="*50)
    
    # Start the main menu
    main_menu()
