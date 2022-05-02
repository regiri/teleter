# MISHA LOX

import discord
from discord.ext import commands
from discord.ext.commands import Context
from data import db_session
from data.user import User
from data.event import Event

intents = discord.Intents.default()
intents.members = True

returns = {
    'not_registered': 'зарегайся сначала, чел'
}


class TeleterCog(commands.Cog):
    def __init__(self, d_bot):
        self.bot = d_bot

    @commands.command(name='сколько_деняк')
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

    @commands.command(name='регистрация')
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

    @commands.command(name='помощь')
    async def pleh(self, ctx: Context):
        await ctx.send("Миша лох")

    @commands.command(name='создать_событие')
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

    @commands.command(name='доска_событий')
    async def show_board(self, ctx: Context):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            events = db_sess.query(Event).filter(Event.closed == False).all()
            if events:
                for event in events:
                    await ctx.send(f"Событие {event.name} с исходами {event.first_end} и {event.second_end}")
            else:
                await ctx.send('нет событий')
        else:
            await ctx.send(returns['not_registered'])


bot = commands.Bot(command_prefix='!!', intents=intents)
bot.add_cog(TeleterCog(bot))
db_session.global_init("db/teleter.sqlite")
TOKEN = 'OTcwNDQ0MzY2MTcyNzgyNjQz.Ym8Cvg.7C80LVXmfWDZAfdYAeUes_WXXf8'
bot.run(TOKEN)
