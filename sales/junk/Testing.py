
    
    Account = db.relationship('Accounts', backref='customers')
    User = db.Column(db.String(), nullable = False)
    
class Accounts(db.Model):
    #Creating a Database for Payments
    id = db.Column(db.Integer(), primary_key = True)
    Customer_ID = db.Column(db.Integer(), nullable = False)
    Product_ID = db.Column(db.Integer(), nullable = False)
    Date_Created = db.Column(db.String(), default= datetime.now, nullable = False)
    Date_Updated = db.Column(db.DateTime(), default= datetime.now, onupdate= datetime.now, nullable = False)
    Owner_ID = db.Column(db.Integer(), db.ForeignKey('customers.id'), nullable = False)
    Blocks = db.relationship('Products', backref='accounts')
    User = db.Column(db.String(), nullable = False)
    

    Owner_ID = db.Column(db.Integer(), db.ForeignKey('accounts.id'), nullable = False)
    Payments = db.relationship('Blocks', backref='products')
    

    



class Cement(db.Model):
    #Creating a Database for Cement
    id = db.Column(db.Integer(), primary_key = True)
    Product_ID = db.Column(db.Integer(), nullable = False)
    Type = db.Column(db.String(), nullable = False)
    Quantity = db.Column(db.Integer(), nullable = False)
    Remainder = db.Column(db.Integer(), nullable = False)
    Customer_ID = db.Column(db.Integer(), nullable = False)
    Date_Created = db.Column(db.String(), default= datetime.now, nullable = False)
    Date_Updated = db.Column(db.DateTime(), default= datetime.now, onupdate= datetime.now, nullable = False)
    Owner_ID = db.Column(db.Integer(), db.ForeignKey('accounts.id'), nullable = False)
    Payments = db.relationship('Payments', backref='cement')
    User = db.Column(db.String(), nullable = False)
    
class Sand(db.Model):
    #Creating a Database for River_Sand
    id = db.Column(db.Integer(), primary_key = True)
    Product_ID = db.Column(db.Integer(), nullable = False)
    Type = db.Column(db.String(), nullable = False)
    Quantity = db.Column(db.Integer(), nullable = False)
    Remainder = db.Column(db.Integer(), nullable = False)
    Customer_ID = db.Column(db.Integer(), nullable = False)
    Date_Created = db.Column(db.String(), default= datetime.now, nullable = False)
    Date_Updated = db.Column(db.DateTime(), default= datetime.now, onupdate= datetime.now, nullable = False)
    Owner_ID = db.Column(db.Integer(), db.ForeignKey('accounts.id'), nullable = False)
    Payments = db.relationship('Payments', backref='sand')
    User = db.Column(db.String(), nullable = False)
    
class Poles(db.Model):
    #Creating a Database for Poles
    id = db.Column(db.Integer(), primary_key = True)
    Product_ID = db.Column(db.Integer(), nullable = False)
    Type = db.Column(db.String(), nullable = False)
    Quantity = db.Column(db.Integer(), nullable = False)
    Remainder = db.Column(db.Integer(), nullable = False)
    Customer_ID = db.Column(db.Integer(), nullable = False)
    Date_Created = db.Column(db.String(), default= datetime.now, nullable = False)
    Date_Updated = db.Column(db.DateTime(), default= datetime.now, onupdate= datetime.now, nullable = False)
    Owner_ID = db.Column(db.Integer(), db.ForeignKey('accounts.id'), nullable = False)
    Payments = db.relationship('Payments', backref='poles')
    User = db.Column(db.String(), nullable = False)
    
class Lintels(db.Model):
    #Creating a Database for Lintels
    id = db.Column(db.Integer(), primary_key = True)
    Product_ID = db.Column(db.Integer(), nullable = False)
    Type = db.Column(db.String(), nullable = False)
    Customer_ID = db.Column(db.Integer(), nullable = False)
    Date_Created = db.Column(db.String(), default= datetime.now, nullable = False)
    Date_Updated = db.Column(db.DateTime(), default= datetime.now, onupdate= datetime.now, nullable = False)
    Owner_ID = db.Column(db.Integer(), db.ForeignKey('accounts.id'), nullable = False)
    Payments = db.relationship('Payments', backref='lintels')
    User = db.Column(db.String(), nullable = False)
    
class Delivery(db.Model):
    #Creating a Database for Delivery
    id = db.Column(db.Integer(), primary_key = True)
    Area = db.Column(db.String(), nullable = False)
    Quantity = db.Column(db.Integer(), nullable = False)
    Remainder = db.Column(db.Integer(), nullable = False)
    Customer_ID = db.Column(db.Integer(), nullable = False)
    Date_Schedule = db.Column(db.DateTime(), nullable = False)
    Date_Created = db.Column(db.String(), default= datetime.now, nullable = False)
    Date_Updated = db.Column(db.DateTime(), default= datetime.now, onupdate= datetime.now, nullable = False)
    Owner_ID = db.Column(db.Integer(), db.ForeignKey('accounts.id'), nullable = False)
    Payments = db.relationship('Payments', backref='delivery')
    User = db.Column(db.String(), nullable = False)
    
    
#Cement = db.relationship('Cement', backref='accounts')
#Sand = db.relationship('Sand', backref='accounts')
#Poles = db.relationship('Poles', backref='accounts')
#Lintels = db.relationship('Lintels', backref='accounts')
#Delivery = db.relationship('Delivery', backref='accounts')



    

#Handling Sales Information
@main.route('/sales')
@login_required
def sales():
    #Get all Database class entries as a list
    tickets= Items.query.all() 
    #Pass tickets values to be accessed by html sales template
    return render_template('sales.html', tickets_list= tickets)
