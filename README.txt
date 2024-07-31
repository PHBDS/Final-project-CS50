# Shopping List
#### Video Demo:  <URL HERE>
#### Description:
This project is a web-based shopping list application built using Flask, a Python web framework. 
The application allows users to create and manage a shopping list. 
Users can add new products to their list, mark items as bought, and update the quantity of bought items. 
The application supports user authentication, enabling each user to manage their own shopping list independently.

Key Features

Users can register for a new account and log in to the application.
User authentication ensures that each user’s data is kept separate and secure.

Users can add new items to their shopping list.
When adding a new item, users can either type a new category or select an existing one from a dynamically generated list of previously used categories.
Items can be marked as bought, which moves them from the active shopping list to the bought products list.
Users can update the quantity of bought items, which will return them to the active shopping list with the updated quantity.
Quantity is not a mandatory input, in case field is empty, it will be added as "some" as the difference between active list and inactive list is 0 or not 0 in the quantity field.


The category field in the new item form uses a <datalist> element, which is dynamically populated with categories previously used by the user.