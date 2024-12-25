

class Cart():
    def __init__(self,request):
        self.session = request.session

        #for getting the current session key
        cart = self.session.get('session_key')


        #creating new session for new user
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #for ensuring this works in all pages
        self.cart = cart