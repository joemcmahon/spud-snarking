# Spud's personality module

Our robot DJ at RadioSpiral has gone through a number of implementations, but he's always been himself:
a somewhat snarky and flippant little bot, who tends to pipe up when he's mentioned (or spoken to!), and
who has a fascination with Brian Eno's Oblique Strategies.

This repository implements a Discord bot that uses presence intent to lurk in all the channels, and
message intent to watch the text go by and chime in when someone mentions him or "oblique" or "strategies".

This version of Spud keeps his responses in YAML files, making it easy to expand his vocabulary. His self-recognition
is hard-coded but there's no reason that couldn't be moved to his .env at a later date to make other lurker bots.

# Running Spud

Pretty easy! Create a .env with a Discord bot token. The bot should have
 - Public bot
 - Presence intent
 - Message content intent

And that's it. Create your bot token with those set and you're good to go. Copy that to .env as the value of
BOT_TOKEN, and do `docker compose up --build` to launch him.

Once he's up, invite him to your Discord, and he'll be everywhere, listening for his trigger keywords.

# Possible enhancements

This is a good skeleton for any bot you'd like to have looking to be helpful behind the scenes, since he sees all and knows all.
He has the advantage that every user can address him, but also the disadvantage that every user can ask him to do things. I
recommend that you keep him limited to minor things, like weather lookups or the like. You probably shouldn't, for instance,
hook him up to an LLM and allow arbitrary queries.

Have fun!
