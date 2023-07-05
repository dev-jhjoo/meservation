import uuid
from django.db import models 
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    # 유저 생성
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("email은 필수입니다.")
        if not username:
            raise ValueError("username은 필수입니다.")
        if not password:
            raise ValueError("password는 필수입니다.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)

        return user

    # 슈퍼유저 생성
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    id = models.AutoField(_("id"), primary_key=True)

    uuid = models.UUIDField(_("UUID"), default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(_("username"), max_length=50, validators=[username_validator], unique=True)
    
    first_name = models.CharField(_("first name"), max_length=50, blank=True)
    last_name = models.CharField(_("last name"), max_length=50, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    description = models.TextField(_("description"), max_length=50, blank=True)

    is_staff = models.BooleanField(_("staff status"), default=False)

    create_at = models.DateTimeField(_("create_at"), auto_now_add=True)
    update_at = models.DateTimeField(_("update_at"), auto_now=True)
    last_login_at = models.DateTimeField(_("last login"), auto_now=True)

    deleted_at = models.BooleanField(_("deleted at"), default=False)

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    # 관리자 페이지에 표시될 이름
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    # 이메일 정규화 로직
    def clean(self):
        super().clean()
        self.__class__.objects.normalize_email(self.email)

