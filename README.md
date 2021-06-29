# django-ecommerce-with-stripe

An e-commerce site built with Django and Stripe where multiple vendors can sell their products


```
virtualenv 
virtualenv venv
.\venv\Scripts\activate
cd ecommerce
```

```
pip install -r requirements.txt
python manage.py runserver

``` 

 


New db create
```
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -path "*.sqlite3"  -delete
python manage.py makemigrations customer
python manage.py makemigrations 
python manage.py migrate
python manage.py migrate --fake  
```

DB Admin: 'admin', 'admin@example.com', 'adminpass'


<br>
Settings.py 

- [ ] ADD STRIPE PUB KEY AND STRIPE SECRET KEY
- [ ] ADD EMAIL INFORMATION



##### Project Output
![homeOutput](https://github.com/elifnurkarakoc/django-ecommerce/blob/main/output/home.jpg)

![cartOutput](https://github.com/elifnurkarakoc/django-ecommerce/blob/main/output/cart.jpg)

 
 
