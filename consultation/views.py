from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ConsultationForm
from django.conf import settings
from django.contrib import messages
from .models import Consultation
import stripe
from profiles.models import UserProfile
from profiles.forms import UserProfileForm


@require_POST
def cache_consultation_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


@login_required
def consultation(request):

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'consultation_idea': request.POST['consultation_idea'],
            'consultation_number': Consultation.consultation_number,
            'date': Consultation.date
        }

        consultation_form = ConsultationForm(form_data)

        if consultation_form.is_valid():
            consultation = consultation_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            consultation.stripe_pid = pid
            consultation.save()
            return redirect(reverse('consultation_success',
                                    args=[consultation.consultation_number]))
        else:
            messages.error(request, 'There was an error with your form.')
    else:
        stripe_total = (30 * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            consultation_form = ConsultationForm(initial={
                'first_name': profile.default_first_name,
                'last_name': profile.default_last_name,
                'email': profile.default_email,
                'phone_number': profile.default_phone_number,
            })
        except UserProfile.DoesNotExist:
            consultation_form = ConsultationForm()
    else:
        consultation_form = ConsultationForm()

    template = 'consultation/consultation.html'
    context = {
        'consultation_form': consultation_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def consultation_success(request, consultation_number):

    consultation = get_object_or_404(Consultation,
                              consultation_number=consultation_number)

    if request.user.is_authenticated:

        profile = UserProfile.objects.get(user=request.user)
        consultation.user_profile = profile
        consultation.save()

    profile_info = {
        'default_first_name': consultation.first_name,
        'default_last_name': consultation.last_name,
        'default_phone_number': consultation.phone_number,
        'default_email': consultation.email,
    }

    user_profile_form = UserProfileForm(profile_info, instance=profile)

    if user_profile_form.is_valid():
        user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {consultation_number}.')
        
    template = 'consultation/consultation_success.html'
    context = {
        'consultation': consultation,
        'from_profile': False,
        'from_admin': False,
    }

    return render(request, template, context)
