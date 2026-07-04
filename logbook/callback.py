import json
import urllib.request

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import StudentLogbook


@csrf_exempt
def onlyoffice_callback(request, logbook_id):
    """
    Receives save notifications from ONLYOFFICE Document Server.
    """

    if request.method != "POST":
        return JsonResponse({"error": 0})

    logbook = get_object_or_404(
        StudentLogbook,
        pk=logbook_id
    )

    try:
        payload = json.loads(
            request.body.decode("utf-8")
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": 1})

    print("ONLYOFFICE CALLBACK:")
    print(payload)

    status = payload.get("status")

    # 2 = Ready for saving
    # 6 = Force Save
    if status in (2, 6):

        download_url = payload.get("url")

        if not download_url:
            return JsonResponse({"error": 1})

        try:

            with urllib.request.urlopen(download_url) as response:

                with open(
                    logbook.logbook_file.path,
                    "wb"
                ) as output:

                    output.write(response.read())

            # update timestamp
            logbook.save(update_fields=["updated_at"])

            print("Document saved successfully.")

        except Exception as e:

            print("ONLYOFFICE SAVE ERROR:", e)

            return JsonResponse({"error": 1})

    return JsonResponse({"error": 0})