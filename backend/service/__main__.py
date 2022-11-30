import asyncio
import json
import logging

import tornado.web

from service.schema import UserInput  # isort: skip
from service.send import send_to_que  # isort: skip

logger = logging.getLogger(__name__)


def phone_validator(phone):
    phone = phone.replace("+7", "8")
    for ch in ["(", ")", "-", " "]:
        phone = phone.replace(ch, "")
    if not phone.isdigit():
        return ""
    if len(phone) > 15:
        return ""
    return phone


class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Content-type", "application/json")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def options(self):
        pass

    def filter(self, message):
        message["phone"] = phone_validator(message["phone"])
        if not message["phone"] or not message["name"] or not message["surname"]:
            raise tornado.web.HTTPError(status_code=422, log_message="wrong input")
        try:
            UserInput(**message)
        except Exception as exc:
            logger(exc)
            logger.error("wrong user input validation")
            raise tornado.web.HTTPError(
                status_code=422, log_message="wrong input"
            ) from exc
        return message

    def post(self):
        data = self.request.body
        message = json.loads(data)
        message = self.filter(message)
        message = json.dumps(message)
        logger.info("try to send ")
        print("message", message)
        send_to_que(message)
        self.write(data)


async def main():
    application = tornado.web.Application([(r"/", MainHandler)])
    application.listen(80)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
