import asyncio
import json

import tornado.web
from service.send import send_to_que


class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Content-type", "application/json")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def options(self):
        pass

    def post(self):
        data = self.request.body
        send_to_que(data)
        self.write(data)


async def main():
    application = tornado.web.Application([(r"/", MainHandler)])
    application.listen(80)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
