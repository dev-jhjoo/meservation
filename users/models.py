import uuid
from django.db import models 
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    # 유저 생성
    def create_user(self, nickname, email, password, first_name=None, last_name=None, description=None):
        if not email:
            raise ValueError("email은 필수입니다.")
        if not nickname:
            raise ValueError("nickname은 필수입니다.")
        if not password:
            raise ValueError("password는 필수입니다.")

        user = self.model(
            nickname=nickname,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            description=description,
        )

        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)

        return user

    # 슈퍼유저 생성
    def create_superuser(self, nickname, email, password):
        user = self.create_user(
            nickname=nickname,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    nickname_validator = UnicodeUsernameValidator()

    id = models.AutoField(_("id"), primary_key=True)

    uuid = models.UUIDField(_("UUID"), default=uuid.uuid4, editable=False, unique=True)
    nickname = models.CharField(_("nickname"), max_length=50, validators=[nickname_validator], unique=True)
    
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
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    class Meta:
        # db 테이블명 지정
        db_table = "users"

    
    def clean(self):
        super().clean()
        # 이메일 정규화 로직
        self.__class__.objects.normalize_email(self.email)

