from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Listing, ListingImage, Category, SubCategory
from cloudinary.forms import CloudinaryFileField 


class SellerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telegram_username = forms.CharField(max_length=100, required=False)
    phone = forms.CharField(max_length=20, required=False)
    location = forms.CharField(max_length=200, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'telegram_username', 'phone', 'location', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.telegram_username = self.cleaned_data['telegram_username']
        user.phone = self.cleaned_data['phone']
        user.location = self.cleaned_data['location']
        if commit:
            user.save()
        return user


from django.forms import inlineformset_factory

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'category', 'subcategory', 
                 'condition', 'location', 'contact_telegram']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'subcategory': forms.Select(attrs={'disabled': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = SubCategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
                self.fields['subcategory'].widget.attrs.pop('disabled', None)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.all()
            self.fields['subcategory'].widget.attrs.pop('disabled', None)

class ListingImageForm(forms.ModelForm):
    image = CloudinaryFileField(
        options={
            'folder': 'listings',
            'transformation': {
                'quality': 'auto:good',
                'fetch_format': 'auto',
                'width': 800,
                'height': 600,
                'crop': 'limit'
            }
        }
    )
    
    class Meta:
        model = ListingImage
        fields = ['image', 'is_primary']
        widgets = {
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'is-primary-checkbox'
            })
        }

# Updated FormSet
ListingImageFormSet = inlineformset_factory(
    Listing,
    ListingImage,
    form=ListingImageForm,
    fields=('image', 'is_primary'),
    extra=1,
    can_delete=True,
    widgets={
        'is_primary': forms.CheckboxInput(attrs={
            'class': 'is-primary-checkbox'
        })
    }
)

class ListingSearchForm(forms.Form):
    search = forms.CharField(max_length=200, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(), required=False)
    condition = forms.ChoiceField(choices=[('', 'Any')] + Listing.CONDITION_CHOICES, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    sort_by = forms.ChoiceField(choices=[
        ('newest', 'Newest First'),
        ('oldest', 'Oldest First'),
        ('price_low', 'Price: Low to High'),
        ('price_high', 'Price: High to Low'),
    ], required=False)