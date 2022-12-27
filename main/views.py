from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Category, Urun, UrunFotograf, Sepet, Favoriler, Adres, CreditCard, Renk, Beden , Siparis, SiparisUrun
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.forms import UserUpdateForm, SepetForm, AddressForm, CreditCardForm, SiparisForm

# Create your views here.


#hesap işlemleri

def login_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    context = {
        "categories" : Category.objects.all()
    }
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {
                "error": "username ya da password yanlis" 
            })
    return render(request, "login.html", context)

def register_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    context = {
        "categories" : Category.objects.all()
    }
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "register.html", {"error": "username kullanılıyor."})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "register.html", {"error": "email kullanılıyor."})
                else:
                    user = User.objects.create_user(username=username, email=email,first_name=firstname, last_name=lastname,password=password)
                    user.save()
                    return redirect("login")
        else:
            return render(request, "register.html", {"error":"parolar eşleşmiyor."})
    return render(request, "register.html",context)

def logout_request(request):
    logout(request)
    return redirect("home")


#Search


def search_product(request):

    if request.method == "POST":
        search = request.POST['search']
        categories = Category.objects.all()
        urunler = Urun.objects.filter(Q(name__contains=search) | Q(barkod__contains = search))
        context = {
            "categories" : categories,
            'search' : search,
            'urunler' : urunler
        }
        return render(request, "search.html" ,context)
    else:
        return render(request, "search.html" ,context)








def index(request):
    current_user = request.user
    request.session['sepet_urunler'] = Sepet.objects.filter(user_id=current_user.id).count()
    context = {
        "categories" : Category.objects.all()
    }
    return render(request, "index.html", context)

def urunler(request, slug):
    context = {
        "urunler": Urun.objects.filter(category__slug = slug),
        "fotograflar": UrunFotograf.objects.all(),
        "categories" : Category.objects.all(),
        "renkler": Renk.objects.all(),
        "bedenler": Beden.objects.all(),
    }
    selected_color = request.GET.get('renk')
    selected_size = request.GET.get('beden')

    if selected_color:
        context["urunler"] = context["urunler"].filter(renk__id=selected_color)

    if selected_size:
        context["urunler"] = context["urunler"].filter(beden__id=selected_size)

    context["selected_color"] = selected_color
    context["selected_size"] = selected_size
    return render(request,"urunler.html", context)


def urun_detay(request , slug):
    urun = Urun.objects.get(slug=slug)
    return render(request,"urun_detay.html",{
        "urun" : urun,
        "categories" : Category.objects.all()
    })



@login_required(login_url='/login')
def favoriler(request):
    categories = Category.objects.all()
    user = request.user
    favoriler = Favoriler.objects.filter(user_id = user.id)


    context = {
        'favoriler':favoriler,
        'categories': categories,
    }
    
    return render(request, 'favoriler.html',context)

