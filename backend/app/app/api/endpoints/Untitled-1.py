


# url = (
                
#             )
# get_pw = get_password(db)

# headers = {}
# payload = {}
# data = []
# response = requests.request(
#     "GET",
#     url,
#     headers=headers,
#     data=payload,
#     auth=(get_pw["username"], get_pw["password"]),
# )




from fastapi import APIRouter, Depends, Form, Request
import json, requests

# url = "http://192.168.1.214:8000/article/article_content_approve"


# headers = {}
# payload = {"token":"P8Ihs2lZTgV69YS1vA0wk82zRYP2H4",
#            "article_id":4}
# data = []

# response = requests.request(
#     "POST",
#     url,
#     headers=headers,
#     data=payload,
# )
# print(response.content)