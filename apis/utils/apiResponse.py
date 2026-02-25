from urllib.parse import urlencode
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models.deletion import ProtectedError
from django.db import IntegrityError
from django.db.models.fields.files import FieldFile

from rest_framework.response import Response
from rest_framework.exceptions import ErrorDetail

def api_success(results, status=200, message="Operation successful"):
    if results is None:
        results = {}
    data = {'success': True, "message": message}
    if "results" in results:
        data.update(results)
    else:
        data["results"] = results

    return Response(data, status=status)


def api_error(data, status=400, message="Something went wrong!"):
    if data is None:
        data = {}

    if not isinstance(data, dict):
        data = {'results': data}
    data['success'] = False
    data["message"] = message
    return Response(data, status=status)

   
   
def response_create(results, status=201, message="Successfully created.", item_name=None):
    if results is None:
        results = {}
        
    if item_name != None:
        message=''
        message=f"{item_name.capitalize()} created successfully."
        
    data = {'success': True, "message": message}
    if "results" in results:
        data.update(results)
    else:
        data["results"] = results

    return Response(data, status=status)



def response_list(results=None, status=200, message="Successfully retrieved list.", item_name=None):

    if results is None:
        results = []
        
    if item_name:
        message = f"{item_name.capitalize()} list retrieved successfully."
        
    data = {'success': True, 'message': message}
    
    # Handle both direct results and pre-formatted {'results': [...]}
    if isinstance(results, dict) and 'results' in results:
        data.update(results)
    else:
        data['results'] = results
        
    return Response(data, status=status)



def response_update(results=None, status=200, message="Successfully updated.", item_name=None, serializer=None):
    
    if results is None:
        results = {}
        
    # Get updated fields from serializer if available
    updated_fields = []
    if serializer is not None and hasattr(serializer, 'validated_data'):
        updated_fields = list(serializer.validated_data.keys())
    
    if item_name:
        message = f"{item_name.capitalize()} updated successfully."
    
    data = {
        'success': True,
        'message': message,
        'results': results
    }
    
    if len(updated_fields) !=0:
        data['updated_fields'] = updated_fields

    return Response(data, status=status)



def response_details(results, status=200, message="Successfully retrieved.", item_name=None):
    if item_name:
        message = f"{item_name.capitalize()} details retrieved successfully."
        
    data = {'success': True, 'message': message}
    if isinstance(results, dict) and 'results' in results:
        data.update(results)
    else:
        data['results'] = results
        
    return Response(data, status=status)


def response_delete(item=None, item_name=None, status=200, message="Successfully deleted.", request=None):
    if item_name:
        message = f"{item_name.capitalize()} deleted successfully."
    
    response_data = {
        'success': True,
        'message': message,
    }
    
    ## Get all model fields dynamically
    if item is not None:
        # deleted_data = {
        #     field.name: getattr(item, field.name)
        #     for field in item._meta.fields
        #     if field.name not in ['password', 'secret_key']  # Exclude sensitive fields
        # }
        
        deleted_data = {}
        for field in item._meta.fields:
            if field.name in ['password', 'secret_key']:
                continue
            
            value = getattr(item, field.name)
            
            # Handle FileField/ImageField
            if isinstance(value, FieldFile):
                deleted_data[field.name] = value.name if value else None  # File path or None
            # Handle ForeignKey
            elif hasattr(value, 'id'):
                deleted_data[field.name] = value.id
            # Handle other fields
            else:
                deleted_data[field.name] = value
        
        # Add audit info
        deleted_data.update({
            'deleted_at': timezone.now().isoformat(),
            'deleted_by': request.user.name if request else None
        })
        
        ## Use dynamic key based on model name
        # if item_name != None:
        #     response_data[f'deleted_{item_name.lower()}'] = deleted_data
        # else:
        #     response_data[f'deleted_info'] = deleted_data
        
        response_data[f'deleted_info'] = deleted_data
    
    return Response(response_data, status=status)



def response_error(error, status=400, message="Something went wrong!"):
    if error is None or error == '':
        error = message

    ##? Handle ProtectedError
    if isinstance(error, ProtectedError):
        # protected_objects = list(error.protected_objects)
        # references = [str(obj) for obj in protected_objects]
        
        """
        Example:
        {
            "success": false,
            "message": "Something went wrong!",
            "error": {
                "message": "ProtectedError",
                "referenced_by": ["Related Object 1", "Related Object 2"],
                "count": 2
            }
        }
        """
        data = {
            "success": False,
            "message": message,
            "error": {
                "message": "ProtectedError",
                # "referenced_by": references,
                # "count": len(references)
            }
        }
    
    ##? Handle IntegrityError (database errors: unique constraint violations)
    elif isinstance(error, IntegrityError):
        """
        Example:
        {
            "success": false,
            "message": "Something went wrong!",
            "error": {
                "message": "IntegrityError",
                "details": "CHECK constraint failed: myapp_mymodel"
            }
        }
        """
        data = {
            "success": False,
            "message": message,
            "error": {
                "message": "IntegrityError",
                "details": str(error)
            }
        }
    
    ##? Handle general exceptions
    elif isinstance(error, Exception):
        """
        Example:
        {
            "success": false,
            "message": "Something went wrong!",
            "error": {
                "message": "Some general error occurred.",
                "details": "An unexpected error occurred"
            }
        }
        """
        data = {
            "success": False,
            "message": message,
            "error": {
                "message": str(error),
                "details": "An unexpected error occurred"
            }
        }
    
    ##? Handle list of errors
    elif isinstance(error, list):
        """
        Example:
        {
            "success": false,
            "message": "Something went wrong!",
            "errors": [
                "Error 1 description",
                "Error 2 description"
            ]
        }
        """
        data = {
            "success": False,
            "message": message,
            "errors": error
        }
    
    ##? Handle dictionary (single error or more structured details)
    elif isinstance(error, dict):
        data = {
            "success": False,
            "message": message,
            "error": error
        }
    
    ##? Handle string error
    else:
        """
        Example:
        {
            "success": false,
            "message": "Something went wrong!",
            "error": {
                "message": "A general error occurred."
            }
        }
        """
        data = {
            "success": False,
            "message": message,
            "error": {"message": error}
        }

    return Response(data, status=status)



def response_permission_denied(required_permission=[], status=403, message="You do not have permission to perform this action."):
    data = {
        'success' : False,
        'message' : message,
        'error'   : {
            'message': 'Permission Denied'
        },
        'required_permission': required_permission
    }
    return Response(data, status=status)