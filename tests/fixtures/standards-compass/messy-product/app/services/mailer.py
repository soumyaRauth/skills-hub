import os
import requests


def send_report_email(visit):
    return requests.post(
        "https://api.mailprovider.example/v3/send",
        json={
            "to": visit.client_email,
            "subject": f"Inspection report — {visit.site_name}",
            "html": visit.report_html,
            "attachments": [p.url for p in visit.photos],
        },
        headers={"Authorization": "Bearer " + os.environ["MAIL_API_KEY"]},
    )
