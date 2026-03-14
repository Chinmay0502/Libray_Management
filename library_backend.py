import json
import random
import string
from pathlib import Path
from datetime import datetime


class Library:
    database = "library.json"
    data = {"books": [], "members": []}

    if Path(database).exists():
        with open(database, "r") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)
    else:
        with open(database, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def save_data(cls):
        with open(cls.database, "w") as f:
            json.dump(cls.data, f, indent=4)

    @staticmethod
    def generate_id(prefix="B"):
        return prefix + "-" + ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=5)
        )

    @classmethod
    def add_book(cls, title, author, copies):
        book = {
            "id": cls.generate_id(),
            "title": title,
            "author": author,
            "total_copies": copies,
            "available_copies": copies,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        cls.data["books"].append(book)
        cls.save_data()

    @classmethod
    def add_member(cls, name, email):
        member = {
            "id": cls.generate_id("M"),
            "name": name,
            "email": email,
            "borrowed": []
        }

        cls.data["members"].append(member)
        cls.save_data()

    @classmethod
    def get_books(cls):
        return cls.data["books"]

    @classmethod
    def get_members(cls):
        return cls.data["members"]
    
    @classmethod
    def borrow_book(cls, member_id, book_id):
        member = next((m for m in cls.data["members"] if m["id"] == member_id), None)
        if not member:
            return "Member not found"

        book = next((b for b in cls.data["books"] if b["id"] == book_id), None)
        if not book:
            return "Book not found"

        if book["available_copies"] <= 0:
            return "No copies available"

        borrow_entry = {
            "book_id": book["id"],
            "title": book["title"],
            "borrow_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        member["borrowed"].append(borrow_entry)
        book["available_copies"] -= 1

        cls.save_data()
        return "Book borrowed successfully"

    @classmethod
    def return_book(cls, member_id, book_id):
        member = next((m for m in cls.data["members"] if m["id"] == member_id), None)
        if not member:
            return "Member not found"

        borrowed_book = next((b for b in member["borrowed"] if b["book_id"] == book_id), None)
        if not borrowed_book:
            return "This book was not borrowed by this member"

        member["borrowed"].remove(borrowed_book)

        book = next((b for b in cls.data["books"] if b["id"] == book_id), None)
        if book:
            book["available_copies"] += 1

        cls.save_data()
        return "Book returned successfully"
