# Shopping List
#### Video Demo:  <URL HERE>
### Description:

This project is a web-based shopping list application built using Flask, a Python web framework. 
The application allows users to create and manage a shopping list.   
Users can add new products to their list, mark items as bought, and update the quantity of bought items.   
The application supports user authentication, enabling each user to manage their own shopping list independently.

### Key Features

1. User Authentication:

Users can register for a new account and log in and out of the application.  
User authentication ensures that each user’s data is kept separate and secure.

2. Item Management:

Add New Item: Users can add new items to their shopping list, specifying the item name, category, and quantity. If the category does not exist, it is created automatically.  
If categotry or quantity are empty they are assigned to "Undefined" and "some"  
Update Quantity: Users can update the quantity to transfer that item to the active shopping list  
Mark as Bought: Users can mark items as bought, which updates their status and quantity to 0 and transfer item to the inactive list.  
Delete Item: Users can delete items from their list. If a category becomes empty after deletion, the category itself is removed from the database.

3. View and Manage Lists:

View active list: Users can view all items in their shopping list categorized by their respective categories.
View Inactive list Items: Users can view items that have been marked as bought.
Items can be transfered from one list to the other with one click

### Technologies Used:
Flask , SQLite, HTML/CSS, Git/GitHub

#### GitHub Repository:
The project is hosted on GitHub at https://github.com/PHBDS/Final-project-CS50.

## Files description
### 1. app.py 

Python codes that works on the back end

1. /login Route: Handles user login.  
Renders the login page (login.html).  
If there’s a message and message_type in the URL parameters, they are passed to the template to display error messages.  
Checks if username and password are provided.  
Queries the database for the user with the submitted username.  
Validates the password against the stored hash.  
If validation fails, redirects back to the login page with an error message.  
If successful, sets the user_id in the session and redirects to the home page.  

2. /logout Route: Logs the user out and clears the session.  
Clears the user session by calling session.clear().  
Redirects the user to the login page after logging out.

3. /register Route:  Handles user registration.  
Ensures that username, password, and confirmation fields are provided.  
Checks if the password matches the confirmation field.  
Checks if the username already exists in the database.  
If any checks fail, redirects back to the registration page with an appropriate error message.  
If all checks pass, inserts the new user into the database, starts a session for the user, and redirects to the home page.

4. / Route (Home Page): Displays and manages the user's shopping list.  
-GET:  
Retrieves and displays all items in the shopping list that are not marked as bought.  
Retrieves and displays all items marked as bought.  
Retrieves all distinct categories for the user.  
Renders the home page (index.html) with the lists of items and categories.  

-POST:  
Handles different types of form submissions related to managing the shopping list:  
#### Add New Item:
Adds a new item to the list or updates an existing item's quantity.   
If the category does not exist, it creates a new one.   
Redirects back to the home page with a success or warning message. 

#### Mark as Bought:
Marks an item as bought by setting its quantity to 0.  
Redirects back to the home page with a success or error message.  

#### Update Quantity:
Updates the quantity of an existing item.  
Redirects back to the home page with a success or error message.  

#### Delete Item: 
Deletes an item from the list.  
If the category becomes empty after deletion, it also deletes the category.  
Redirects back to the home page with a success message.

5. after_request Function: Ensures responses are not cached.  
Modifies the response headers to include Cache-Control, Expires, and Pragma directives to prevent caching.

6. login_required Function: Decorator to ensure that a route is accessible only to logged-in users.  
Checks if the user_id exists in the session.  
Redirects to the login page if user_id is not found in the session.  
Allows access to the decorated function if the user is logged in.



