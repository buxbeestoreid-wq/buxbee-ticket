import discord
from discord.ext import commands
import os
import asyncio

GUILD_ID = 1543725449438564414
CATEGORY_ID = 1566564296882913320
TICKET_CHANNEL_ID = 1566565308070756352

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== TOMBOL CLOSE =====
class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Ticket akan ditutup dalam 3 detik...", ephemeral=False)
        await asyncio.sleep(3)
        try:
            await interaction.channel.delete(reason=f"Ticket ditutup oleh {interaction.user}")
        except Exception as e:
            print(f"Close error: {e}")

# ===== TOMBOL PANEL =====
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(self, interaction: discord.Interaction, label: str):
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

            # --- EMBED GAMEPASS = PRICELIST ---
            if label == "ROBUX GAMEPASS":
                embed = discord.Embed(
                    title="Ticket - ROBUX GAMEPASS",
                    description=f"Halo {interaction.user.mention}! Terima kasih sudah buka ticket.\n\n# PRICELIST ROBUX VIA GAMEPASS 🔥\n\n⏳ Pending 5 Hari\n✅ Sudah After Tax\n⚡ Semi fast proses (max 1x24 jam)\n\n* 100 rbx → Rp 13.500\n* 200 rbx → Rp 27.000\n* 300 rbx → Rp 41.000\n* 400 rbx → Rp 55.000\n* 500 rbx → Rp 70.000\n* 600 rbx → Rp 75.000\n* 700 rbx → Rp 95.000\n* 800 rbx → Rp 110.000\n* 900 rbx → Rp 115.000\n* 1000 rbx → Rp 140.000\n\n**nominal lain:**\n140 × jumlah robux yg di inginkan\ncontoh : 140 × 2000 rbx = 280.000\n\n⚠️ note :\n**TIDAK PERLU BUAT KODE GAMEPASS (HANYA PENGIRIMANNYA SAJA YANG SEDIKIT MEMAKAN WAKTU)**\n\nSilahkan ketik nominal yang mau kamu order ya!",
                    color=0xFFD700
                )
            else:
                embed = discord.Embed(
                    title=f"Ticket - {label}",
                    description=f"Halo {interaction.user.mention}! Terima kasih sudah buka ticket.\n\nSilahkan ketik pesanan kamu disini. Admin akan segera membalas.\n\n**Jenis:** {label}",
                    color=0xFFD700
                )

            await channel.send(content=f"{interaction.user.mention}", embed=embed, view=CloseView())
            await interaction.followup.send(f"Ticket kamu berhasil dibuat! {channel.mention}", ephemeral=True)

        except Exception as e:
            print(f"ERROR CREATE TICKET: {e}")
            await interaction.followup.send(f"Gagal buat ticket, error: {e}. Hubungi admin!", ephemeral=True)

    @discord.ui.button(label="ROBUX GAMEPASS", style=discord.ButtonStyle.primary, custom_id="ticket_gamepass", emoji="🎫")
    async def gamepass_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "ROBUX GAMEPASS")

    @discord.ui.button(label="ROBUX VIA USN", style=discord.ButtonStyle.primary, custom_id="ticket_viausn", emoji="🎫")
    async def viausn_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "ROBUX VIA USN")

@bot.event
async def on_ready():
    print(f"Bot {bot.user} Online!")
    bot.add_view(TicketView())
    bot.add_view(CloseView())
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
    embed.set_image(url="https://raw.githubusercontent.com/buxbeestoreid-wq/buxbee-ticket/main/IMG_1777.png")
    await interaction.response.send_message(embed=embed, view=TicketView())
    print("Setup ticket sent!")

bot.run(os.getenv("DISCORD_TOKEN"))
