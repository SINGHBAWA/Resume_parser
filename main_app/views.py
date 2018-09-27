from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from main_app.utils.drive_api import GoogleDrive
from main_app.utils.ip_location_utils import get_ip_address, get_city, get_location
from main_app.utils.sf_api import SFConnectAPI
from main_app.utils.drive_utils import get_folder_id
import re

gd_instance = GoogleDrive()
sf_instance = SFConnectAPI()


def home(request):
    print('redirecting')
    return render(request, "application_form.html", {'designations': ['', 'Developer', 'Consultant']})


def upload_details(request):
    print("uploading details")
    try:
        if request.method == 'POST':
            name = str(request.POST.get("Name")).strip()
            email = request.POST.get("Email__c")
            contact = request.POST.get("Contact_Number__c")
            designation = request.POST.get("Designation__c")
            resume = request.FILES["resumeFile"]

            if not name or name == "" or not bool( re.match( '^[a-zA-Z ]+$', name ) ):
                messages.error(request, "Error: Name field must contains only Characters")
                return HttpResponseRedirect('/home/')

            if not re.match('^[0-9]+$', contact):
                messages.error(request, "Error: Phone field must contains only Numbers" )
                return HttpResponseRedirect( '/home/' )


            # Uploading the file in salesforce
            file_name = name + " | " + contact + " | " + email
            folder_id = get_folder_id(designation)

            file_id, file_url = gd_instance.upload_file(file_name, media=resume, folder_id=folder_id)

            ip_address = get_ip_address()
            if not ip_address or ip_address == '127.0.0.1':
                ip_address = '116.75.226.225'

            location = get_location(ip_address)
            city = get_city(ip_address)

            sf_instance.create_record(object_name='Resume_Google_Drive_Link__c',
                                      data={'Name__c': name,
                                            'Contact_Number__c': contact,
                                            'Email__c': email,
                                            'Google_Drive_URL__c': file_url,
                                            'Position__c': designation,
                                            'Address__latitude__s': location[1],
                                            'Address__longitude__s': location[0],
                                            'City__c': city,
                                            })

            messages.success( request, 'You have applied successfully !!!' )
    except Exception as ex:
        print("Exception:"+ repr(ex))
        messages.error( request, 'Unable to process request.. try again later !!!' )
    return HttpResponseRedirect('/home/')