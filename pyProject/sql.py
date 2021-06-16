import sqlite3
import random
import string
from datetime import date
from tkinter import *

window=Tk()
window.title("Dataset Project")
window.geometry("700x700")
un=Label(window,text="Library Management System",font=('poppins',15),fg='red',bg='yellow',relief=RIDGE)
un.grid(row=0,column=0)

class Init():
	def __init__(self,conn):
		self.conn = conn


	def tables(self):
		try:
			self.conn.execute("""CREATE TABLE books (
    			id   VARCHAR (16) PRIMARY KEY UNIQUE NOT NULL,
    			name VARCHAR      NOT NULL);""")

			self.conn.execute("""CREATE TABLE avail (
    			id        VARCHAR (16) REFERENCES books (id),
    			available INTEGER      DEFAULT (1),
    			total     INTEGER      DEFAULT (1) );""")

			self.conn.execute("""CREATE TABLE record (
    			book_id      VARCHAR (16) REFERENCES books (id),
    			id           VARCHAR      PRIMARY KEY,
    			deposited_on DATETIME     NOT NULL,
    			issued_on    DATETIME     NOT NULL);""")
		except Exception as ignore:
			raise

class Book:

	def __init__(self,conn,name):
		self.conn = conn
		self.cursor = self.conn.cursor()
		self.id = self.generateId()
		self.name = name

	def getIds(self):
		self.cursor.execute("""Select id from books where 1""")
		return [tup[0] for tup in self.cursor.fetchall()]

	def getId(self):
		self.cursor.execute("SELECT id from books where name = ?",(self.name,))
		return self.cursor.fetchone()[0]

	def getNames(self):
		self.cursor.execute("SELECT name FROM books WHERE 1")
		return [tup[0] for tup in self.cursor.fetchall()]

	def getQuantity(self,id):
		self.cursor.execute("SELECT total from avail WHERE id = ?",(id,))
		return self.cursor.fetchone()[0]

	def getAvailable(self,id):
		self.cursor.execute("SELECT available from avail WHERE id = ?",(id,))
		return self.cursor.fetchone()[0]
	def getDate(self):

		return date.today()
	def isAvailable(self,id):
		if self.getAvailable(id)>0:
			return True
		return False
	def isThere(self,id):
		if self.getQuantity(id)>0:
			return True
		return False

	def generateId(self):
		id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
		if id not in self.getIds():
			return id
		else:
			self.generateId()
	def generateRecordId(self):
		id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
		self.cursor.execute("SELECT id from record WHERE 1")
		ids = [tup[0] for tup in self.cursor.fetchall()]
		if id not in ids:
			return id
		else:
			self.generateId()

	def add(self):
		if self.name in self.getNames():
			# exists
			# Increment Quantity and Available
			id = self.cursor.execute("SELECT id from books where name = ?;",(self.name,)).fetchone()[0]
			self.cursor.execute("SELECT id, available, total FROM avail WHERE id = ?;",(id,))
			row = self.cursor.fetchone()

			#self.cursor.execute("INSERT INTO avail (id, available, total) VALUES (?,?,?);",(row[0],row[1]+1,row[2]+1))
			self.cursor.execute("UPDATE avail SET id = ?, available = ?, total = ? WHERE id = ?",(row[0],row[1]+1,row[2]+1,row[0]))
		else:
			#not exists
			#Add new
			id = self.generateId()
			self.cursor.execute("INSERT INTO books (id,name) VALUES (?,?);",(id, self.name))
			self.cursor.execute("INSERT INTO avail (id, available, total) VALUES (?,?,?);",(id, 1,1))
		self.conn.commit()

	def delete(self):

		id = self.getId(self.name)

		if id in self.getIds():
			#exists
			if self.getAvailable(id) == 0:
				print("Error Occured, The Book is not yet returned")
				return
			else:
				#total
				if self.getQuantity(id) == 1:
					self.cursor.execute("DELETE FROM books WHERE id = ?",(id,))
					self.cursor.execute("DELETE FROM avail WHERE id = ?",(id,))
				else:
					row = self.cursor.execute("SELECT * from avail WHERE id = ?",(id,)).fetchone()
					self.cursor.execute("UPDATE avail SET id = ?, available = ?, total = ? WHERE id = ?",(row[0],row[1]-1,row[2]-1,row[0]))
		else:
			print("Error Occured, The Book Doesn't Found")
			return
		self.conn.commit()

	def issueTo(self, by,by_id):
		id = self.getId()
		if self.isAvailable(id):
			#add to record
			self.cursor.execute("INSERT into record (book_id,id,issued_on,by, by_id) VALUES (?,?,?,?,?)",(id, self.generateRecordId(), self.getDate(), by, by_id))
			#decrease Avalable

			row = self.cursor.execute("SELECT * from avail WHERE id = ?",(id,)).fetchone()
			self.cursor.execute("UPDATE avail SET available = ? WHERE id = ?",(row[1]-1,row[0]))
			self.conn.commit()
		else:
			print("The Book is not available for Issueing")
	def deposite(self, by,by_id):
		id = self.getId()
		if self.isThere(id):
			#update record
			self.cursor.execute("UPDATE record SET deposited_on = ? WHERE by = ? AND by_id = ?",(self.getDate(), by, by_id))
			#increment Avalable

			row = self.cursor.execute("SELECT * from avail WHERE id = ?",(id,)).fetchone()
			self.cursor.execute("UPDATE avail SET available = ? WHERE id = ?",(row[1]+1,row[0]))
			self.conn.commit()
		else:
			print("The Book does'nt exists")

