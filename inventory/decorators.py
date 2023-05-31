# from django.contrib.auth.decorators import user_passes_test

# # This decorator checks if the user is active and a staff member before allowing access to the view.
# def staff_required(view_func):
#     decorated_view_func = user_passes_test(lambda user: user.is_active and user.is_staff)
#     return decorated_view_func(view_func)