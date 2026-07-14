from accounts.models import CustomUser


def generate_username(prefix):

    last = (
        CustomUser.objects
        .filter(username__startswith=prefix)
        .order_by("-username")
        .first()
    )

    if last:
        number = int(last.username.replace(prefix, "")) + 1
    else:
        number = 1

    return f"{prefix}{number:04d}"