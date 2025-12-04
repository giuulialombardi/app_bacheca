import datetime
import json

import tornado.escape
from bson import ObjectId
from db import messages
from auth import BaseHandler


class MessageHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        cursor = messages.find({})
        out = []

        async for t in cursor:
            author = t["author"]
            try:
                if isinstance(author, str) and author.startswith("{"):
                    author_obj = json.loads(author)
                    email = author_obj.get("email", author)
                else:
                    email = author
            except:
                email = author
            out.append({
                "id": str(t["_id"]),
                "text": t["text"],
                "author": email,
                "created_at": t["created"]
            })

        return self.write_json({"items": out})

    async def post(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        body = tornado.escape.json_decode(self.request.body)
        text = body.get("text", "").strip()

        if not text:
            return self.write_json({"error": "Testo obbligatorio"}, 400)

        email = (self.get_secure_cookie("user")).decode("utf-8")
        result = await messages.insert_one({
            "user_id": ObjectId(user["id"]),
            "text": text,
            "created": datetime.datetime.now().isoformat(),
            "author": email
        })

        return self.write_json({"id": str(result.inserted_id)}, 201)

class MessageDeleteHandler(BaseHandler):
    async def delete(self, task_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        await messages.delete_one({
            "_id": ObjectId(task_id),
            "user_id": ObjectId(user["id"])
        })

        return self.write_json({"message": "Eliminato"})