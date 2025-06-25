class CartManager:
    """Utility class for managing in-memory cart (demo purposes)"""
    
    def __init__(self):
        self.cart = []
    
    def add_item(self, item, quantity=1):
        """Add an item to the cart"""
        self.cart.append({"item": item, "quantity": quantity})
        return {"status": "added", "item": item, "quantity": quantity}
    
    def view_cart(self):
        """View the current cart contents"""
        return self.cart.copy()
    
    def clear_cart(self):
        """Clear the cart"""
        self.cart = []
        return {"status": "cleared"}
    
    def get_cart_count(self):
        """Get the number of items in the cart"""
        return len(self.cart) 