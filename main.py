# PETYA LOX
# MISHA LOX

import discord
from discord.ext import commands
from discord.ext.commands import Context
from data import db_session
from data.user import User
from data.event import Event
from data.bet import Bet
from flex import Flex
from globals import ERRORS, TOKEN, COMMAND_NAMES, MESSAGES, HELP

intents = discord.Intents.default()
intents.members = True


class TeleterCog(commands.Cog):
    def __init__(self, d_bot):
        self.bot = d_bot

    @commands.command(name=COMMAND_NAMES['show_money'])
    async def show_money(self, ctx: Context):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            await ctx.send(MESSAGES['show_money_1'].format(user.money))
            if user.money <= 100:
                await ctx.send(MESSAGES['show_money_2_1'])
            elif user.money > 10000:
                await ctx.send(MESSAGES['show_money_2_2'])
        else:
            await ctx.send(ERRORS['not_registered'])

    @commands.command(name=COMMAND_NAMES['register'])
    async def register(self, ctx: Context):
        db_sess = db_session.create_session()
        print(ctx.author.id)
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            await ctx.send(ERRORS['already_registered'])
        else:
            await ctx.send(MESSAGES['user_registered'])
            db_sess.add(User(ctx.author.id))
            db_sess.commit()

    @commands.command(name=COMMAND_NAMES['pleh'])
    async def pleh(self, ctx: Context):
        await ctx.send('\n'.join(HELP))

    @commands.command(name=COMMAND_NAMES['create_event'])
    async def create_event(self, ctx: Context, event_name, end_1, end_2):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            event = Event(ctx.author.id, event_name, end_1, end_2)
            db_sess.add(event)
            db_sess.commit()
            await ctx.send(MESSAGES['create_event'].format(event_name))
        else:
            await ctx.send(ERRORS['not_registered'])

    @commands.command(name=COMMAND_NAMES['show_board'])
    async def show_board(self, ctx: Context):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            events = db_sess.query(Event).filter(Event.closed == False).all()
            if events:
                for (i, event) in enumerate(events):
                    await ctx.send(
                        MESSAGES['show_board_1'].format(
                            i + 1, event.name, event.first_end, event.second_end, event.open_id
                        )
                    )
            else:
                await ctx.send(MESSAGES['show_board_2'])
        else:
            await ctx.send(ERRORS['not_registered'])

    @commands.command(name=COMMAND_NAMES['close_event'])
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
                await ctx.send(MESSAGES['close_event'])
            else:
                await ctx.send(ERRORS['event_not_exist'])
        else:
            await ctx.send(ERRORS['not_registered'])

    @commands.command(name=COMMAND_NAMES['make_bet'])
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
                                MESSAGES['make_bet_1_1'].format(
                                    money, event.first_end if bet.is_first else event.second_end, bet.bet_cnt
                                )
                            )
                        else:
                            await ctx.send(ERRORS['not_enough_money'])
                    else:
                        await ctx.send(ERRORS['bet_on_two_sides'])
                else:
                    if user.subtract_money(money):
                        bet = Bet(user.id, open_id, not bool(number - 1), money)
                        await ctx.send(
                            MESSAGES['make_bet_1_2'].format(
                                money, event.first_end if bet.is_first else event.second_end, bet.bet_cnt
                            )
                        )
                        db_sess.add(bet)
                    else:
                        await ctx.send(ERRORS['not_enough_money'])
            else:
                await ctx.send(ERRORS['event_not_exist'])
        else:
            await ctx.send(ERRORS['not_registered'])
        db_sess.commit()


bot = commands.Bot(command_prefix='!!', intents=intents)
bot.add_cog(Flex(bot))
bot.add_cog(TeleterCog(bot))
db_session.global_init("db/teleter.sqlite")
bot.run(TOKEN)