@login_required(login_url='/login')
def favorilere_ekle(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    urunkontrol = Favoriler.objects.filter(urun_id = id, user_id = current_user.id)
    if urunkontrol:
        messages.success(request, "Ürün zaten favorilerinde.")
        return HttpResponseRedirect(url)
    else:
        if request.method == 'POST':
            data = Favoriler()
            data.user_id = current_user.id
            data.urun_id = id
            data.save()
        messages.success(request, "Ürün favorilere eklendi.")
        return HttpResponseRedirect(url)

@login_required(login_url='/login')
def favorilerden_sil(request, id):
    Favoriler.objects.filter(id=id).delete()
    messages.success(request, 'Ürün Favorilerden Silinmiştir.')
    return HttpResponseRedirect("/favoriler")






@login_required(login_url='/login')
def sepet(request):
    categories = Category.objects.all()
    user = request.user
    sepet = Sepet.objects.filter(user_id = user.id)
    total = 0

    for rs in sepet:
        total += rs.urun.fiyat * rs.miktar

    context = {
        'sepet':sepet,
        'categories': categories,
        'total': total
    }
    
    return render(request, 'sepet.html',context)


@login_required(login_url='/login')
def sepete_ekle(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    urunkontrol = Sepet.objects.filter(urun_id = id, user_id=current_user.id)
    if request.method == 'POST':
        form = SepetForm(request.POST)
        if form.is_valid():
            if urunkontrol:
                data = Sepet.objects.get(urun_id =id)
                data.miktar += form.cleaned_data['miktar']
                data.save()
            else:
                data = Sepet()
                data.user_id = current_user.id
                data.urun_id = id
                data.miktar = form.cleaned_data['miktar']
                data.save()
            request.session['sepet_urunler'] = Sepet.objects.filter(user_id=current_user.id).count()
            messages.success(request, "Ürün sepete eklendi.")
            return HttpResponseRedirect(url)


@login_required(login_url='/login')
def sepetten_sil(request, id):
    current_user = request.user
    Sepet.objects.filter(id=id).delete()
    request.session['sepet_urunler'] = Sepet.objects.filter(user_id=current_user.id).count()
    messages.success(request, 'Ürün Sepetten Silinmiştir.')
    return HttpResponseRedirect("/sepet")

@login_required(login_url='/login')
def profile(request):
    context = {
        'user' : request.user,
        'categories': Category.objects.all()
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/login')
def profile_sil(request, id):
    User.objects.filter(id=id).delete()
    messages.warning(request, 'Hesabınız silinmiştir.')
    return HttpResponseRedirect("/login")

@login_required(login_url='/login') # Check login
def profile_email_guncelle(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/profile')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        context = {
            'category': category,
            'user_form': user_form,
        }
        return render(request, 'profile_email_guncelle.html', context)

@login_required(login_url='/login') # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/profile')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/password')
    else:
        #category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'profile_parola_guncelle.html', {'form': form, #'category': category
                       })

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('address_list')
    else:
        form = AddressForm()
    return render(request, 'add_address.html', {'form': form})

def address_list(request):
    addresses = Adres.objects.filter(user=request.user)
    return render(request, 'address_list.html', {'addresses': addresses})

def delete_address(request, address_id):
    Adres.objects.get(id=address_id).delete()
    return redirect('address_list')


def add_credit_card(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            credit_card = form.save(commit=False)
            credit_card.user = request.user
            credit_card.save()
            return redirect('credit_card_list')
    else:
        form = CreditCardForm()
    return render(request, 'add_credit_card.html', {'form': form , "categories" : Category.objects.all()})

def credit_card_list(request):
    credit_cards = CreditCard.objects.filter(user=request.user)
    return render(request, 'credit_card_list.html', {'credit_cards': credit_cards, "categories" : Category.objects.all()})

def delete_credit_card(request, credit_card_id):
    CreditCard.objects.get(id=credit_card_id).delete()
    return redirect('credit_card_list')




def favorilere_eklenen_urunler_kategori(request):
    # Eğer kullanıcı superuser değilse, hata mesajı göster
    if not request.user.is_superuser:
        return HttpResponse("Bu sayfaya erişim izniniz yok.")
    # Tüm kategorileri al
    kategoriler = Category.objects.all()

    # Her kategori için en çok favorilere eklenen üç ürünü belirle
    favorilere_eklenen_urunler_kategori = {}
    for kategori in kategoriler:
        favorilere_eklenen_urunler = Favoriler.objects.filter(urun__category=kategori).values('urun').annotate(num_favoriler=Count('urun')).order_by('-num_favoriler')[:3]
        en_cok_favorilere_eklenen_urunler = []
        for favorilere_eklenen_urun in favorilere_eklenen_urunler:
            en_cok_favorilere_eklenen_urunler.append(Urun.objects.get(id=favorilere_eklenen_urun['urun']))
        favorilere_eklenen_urunler_kategori[kategori.name] = en_cok_favorilere_eklenen_urunler

    # Sayfayı render et
    return render(request, 'favorilere_eklenen_urunler_kategori.html', {'favorilere_eklenen_urunler_kategori': favorilere_eklenen_urunler_kategori, "categories" : Category.objects.all()})


def siparis(request):
    category = Category.objects.all()
    current_user = request.user
    sepet = Sepet.objects.filter(user_id = current_user.id)
    total = 0
    for rs in sepet:
        total += rs.urun.fiyat * rs.miktar

    if request.method == 'POST':
        form = SiparisForm(request.POST)
        if form.is_valid():

            data = Siparis()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.adres = form.cleaned_data['adres']
            data.telefon = form.cleaned_data['telefon']
            data.kredi_karti = form.cleaned_data['kredi_karti']
            data.user_id = current_user.id
            data.toplam_tutar = total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() #


            for rs in sepet:
                detail = SiparisUrun()
                detail.siparis_id  = data.id # Order Id
                detail.urun_id     = rs.urun_id
                detail.user_id     = current_user.id
                detail.miktar      = rs.miktar
                detail.fiyat       = rs.urun.fiyat
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                urun = Urun.objects.get(id=rs.urun_id)
                urun.stok -= rs.miktar
                urun.save()
                #************ <> *****************

            Sepet.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            messages.success(request, "Siparişiniz Verilmiştir.")
            return render(request, '/sepet',{'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/sepet")

    form= SiparisForm()
    context = {'sepet': sepet,
               'category': category,
               'total': total,
               'form': form,
               }
    return render(request, 'siparis.html', context)

@login_required(login_url='/login') # Check login
def siparislerim(request):
    category = Category.objects.all()
    current_user = request.user
    siparis=Siparis.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'siparisler': siparis,
               }
    return render(request, 'siparislerim.html', context)
















# @login_required(login_url='/login')
# def siparis(request):
#     categories = Category.objects.all()
#     user = request.user
#     sepet = Sepet.objects.filter(user_id = user.id)
#     kredi_kart = CreditCard.objects.filter(user_id = user.id)
#     adres = Adres.objects.filter(user_id = user.id)
#     total = 0
#     for rs in sepet:
#         total += rs.urun.fiyat * rs.miktar
#     if(total == 0):
#         return HttpResponse("Sepetiniz Boş.")
#     else:
#         context = {
#             'sepet':sepet,
#             'categories': categories,
#             'kredi_kart': kredi_kart,
#             'adres': adres,
#             'total': total
#         }
#         return render(request, 'siparis.html',context)