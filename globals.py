ERRORS = {
    'not_registered': 'зарегайся сначала, чел.',
    'already_registered': 'такой пользователь уже есть.',
    'event_not_exist': 'такого события не найдено.',
    'bet_on_two_sides': 'никаких вилок, чел. ложек тоже не надо. (нельзя ставить на оба исхода события))',
    'not_enough_money': 'у тебя не хватает деняк, чел.',
    'flex_not_started': 'сначала запустите флекс.',
    'wrong_url': 'неправильный url прекола.',
    'flex_not_connected': 'флекс не подключен.',
    'flex_does_not_occur': 'флекса не происходит',
    'flex_not_stopped': 'флекс не прекращался',
    'already_connected': 'Уже подключен или не удалось подключится'
}

MESSAGES = {
    'user_registered': 'пользователь успешно зареган.',
    'show_money_1': 'у тебя {} деняк.',
    'show_money_2_1': 'нищеброд.',
    'show_money_2_2': 'настоящий богач!',
    'create_event': 'Событие {} создано успешно!',
    'show_board_1': '{0}. Событие {1} с исходами {2} и {3}, публичный ID = {4}',
    'show_board_2': 'нет событий.',
    'close_event': 'событие закрыто! поздравляю победителей.',
    'make_bet_1_1': 'чел, ты добавил {0} на {1}\nтеперь там: {2}.',
    'make_bet_1_2': 'чел, ты поставил {0} на {1}\nставка: {2}.'
}

TOKEN = 'OTcwNDQ0MzY2MTcyNzgyNjQz.Ym8Cvg.7C80LVXmfWDZAfdYAeUes_WXXf8'

COMMAND_NAMES = {
    'show_money': 'сколько_деняк',
    'register': 'регистрация',
    'pleh': 'помощь',
    'create_event': 'создать_событие',
    'show_board': 'доска_событий',
    'close_event': 'закрыть_событие',
    'make_bet': 'ставка',
    'flex': 'флекс',
    'stop_flex': 'стоп',
    'pause_flex': 'пауза',
    'resume_flex': 'продолжить'
}

YDL_OPTIONS = {
    'format': 'bestaudio',
    'noplaylist': 'False'
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

HELP = [
    'команды бота:',
    '!!помощь - выводит эту подсказку',
    '!!регистрация - зарегистрироваться в системе',
    '!!сколько\_деняк - проверить свой баланс',
    '!!доска\_событий - показать открытые ставки (события)',
    '!!создать\_событие Название Исход\_1 Исход\_2 - создает ставку с двумя исходами,' +
    ' возвращает открытый ID по которому можно поставить на событие',
    '!!закрыть\_событие Открытый_ID Исход (0 или 1) - закрытие ставок и подсчет деняк',
    '!!ставка Открытый\_ID Исход (0 или 1) Кол-во\_деняк - поставить ден\_ки на один из исходов события',
    '!!флекс url - запустить музыку в голосовом канале',
    '!!стоп - выключить музыку в голосовом канале',
    '!!пауза - остановить музыку в голосовом канале',
    '!!продолжить - снять музыку с паузы'
]
