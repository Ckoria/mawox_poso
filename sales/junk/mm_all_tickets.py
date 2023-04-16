from sales.junk.Get_Customers import get_ticket
from sales import app, db

tickets_list = get_ticket(5, "Quote Pending")
#MM All Clients Database   
class Items(db.Model):
    #Creating a Database for items
    id = db.Column(db.Integer(), primary_key = True)
    First_Name = db.Column(db.String(length=30), nullable = False)
    Last_Name = db.Column(db.String(), nullable = False)
    Cell_No = db.Column(db.String(), nullable = False, unique = True)
    Quote = db.Column(db.String(), nullable = False)
    Model = db.Column(db.String(), nullable = False)
    Issue_Type = db.Column(db.String(), nullable = False)
    Date_Created = db.Column(db.String(), nullable = False)
    Note_Date = db.Column(db.String(), nullable = False)
    Note = db.Column(db.String(), nullable = False)
    Tel_No = db.Column(db.String(), nullable = False, unique = True)
    Email = db.Column(db.String(), nullable = False, unique = True)
    Address = db.Column(db.String(), nullable = False)
        
    def __repr__(self):
        return f'Items {self.First_Name}'
   
with app.app_context():
    for item in tickets_list:
        myItems  = Items( 
                        First_Name=item[0], Last_Name=item[1],
                        Cell_No=item[2],Quote=item[3],
                        Model=item[4], Issue_Type=item[5],
                        Date_Created=item[6], Note_Date=item[7],
                        Note=item[8], Tel_No=item[9],
                        Email=item[10], Address=item[11]
            )
        try:    
            db.session.add(myItems) 
            db.session.commit()  
        except:
            db.session.rollback()
      