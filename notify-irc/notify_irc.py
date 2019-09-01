#! /usr/bin/env python

import sys
import argparse

import pydle


class NotifyIRC(pydle.Client):
    def __init__(self, channel, channel_key, notification, use_notice=False, **kwargs):
        super().__init__(**kwargs)
        self.channel = channel if channel.startswith("#") else f"#{channel}"
        self.channel_key = channel_key
        self.notification = notification
        self.use_notice = use_notice

    async def on_connect(self):
        await super().on_connect()
        await self.join(self.channel, self.channel_key)

    async def on_join(self, channel, user):
        await super().on_join(channel, user)
        if user != self.nickname:
            return
        if self.use_notice:
            await self.notice(self.channel, self.notification)
        else:
            await self.message(self.channel, self.notification)
        await self.part(self.channel)

    async def on_part(self, channel, user, message=None):
        await super().on_part(channel, user, message)
        await self.quit()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default="chat.freenode.net")
    parser.add_argument("-p", "--port", default=6667, type=int)
    parser.add_argument("--password", default=None, help="Optional server password")
    parser.add_argument("--nickname", default="github-notify")
    parser.add_argument(
        "--sasl-password", help="Nickname password for SASL authentication"
    )
    parser.add_argument("--channel", required=True, help="IRC #channel")
    parser.add_argument("--channel-key", help="IRC #channel password")
    parser.add_argument("--tls", action="store_true")
    parser.add_argument(
        "--notice", action="store_true", help="Use NOTICE instead if PRIVMSG"
    )
    parser.add_argument("--message", required=True)
    return parser.parse_args()


def main():
    args = get_args()

    client = NotifyIRC(
        channel=args.channel,
        channel_key=args.channel_key or None,
        notification=args.message,
        use_notice=args.notice,
        nickname=args.nickname,
        sasl_username=args.nickname,
        sasl_password=args.sasl_password or None,
    )
    client.run(
        hostname=args.server,
        port=args.port,
        password=args.password or None,
        tls=args.tls,
        tls_verify=args.tls,
    )


if __name__ == "__main__":
    main()
