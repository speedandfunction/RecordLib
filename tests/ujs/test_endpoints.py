import pytest
from rest_framework.response import Response

def test_search_ujs_by_name_missing_data(admin_client):
    resp = admin_client.post('/ujs/search/name/', follow=True)
    assert resp.status_code == 400
    assert resp.data['errors']['first_name'][0].code == 'required'


def test_search_ujs_by_name(admin_client, monkeypatch):

    def mockresponse(url, data, follow):
        return(
            Response({
                'searchResults': {
                    'CP': {
                        'dockets': [
                            {
                                'caption': 'Comm. v. Smith, J.', 
                                'case_status': 'Active', 
                                'dob': '1/1/2000',
                                'docket_number': 'CP-12345',
                                'docket_sheet_url': 'https://ujsportal.pacourts.us.gov/lalala',
                                'otn':'1234',
                                'summary_url': 'https://ujsportal.pacourts.us.gov/bababa',
                            },
                        ],  
                        'msg': "Success",
                    },
                    'MDJ': {
                        'dockets': [],
                        'msg': "    Search completed. No dockets found."
                    }
                }, 
            },
            200
        )
    )
        

    monkeypatch.setattr(admin_client, 'post', mockresponse)

    resp = admin_client.post(
        '/ujs/search/name/', 
        data={
            "first_name":"Jane",
            "last_name":"Smith",
        },
        follow=True)
    assert resp.status_code == 200
    assert all( [ court in resp.data['searchResults'].keys() for court in ["CP", "MDJ"]] )


   