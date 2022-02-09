import parse
from typing import Optional, Union

from mcdreforged.api.rtext import RAction, RColor, RText, RTextList
from mcdreforged.api.types import PluginServerInterface, CommandSource
from mcdreforged.api.command import Literal
from mcdreforged.api.decorator import new_thread

from multi_rcon_api.multi_rcon import MultiRcon


configPath = 'config/online.json'
defaultConfig = {
    "join": True,
    "click_event": True
}

config: Optional[dict] = None


def tr(translation_key: str):
    server = PluginServerInterface.get_instance()
    return server.tr("online.{}".format(translation_key))


def get_server_rtext(name):
    if config['click_event']:
        return RText(name, color=RColor.aqua).c(RAction.run_command, f"/server {name}")
    else:
        return RText(name, color=RColor.aqua)


@new_thread()
def get_list(src: Union[CommandSource, str]):  # 获得玩家列表
    global config
    list_text = ''
    query_result = MultiRcon.get_instance().group_command('list')
    formatters = (
        # <1.16
        # There are 6 of a max 100 players online: 122, abc, xxx, www, QwQ, bot_tob
        r'There are {amount:d} of a max {limit:d} players online:{players}There are {dummy}',
        r'There are {amount:d} of a max {limit:d} players online:{players}',
        # >=1.16
        # There are 1 of a max of 20 players online: Fallen_Breath
        r'There are {amount:d} of a max of {limit:d} players online:{players}There are {dummy}',
        r'There are {amount:d} of a max of {limit:d} players online:{players}',
    )
    for server in query_result:
        list_text += get_server_rtext(server) + ' '

        res = query_result.get(server)
        if res.get('connected'):
            for formatter in formatters:
                parsed = parse.parse(formatter, res['data'])
                if parsed is not None and parsed['players'].startswith(' '):
                    player_number = parsed['amount']
                    players_str = parsed['players'][1:]

                    list_text += RTextList(
                        RText(tr("total_online_num"), color=RColor.gray),
                        RText(' ' + str(player_number), color=RColor.green)
                    )
                    if player_number != 0:
                        list_text += RTextList(
                            ' ',
                            RText(tr("online_player_list"), color=RColor.gray),
                            RText(' ' + players_str, RColor.gold)
                        )
                    break
            else:
                list_text += RText(tr('unparseable_list'), color=RColor.red)
        else:
            list_text += RText(tr('server_stopped'), color=RColor.red)
        list_text += "\n"
    if isinstance(src, str):
        PluginServerInterface.get_instance().tell(src, list_text)
    else:
        src.reply(list_text)


def on_player_joined(server, player, info):
    if config['join']:
        get_list(player)


def on_load(server: PluginServerInterface, old):
    global config
    server.register_help_message('!!online', tr('help'))
    server.register_command(Literal('!!online').runs(lambda src: get_list(src)))
    config = server.load_config_simple(default_config=defaultConfig)
