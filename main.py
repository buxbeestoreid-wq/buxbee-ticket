import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

TICKET_CATEGORY_ID = 123456789012345678
ADMIN_ROLE_ID = 123456789012345678

# === PRICELIST VIA SEND ===
PRICELIST_SEND = """# PRICELIST ROBUX VIA SEND USERNAME
_Buxbeestore.id🐝_

**KELIPATAN 10 RBX (ECERAN) PROSES FAST SATSET:**
10 rbx ➔ Rp 3.000
20 rbx ➔ Rp 5.500
30 rbx ➔ Rp 7.500
40 rbx ➔ Rp 9.500
50 rbx ➔ Rp 11.000

**KELIPATAN 100 RBX PROSES FAST SATSET:**
100 rbx ➔ Rp 15.500
200 rbx ➔ Rp 31.000
300 rbx ➔ Rp 46.500
400 rbx ➔ Rp 62.000
500 rbx ➔ Rp 75.000
600 rbx ➔ Rp 90.500
700 rbx ➔ Rp 106.000
800 rbx ➔ Rp 121.500
900 rbx ➔ Rp 137.000
1.000 rbx ➔ Rp 150.000

𓈃 Notes:
⚠️ sebelum beli pastikan akun penerima robux tidak limit!
⚠️ wajib sudah verif usia 18+
⚠️ wajib sudah verifikasi 2 langkah
⚠️ jangan langsung payment (tunggu ditotalin dulu, baru boleh payment)
⚠️ setelah payment wajib ss bukti transfer yang jelas agar bisa diproses
**⚠️ BUKAN ROBLOX KIDS / SELECT**
**⌛️ HARGA JUGA DAPAT BERUBAH-UBAH, TIDAK MENENTU.**
"""

# === PRICELIST GAMEPASS - ASLI ===
PRICELIST_GAMEPASS = """# PRICELIST ROBUX VIA GAMEPASS 🔥

⏳ Pending 5 Hari
✅ Sudah After Tax
⚡ Semi fast proses (max 1x24 jam)

 * 100 rbx → Rp 13.500
 * 200 rbx → Rp 27.000
 * 300 rbx → Rp 41.000
 * 400 rbx → Rp 55.000
 * 500 rbx → Rp 70.000
 * 600 rbx → Rp 75.000
 * 700 rbx → Rp 95.000
 * 800 rbx → Rp 110.000
 * 900 rbx → Rp 115.000
 * 1000 rbx → Rp 140.000

nominal lain:
140 × jumlah robux yg di inginkan
contoh : 140 × 2000 rbx = 280.000

⚠️ note :
**TIDAK PERLU BUAT KODE GAMEPASS (HANYA PENGIRIMANNYA SAJA YANG SEDIKIT MEMAKAN WAKTU)**
"""

class CloseButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Ticket ditutup...", ephemeral=True)
        await interaction.channel.delete()

async def buat_ticket(interaction, tipe, pricelist):
    guild = interaction.guild
    user = interaction.user
    for channel in guild.channels:
        if channel.name == f"ticket-{user.name.lower()}":
            await interaction.response.send_message(f"Kamu udah punya ticket! {channel.mention}", ephemeral=True)
            return
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.get_role(ADMIN_ROLE_ID): discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }
    category = guild.get_channel(TICKET_CATEGORY_ID)
    channel = await guild.create_text_channel(f"{tipe}-{user.name}", category=category, overwrites=overwrites)
    embed = discord.Embed(title=f"🐝 BUXBEESTORE.ID - {tipe.upper()}", color=0xFFD700)
    embed.description = f"Halo {user.mention}!\n\n{pricelist}\n\n**📝 FORMAT ORDER:**\n`Username Roblox : \nJumlah Robux : \nPayment : `"
    embed.set_footer(text="BUXBEESTORE.ID • PEOPLE COME & GO")
    await channel.send(embed=embed, view=CloseButton())
    await interaction.response.send_message(f"Ticket kamu dibuat! {channel.mention}", ephemeral=True)

class TicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="🎫 ROBUX GAMEPASS", style=discord.ButtonStyle.blurple, custom_id="ticket_gamepass")
    async def gamepass(self, interaction: discord.Interaction, button: discord.ui.Button):
        await buat_ticket(interaction, "gamepass", PRICELIST_GAMEPASS)
    @discord.ui.button(label="🎫 ROBUX VIA SEND", style=discord.ButtonStyle.blurple, custom_id="ticket_send")
    async def via_send(self, interaction: discord.Interaction, button: discord.ui.Button):
        await buat_ticket(interaction, "via-send", PRICELIST_SEND)

@bot.event
async def on_ready():
    bot.add_view(TicketButton())
    bot.add_view(CloseButton())
    print(f"Bot {bot.user} Online!")
    try: await bot.tree.sync()
    except Exception as e: print(e)

@bot.tree.command(name="setup-ticket", description="Pasang panel ticket")
async def setup_ticket(interaction: discord.Interaction):
    embed = discord.Embed(title="Order Here!", description="Selamat datang di layanan pemesanan Buxbee Store🐝! Gunakan fitur ini untuk melakukan pemesanan atau bertanya seputar produk kami.\n\n📋 **CARA MEMBUKA TICKET**\n1. Klik tombol di bawah ini.\n2. Channel privat baru akan muncul untuk kamu.", color=0xFFD700)
    await interaction.channel.send(embed=embed, view=TicketButton())
    await interaction.response.send_message("Panel ticket berhasil dipasang!", ephemeral=True)

bot.run(TOKEN)
