# small ecommerce without shop-module (Django/Python)

<h2>Introduction</h2>
A small shopping website using Python/Django with bootstrap for a friend who was organizing a group purchase. <br></br>
The website includes features such as creating product descriptions, calculating costs, creating and validating discount coupons, setting up free shipping, implementing automatic Gmail sending, and providing progress reports on account payments.
<br></br>
For the front-end, I utilized JavaScript cookies and sessions, while the back-end is based on the Django MTV framework. The biggest challenge was accommodating various user scenarios that involve cost interactions, such as shipping fees, purchase amounts, and delivery options.

<h2>Install</h2>
1. git clone https://github.com/SiaoChi/ecommerce/<br>

2. pip install -ur requirements.txt (os)<br>

3. change your database information<br>

4. executive <br>
```
python manage.py makemigrations
python manage.py migrate
```

5. create superuser<br>
```
python manage.py createsuperuser
```

6. static<br>
```
python manage.py collectstatic --noinput
```
7. run server<br>
```
python manage.py
```

<h2>Functions</h2>

1. Create product/cost/photo/description
2. Establish shipping methods/shipping fees/free shipping mechanism
3. Set up shopping cart coupons
4. Establish automatic email system for order confirmation
5. Fill in payment information
6. Track shipment progress


<h2>project structure</h2>

```
ecommerce/
├── __pycache__
├── ecommerce
│   └── __pycache__
├── shop
│   ├── __pycache__
│   └── migrations
│       └── __pycache__
├── static
│   ├── css
│   ├── images
│   │   └── product
│   └── js
└── templates
```

