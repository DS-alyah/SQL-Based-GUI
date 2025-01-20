import sqlite3
from tkinter import Tk, Frame, Label, Button, Entry, ttk, messagebox


class BookstoreAdminGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Bookstore Management System")
        self.root.geometry("1200x1200")
        self.root.configure(bg='#f0f0f0')

        self.admin_credentials = {"admin": "1234", "manager": "5678"}

        self.sidebar_frame = Frame(self.root, bg='#f0f0f0', width=200)
        self.sidebar_frame.pack(side='left', fill='y')

        self.content_frame = Frame(self.root, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)

        self.setup_login_screen()

    def run(self):
        """
        Starts the Tkinter main loop.
        """
        self.root.mainloop()

    def setup_login_screen(self):
        """
        Displays the login screen.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        # Welcome Header
        header_frame = Frame(self.root, bg='#acdbec')
        header_frame.pack(fill='x')
        Label(
            header_frame,
            text="Welcome to the Bookstore Management System",
            bg='#acdbec',
            fg='white',
            font=('Helvetica', 18, 'bold'),
            pady=10
        ).pack()

        login_frame = Frame(self.root, bg='#f0f0f0')
        login_frame.place(relx=0.5, rely=0.5, anchor='center')

        Label(login_frame, text="Username:", bg='#f0f0f0').grid(row=0, column=0, pady=5)
        self.username_entry = Entry(login_frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        Label(login_frame, text="Password:", bg='#f0f0f0').grid(row=1, column=0, pady=5)
        self.password_entry = Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        Button(
            login_frame,
            text="Login",
            command=self.validate_login,
            bg='#acdbec',
            fg='black',
            width=15
        ).grid(row=2, column=0, columnspan=2, pady=20)

    def validate_login(self):
        """
        Validates the admin login credentials.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.admin_credentials and self.admin_credentials[username] == password:
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.show_books_management()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_books_management(self):
        """
        Displays the Books Management page with a sidebar for actions.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        # Top Navigation Bar
        nav_frame = Frame(self.root, bg='#acdbec', height=50)  # Use header color
        nav_frame.pack(fill='x')

        search_entry = Entry(nav_frame, width=30)
        search_entry.pack(side='left', padx=10, pady=10)

        def search_books():
             search_term = search_entry.get()
             db = BookstoreAdmin("DB.db")
             results = db.search_books(search_term)
             self.display_table(results, ['Title', 'Category', 'Price', 'Stock', 'Quantity'])

        Button(
            nav_frame,
            text="Search Books",
            command=search_books,
            bg='#4CAF50',
            fg='black',
            width=15
        ).pack(side='left', padx=10, pady=10)

        Button(
            nav_frame,
            text="Manage Books",
            command=self.show_books_management,
            bg='#4CAF50',  
            fg='black',    
            width=15,
        ).pack(side='left', padx=10, pady=10)

        Button(
            nav_frame,
            text="Manage Orders",
            command=self.manage_orders,
            bg='#4CAF50',  # Button background color
            fg='black',    # Text color (foreground)
            width=20,
            relief="flat"
        ).pack(side='left', padx=10, pady=10)

        Button(
            nav_frame,
            text="Log Out",
            command=self.setup_login_screen,
            bg='#4CAF50',  # Button background color
            fg='black',    # Text color (foreground)
            width=15,
            relief="flat"
        ).pack(side='left', padx=10, pady=10)
        

        # Sidebar for Actions
        sidebar_frame = Frame(self.root, bg='#f0f0f0', width=200)
        sidebar_frame.pack(side='left', fill='y')

        self.content_frame = Frame(self.root, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)

        actions = [
            ("Filter by Category",self.filter_books_by_category),
            ("Search by Date", self.search_books_by_date),
            ("Sort by Price", self.sort_books_by_price),
            ("Show Best Books", self.show_best_books),
            ("Books Above Average Price", self.show_books_above_avg_price),
            ("Update Prices", self.update_low_stock_prices),
            ("Delete Low-Rated Books", self.delete_low_rated_books),  
        ]

        for text, command in actions:
            Button(
                sidebar_frame,
                text=text,
                command=command,
                bg='#2196F3',
                fg='black',
                width=20
            ).pack(pady=10)

        # Display Books Table
        db = BookstoreAdmin("DB.db")
        books = db.view_all_books()
        self.display_table(books, ['Title', 'Category', 'Rating', 'Price', 'Stock', 'Quantity'])

    def clear_sidebar(self):
        """
        Clears all widgets in the sidebar frame
        """
        if hasattr(self, 'sidebar_frame') and self.sidebar_frame.winfo_exists():
            for widget in self.sidebar_frame.winfo_children():
                widget.destroy()
            self.sidebar_frame.update()

    def search_books_by_date(self):
        """
        Function to search books by date.
        """
        self.clear_content_frame()
        date_frame = Frame(self.content_frame, bg='white')
        date_frame.pack(pady=10)

        Label(date_frame, text="Enter Date (YYYY-MM-DD):", bg='white').pack(side='left')
        date_entry = Entry(date_frame)
        date_entry.pack(side='left', padx=5)

        def filter_books_by_date():
            user_date = date_entry.get()
            db = BookstoreAdmin("DB.db")
            books = db.books_added_after_date(user_date)
            self.display_table(books, ['Title', 'AddedDate'])

        Button(date_frame, text="Search", command=filter_books_by_date, bg='#2196F3', fg='black').pack(side='left', padx=5)

    def filter_books_by_category(self):
        """
        Filters books by selected category.
        """
        self.clear_content_frame()

        db = BookstoreAdmin("DB.db")
        categories = db.get_all_categories()

        filter_frame = Frame(self.content_frame, bg='white')
        filter_frame.pack(pady=10)

        Label(filter_frame, text="Select Category: ", bg='white').pack(side='left')
        category_var = ttk.Combobox(filter_frame, values=[cat[1] for cat in categories], state="readonly")
        category_var.pack(side='left', padx=5)

        def filter_books():
            selected_category = category_var.get()
            category_id = next((cat[0] for cat in categories if cat[1] == selected_category), None)
            if category_id:
                books = db.get_books_by_category(category_id)
                self.display_table(books, ['Title', 'Price', 'Stock', 'Quantity', 'Rating'])

        Button(filter_frame, text="Filter", command=filter_books, bg='#2196F3', fg='black').pack(side='left', padx=5)

    def sort_books_by_price(self):
        db = BookstoreAdmin("DB.db")
        sorted_books = db.books_sorted_by_price_desc()
        self.display_table(sorted_books, ['Title', 'Price'])

    def show_best_books(self):
        db = BookstoreAdmin("DB.db")
        best_books = db.query_select_best_books()
        self.display_table(best_books, ['Title', 'Price', 'RatingID', 'Stock'])

    def show_books_above_avg_price(self):
        db = BookstoreAdmin("DB.db")
        above_avg_books = db.select_books_above_avg_price()
        self.display_table(above_avg_books, ['Title', 'Price'])

    def delete_low_rated_books(self):
        db = BookstoreAdmin("DB.db")
        db.delete_low_rated_out_of_stock_books()
        messagebox.showinfo("Success", "Low-rated out-of-stock books have been deleted.")
        self.show_books_management()

    def update_low_stock_prices(self):
        db = BookstoreAdmin("DB.db")
        db.update_prices_for_low_stock_books()
        messagebox.showinfo("Success", "Prices for low-stock books have been updated.")
        self.show_books_management()

    def display_table(self, data, columns):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill='both', expand=True)

        for row in data:
            tree.insert('', 'end', values=row)

    def display_books_count_and_avg(self):
        """
        Displays the count of books and average price in the sidebar.
        """
        db = BookstoreAdmin("DB.db")
        total_books, avg_price = db.count_books_and_avg_price()

        count_avg_frame = Frame(self.content_frame, bg='white')
        count_avg_frame.pack(pady=10)

        count_avg_text = Text(count_avg_frame, height=5, width=40)
        count_avg_text.pack()

        count_avg_text.insert('1.0', f"Total Books: {total_books}\nAverage Price: ${avg_price:.2f}")
        count_avg_text.config(state="disabled")


    def manage_orders(self):
        """
        Displays the orders management interface
        """
        # Clear everything first
        for widget in self.root.winfo_children():
            widget.destroy()

        # Recreate the navigation bar
        nav_frame = Frame(self.root, bg='#acdbec', height=50)
        nav_frame.pack(fill='x')

        Button(
            nav_frame,
            text="Manage Books",
            command=self.show_books_management,
            bg='#4CAF50',
            fg='black',
            width=15,
        ).pack(side='left', padx=10, pady=10)

        Button(
            nav_frame,
            text="Manage Orders",
            command=self.manage_orders,
            bg='#4CAF50',
            fg='black',
            width=20,
        ).pack(side='left', padx=10, pady=10)

        Button(
            nav_frame,
            text="Log Out",
            command=self.setup_login_screen,
            bg='#4CAF50',
            fg='black',
            width=15,
        ).pack(side='left', padx=10, pady=10)

        # Create new sidebar and content frames
        self.sidebar_frame = Frame(self.root, bg='#f0f0f0', width=200)
        self.sidebar_frame.pack(side='left', fill='y')

        self.content_frame = Frame(self.root, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)

        # Add new buttons to sidebar
        Button(
            self.sidebar_frame,
            text="View Recent Orders",
            command=self.view_recent_orders,
            bg='#2196F3',
            fg='black',
            width=20
        ).pack(pady=10)
    
        Button(
            self.sidebar_frame,
            text="View Customers",
            command=self.view_customers,
            bg='#2196F3',
            fg='black',
            width=20
        ).pack(pady=10)

        # Show recent orders by default
        self.view_recent_orders()

    def view_recent_orders(self):
        """
        Displays recent orders in the content frame
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        db = BookstoreAdmin("DB.db")
        conn = sqlite3.connect("DB.db")
        cursor = conn.cursor()

        query = """
        SELECT 
            Customer.name AS Customer_Name,
            Customer.email AS Email,
            Orders.OrderID AS Order_ID,
            Orders.order_date AS Order_Date
        FROM Customer
        INNER JOIN Orders
        ON Customer.customerID = Orders.customerID;
        """
        db.cursor.execute(query)
        orders = db.cursor.fetchall()
        self.display_table(orders, ['Customer Name', 'Email', 'Book Quantity', 'Order Date'])

    def view_customers(self):
        """
        Displays customer list in the content frame
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        db = BookstoreAdmin("DB.db")
        conn = sqlite3.connect("DB.db")
        cursor = conn.cursor()
        query = """
        SELECT CustomerID, Name, Email, Phone
        FROM Customer
        ORDER BY Name;
        """
        db.cursor.execute(query)
        customers = db.cursor.fetchall()
        self.display_table(customers, ['Customer ID', 'Name', 'Email', 'Phone'])

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()



class BookstoreAdmin:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def view_all_books(self):
        query = """
        SELECT Books.Title, Categories.Book_category, Star_ratings.Star_rating,
               Books.Price, Books.Stock, Books.Quantity
        FROM Books
        LEFT JOIN Categories ON Books.CategoryID = Categories.CategoryID
        LEFT JOIN Star_ratings ON Books.RatingID = Star_ratings.RatingID;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def query_select_best_books(self, min_rating=4):
        query = """
        SELECT Title, Price, RatingID
        FROM Books
        WHERE RatingID >= ?
        ORDER BY RatingID DESC, Price ASC
        LIMIT 10;
        """
        self.cursor.execute(query, (min_rating,))  # Use a single parameter as a tuple
        return self.cursor.fetchall()

    def books_sorted_by_price_desc(self):
        query = """
        SELECT Title, Price
        FROM Books
        ORDER BY Price DESC;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_books_above_avg_price(self):
        query = """
        SELECT Title, Price
        FROM Books
        WHERE Price > (SELECT AVG(Price) FROM Books);
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_low_rated_out_of_stock_books(self):
        query = """
        DELETE FROM Books
        WHERE Stock = 'No' AND RatingID < 3;
        """
        self.cursor.execute(query)
        self.conn.commit()

    def update_prices_for_low_stock_books(self):
        """
        Decreses the price of books with low stock by 10%.
        """
        query = """
        UPDATE Books
        SET Price = Price - (Price * 1.1)
        WHERE Stock > 50 AND Price > 100;
        """
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_categories(self):
        """
        Fetches all book categories for filtering.
        """
        query = """
        SELECT CategoryID, Book_category
        FROM Categories
        ORDER BY Book_category;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_books_by_category(self, category_id):
        """
        Fetches books by the given category ID.
        """
        query = """
        SELECT Books.Title, Books.Price, Books.Stock, Books.Quantity, Star_ratings.Star_rating
        FROM Books
        LEFT JOIN Star_ratings ON Books.RatingID = Star_ratings.RatingID
        WHERE Books.CategoryID = ?
        ORDER BY Books.Title;
        """
        self.cursor.execute(query, (category_id,))
        return self.cursor.fetchall()
    
    def books_added_after_date(self, user_date):
        """
        Fetch books added after a user-specified date.
        """
        query = """
        SELECT Title, AddedDate
        FROM Books
        WHERE AddedDate > ?;
        """
        self.cursor.execute(query, (user_date,))
        return self.cursor.fetchall()
    
    def search_books(self, keyword):
        query = """
        SELECT Books.Title, Categories.Book_category, Books.Price, 
               Books.Stock, Books.Quantity
        FROM Books
        LEFT JOIN Categories ON Books.CategoryID = Categories.CategoryID
        WHERE Books.Title LIKE ? OR Categories.Book_category LIKE ?;
        """
        self.cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))
        return self.cursor.fetchall()

    def view_customers(self):
        """
        Displays customer list in the content frame
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        db = BookstoreAdmin("DB.db")
        conn = sqlite3.connect("DB.db")
        cursor = conn.cursor()
        query = """
        SELECT CustomerID, Name, Email, Phone
        FROM Customers
        ORDER BY Name;
        """
        db.cursor.execute(query)
        customers = db.cursor.fetchall()
        self.display_table(customers, ['Customer ID', 'Name', 'Email', 'Phone'])
        
    
if __name__ == "__main__":
    app = BookstoreAdminGUI()
    app.run()
