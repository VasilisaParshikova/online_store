# Online music store

The goal of the project was to create a functional marketplace for music products.

The project consists of three applications:
- shop_app (all logic related to the catalog and product pages)
- orders_app (all logic related to the shopping cart, placing and paying for orders, order history)
- user_app (all logic related to user personal data, registration, authentication)

The website has the following functionality:
- Catalog
- Search and filter products in the catalog
- Page for viewing detailed information about the product
- Adding a product to the shopping cart using buttons from the catalog page and from the product page
- Ability to view items in the shopping cart, remove items from and change the quantity of items in the shopping cart
- Implemented a custumers’ personal account
- Making and payment (mock) of the order
- View order history
- User registration and authentication
- All functions of the website exept making and paying for an order are possible for unregistered users. The ability to register or authenticate at the first stage of ordering has been implemented. After user login into the site or registers, all items added to the shopping cart before authentication are automatically transferred to the user's shopping cart.
- The administrative panel has been configured.

### My contribution
In this project, I implemented the backend from designing the structure of applications, links and the project database to implementing scripts for all functionality of the website. Also, if necessary, I made some additions and adjustments to the provided front-end of the site.

### Used stack
Python 3.9

Django 4.1.7

Database - built-in Django ORM and default sqlite database were used

The following files have been prepared to deploy the project:
- requirements.txt
- fixtures folder with all necessary to demonstrate the work of the project data fixtures 