This is a demo website for a food ordering system built using Django, HTML, and Bootstrap. The website demonstrates the integration of the PayPal payment gateway using its API. The focus of this project is on the payment gateway integration, but it also includes a basic structure for a food ordering system.

**Features:**

Menu Display: Showcasing various food items available for order.

Order Management: Users can add items to the cart and place orders.

PayPal Integration: Secure payment processing via PayPal.

Responsive Design: Built using Bootstrap for a mobile-first, responsive UI.


**Clone the Repository:**

git clone https://github.com/afthabsheikh/food-ordering-system-demo.git

cd food-ordering-system-demo


**Apply Migrations:**

python manage.py migrate

Run the Development Server:


**Runserver:**

python manage.py runserver


**Open the Website:**

Visit http://127.0.0.1:8000 in your web browser.


**PayPal Integration:**

The website integrates PayPal's API for handling payments. Ensure you have a PayPal developer account and the necessary credentials.


**Configuration:**

Update the PayPal configuration in your settings.py:

PAYPAL_CLIENT_ID = 'your-client-id'

PAYPAL_CLIENT_SECRET = 'your-client-secret'


**Usage:**

Navigate through the menu, select items, and add them to your cart.

Proceed to checkout to review your order.

Complete the payment using the PayPal option.


**Customization:**

Replace Placeholder Images: The website contains placeholder images that need to be replaced with relevant food item images.

UI Adjustments: Customize the UI as per your brand guidelines using Bootstrap or custom CSS.
