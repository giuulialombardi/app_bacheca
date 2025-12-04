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
            out.append({
                "id": str(t["_id"]),
                "text": t["text"],
                "done": t["done"]
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

        result = await messages.insert_one({
            "user_id": ObjectId(user["id"]),
            "text": text,
            "done": False
        })

        return self.write_json({"id": str(result.inserted_id)}, 201)


class MessageUpdateHandler(BaseHandler):
    async def put(self, task_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        body = tornado.escape.json_decode(self.request.body)
        done = body.get("done")

        await messages.update_one(
            {"_id": ObjectId(task_id), "user_id": ObjectId(user["id"])},
            {"$set": {"done": bool(done)}}
        )

        return self.write_json({"message": "Aggiornato"})


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