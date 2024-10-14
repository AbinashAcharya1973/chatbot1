import mysql.connector

# Connect to MySQL database
def connect_to_db():
    connection = mysql.connector.connect(
        host='localhost',
        user='your-username',
        password='your-password',
        database='sales_db'  # Replace with your actual database name
    )
    return connection

# Fetch sales details for a specific invoice
def get_invoice_details(invoice_id, connection):
    cursor = connection.cursor(dictionary=True)
    
    # Fetch general invoice details from `invoicehead`
    cursor.execute("SELECT * FROM invoicehead WHERE invoice_id = %s", (invoice_id,))
    invoice = cursor.fetchone()
    
    if not invoice:
        return f"No invoice found with ID {invoice_id}."

    # Fetch detailed items from `invoicedetails`
    cursor.execute("SELECT product_name, quantity, price FROM invoicedetails WHERE invoice_id = %s", (invoice_id,))
    details = cursor.fetchall()

    if not details:
        return f"No details available for invoice ID {invoice_id}."
    
    # Format and return invoice details
    invoice_info = (f"Invoice ID: {invoice['invoice_id']}\n"
                    f"Customer Name: {invoice['customer_name']}\n"
                    f"Invoice Date: {invoice['invoice_date']}\n"
                    f"Total Amount: {invoice['total_amount']}\n"
                    f"Items:\n")
    
    for detail in details:
        invoice_info += (f"- {detail['product_name']}: {detail['quantity']} units @ ${detail['price']} each\n")
    
    return invoice_info

# Fetch sales summary for a customer
def get_customer_sales_summary(customer_name, connection):
    cursor = connection.cursor(dictionary=True)
    
    # Fetch all invoices for the given customer from `invoicehead`
    cursor.execute("SELECT * FROM invoicehead WHERE customer_name = %s", (customer_name,))
    invoices = cursor.fetchall()
    
    if not invoices:
        return f"No sales records found for customer {customer_name}."

    # Format and return sales summary
    summary = f"Sales Summary for {customer_name}:\n"
    
    for invoice in invoices:
        summary += (f"- Invoice ID: {invoice['invoice_id']}, Date: {invoice['invoice_date']}, "
                    f"Total Amount: ${invoice['total_amount']}\n")
    
    return summary

# Main chatbot function
def chatbot():
    connection = connect_to_db()
    print("Sales Bot: Hello! How can I assist you with sales information today? Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ")

        if user_input.lower() == 'quit':
            print("Sales Bot: Goodbye!")
            break
        
        # Parse user input and respond accordingly
        if user_input.startswith("Invoice details for ID"):
            try:
                invoice_id = int(user_input.split()[-1])
                response = get_invoice_details(invoice_id, connection)
            except ValueError:
                response = "Please provide a valid invoice ID."
        
        elif user_input.startswith("Sales summary for"):
            customer_name = user_input.split("for", 1)[-1].strip()
            response = get_customer_sales_summary(customer_name, connection)
        elif user_input.startswith("Highest sold product"):
            # Implement logic to fetch and return the highest sold product
            # This would involve querying the database for sales data and calculating the highest sold product.
            # For simplicity, we'll just return a placeholder response.
            response = "The highest sold product is 'Product X'."
        else:
            response = "Sorry, I can only provide 'Invoice details for ID' or 'Sales summary for customer'."
        
        print(f"Sales Bot: {response}\n")
    
    connection.close()

# Run chatbot
if __name__ == "__main__":
    chatbot()
