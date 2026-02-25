
## Django Rest Framework
REST_FRAMEWORK = {

    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        ##! JWT Authentication
        ## এটা আমারা ব্যবহার করবো কারণ আমরা Password change এর পরে পুরানো token গুলোকে blacklist করতে চাইছি।
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        
        ## Custom Password Aware JWT Authentication এতে আমরা token issue time এবং password changed time এর ভিত্তিতে token এর বৈধতা যাচাই করতে পারবো।
        'apis.utils.token.PasswordAwareJWTAuthentication',
        
        ##! Keep SessionAuthentication if you need the browsable API
        'rest_framework.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'config.exceptions.custom_exception_handler',

    # 'DEFAULT_FILTER_BACKENDS': [
    #         'django_filters.rest_framework.DjangoFilterBackend'
    #     ],

}