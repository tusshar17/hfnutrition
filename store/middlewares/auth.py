from django.shortcuts import redirect

def auth_middleware(get_response):

    def middleware(request):

        print(request.META['PATH_INFO'])
        returnURL = request.META['PATH_INFO']
        if not (request.session.get('customer_email') or request.session.get('customer_phone')):
            return redirect(f'signup-login?return_url={returnURL}')

        response = get_response(request)
        return response
    
    return middleware