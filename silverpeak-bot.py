import os
import time
import re
from slackclient import SlackClient
from helpers import appliances
import settings

# instantiate Slack client
slack_client = SlackClient(settings.SLACK_CLIENT_TOKEN)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
COMMANDS = ['devices']
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

#
#    variables responses "welcome" and default
#
event_welcome = ("hi silverpeak", "hello silverpeak", "helo silverpeak", ".help", ".home")
# Default response is help text for the user
event_help = "` .help `"
#
#    welcome
#
event_welcome_table = [
                "Hi, I am the Silver Peak Bot :robot_face:, I know a lot of Silverpeak Stuff stuff :sunglasses:, to use me type any: `.command`",
                "or `@Silver Peak Bot command` for more informations. If you stuck - type `.help` or `.home` to go back to main menu.\n\n",
                "\nfor *Silverpeak*\n",
                "        |\n",
                "        |> *Info* - type:  `.devices` or `@Silver Peak Bot devices`\n",
                "\n\n",
                "suggestions/bugs - contact <https://github.com/minitriga> / #Axians-UK / Silver Peak Bot v0.1\n"
                ]

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]

# all @silver peak bot commands response

            if event["text"].lower().startswith("hi <@%s>" % starterbot_id):
                print("response to event: %s" % event["text"])
                return event["text"], event["channel"]

# all . commands reponse
            if event["text"].startswith("."):
                print("response to event: %s" % event["text"])
                return event["text"], event["channel"]

# welcome
            if event["text"].lower().startswith(event_welcome):
                print("event HELLO received: %s" % event["text"])
                return event["text"], event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(COMMANDS)

    # Finds and executes the given command, filling in response
    response = None

    if command.lower().startswith(event_welcome):
        response = ''.join(event_welcome_table)

    # This is where you start to implement more commands!
    elif command.lower().startswith(".devices") or command.lower().startswith("devices"):
            output = appliances()
            #response = "```{}```".format(appliances)
            response = output

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
