import jwt
from django.conf import settings


class OnlyOfficeConfig:

    @staticmethod
    def get_config(document, user):

        config = {

            "document": {

                "fileType": document["fileType"],

                "key": document["key"],

                "title": document["title"],

                "url": document["url"],

            },

            "documentType": "word",

            "editorConfig": {

                "mode": "edit",

                "lang": "en",

                "callbackUrl": document["callback"],

                "user": {

                    "id": str(user.id),

                    "name": user.get_full_name() or user.username,

                },

                "customization": {

                    "autosave": True,

                    "forcesave": True,

                    "comments": True,

                    "chat": False,

                    "compactToolbar": False,

                    "toolbarNoTabs": False,

                    "trackChanges": False,

                },

            },

            "permissions": {

                "edit": True,

                "download": True,

                "print": True,

                "copy": True,

                "comment": True,

                "review": True,

                "fillForms": True,

            },

        }

        token = jwt.encode(
            config,
            settings.ONLYOFFICE_JWT_SECRET,
            algorithm="HS256",
        )

        if isinstance(token, bytes):
            token = token.decode("utf-8")

        # IMPORTANT: Include the token inside the config
        config["token"] = token

        return {

            "documentServerUrl": settings.ONLYOFFICE_DOCUMENT_SERVER,

            "config": config,

        }