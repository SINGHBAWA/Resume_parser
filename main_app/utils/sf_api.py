"""
    SALESFORCE API MODULE
"""
import http.client
from simple_salesforce import Salesforce, SFType
from simple_salesforce import SalesforceLogin
from main_app.Constants.sf_config import ConnectionString


class SFConnectAPI:
    """
        SALESFORCE API CLASS
    """
    sf = None
    sf_bulk = None

    def __init__(self, sf_config=ConnectionString):
        """
        :param sf_config:
        """
        print("connecting with salesforce.")
        # self.sf = Salesforce(username=sf_config.USERNAME,
        #                      password=sf_config.PASSWORD,
        #                      sandbox=True)
        # security_token=sf_config.SF_AUTH_TOKEN)
        try:
            self.sf = Salesforce(instance=sf_config.SF_URL,
                                 session_id=sf_config.ACCESS_TOKEN,
                                 sandbox=True)
        except:
            sf_config.ACCESS_TOKEN = self.get_access_token()
            self.sf = Salesforce(instance=sf_config.SF_URL,
                                 session_id=sf_config.ACCESS_TOKEN,
                                 sandbox=True)

        self.sf_config = sf_config
        print("connection success")

    def get_header(self, session_id):
        """
        :return:
        """
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + session_id,
            'X-PrettyPrint': '1'
        }

    def get_access_token(self):
        """
        :return:
        """
        data = {'client_secret': ConnectionString.CLIENT_SECRET,
                'username': ConnectionString.USERNAME,
                'password': ConnectionString.PASSWORD,
                'client_id': ConnectionString.CONSUMER_KEY,
                'redirect_uri': ConnectionString.REDIRECT_URI}
        import requests
        service = requests.post("https://test.salesforce.com/services/oauth2/token?grant_type=password", data=data)
        print(service.json())
        return service.json().get("access_token")

    def execute_soql(self, query):
        """
        :param sf_conn:
        :param query:
        :param host:
        :return:
        """

        result = self.sf.query(query)
        return result

    def create_record(self, object_name=None, data=None):
        # session_id = self.get_login_connection()
        session_id = ConnectionString.ACCESS_TOKEN
        try:
            sf_obj = SFType(object_name, session_id, self.sf_config.SF_URL)
            result = sf_obj.create(data)
        except Exception as ex:
            result = ex
            print(repr(ex))
        return result

    def update_record(self, record_id=None, object_name=None, data=None):
        session_id = ConnectionString.ACCESS_TOKEN
        try:
            sf_obj = SFType( object_name, session_id, self.sf_config.SF_URL )
            result = sf_obj.update(record_id, data)
        except Exception as ex:
            result = ex
            print(repr(ex))
        return result



# import datetime
# from datetime import timedelta
# # sf = SFConnectAPI()
# #
# # query = "select id from Contact limit 10"
# # print(str(sf.get_access_token()))
# # username = "amansinghbawa"
# # password = "7800100291"
# sf_instance = SFConnectAPI()
# emp = sf_instance.execute_soql("select id,Name from Attendance__c where date__c >={start_date} " \
#                                "AND date__c <={end_date}".format(start_date=datetime.date.today(),
#                                                                end_date=datetime.date.today() + timedelta(days=5) ))
# print(repr(emp['records']))

# import requests
#
# params = {
#     "grant_type": "password",
#     "client_id": ConnectionString.CONSUMER_KEY,  # Consumer Key
#     "client_secret": ConnectionString.CLIENT_SECRET,  # Consumer Secret
#     # "username": ConnectionString.USERNAME,  # The email you use to login
#     # "password": ConnectionString.PASSWORD,
#     "redirect_uri": "https://www.google.com"
# # Concat your password and your security token
# }
# r = requests.post("https://login.salesforce.com/services/oauth2/token", params=params)
# print(repr(r))
# access_token = r.json().get("access_token")
# instance_url = r.json().get("instance_url")
# print("Access Token:", access_token)
# print("Instance URL", instance_url)

# # access_token = '00D7F0000048jEa!ARcAQDqX99zhupkuv8RzVXYjEP7d_ZtcNQrMM2rK1O76mSvUt.UJF8ldlRzThVN3xXRmAjLzvC8yGZKUN7XBCK2aijl7t1ns'
#
# from simple_salesforce import Salesforce
# sf = Salesforce(instance='ap5.salesforce.com', session_id=access_token)
# result = sf.query("select id from Attendance__c")
# print(repr(result))<class 'tuple'>:
# sf_instance = SFConnectAPI()
# location = (77.2167, 28.6667)
# sf_instance.create_record( object_name='Resume_Google_Drive_Link__c',
#                            data={'Name__c': 'TEST RECORD 1',
#                                  'Contact_Number__c': '9936556447',
#                                  'Email__c': 'sdfffg@gmail.com',
#                                  'Google_Drive_URL__c': 'https://drive.google.com/file/d/1Stu3UScJ6uy8V9zGa1rqVAGxNehlry6c/view',
#                                  'Position__c': 'Developer',
#                                  'Address__latitude__s': location[1],
#                                  'Address__longitude__s': location[0],
#                                  'City__c': 'Delhi',
#                                  } )
# conn = Salesforce(username=ConnectionString.USERNAME,
#                   password=ConnectionString.PASSWORD,
#                   sandbox=True)

# print(repr(conn))

# import requests
#
# data = {'client_secret': ConnectionString.CLIENT_SECRET,
#         'client_id': ConnectionString.CONSUMER_KEY,
#         'redirect_uri': ConnectionString.REDIRECT_URI}
# result = requests.post(' https://test.salesforce.com/services/oauth2/authorize?response_type=code', data=data)
# print(result.json())