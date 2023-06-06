from typing import Any
from django.views import View
from .models import Contact
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q


@method_decorator(csrf_exempt, name='dispatch')
class ContactView(View):

    def __init__(self, **kwargs: Any) -> None:
        self.response = {}
    
    def get_response(self, contacts_objs, secondary_contact):
        result = dict()
        secondaryContactIds = []
        primary_contactId = contacts_objs.first().pk

        emails = [each_contact_obj.email for each_contact_obj in contacts_objs]
        emails.append(secondary_contact.email)
        phoneNumber = [each_contact_obj.phoneNumber for each_contact_obj in contacts_objs]
        phoneNumber.append(secondary_contact.phoneNumber)
        secondary_contacts = [each_contact_obj for each_contact_obj in contacts_objs if each_contact_obj.linkPrecedence == 'secondary']
        if secondary_contacts:
            secondaryContactIds = [ each_secondary.pk for each_secondary in  secondary_contacts]
        secondaryContactIds.append(secondary_contact.pk)
        result['contact'] = {}
        result['contact']['primary_contactId'] = primary_contactId
        result['contact']['email'] = emails
        result['contact']['phoneNumber'] = phoneNumber
        result['contact']['secondaryContactIds'] = secondaryContactIds
        return result

    def post(self, request):
        try:
            params = json.loads(request.body)
            email = params.get("email")
            phone = params.get("phoneNumber")
            import pdb;pdb.set_trace()
            contact_objs  = Contact.objects.filter(Q(phoneNumber=phone) | Q(email=email))

            if not contact_objs: # primary contact
                primary_contact = Contact.objects.create(phoneNumber=phone, email=email) # primary item creation
                self.response['contact'] = {}
                self.response['contact']['primary_contactId'] = primary_contact.pk
                self.response['contact']['email'] = primary_contact.email
                self.response['contact']['phoneNumber'] = primary_contact.phoneNumber
                self.response['contact']['secondaryContactIds'] = []
            else:
                primary_contact = contact_objs.first()
                secondary_contact = Contact.objects.create(phoneNumber=phone, email=email,\
                                              linkedId=primary_contact, linkPrecedence='secondary')
                self.response = self.get_response(contact_objs, secondary_contact)
        

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        return JsonResponse(self.response, safe=False)
