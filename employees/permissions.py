from django.shortcuts import redirect

def hr_or_admin(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if user has a profile
        if not hasattr(request.user, 'userprofile'):
            return redirect('dashboard')

        role = request.user.userprofile.role

        # Allow only HR and Admin
        if role in ["admin", "hr"]:
            return view_func(request, *args, **kwargs)

        # Otherwise redirect
        return redirect('dashboard')
        
    return wrapper
