CREATE DATABASE libraryDB;
USE libraryDB;
CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(100),
    Author VARCHAR(100),
    Publisher VARCHAR(100),
    Year INT,
    Genre VARCHAR(50),
    Quantity INT
);
CREATE TABLE Members (
    MemberID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(15),
    Address VARCHAR(200),
    JoinDate DATE
);
CREATE TABLE IssuedBooks (
    IssueID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT,
    MemberID INT,
    IssueDate DATE,
    ReturnDate DATE,
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);
INSERT INTO Books (Title, Author, Publisher, Year, Genre, Quantity)
VALUES 
('The Alchemist', 'Paulo Coelho', 'HarperOne', 1993, 'Fiction', 5),
('1984', 'George Orwell', 'Secker & Warburg', 1949, 'Dystopian', 3),
('Clean Code', 'Robert C. Martin', 'Prentice Hall', 2008, 'Programming', 4);

INSERT INTO Members (Name, Email, Phone, Address, JoinDate)
VALUES 
('Ansh Sharma', 'kartavyasharma810@gmail.com', '9876543210', 'Delhi, India', CURDATE()),
('Akshat Mehta', 'akshatmehta810@gmail.com', '9123456789', 'Mumbai, India', CURDATE());

INSERT INTO IssuedBooks (BookID, MemberID, IssueDate, ReturnDate)
VALUES 
(1, 1, CURDATE(), NULL),
(3, 2, CURDATE(), NULL);

SELECT * FROM Books;

SELECT ib.IssueID, b.Title, m.Name, ib.IssueDate, ib.ReturnDate
FROM IssuedBooks ib
JOIN Books b ON ib.BookID = b.BookID
JOIN Members m ON ib.MemberID = m.MemberID;

SELECT Title, Quantity FROM Books WHERE Quantity > 0;