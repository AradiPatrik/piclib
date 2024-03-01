# Requirements
As an admin
I want to add/delete/edit books in the library

As an admin
I want to check which books are lended, and queues for books

As a user
I want to rent/return a book or queue up/unqueue for unavailable book.

As a user
I want to check which books are lended by me, which books I'm queuing for (place in queue)

As a user
I want to get notified when I should return a book, or if someone's queueing for the book I'm reading and if I am the next in queue for a book

# Database Design
``` mermaid
erDiagram

Book ||--o{ Lend : lended-book
User ||--o{ Lend : lended-to
Book ||--o{ Queue : queued-for
User ||--o{ Queue : queue-for

Book {
    string isbn
    string author
    string title
    date date_added
}

User {
    string slack_id
}

Lend {
    int id
    string slack_id
    string book_id
    date lend_date
    date return_date
}

Queue {
    int id
    string slack_id
    string book_id
    date queue_date
}


```