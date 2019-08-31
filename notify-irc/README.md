# Send Notification Message to IRC

### Usage

See [action.yml](./action.yml) For comprehensive list of options.
 
Example, send compare url to freenode IRC:
```yaml
name: "Push Notification"
on: push

jobs:
  irc:
    runs-on: ubuntu-latest
    steps:
      - uses: rectalogic/actions/notify-irc@v1
        with:
            channel: "#mychannel"
            nickname: my-github-notifier
            message: Push commits ${{ github.event.compare }}
```