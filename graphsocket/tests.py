from django.test import TestCase

# Create your tests here.


@run_async
@connection_status
@user_admin
def enable_module(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat

    if len(args) >= 1:
        enable_module = "bot.modules." + args[0].rsplit(".", 1)[0]

        try:
            module = importlib.import_module(enable_module)
        except:
            update.effective_message.reply_text("Does that module even exist?")
            return

        try:
            command_list = module.__command_list__
        except:
            update.effective_message.reply_text("Module does not contain command list!")
            return

