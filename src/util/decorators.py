#coding=UTF-8

'''
                                        DECORATORS
'''

import functools 
from django.http import HttpRequest

def check_is_not_logged(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request = None
            for x in args:
                if isinstance(x, HttpRequest):
                    request = x
                    break
            if not request:
                for k in kwargs:
                    if isinstance(kwargs[k], HttpRequest):
                        request = kwargs[k]
                        break 
            
            if request.session.has_key('type'): #Is Logged
                return request.redirect_to('/user') 
            else:
                return func(*args, **kwargs)
                
        return wrapper

def check_is_logged(value):
    ''' 
         0 - Users
         1 - Doctors and Attendants and Dentists
    '''
    def factory(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request = None
            for x in args:
                if isinstance(x, HttpRequest):
                    request = x
                    break
            if not request:
                for k in kwargs:
                    if isinstance(kwargs[k], HttpRequest):
                        request = kwargs[k]
                        break 
            
            type = request.session.get('type', None)
            
            if type:
                return func(*args, **kwargs)
            else:
                if value == 0:
                    request.session['scheduling'] = '/scheduling?' + str(request.META['QUERY_STRING'])
                    return request.render('user/log\ in\ or\ registexr.xhtml', {}, request)
                elif value == 1:
                    return request.render('base/login.xhtml', {}, request)
        return wrapper   
    return factory

def check_is_some_roles(func, roles, error_message):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        request = None
        for x in args:
            if isinstance(x, HttpRequest):
                request = x
                break
        if not request:
            for k in kwargs:
                if isinstance(kwargs[k], HttpRequest):
                    request = kwargs[k]
                    break 
        
        type = request.session.get('type')
        if type in roles:
            return func(*args, **kwargs)
        else:
            d = {}
            d['confirmation'] = {
                 'status'  : 'OK',
                 'title'   : 'There was an error',
                 'message' : error_message
                 }
            return request.render('base/error.xhtml', d, request)
    return new_func

#def check_is_user(func):
#    return check_is_some_roles(func, [login_control.LOGIN_TYPE_USER], 'Sorry, you're not logged in.')
#
#def check_is_doctor(func):
##    return check_is_some_roles(func, [login_control.LOGIN_TYPE_DOCTOR], 'Sorry, you're not logged in.')            
#    return check_is_some_roles(func, [login_control.LOGIN_TYPE_DENTIST], 'Sorry, you're not logged in.')            
#
#def check_is_attendant(func):
#    return check_is_some_roles(func, [login_control.LOGIN_TYPE_ATTENDANT], 'Sorry, you're not logged in.')
#
#def check_is_attendant_or_doctor(func):
#    return check_is_some_roles(func, [login_control.LOGIN_TYPE_ATTENDANT, login_control.LOGIN_TYPE_DOCTOR, login_control.LOGIN_TYPE_DENTIST], 'Sorry, only dentists and caregivers have access to this page.')

