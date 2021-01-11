from discord.ext import commands

from core.models import HostingMethod, PermissionLevel, getLogger

logger = getLogger(__name__)


def has_permissions_predicate(permission_level: PermissionLevel = PermissionLevel.REGULAR,):
    async def predicate(ctx):
        return await check_permissions(ctx, ctx.command.qualified_name)

    predicate.permission_level = permission_level
    return predicate


