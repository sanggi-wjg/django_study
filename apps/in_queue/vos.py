class ValueObject(object):
    pass


class InQueue(ValueObject):

    def __init__(self):
        self.packageCd = None
        self.productCd = None
        self.productItemCd = None
        self.productName = None
        self.productUnitPrice = None
        self.inOrderCd = None
        self.inOrderDate = None

    def __repr__(self):
        return '{} {}'.format(self.packageCd, self.productCd)
