class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_title = db.Column(db.String(100), nullable=False, default="Bitbanta store")
    site_logo = db.Column(db.String(100), nullable=True)  # Store logo file path
    contact_email = db.Column(db.String(100), nullable=False, default="info@bitbanta.com")
    contact_phone = db.Column(db.String(20), nullable=False, default="123-456-7890")
    address = db.Column(db.Text, nullable=True, default="123 Main St, City, Country")
    maintenance_mode = db.Column(db.Boolean, default=False)
    notifications_new_orders = db.Column(db.Boolean, default=True)
    notifications_customer_inquiries = db.Column(db.Boolean, default=True)
    notifications_low_stock = db.Column(db.Boolean, default=True)

    @staticmethod
    def get_settings():
        # Singleton pattern to ensure only one settings record
        settings = Settings.query.first()
        if not settings:
            settings = Settings()
            db.session.add(settings)
            db.session.commit()
        return settings



# Models (User, Product, CartItem)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(100), nullable=False, default='default.jpg')
    category = db.Column(db.String(20), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    # Define the relationship to CartItem with a backref
    cart_items = db.relationship('CartItem', backref='product', lazy=True)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Corrected here
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('User', backref='cart_items')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Assuming you have a user table
    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order {self.id}, User {self.user_id}>"


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<OrderItem {self.id}, Order {self.order_id}, Products {self.product_id}>"


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f'<Subscriber {self.email}>'

