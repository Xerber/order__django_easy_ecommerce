from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate, logout, get_user_model
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserAuthForm, PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from .decorators import user_not_authenticated
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.db.models.query_utils import Q
from django.utils.html import format_html

# Create your views here.
def my_account(request):
    reg_form = UserRegisterForm()
    auth_form = UserAuthForm()
    context ={
      'reg_form': reg_form,
      'auth_form': auth_form,
    }
    return render(request, 'account/my_account.html', context)


def register_view(request):
    form = UserRegisterForm()
    auth_form = UserAuthForm()
    context ={
      'reg_form': form,
      'auth_form': auth_form,
    }
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password1 = form.cleaned_data['password1']
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Пользователь с таким Email уже зарегистрирован")
                return render(request, 'account/my_account.html', context)
            new_user = form.save()
            messages.success(request, f'Привет {username}! Аккаунт был успешно создан')
            new_user = authenticate(username=username,password = password1)
            login(request, new_user)
            return redirect("shop:index")
        else:
          messages.warning(request, form.errors)
    return render(request, 'account/my_account.html', context)


def auth_view(request):
  context ={}
  if request.user.is_authenticated:
    messages.warning(request, "Вы уже авторизованы")
    return redirect("shop:index")

  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get('password')

    try:
      user = User.objects.get(username=username)
      context['user'] = user
    except:
      messages.warning(request, f"Пользователь с именем {username} не существует. Проверьте правильность ввода")
      return redirect("account:my_account")

    user = authenticate(username = username,password = password)

    if user is not None:
      login(request, user)

      if request.POST.get("rememberme"):
        request.session.set_expiry(5184000)
        request.session.modified = True

      messages.success(request, "Авторизация успешна")
      return redirect("shop:index")
    else:
      messages.warning(request, "Авторизация неуспешна. Проверьте правильность ввода пароля")
      return redirect("account:my_account")
  form = UserAuthForm()
  context['auth_form'] = form
  return render(request, 'account/my_account.html', context)


def logout_view(request):
  logout(request)
  messages.success(request, 'Вы успешно вышли из своей учетной записи')
  return redirect("shop:index")


@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Запрос на сброс пароля"
                message = render_to_string("account/password_reset_mail.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        format_html("""
                        <h3>Письмо c инструкцией по сбросу пароля быо отправлено</h3><hr>
                        <p>
                            Мы отправили Вам инструкцию по сбросу пароля. 
                            Вы должны скоро его получить.<br>Если письмо не пришло - проверьте папку "Спам" или свяжитесь с нами.
                        </p>
                        """)
                    )
                else:
                    messages.warning(request, format_html("Проблема при отправке письма, <b>SERVER PROBLEM</b>"))
            else:
                messages.warning(request, "Аккаунт с указанным имейлом не найден")
                return redirect('account:password_reset')

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="account/password_reset.html", 
        context={"form": form}
        )


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, format_html("Ваш пароль был изменён. Вы можете <b> войти </b> с новый паролем"))
                return redirect('account:my_account')
            else:
                for error in list(form.errors.values()):
                    messages.warning(request, error)

        form = SetPasswordForm(user)
        return render(request, 'account/password_reset_confirm.html', {'form': form})
    else:
        messages.warning(request, "Ссылка просрочена")

    messages.warning(request, 'Внутренняя ошибка. Перенаправляем на главную страницу')
    return redirect("shop:index")