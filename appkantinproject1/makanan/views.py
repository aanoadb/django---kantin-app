from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Makanan
from .models import CartItem
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    searchMakanan = request.GET.get('nama')
    if searchMakanan:
        makanans = Makanan.objects.filter(nama__icontains=searchMakanan)
    else:
        makanans = Makanan.objects.all()
    return render(request, 'home.html', {'searchMakanan':searchMakanan, 'makanans' : makanans})

def detail(request,makanan_id):
    makanan = get_object_or_404(Makanan,pk=makanan_id)
    return render(request,'detail.html',{'makanan' : makanan})

def add_to_cart(request,makanan_id):
    makanan_id = int(makanan_id)
    makanan = Makanan.objects.get(pk=makanan_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1)) #jumlah pesanan dari form
        if quantity < 1:
            quantity = 1 #minimal pesanan 1
        
        # cart item jika sudah ada pesanan makanan tsb
        # created jika belum ada pesanan makanan tsb maka disimpan dan created = true
        cart_item, created = CartItem.objects.get_or_create(makanan=makanan)
        
        #If the item sudah ada (exists), update the quantity and item_total
        if not created:
            cart_item.quantity += quantity
            cart_item.item_total = quantity * makanan.harga
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.item_total = quantity * makanan.harga
            cart_item.save()
    return redirect('cart')

def view_cart(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.item_total for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, makanan_id):
    makanan_id = int(makanan_id)
    makanan = Makanan.objects.get(pk=makanan_id)
    try:
        cart_item = CartItem.objects.get(makanan=makanan)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')
