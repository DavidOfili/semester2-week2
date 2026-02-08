### a) For each pair of tables below, state the type of relationship (one-to-one, one-to-many, or many-to-many) and briefly explain your reasoning.

**i. Members and loans [2]**
**One-to-many.** One member can have many loans over time, but each loan record belongs to one specific member (via `member_id`).

**ii. Books and loans [2]**
**One-to-many.** One book can appear in many loan records over time (borrowed multiple times), but each loan record refers to one specific book (via `book_id`).

**iii. Members and books [2]**
**Many-to-many.** A member can borrow many books, and a book can be borrowed by many members (at different times). The `loans` table is the “link table” that represents this relationship.

---

### b) A query joins members to loans using an INNER JOIN.

**i. Explain what happens to members who have never borrowed a book. [2]**
They **do not appear** in the results, because an `INNER JOIN` only keeps rows where there is a matching record in **both** tables. No loan = no match.

**ii. Explain how the results of the query would change if a LEFT JOIN were used instead. [2]**
All members would appear. Members with no loans would still be listed, but the loan columns would be **NULL/blank** for them.

---

### c) The head librarian would like to see how many books have been borrowed by each library member.

**i. Write an SQL query which would show the name of each library member and how many loans they have taken out. [5]**

```sql
SELECT m.member_name,
       COUNT(l.loan_id) AS loan_count
FROM members m
LEFT JOIN loans l ON l.member_id = m.member_id
GROUP BY m.member_id, m.member_name
ORDER BY loan_count DESC;
```

(Using `LEFT JOIN` ensures members with zero loans still show, with `loan_count = 0`.)

---

### d) The head librarian asks: “Why don’t you store the book title with the loan? Wouldn’t that make it easier to see the data?”

**i. Explain, using appropriate non-technical language, why this would be bad database design. [5]**
Because it would mean copying the same book title into lots of loan records. That creates duplication and mistakes: if a title is corrected (e.g., a typo fixed), you would have to update it in many places and some records might be missed, leaving inconsistent data. Storing the title once in the `books` table and linking to it from `loans` means the information stays accurate and up to date everywhere, while still being easy to view using a join when needed.
