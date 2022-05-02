# MISHA LOX

import discord
from discord.ext import commands
from discord.ext.commands import Context
from data import db_session
from data.user import User
from data.event import Event
from data.bet import Bet

intents = discord.Intents.default()
intents.members = True

returns = {
    'not_registered': 'зарегайся сначала, чел.',
    'event_not_exist': 'такого события не найдено.',
    'bet_on_two_sides': 'никаких вилок, чел. ложек тоже не надо. (нельзя ставить на оба исхода события))',
    'not_enough_money': 'у тебя не хватает деняк, чел.'
}

command_names = {
    'show_money': 'сколько_деняк',
    'register': 'регистрация',
    'pleh': 'помощь',
    'create_event': 'создать_событие',
    'show_board': 'доска_событий',
    'close_event': 'закрыть_событие',
    'make_bet': 'ставка'
}


class TeleterCog(commands.Cog):
    def __init__(self, d_bot):
        self.bot = d_bot

    @commands.command(name=command_names['show_money'])
    async def show_money(self, ctx: Context):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            await ctx.send(f'у тебя {user.money} деняк')
            if user.money <= 100:
                await ctx.send(f'нищеброд')
            elif user.money > 10000:
                await ctx.send(f'настоящий богач')
        else:
            await ctx.send(returns['not_registered'])

    @commands.command(name=command_names['register'])
    async def register(self, ctx: Context):
        db_sess = db_session.create_session()
        print(ctx.author.id)
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            await ctx.send("Такой пользователь уже есть")
            return
        else:
            await ctx.send("Пользователь успешно зареган")
            db_sess.add(User(ctx.author.id))
            db_sess.commit()
            return

    @commands.command(name=command_names['pleh'])
    async def pleh(self, ctx: Context):
        await ctx.send("Миша лох")

    @commands.command(name=command_names['create_event'])
    async def create_event(self, ctx: Context, event_name, end_1, end_2):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            event = Event(ctx.author.id, event_name, end_1, end_2)
            db_sess.add(event)
            db_sess.commit()
            await ctx.send(f"Событие {event_name} создано успешно!")
        else:
            await ctx.send(returns['not_registered'])

    @commands.command(name=command_names['show_board'])
    async def show_board(self, ctx: Context):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            events = db_sess.query(Event).filter(Event.closed == False).all()
            if events:
                for (i, event) in enumerate(events):
                    await ctx.send(
                        f"{i + 1}. Событие {event.name} с исходами {event.first_end}" +
                        f" и {event.second_end}, публичный ID = {event.open_id}"
                    )
            else:
                await ctx.send('нет событий')
        else:
            await ctx.send(returns['not_registered'])

    @commands.command(name=command_names['close_event'])
    async def close_event(self, ctx: Context, open_id: int, finale: int):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            event = db_sess.query(Event).filter(Event.open_id == open_id).first()
            if event and not event.closed:
                bets = db_sess.query(Bet).filter(Bet.event_open_id == open_id).all()
                percents = {}
                bank = event.first_bank + event.second_bank
                if not bool(finale - 1):
                    for bet in bets:
                        if bet.is_first:
                            percents[bet] = bet.bet_cnt / event.first_bank
                else:
                    for bet in bets:
                        if not bet.is_first:
                            percents[bet] = bet.bet_cnt / event.second_bank
                for (bet, percent) in percents.items():
                    bet.user.add_money(int(percent * bank))
                event.closed = True
                db_sess.commit()
                await ctx.send("событие закрыто! поздравляю победителей")
            else:
                await ctx.send(returns['event_not_exist'])
        else:
            await ctx.send(returns['not_registered'])

    @commands.command(name=command_names['make_bet'])
    async def make_bet(self, ctx: Context, open_id: int, number: int, money: int):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            event = db_sess.query(Event).filter(Event.open_id == open_id).first()
            if event:
                bet = db_sess.query(Bet).filter(Bet.event_open_id == open_id).first()
                if bet:
                    if bool(number - 1) != bet.is_first:
                        if user.subtract_money(money):
                            bet.add_money(money)
                            if bet.is_first:
                                event.first_bank += money
                            else:
                                event.second_bank += money
                            await ctx.send(
                                f"Чел, ты добавил {money} на {event.first_end if bet.is_first else event.second_end}\n" +
                                f"теперь там: {bet.bet_cnt}"
                            )
                        else:
                            await ctx.send(returns['not_enough_money'])
                    else:
                        await ctx.send(returns['bet_on_two_sides'])
                else:
                    if user.subtract_money(money):
                        bet = Bet(user.id, open_id, not bool(number - 1), money)
                        await ctx.send(
                            f"Чел, ты поставил {money} на {event.first_end if bet.is_first else event.second_end}\n" +
                            f"ставка: {bet.bet_cnt}"
                        )
                        db_sess.add(bet)
                    else:
                        await ctx.send(returns['bet_on_two_sides'])
            else:
                await ctx.send(returns['event_not_exist'])
        else:
            await ctx.send(returns['not_registered'])
        db_sess.commit()


bot = commands.Bot(command_prefix='!!', intents=intents)
bot.add_cog(TeleterCog(bot))
db_session.global_init("db/teleter.sqlite")
TOKEN = 'OTcwNDQ0MzY2MTcyNzgyNjQz.Ym8Cvg.7C80LVXmfWDZAfdYAeUes_WXXf8'
bot.run(TOKEN)
