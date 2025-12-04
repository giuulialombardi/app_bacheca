import asyncio
import tornado.web
import tornado.escape

from db import COOKIE_SECRET, PORT
from auth import RegisterHandler, LoginHandler, LogoutHandler
from messages import MessageHandler, MessageUpdateHandler, MessageDeleteHandler


def make_app():
    return tornado.web.Application(
        [
            (r"/api/register", RegisterHandler),
            (r"/api/login", LoginHandler),
            (r"/api/logout", LogoutHandler),

            (r"/api/tasks", MessageHandler),
            (r"/api/tasks/([a-f0-9]{24})", MessageUpdateHandler),
            (r"/api/tasks/([a-f0-9]{24})/delete", MessageDeleteHandler),

            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),

            (r"/", tornado.web.RedirectHandler, {"url": "/static/login.html"}),
        ],
        cookie_secret=COOKIE_SECRET,
        autoreload=True,
        debug=True
    )


async def main():
    app = make_app()
    app.listen(PORT)
    print(f"Server avviato su http://localhost:{PORT}")

    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer spento.")
    except Exception as e:
        print(f"Errore critico durante l'avvio del server: {e}")