from django.db import models

class Order(models.Model):

    owner = models.ForeignKey('auth.User', related_name='orders', on_delete=models.CASCADE)

    """
    The intent was for this model was to pull data from the main db, but never quite got approval to query it directly.

    These would then be queried against the order checklists defined through the relationship between the Retailer and Supplier models - to ultimately
    result in a display of what was missing, so that the customer could be contacted to confirm or contest the absence.

    Probably would have been much clearer if I'd used a second database for testing...but it served its purpose of demonstrating what I was going for overall.
    """

    recieved = models.DateTimeField(auto_now_add=True)
    supplier = models.CharField(max_length=4)
    retailer = models.CharField(max_length=4)
    ordernum = models.CharField(max_length=20)

    def __str__(self):

        return f'{self.ordernum} - {self.supplier} - {self.retailer} - {self.recieved}'
    
    class Meta:

        ordering = ['recieved']

class Retailer(models.Model):

    owner = models.ForeignKey('auth.User', related_name='retailers', on_delete=models.CASCADE)

    """
    The relationship between this model and that of the Supplier model is intended to be used create 'checklists' - the items of which are then queried against
    the real db data (or for demonstration purposes the Order model above...) using the account and retailer codes and filtered by recieved date. To eventually
    result in a front-end display of orders recieved for the given days operations.

    This is presently done manually by going through the orders on the WMS with printed out checklists that are hardly ever up to date (rendering the process mostly
    pointless.)

    Seemed silly.
    """

    code = models.CharField(max_length=4)
    name = models.CharField(max_length=100)
    list = models.ManyToManyField('Supplier')

    def __str__(self):

        return f'{self.code}: {self.name}'

class Supplier(models.Model):

    owner = models.ForeignKey('auth.User', related_name='suppliers', on_delete=models.CASCADE)

    code = models.CharField(max_length=4)
    name = models.CharField(max_length=100)

    def __str__(self):
    
        return f'{self.code}: {self.name}'

class Concession(models.Model):

    owner = models.ForeignKey('auth.User', related_name='concessions', on_delete=models.CASCADE)

    """ 
    Concessions/Derogations are customer requests with retailer permission to use stock with a life outside of the agreed
    'life into depot' range.

    These were printed by the customer, filled out, scanned in, emailed to us, printed again, stored in a folder and also manually
    typed into an excel sheet (with frequent mistakes and misplacings) that was then used by multiple departments.

    This caused endless, stressful, expensive issues...seemed silly.

    This model stores the necessary information and can be accessed by everyone that needs it - plan was to build a form into the
    front end client so that customers can create/amend concessions online, thereby outsourcing the mistakes and improving communication
    fidelity between departments.
    """

    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    best_before = models.DateField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):

        return f'RETAILER: {self.retailer} SUPPLIER: {self.supplier} PRODUCT: {self.product}'

class Memo(models.Model):

    owner = models.ForeignKey('auth.User', related_name='memos', on_delete=models.CASCADE)

    """ To store order related notes that don't quite constitute a concession, see above """

    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    content = models.TextField()

    def __str__(self):

        return f'RETAILER: {self.retailer} SUPPLIER: {self.supplier}  START: {self.start_date}, END: {self.end_date} - ({len(self.content)} characters)'

class ManualOrder(models.Model):

    owner = models.ForeignKey('auth.User', related_name='manuals', on_delete=models.CASCADE)

    """ Replacement system for printing 'small' orders, i.e. anything not recieved via EDI (emails/attachments) and storing them in physical trays...
    things were always going missing, seemed silly. """

    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    processing = models.DateField(null=True)
    details = models.TextField(max_length=500)
    attachments = models.FileField()

    def __str__(self):

        return f'RETAILER: {self.retailer} SUPPLIER: {self.supplier} PROCESSING: {self.processing} FILES: {self.attachments}'
