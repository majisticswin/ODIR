# customer.py
# Area 1: Customer Account — Mitul Joarder
# Handles customer data: registration, password hashing, JSON file storage.

import hashlib
import json
import os

# Path to the flat-file database (easy to swap for a real DB later)
CUSTOMERS_FILE = os.path.join(os.path.dirname(__file__), 'customers.json')


class Customer:
    def __init__(self, first_name, last_name, email, phone, password_hash):
        self.first_name   = first_name.strip()
        self.last_name    = last_name.strip()
        self.email        = email.strip().lower()
        self.phone        = phone.strip()
        self.password_hash = password_hash

    # -------------------------------
    # Password helpers
    # -------------------------------

    @staticmethod
    def hash_password(plain_text):
        """Return SHA-256 hex digest of a plain-text password."""
        return hashlib.sha256(plain_text.encode('utf-8')).hexdigest()

    def check_password(self, plain_text):
        return self.password_hash == Customer.hash_password(plain_text)

    # -------------------------------
    # Serialisation
    # -------------------------------

    def to_dict(self):
        return {
            'first_name':    self.first_name,
            'last_name':     self.last_name,
            'email':         self.email,
            'phone':         self.phone,
            'password_hash': self.password_hash,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            d['first_name'],
            d['last_name'],
            d['email'],
            d['phone'],
            d['password_hash'],
        )

    # -------------------------------
    # File-backed persistence
    # -------------------------------

    @staticmethod
    def _load_all():
        if not os.path.exists(CUSTOMERS_FILE):
            return []
        with open(CUSTOMERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def _save_all(records):
        with open(CUSTOMERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2)

    @staticmethod
    def find_by_email(email):
        """Return a Customer object or None."""
        target = email.strip().lower()
        for record in Customer._load_all():
            if record['email'] == target:
                return Customer.from_dict(record)
        return None

    @staticmethod
    def email_exists(email):
        return Customer.find_by_email(email) is not None

    def save(self):
        """Insert or update this customer in the JSON store."""
        records = Customer._load_all()
        for i, record in enumerate(records):
            if record['email'] == self.email:
                records[i] = self.to_dict()
                Customer._save_all(records)
                return
        records.append(self.to_dict())
        Customer._save_all(records)
