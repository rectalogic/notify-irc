# Send Notification Message to IRC

### Usage

See [action.yml](./action.yml) For comprehensive list of options.
 
Example, send notifications to Libera Chat IRC channel:

```yaml
name: "Push Notification"
on: [push, pull_request, create]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: irc push
        uses: rectalogic/notify-irc@v1
        if: github.event_name == 'push'
        with:
          channel: "#mychannel"
          nickname: my-github-notifier
          message: |
            ${{ github.actor }} pushed ${{ github.event.ref }} ${{ github.event.compare }}
            ${{ join(github.event.commits.*.message) }}
      - name: irc pull request
        uses: rectalogic/notify-irc@v1
        if: github.event_name == 'pull_request'
        with:
          channel: "#mychannel"
          nickname: my-github-notifier
          message: |
            ${{ github.actor }} opened PR ${{ github.event.html_url }}
      - name: irc tag created
        uses: rectalogic/notify-irc@v1
        if: github.event_name == 'create' && github.event.ref_type == 'tag'
        with:
          channel: "#mychannel"
          nickname: my-github-notifier
          message: |
            ${{ github.actor }} tagged ${{ github.repository }} ${{ github.event.ref }}
```
