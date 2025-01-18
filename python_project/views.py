from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import database
from rest_framework import status
import re
import os

def myapp(request): 
    return render(request, 'main.html')


@api_view(['GET', 'POST'])
def getData(request) :
    if request.method == 'GET':
        data = database.radius
        return Response(data)
        
    elif request.method == 'POST':

        app_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(app_dir, 'database.py') 
        
        field = next(iter(request.data))
        value = request.data[field]         

        
        with open(db_path,'r') as file:
                content = file.read()

            # Create the pattern to match the specific field in the radius dictionary
        pattern = fr'"{field}"\s*:\s*"[^"]*"'
        replacement = f'"{field}": "{value}"'

            # Replace the old value with new value
        new_content = re.sub(pattern, replacement, content)

            # Write back to the file
        with open(db_path, 'w') as file:
            file.write(new_content) 
        return Response(database.radius, status=status.HTTP_201_CREATED)


