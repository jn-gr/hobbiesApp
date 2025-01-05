from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Hobby(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    # Prevents hobbies from being split up into single-letters.
    def save(self, *args, **kwargs):
        if len(self.name.strip()) < 2:
            raise ValueError("Hobby must be at least two characters long.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Allows the existence of a superuser within the admin panel.
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    friends = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="friends_set")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def add_friend(self, user):
        """Add a user to the friends list."""
        if user != self:
            self.friends.add(user)

    def remove_friend(self, user):
        """Remove a user from the friends list."""
        self.friends.remove(user)

    def is_friend(self, user):
        """Check if a user is a friend."""
        return self.friends.filter(id=user.id).exists()

    def get_sent_requests(self):
        """Get all friend requests sent by this user."""
        return self.sent_requests.filter(status="pending")

    def get_received_requests(self):
        """Get all friend requests received by this user."""
        return self.received_requests.filter(status="pending")


class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def accept(self):
        """Accept the friend request and establish the friendship."""
        self.status = "accepted"
        self.save()
        self.from_user.add_friend(self.to_user)
        self.to_user.add_friend(self.from_user)

    def reject(self):
        """Reject the friend request."""
        self.status = "rejected"
        self.save()

    def __str__(self):
        return f"Friend Request from {self.from_user} to {self.to_user} ({self.status})"