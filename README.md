# Online-Shop-Database
An online shop database management code written with python and SQLite3 and the UI created with prettyTable. This was done as a final project for my university's database course.

Navigating the database is done through a simple and sleek UI (run on the terminal), by entering numbers correlating to an action, along with a "back" option in every scenario to minimize restarting from the beginning of the tree.

You can sign up as a seller or buyer, and your username and password is saved for later use. Entering the password wrong will block you from entering the account. There is an option to enter as a guest which does not require signing up. This feature allows you to view the online shop database while preventing actions such as buying or selling.

Signing in as a seller enables you to add new products to the database, and delete or edit existing ones from the database, while signing in as a customer lets you buy and search for products, add them to your cart to buy later, and view your purchase history. Removing items from your cart can easily be done in the See Purchase History section. 

What can be done next?
1. Hashing could be implemented for improved security, instead of the current system (which is matching the text in the saved file to the one being entered in the terminal) this is being used.
2. For a more intuitive user experience, adding graphics would be optimal; e.g. designing and setting up a working website.
