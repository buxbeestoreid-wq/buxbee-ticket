import discord
from discord.ext import commands
import os

GUILD_ID = 1543725449438564414
CATEGORY_ID = 1566564296882913320
TICKET_CHANNEL_ID = 1566565308070756352

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(self, interaction: discord.Interaction, label: str):
        # Biar gak timeout
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            guild = interaction.guild
            category = guild.get_channel(CATEGORY_ID)
            if category is None:
                category = await guild.fetch_channel(CATEGORY_ID)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True, embed_links=True),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
            }

            channel = await guild.create_text_channel(
                name=f"ticket-{interaction.user.name}-{label.lower().replace(' ', '-')}",
                category=category,
                overwrites=overwrites,
                reason=f"Ticket {label} by {interaction.user}"
            )

            embed = discord.Embed(
                title=f"Ticket - {label}",
                description=f"Halo {interaction.user.mention}! Terima kasih sudah buka ticket.\n\nSilahkan ketik pesanan kamu disini. Admin akan segera membalas.\n\n**Jenis:** {label}",
                color=0xFFD700
            )
            await channel.send(content=f"{interaction.user.mention}", embed=embed)
            await interaction.followup.send(f"Ticket kamu berhasil dibuat! {channel.mention}", ephemeral=True)

        except Exception as e:
            print(f"ERROR CREATE TICKET: {e}")
            await interaction.followup.send(f"Gagal buat ticket, error: {e}. Hubungi admin!", ephemeral=True)

    @discord.ui.button(label="ROBUX GAMEPASS", style=discord.ButtonStyle.primary, custom_id="ticket_gamepass", emoji="🎫")
    async def gamepass_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "ROBUX GAMEPASS")

    @discord.ui.button(label="ROBUX VIA SEND", style=discord.ButtonStyle.primary, custom_id="ticket_viasend", emoji="🎫")
    async def viasend_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "ROBUX VIA SEND")

@bot.event
async def on_ready():
    print(f"Bot {bot.user} Online!")
    bot.add_view(TicketView())
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Sync error: {e}")

@bot.tree.command(name="setup-ticket", description="Setup panel ticket Buxbee")
async def setup_ticket(interaction: discord.Interaction):
    if interaction.channel_id != TICKET_CHANNEL_ID:
        await interaction.response.send_message("Command ini hanya bisa di #open-ticket!", ephemeral=True)
        return

    embed = discord.Embed(
        title="Order Here!",
        description="Selamat datang di layanan pemesanan Buxbee Store 🐝! Gunakan fitur ini untuk melakukan pemesanan atau bertanya seputar produk kami.\n\n**📋 CARA MEMBUKA TICKET**\n1. Klik tombol di bawah ini.\n2. Channel privat baru akan muncul untuk kamu.",
        color=0xFFD700
    )
    await interaction.response.send_message(embed=embed, view=TicketView())
    # Kirim ulang biar view nya nempel terus
    print("Setup ticket sent!")

bot.run(os.getenv("DISCORD_TOKEN"))
