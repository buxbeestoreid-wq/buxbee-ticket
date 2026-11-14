import discord
from discord.ext import commands
import os
import asyncio
import datetime

GUILD_ID = 1543725449438564414
CATEGORY_ID = 1566564296882913320
TICKET_CHANNEL_ID = 1566565308070756352
LOG_CHANNEL_ID = 1571295129850089713
VOUCH_CHANNEL_ID = 1571297110601629757
QRIS_URL = "https://raw.githubusercontent.com/buxbeestoreid-wq/buxbee-ticket/main/IMG_1782.png"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Counter Ticket ID buat Vouch
ticket_counter = 1
try:
    with open("ticket_counter.txt", "r") as f:
        ticket_counter = int(f.read().strip())
except:
    ticket_counter = 1

def save_counter():
    with open("ticket_counter.txt", "w") as f:
        f.write(str(ticket_counter))

# ===== MODAL VOUCH =====
class VouchModal(discord.ui.Modal, title="Kasih Vouch ⭐"):
    nominal = discord.ui.TextInput(label="Nominal", placeholder="Contoh: Rp 33.000", required=True)
    rating = discord.ui.TextInput(label="Rating (1-5)", placeholder="Contoh: 5", required=True, max_length=1)
    komentar = discord.ui.TextInput(label="Komentar", placeholder="Contoh: mantapp", required=True, style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        global ticket_counter
        await interaction.response.send_message("Vouch kamu berhasil dikirim! Makasih ya ⭐", ephemeral=True)
        channel = interaction.channel
        buyer_id = None
        try:
            buyer_id = int(channel.topic) if channel.topic and channel.topic.isdigit() else None
        except:
            buyer_id = None
        buyer = interaction.guild.get_member(buyer_id) if buyer_id else interaction.user
        if buyer is None:
            buyer = interaction.user

        try:
            r = int(self.rating.value)
            if r < 1: r = 1
            if r > 5: r = 5
        except:
            r = 5
        stars = "⭐" * r

        if "gamepass" in channel.name.lower():
            via_text = "VIA GAMEPASS"
            source_text = f"robux-via-gamepass-{ticket_counter}-{buyer.name}"
        else:
            via_text = "VIA USN"
            source_text = f"robux-via-username-{ticket_counter}-{buyer.name}"

        try:
            vouch_channel = interaction.guild.get_channel(VOUCH_CHANNEL_ID)
            if vouch_channel is None:
                vouch_channel = await interaction.guild.fetch_channel(VOUCH_CHANNEL_ID)
            if vouch_channel:
                embed = discord.Embed(title="✅ VOUCH RECEIVED ✅", color=0x2ECC71)
                embed.add_field(name="Ticket ID", value=str(ticket_counter), inline=False)
                embed.add_field(name="Nominal", value=self.nominal.value, inline=False)
                embed.add_field(name="Seller", value=interaction.user.mention, inline=False)
                embed.add_field(name="Buyer", value=buyer.mention, inline=False)
                embed.add_field(name="Handled by", value=interaction.user.mention, inline=False)
                embed.add_field(name="Rating", value=stars, inline=False)
                embed.add_field(name="Komentar", value=f"{self.komentar.value} 💗", inline=False)
                embed.add_field(name="Source", value=source_text, inline=False)
                now = datetime.datetime.now()
                embed.set_footer(text=f"MIPI STORE Vouch System | {now.strftime('%B %d, %Y at %I:%M %p')} | {via_text}")
                try:
                    embed.set_thumbnail(url=buyer.display_avatar.url)
                except:
                    pass
                await vouch_channel.send(embed=embed)
                await vouch_channel.send(f"**Vouch - {buyer.name} | Ticket #{ticket_counter}**\n💗 Vouch dari {buyer.mention} 📦 Paket: {self.nominal.value} | {via_text}")
                ticket_counter += 1
                save_counter()
        except Exception as e:
            print(f"Vouch error: {e}")

# ===== MODAL PAS CLOSE =====
class CloseModal(discord.ui.Modal, title="Close Ticket - Isi Data Order"):
    nickname = discord.ui.TextInput(label="Nickname Roblox", placeholder="Contoh: SONxMRafii", required=True)
    username = discord.ui.TextInput(label="Username Roblox", placeholder="Contoh: 1mrafii", required=True)
    jumlah = discord.ui.TextInput(label="Jumlah Robux", placeholder="Contoh: 500", required=True)
    total = discord.ui.TextInput(label="Total Harga", placeholder="Contoh: Rp 78.000", required=True)
    payment = discord.ui.TextInput(label="Payment", placeholder="Contoh: QRIS / DANA / GOPAY", required=True, default="QRIS")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Menyimpan log & menutup ticket dalam 3 detik...", ephemeral=True)
        channel = interaction.channel
        if "gamepass" in channel.name.lower():
            panel_text = "Robux Via Gamepass"
            via_text = "VIA GAMEPASS"
        else:
            panel_text = "Robux Via Username"
            via_text = "VIA USN"
        try:
            log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
            if log_channel is None:
                log_channel = await interaction.guild.fetch_channel(LOG_CHANNEL_ID)
            if log_channel:
                log_embed = discord.Embed(title="🔒 Ticket Log", color=0xFFD700)
                log_embed.add_field(name="🎫 Ticket", value=channel.name, inline=False)
                log_embed.add_field(name="🔒 Action", value="Closed", inline=False)
                log_embed.add_field(name="⚡ Panel", value=panel_text, inline=False)
                log_embed.add_field(name="🎀 Member", value=interaction.user.mention, inline=False)
                log_embed.add_field(name="✨ Nickname Roblox", value=self.nickname.value, inline=False)
                log_embed.add_field(name="👤 Username Roblox", value=self.username.value, inline=False)
                log_embed.add_field(name="✨ Jumlah Robux", value=self.jumlah.value, inline=False)
                log_embed.add_field(name="💰 Total Harga", value=self.total.value, inline=False)
                log_embed.add_field(name="🧾 Payment", value=self.payment.value, inline=False)
                log_embed.add_field(name="✅ Admin", value=interaction.user.mention, inline=False)
                log_embed.set_footer(text=f"{via_text} | Project by Mipi Store")
                await log_channel.send(embed=log_embed)
        except Exception as e:
            print(f"Log error: {e}")
        await asyncio.sleep(3)
        try:
            await channel.delete(reason=f"Ticket ditutup oleh {interaction.user}")
        except Exception as e:
            print(f"Close error: {e}")

# ===== TOMBOL DI DALAM TICKET: CLOSE + VOUCH =====
class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CloseModal())

    @discord.ui.button(label="⭐ Kasih Vouch", style=discord.ButtonStyle.success, custom_id="vouch_ticket")
    async def vouch_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(VouchModal())

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
                topic=str(interaction.user.id),
                reason=f"Ticket {label} by {interaction.user}"
            )
            if label == "ROBUX GAMEPASS":
                embed = discord.Embed(
                    title="Ticket - ROBUX GAMEPASS",
                    description=f"Halo {interaction.user.mention}! Terima kasih sudah buka ticket.\n\n# PRICELIST ROBUX VIA GAMEPASS 🔥\n\n⏳ Pending 5 Hari\n✅ Sudah After Tax\n⚡ Semi fast proses (max 1x24 jam)\n\n* 100 rbx → Rp 13.500\n* 200 rbx → Rp 27.000\n* 300 rbx → Rp 41.000\n* 400 rbx → Rp 55.000\n* 500 rbx → Rp 70.000\n* 600 rbx → Rp 75.000\n* 700 rbx → Rp 95.000\n* 800 rbx → Rp 110.000\n* 900 rbx → Rp 115.000\n* 1000 rbx → Rp 140.000\n\n**nominal lain:**\n140 × jumlah robux yg di inginkan\ncontoh : 140 × 2000 rbx = 280.000\n\n⚠️ note :\n**TIDAK PERLU BUAT KODE GAMEPASS (HANYA PENGIRIMANNYA SAJA YANG SEDIKIT MEMAKAN WAKTU)**\n\nSilahkan ketik nominal yang mau kamu order ya!\n\n**💳 PEMBAYARAN:**\nSilahkan scan QRIS di bawah ini untuk transfer, lalu kirim bukti TF nya disini!",
                    color=0xFFD700
                )
            elif label == "ROBUX VIA USN":
                embed = discord.Embed(
                    title="Ticket - ROBUX VIA USN",
                    description=f"Halo {interaction.user.mention}! Terima kasih sudah buka ticket.\n\n# PRICELIST ROBUX VIA SEND USERNAME\n_Buxbeestore.id🐝_\n\n**KELIPATAN 10 RBX (ECERAN) PROSES FAST SATSET:**\n\n10 rbx ➔ Rp 3.000\n20 rbx ➔ Rp 5.500\n30 rbx ➔ Rp 7.500\n40 rbx ➔ Rp 9.500\n50 rbx ➔ Rp 11.000\n\n**KELIPATAN 100 RBX PROSES FAST SATSET:**\n100 rbx ➔ Rp 15.500\n200 rbx ➔ Rp 31.000\n300 rbx ➔ Rp 46.500\n400 rbx ➔ Rp 62.000\n500 rbx ➔ Rp 75.000\n600 rbx ➔ Rp 90.500\n700 rbx ➔ Rp 106.000\n800 rbx ➔ Rp 121.500\n900 rbx ➔ Rp 137.000\n1.000 rbx ➔ Rp 150.000\n\n𓈃 Notes:\n⚠️ sebelum beli pastikan akun penerima robux tidak limit!\n⚠️ wajib sudah verif usia 18+\n⚠️ wajib sudah verifikasi 2 langkah\n⚠️ jangan langsung payment (tunggu ditotalin dulu, baru boleh payment)\n⚠️ setelah payment wajib ss bukti transfer yang jelas agar bisa diproses\n**⚠️ BUKAN ROBLOX KIDS / SELECT**\n\n**⌛️ HARGA JUGA DAPAT BERUBAH-UBAH, TIDAK MENENTU.**\n\nSilahkan ketik nominal yang mau kamu order ya!\n\n**💳 PEMBAYARAN:**\nSilahkan scan QRIS di bawah ini untuk transfer, lalu kirim bukti TF nya disini!",
                    color=0xFFD700
                )
            else:
                embed = discord.Embed(title=f"Ticket - {label}", description=f"Halo {interaction.user.mention}! Terima kasih sudah buka ticket.", color=0xFFD700)
            embed.set_image(url=QRIS_URL)
            embed.set_footer(text=f"{label} | Project by Mipi Store")
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
    embed = discord.Embed(title="Order Here!", description="Selamat datang di layanan pemesanan Buxbee Store 🐝! Gunakan fitur ini untuk melakukan pemesanan atau bertanya seputar produk kami.\n\n**📋 CARA MEMBUKA TICKET**\n1. Klik tombol di bawah ini.\n2. Channel privat baru akan muncul untuk kamu.", color=0xFFD700)
    embed.set_image(url="https://raw.githubusercontent.com/buxbeestoreid-wq/buxbee-ticket/main/IMG_1777.png")
    embed.set_footer(text="Project by Mipi Store")
    await interaction.response.send_message(embed=embed, view=TicketView())
    print("Setup ticket sent!")

bot.run(os.getenv("DISCORD_TOKEN"))
