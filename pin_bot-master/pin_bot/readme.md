# pin_bot

## Description

For everyone can edit the pinned message in APK test group

## Additional Features:

- Can hide/show channels that are being used at the moment
- Monitor traffic on the channel code and domain name for easy tracking of links that are not used.
- Will show domain if is newly added or replaced a new link, will show in the pinned message for at least a day

### Example

https://nvad011.cc/?channelCode=w_10   [4396/4411] [4成]

[4396/4411] --> total request going to link https://nvad011.cc/?channelCode=w_10 over total request going to w_10 channel

&nbsp;&nbsp;&nbsp;|  
&nbsp;&nbsp;&nbsp;--> channel will also show when above 150 request per hour, will hide if less. Can be configurable in config.yaml, counter var.

[4成] --> discount, how much it is being deducted.



## Components


### domains.yaml

To Edit what links will show in telegram pin message

### config.yaml

Initial configurations, bot API id, Loki location and configuration.

### bot.py

Base python script to contact telegram API

### domain_template.py

Main python script, will contact loki API to know the traffic on domain link/channel codes every 1 hour. This will also show the message in a presentable way

### pin_update.py

Use for running domain_template.py and will edit the pinned message, can manually run using:

./pin_update.py [message_id] [chat_id]

### update.sh

Use to pull updates from git repository and run pin_update.py, can use for cron to schedule bot edits.

### cnzz.yaml

Add channel codes here to have prefix of "*" indicating the link has cnzz

### percent.sh

Will count the deduction that has been made on the the channel, will also trigger warning if there is a conflict in xin configuration file.