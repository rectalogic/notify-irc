#!/bin/sh

if [ "$INPUT_SSL" == "true" ]; then
    ARG_SSL="--ssl"
else
    ARG_SSL=""
fi
if [ "$INPUT_NOTICE" == "true" ]; then
    ARG_NOTICE="--notice"
else
    ARG_NOTICE=""
fi

exec /notify_irc.py \
    --server "$INPUT_SERVER" \
    --port "$INPUT_PORT" \
    --nickname "$INPUT_NICKNAME" \
    --password "$INPUT_PASSWORD" \
    --channel "$INPUT_CHANNEL" \
    --channel-key "$INPUT_CHANNEL_KEY" \
    --message "$INPUT_MESSAGE" \
    $ARG_SSL $ARG_NOTICE
