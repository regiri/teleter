import discord
from discord.ext import commands
from discord.ext.commands import Context
from data import db_session
from data.user import User
import validators
from validators import ValidationFailure
from globals import ERRORS
from youtube_dl import YoutubeDL
from asyncio import sleep
from globals import YDL_OPTIONS, FFMPEG_OPTIONS, COMMAND_NAMES


def is_string_an_url(url_string: str) -> bool:
    result = validators.url(url_string)
    if isinstance(result, ValidationFailure):
        return False
    return result


is_vc_connected = False


class Flex(commands.Cog):
    def __init__(self, d_bot):
        self.bot = d_bot

    # TODO хочу чтобы по запросу флекс играл рандомный звук или картинка из пула мемов
    @commands.command(name=COMMAND_NAMES['flex'])
    async def flex(self, ctx: Context, url: str):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            # TODO добавить timeout
            # TODO добавить вывод если пользователь не передал url
            '''if not is_string_an_url(url):
                await ctx.send('Неправильный url прекола')
                return
            song = os.path.isfile("song.mp3")
            try:
                if song:
                    os.remove("song.mp3")
            except PermissionError:
                await ctx.send("Дождитесь окончания флекса или используйте комманду 'стоп'")'''
            if not is_string_an_url(url):
                await ctx.send(ERRORS['wrong_url'])
                return
            try:
                voice_channel = discord.utils.get(ctx.guild.voice_channels, name='General')
                await voice_channel.connect()
                voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
                global is_vc_connected
                is_vc_connected = True

                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)

                parsed_url = info['formats'][0]['url']

                voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=parsed_url, **FFMPEG_OPTIONS))

                while voice.is_playing():
                    await sleep(1)
                if not voice.is_paused():
                    await voice.disconnect()
            except Exception as e:
                print(e)
                await ctx.send(ERRORS['already_connected'])
        else:
            await ctx.send(ERRORS['not_registered'])

    @commands.command(name=COMMAND_NAMES['stop_flex'])
    async def stop_flex(self, ctx: Context):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            global is_vc_connected
            if not is_vc_connected:
                await ctx.send(ERRORS['flex_not_started'])
                return
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if voice.is_connected():
                await voice.disconnect()
                is_vc_connected = False
            else:
                await ctx.send(ERRORS['flex_not_connected'])
        else:
            await ctx.send(ERRORS['not_registered'])

    @commands.command(name=COMMAND_NAMES['pause_flex'])
    async def pause_flex(self, ctx: Context):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            global is_vc_connected
            if not is_vc_connected:
                await ctx.send(ERRORS['flex_not_started'])
                return
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if voice.is_playing():
                voice.pause()
            else:
                await ctx.send(ERRORS['flex_does_not_occur'])
        else:
            await ctx.send(ERRORS['not_registered'])

    @commands.command(name=COMMAND_NAMES['resume_flex'])
    async def resume_flex(self, ctx: Context):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            global is_vc_connected
            if not is_vc_connected:
                await ctx.send(ERRORS['flex_not_started'])
                return
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if voice.is_paused():
                voice.resume()
            else:
                await ctx.send(ERRORS['flex_not_stopped'])
        else:
            await ctx.send(ERRORS['not_registered'])

    @commands.command(name='отключить')
    async def disconnect_flex(self, ctx: Context):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == ctx.author.id).first()
        if user:
            global is_vc_connected
            if not is_vc_connected:
                await ctx.send(ERRORS['flex_not_started'])
                return
            voice = ctx.message.guild.voice_client
            await voice.stop()
        else:
            await ctx.send(ERRORS['not_registered'])
