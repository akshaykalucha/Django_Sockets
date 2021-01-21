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

        enabled_cmds = []
        failed_enabled_cmds = []

        for enable_cmd in command_list:
            if enable_cmd.startswith(CMD_STARTERS):
                enable_cmd = enable_cmd[1:]

            if sql.enable_command(chat.id, enable_cmd):
                enabled_cmds.append(enable_cmd)
            else:
                failed_enabled_cmds.append(enable_cmd)

        if enabled_cmds:
            enabled_cmds_string = ", ".join(enabled_cmds)
            update.effective_message.reply_text(f"Enabled the uses of `{enabled_cmds_string}`",
                                                parse_mode=ParseMode.MARKDOWN)

        if failed_enabled_cmds:
            failed_enabled_cmds_string = ", ".join(failed_enabled_cmds)
            update.effective_message.reply_text(f"Are the commands `{failed_enabled_cmds_string}` even disabled?",
                                                parse_mode=ParseMode.MARKDOWN)