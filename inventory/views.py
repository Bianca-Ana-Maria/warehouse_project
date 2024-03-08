# Create Views: Create views to handle CSV file uploads and updating stock levels
import csv
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect

from inventory.models import Product, Stock
from .forms import CSVUploadForm

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process uploaded CSV file
            handle_uploaded_csv(request.FILES['file'])
            return HttpResponseRedirect('/success/')  # Redirect to success page
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form})

# Implement CSV Parsing Logic: Implement the logic to parse the uploaded CSV file and update stock levels
def handle_uploaded_csv(file):
    reader = csv.DictReader(file)
    for row in reader:
        # Assuming CSV has fields like 'product_name' and 'quantity'
        product_name = row['product_name']
        quantity = int(row['quantity'])
        # Get or create product
        product, created = Product.objects.get_or_create(name=product_name)
        if created:
            # Initialize stock if product is newly created
            Stock.objects.create(product=product, quantity=quantity)
        else:
            # Update existing stock
            stock = Stock.objects.get(product=product)
            stock.quantity += quantity
            stock.save()


# Render the upload_form.html template when displaying the upload form and render the success_page.html template after successful CSV processing.
def upload_form_view(request):
    if request.method == 'POST':
        # Process CSV file
        # Redirect to success page after processing
        return redirect('success_page')

    return render(request, 'upload_form.html')

def success_page_view(request):
    return render(request, 'success_page.html')