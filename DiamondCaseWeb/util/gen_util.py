from DiamondCaseWeb.model.product import ProductCategory

""" General utility functions."""
def getCategories():
    """Returns a list of Catagory model objests for populating header"""
    categories = ProductCategory.query.all()
    return categories