Description
To design a multi-user grocery store app with an admin/store manager for buying groceries.
The app should have multiple section for users to select from. All the selected items should
be stored in user’s cart. More sections can be added by the admin/store manager.
Technologies used
• Flask
• Flask_sqlalchemy
• Flask_bcrypt
• Flask_login
• Flask_wtf
DB schema design
    ▪ Users
        • id=Integer, primary_key=True)
        • username=String(20),unique=True, nullable=False
        • email=String(120),unique=True, nullable=False
        • password=String(60), nullable=False
        • cart = String, nullable=True
    ▪ Category
        • c_id=Integer, primary_key=True
        • c_name=String, unique=True, nullable=False
    ▪ Product
        • p_id=Integer, primary_key=True
        • p_name=String, unique=True, nullable=False
        • category = String, nullable=False
        • price=Integer, nullable=False
        • stock=Integer, nullable=False
        • expiry_date=DateTime, nullable=False
Architecture
    • Project Report.pdf
    • run.py
    • presentation.pdf
    • grosto
        ➢ __init__.py
        ➢ routes.py
        ➢ models.py
        ➢ forms.py
        ➢ __pycache__
        ➢ templates
            o layout.html
            o p_edit.html
            o c_edit.html
            o admin_page.html
            o cart.html
            o home.html
            o search_results.html
            o login.html
            o register.html
        ➢ static
            o main.css
    • README.txt
Features
    Two types of users – admin and buyers
    Username = Admin Password=” Administrator”
    For buyers username and password entered on registration.
    Admin can create, update, delete and edit categories and products.
    Buyers can view Categories and products and put them all in their cart.
    Buyers can search for existing categories and products.
