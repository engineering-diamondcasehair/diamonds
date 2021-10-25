from DiamondCaseWeb.model.product import ProductCategory

""" General utility functions."""
def getCategories():
    """Utility function for retriving product category for header.
    
    Returns:
        a list of Catagory model objests for populating header.
    """
    categories = ProductCategory.query.all()
    return categories