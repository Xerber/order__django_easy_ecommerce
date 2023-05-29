# order__django_easy_ecommerce

## A real order from a client who needed to write a website selling computer equipment for a graduation project.

Tasks set:
- So that the site would be publicly available (for 2 months immediately take a cheaper domain of some kind)
> Made on free hosting pythonanywhere. In the future, it can also be extended for free, but for this you need to click on the "Run until 3 months from today" button in the admin panel once every three months

- The site must have an admin panel with the ability to restore the password
> Admin panel implemented, Password recovery too. Password recovery via automatic token generation via email. Emailsponsorily initially need to be configured

- The admin panel should be able to add managers with the differentiation of rights to actions
> Implemented by the Django admin panel. The rights are issued for each model of their own. It is possible to create a "template" of rights, for example, one for the manager, another for the storekeeper, etc.

- Add the ability in the admin panel to change the price of goods, quantity, etc.
> Implemented a full-fledged admin panel where you can create/ delete products, change any data, add extras. images, create categories/subcategories, accept requests from customers from the contacts page, see cart orders, etc.

- The old site is indicated in the presentation, the new one needs to be done "beautifully"
> A passable template has been selected from the free ones possible, according to the theme of the online store. Adapted to the requirements

- If there is no product, write "out of stock"
> Implemented by disabling the + button with the corresponding label. The corresponding inscription is displayed in the "Favorites" + the add to cart button has been removed


## Necessary actions to launch the project:
- First of all, we create a virtual environment
```
python -m venv env
```

We install the necessary dependencies
```
pip install -r requirements.txt
```

Entering your secret key for the project
```
im ecommerce/setting_prod.py
SECRET_KEY
```

To be able to send a token to an email for password recovery, you need to log in to your gmail account - > Security -> Two-step authentication -> Application Passwords -> Create a password. After completing this step, fill in
```
EMAIL_FROM
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
```

Performing migrations to create a database
```
python manage.py migrate
```

Creating a superuser for authorization in the admin panel
```
python manage.py createsuperuser
```