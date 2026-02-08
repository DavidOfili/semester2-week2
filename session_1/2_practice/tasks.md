# Library SQL Exercises

## Datetime in SQL

Some of these tasks use datetimes - you can convert a date into the right format using:
```sql
DATE('20-01-2026') /* convert a specific date to a datetime */
DATE('now') /* convert the current time to a datetime */
DATE('now', '-14 days') /* you can add or subtract days */
```

-- Enable readable output format
.mode columns
.headers on


--1. **List all loans**  
--Show book title, member name, and loan date.

SELECT b.title,
       m.name  AS member_name,
       l.loan_date
FROM Loans l
JOIN Books b   ON l.book_id = b.id
JOIN Members m ON l.member_id = m.id;

--2. **Books and loans**  
--List all books and any loans associated with them.

SELECT b.title,
       m.name      AS member_name,
       l.loan_date,
       l.return_date
FROM Books b
LEFT JOIN Loans l   ON l.book_id = b.id
LEFT JOIN Members m ON l.member_id = m.id;

--3. **Branches and books**  
--List all library branches and the books they hold.

SELECT lb.name AS branch_name,
       lb.city,
       b.title
FROM LibraryBranch lb
LEFT JOIN Books b ON b.branch_id = lb.id;

--4. **Branch book counts**  
--Show each library branch and the number of books it holds.

SELECT lb.name AS branch_name,
       COUNT(b.id) AS book_count
FROM LibraryBranch lb
LEFT JOIN Books b ON b.branch_id = lb.id
GROUP BY lb.id, lb.name;

--5. **Branches with more than 7 books**  
--Show branches that hold more than 7 books.

SELECT lb.name AS branch_name,
       COUNT(b.id) AS book_count
FROM LibraryBranch lb
LEFT JOIN Books b ON b.branch_id = lb.id
GROUP BY lb.id, lb.name
HAVING COUNT(b.id) > 7;

--6. **Members and loans**  
--List all members and the number of loans they have made.

SELECT m.name AS member_name,
       COUNT(l.id) AS loan_count
FROM Members m
LEFT JOIN Loans l ON l.member_id = m.id
GROUP BY m.id, m.name;

--7. **Members who never borrowed**  
--Identify members who have never borrowed a book.

SELECT m.name AS member_name
FROM Members m
LEFT JOIN Loans l ON l.member_id = m.id
WHERE l.id IS NULL;

--8. **Branch loan totals**  
--For each library branch, show the total number of loans for books in that branch.

SELECT lb.name AS branch_name,
       COUNT(l.id) AS total_loans
FROM LibraryBranch lb
LEFT JOIN Books b ON b.branch_id = lb.id
LEFT JOIN Loans l ON l.book_id = b.id
GROUP BY lb.id, lb.name;

--9. **Members with active loans**  
--List members who currently have at least one active loan.

SELECT DISTINCT m.name AS member_name
FROM Members m
JOIN Loans l ON l.member_id = m.id
WHERE l.return_date IS NULL;

--10. **Books and loans report**  
--Show all books and all loans, including books that were never loaned. Include a column classifying each row as “Loaned book” or “Unloaned book.”. You will need to look up how to do this (hint: a case statement would work).

SELECT b.title,
       m.name      AS member_name,
       l.loan_date,
       l.return_date,
       CASE
         WHEN l.id IS NULL THEN 'Unloaned book'
         ELSE 'Loaned book'
       END AS status
FROM Books b
LEFT JOIN Loans l   ON l.book_id = b.id
LEFT JOIN Members m ON l.member_id = m.id;