class Tabels:
	def __init__(self, conn):
		self.conn = conn
		self.cursor = conn.cursor()

	def getBooks(self):
		self.cursor.execute("SELECT * FROM books WHERE 1")
		return self.cursor.fetchall()
	def getAvailable(self):
		self.cursor.execute("SELECT avail.id,books.id,name,available,total FROM avail,books WHERE avail.id==books.id")
		return self.cursor.fetchall()
	def getRecords(self):
		self.cursor.execute("SELECT books.id,book_id,name,issued_on,deposited_on FROM record,books WHERE book_id==books.id")
		return self.cursor.fetchall()


############################################

conn = sqlite3.connect("database.db")
init = Init(conn)

def start():
	conn = sqlite3.connect("database.db")
	init = Init(conn)
	#init.tables()
	#book = Book(conn,"The Merchant of Venice")
	#book.add()
	#book.issueTo("Gursewak Singh", "6167141")
	#book.deposite("Gursewak Singh", "6167141")

	table = Tabels(conn)
	print(table.getAvailable())

def show_books():
        print("???????????????SHOW ALL BOOKS???????????????")
        tb = Tabels(conn)
        rows = tb.getBooks()
        lar = 0
        
        for row in rows:
                if lar<len(row[1]):
                        lar=len(row[1])
        print("!"+"      Unique ID     "+"!"+" "*((lar-len("Name"))//2)+"Name"+" "*((lar-len("Name"))//2)+"!")
        for row in rows:
                print("!"+" "*((20-len(row[0]))//2)+row[0]+" "*((20-len(row[0]))//2)+"!"+" "*((lar-len(row[1]))//2)+row[1]+" "*((lar-len(row[1]))//2)+"!")

def show_records():
        #books.id,book_id,name,issued_on,deposited_on
        print("???????????????SHOW ALL Records???????????????")
        tb = Tabels(conn)
        rows = tb.getRecords()
        lar = 0
        #print(rows[0])
        for row in rows:
                if lar<len(row[0]):
                        lar=len(row[0])
        print("!"+"       Book ID      "+"!"+" "*((40-len("Name"))//2)+"Name"+" "*((40-len("Name"))//2)+"!"+" "*((20-len("Issued On"))//2)+"Issued On"+" "*((20-len("Issued On"))//2)+"!"+" "*((20-len("Deposited On"))//2)+"Deposited On"+" "*((20-len("Deposited On"))//2))
        for row in rows:
                print("!"+" "*((20-len(row[0]))//2)+row[0]+" "*((20-len(row[0]))//2)+"!"+" "*((40-len(row[2]))//2)+row[2]+" "*((40-len(row[2]))//2)+"!"+" "*((20-len(row[3]))//2)+row[3]+" "*((20-len(row[3]))//2)+"!"+" "*((20-len(row[4]))//2)+row[4]+" "*((20-len(row[4]))//2)+"!")
                
def show_avail():
        print("???????????????SHOW Availablity of Books???????????????")
        tb = Tabels(conn)
        rows = tb.getAvailable()
        lar = 0
        for row in rows:
                if lar<len(row[1]):
                        lar=len(row[1])
        print("!"+"      Unique ID     "+"!"+" "*((40-len("Name"))//2)+"Name"+" "*((40-len("Name"))//2)+"!"+" "*((20-len("Available"))//2)+"Available"+" "*((20-len("Available"))//2)+"!"+" "*((20-len("Total"))//2)+"Total"+" "*((20-len("Total"))//2))
        for row in rows:
                print("!"+row[0]+" "*(20-len(row[0]))+"!"+row[2]+" "*(40-len(row[2]))+"!"+str(row[3])+" "*(20-len(str(row[3])))+"!"+str(row[4])+" "*(20-len(str(row[4]))))

def add_book():

        print("???????????????ADD BOOKS???????????????")
        print("Enter Book Name")
        name = input()
        bk = Book(conn,name)
        bk.add()
        print("Book added successfully")
        pass
def delete_book():
        print("???????????????DELETE BOOKS???????????????")
        print("Enter Book Name")
        name = input()
        bk = Book(conn,name)
        bk.delete()
        print("Book Deleted Successfully")
        pass
def issue_book():
        print("???????????????ISSUE BOOKS???????????????")
        name = input("Enter Book Name")
        usr_name = input("Enter User Name")
        usr_id = input("Enter User id")
        bk = Book(conn,name)
        bk.issueTo(usr_name, usr_id)
        print("Book Issued Successfully")
        pass
def return_book():
        print("???????????????Deposite BOOKS???????????????")
        name = input("Enter Book Name")
        usr_name = input("Enter User Name")
        usr_id = input("Enter User id")
        bk = Book(conn,name)
        bk.deposite(usr_name, usr_id)
        print("Book Returned Successfully")
        pass

window.config(bg="grey")
show_books_label=Button(window,text="Show All Books",bg="white",font=("times",20,"bold"),relief=GROOVE,borderwidth=3,width=13,anchor="w", command=show_books)
show_records_label=Button(window,text="Show All Records",bg="white",font=("times",20,"bold"),relief=GROOVE,borderwidth=3,width=13,anchor="w", command=show_records)
show_avail_label=Button(window,text="Show All Available",bg="white",font=("times",20,"bold"),relief=GROOVE,borderwidth=3,width=13,anchor="w", command=show_avail)
add_books_label=Button(window,text="Add Books",bg="white",font=("times",20,"bold"),relief=GROOVE,borderwidth=3,width=13,anchor="w", command=add_book)
delete_books_label=Button(window,text="Delete Books",bg="white",font=("times",20,"bold"),relief=GROOVE,borderwidth=3,width=13,anchor="w", command=delete_book)
return_books_label=Button(window,text="Return Books",bg="white",font=("times",20,"bold"),relief=GROOVE,borderwidth=3,width=13,anchor="w", command=return_book)
issue_books_label=Button(window,text="Issue Books",bg="white",font=("times",20,"bold"),relief=GROOVE,borderwidth=3,width=13,anchor="w", command=issue_book)

def main_menu(top,start):
        add_books_label.place(x=start,y=top)
        delete_books_label.place(x=start,y=top+60)
        return_books_label.place(x=start,y=top+120)
        issue_books_label.place(x=start,y=top+180)

def menu_show(top,start):
        show_books_label.place(x=start,y=top)
        show_avail_label.place(x=start,y=top+60)
        show_records_label.place(x=start,y=top+120)

main_menu(100, 60)
menu_show(100,300)
window.mainloop()
