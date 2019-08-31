#! /usr/bin/env python

import sys
import asyncio
import argparse
import ssl

import irc.client
import irc.client_aio


class NotifyIRC(irc.client_aio.AioSimpleIRCClient):
    def __init__(self, channel, channel_key, message, use_notice=False):
        super().__init__()
        self.channel = channel if channel.startswith("#") else f"#{channel}"
        self.channel_key = channel_key
        self.message = message
        self.use_notice = use_notice

    def on_welcome(self, connection, event):
        connection.join(self.channel, self.channel_key)

    def on_join(self, connection, event):
        command = connection.notice if self.use_notice else connection.privmsg
        for message in self.message.splitlines():
            command(self.channel, message)
        connection.part([self.channel])
        connection.quit()

    def on_quit(self, connection, event):
        sys.exit(0)

    def on_disconnect(self, connection, event):
        sys.exit(1)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default="chat.freenode.net")
    parser.add_argument("-p", "--port", default=6667, type=int)
    parser.add_argument("--nickname", default="github-notify")
    parser.add_argument("--password", default=None, help="Optional nickname password")
    parser.add_argument("--channel", required=True, help="IRC #channel")
    parser.add_argument("--channel-key", help="IRC #channel password")
    parser.add_argument("--ssl", action="store_true")
    parser.add_argument(
        "--notice", action="store_true", help="Use NOTICE instead if PRIVMSG"
    )
    parser.add_argument("--message", required=True)
    return parser.parse_args()


def main():
    args = get_args()

    client = NotifyIRC(
        args.channel, args.channel_key or None, args.message, args.notice
    )

    client.connect(
        args.server,
        args.port,
        args.nickname,
        password=args.password or None,
        connect_factory=irc.connection.AioFactory(ssl=args.ssl),
    )

    client.start()


if __name__ == "__main__":
    main()
