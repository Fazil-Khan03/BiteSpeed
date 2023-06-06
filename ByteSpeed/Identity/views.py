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
        
    def post(self, request):
        try:
            params = json.loads(request.body)
            email = params.get("email")
            phone = params.get("phoneNumber")
            contact_objs = None
            if email and phone:
                contact_objs = Contact.objects.filter(Q(phoneNumber=phone) | Q(email=email))
            elif email:
                 contact_objs = Contact.objects.filter(email=email)
            else:
                 contact_objs = Contact.objects.filter(phoneNumber=phone)

            if not contact_objs: # primary contact
                primary_contact = Contact.objects.create(phoneNumber=phone, email=email) # primary item creation
                self.response['contact'] = {}
                self.response['contact']['primary_contactId'] = primary_contact.pk
                self.response['contact']['email'] = primary_contact.email
                self.response['contact']['phoneNumber'] = primary_contact.phoneNumber
                self.response['contact']['secondaryContactIds'] = []
            else:
                result = dict()

                primary_contacts = contact_objs.filter(linkPrecedence='primary')
                if len(primary_contacts)>1:
                    primary_contacts.last().linkedId = primary_contacts.first()
                    primary_contacts.last().LINK_PRECEDENCE_CHOICES = Contact.SECONDARY
                    primary_contacts.last().save
                    primary_contact = primary_contacts.last()
                else:
                    primary_contact = primary_contacts.first()

                primary_phone = primary_contact.phoneNumber
                primary_email = primary_contact.email
                primary_contactId = primary_contact.pk

                secondary_contacts = contact_objs.filter(linkPrecedence='secondary')
                secondaryContactIds = [secondary_contact.pk for secondary_contact in secondary_contacts]
                emails = [each_contact_obj.email for each_contact_obj in contact_objs]
                phoneNumber = [each_contact_obj.phoneNumber for each_contact_obj in contact_objs]

                secondary_contact  = None
                if email and phone and (primary_email != email or phone != primary_phone):
                    secondary_contact = Contact.objects.create(phoneNumber=phone, email=email, linkedId=primary_contact, linkPrecedence='secondary')
                elif phone and phone != primary_phone:
                    secondary_contact = Contact.objects.create(phoneNumber=phone, email=email, linkedId=primary_contact, linkPrecedence='secondary')
                elif email and primary_email != email:
                    secondary_contact = Contact.objects.create(phoneNumber=phone, email=email, linkedId=primary_contact, linkPrecedence='secondary')

                
                if secondary_contact:
                    emails.append(email)
                    phoneNumber.append(secondary_contact.phoneNumber)
                    secondaryContactIds.append(secondary_contact.pk)

                result['contact'] = {}
                result['contact']['primary_contactId'] = primary_contactId
                result['contact']['email'] = emails
                result['contact']['phoneNumber'] = phoneNumber
                result['contact']['secondaryContactIds'] = secondaryContactIds
                self.response = result
            

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        return JsonResponse(self.response, safe=False)
