import asyncio
from re import A, M, T
import discord
from discord import client
from discord import embeds
from discord import user
from discord import colour
from discord.colour import Color
from discord.ext import commands
import json
import os
import random


os.chdir("D:\\Oom\\หางาน\\code\\Project-Sompong100")

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='e!', intents=intents)

@client.event
async def on_ready() :
    print("Bot Started!")

@client.command()
async def balance(mackngo): #เช็กยอดคงเหลือ
    await open_account(mackngo.author)
    user = mackngo.author
    users = await databank()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"] 

    em = discord.Embed(title = f"{mackngo.author.name}'s balance", color = 0xff8b94)
    em.add_field(name="Wallet balance", value=wallet_amt)
    em.add_field(name="Bank balance", value=bank_amt)
    await mackngo.send(embed = em)

@client.command()
async def send(ctx, member:discord.Member, amount = None): #โอนเงิน
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        embed = discord.Embed(title="Please enter the amount.",color=0xffc0cb)
        await ctx.send(embed=embed)
        return
    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[1]:
        embed = discord.Embed(title="You don't have enough money;)",color=0xb0e0e6)
        await ctx.send(embed=embed)
        return
    if amount < 0:
        embed = discord.Embed(title="Amount must more than zero.",color=0xfff68f)
        await ctx.send(embed=embed)
        return

    await update_bank(ctx.author, -amount, "bank")
    await update_bank(member, amount, "bank")

    await ctx.send(f"You gave {member} {amount} coins!")

@client.command()
async def withdraw(mackngo, amount = None): #ถอนเงิน
    await open_account(mackngo.author)

    if amount == None:
        embed = discord.Embed(title="Please enter the amount.",color=0xffc0cb)
        await mackngo.send(embed=embed)
        return
    
    bal = await update_bank(mackngo.author)

    amount = int(amount)
    if amount > bal[1]:
        embed = discord.Embed(title="You don't have enough money;)",color=0xb0e0e6)
        await mackngo.send(embed=embed)
        return
    if amount < 0:
        embed = discord.Embed(title="Amount must more than zero.",color=0xfff68f)
        await mackngo.send(embed=embed)
        return

    await update_bank(mackngo.author, amount)
    await update_bank(mackngo.author, -amount, "bank")

    embed = discord.Embed(title=f"You withdrew {amount} coins!",color=0xff80ed)
    await mackngo.send(embed=embed)

@client.command()
async def deposit(mackngo, amount = None): #ฝากเงิน
    await open_account(mackngo.author)

    if amount == None:
        embed = discord.Embed(title="Please enter the amount.",color=0xffc0cb)
        await mackngo.send(embed=embed)
        return
    
    bal = await update_bank(mackngo.author)

    amount = int(amount)
    if amount > bal[0]:
        embed = discord.Embed(title="You don't have enough money;)",color=0xb0e0e6)
        await mackngo.send(embed=embed)
        return
    if amount < 0:
        embed = discord.Embed(title="Amount must more than zero.",color=0xfff68f)
        await mackngo.send(embed=embed)
        return

    await update_bank(mackngo.author, -amount)
    await update_bank(mackngo.author, amount, "bank")

    embed = discord.Embed(title=f"You deposited {amount} coins!",color=0xff80ed)
    await mackngo.send(embed=embed)

@client.command()
async def bet(mackngo): #เสี่ยงดวง
    await open_account(mackngo.author)

    users = await databank()
    user = mackngo.author
    earnings = random.randrange(1,11)
    losemoney = random.randrange(1, 1001)
    if  earnings <= 6:
        losemoney = -losemoney
        embed = discord.Embed(title="Oops! You lose %d coins!" %losemoney,color=0xff4040)
        await mackngo.send(embed=embed)
    elif earnings > 6 and earnings < 10:
        embed = discord.Embed(title="You recieve %d coins!" %losemoney,color=0x00ff7f)
        await mackngo.send(embed=embed)
    else:
        losemoney = 0
        embed = discord.Embed(title="Go Find a job!!",color=0x3399ff)
        await mackngo.send(embed=embed)

    users[str(user.id)]["wallet"] += losemoney
    
    with open("bank.json", "w") as f:
        json.dump(users, f)

@client.command()
async def rps(mackngo):  #เป่ายิ้งฉุบ
    await open_account(mackngo.author)
    users = await databank()
    user = mackngo.author
    embed = discord.Embed(title="ต้องการลงเดิมพันเท่าไหร่",color=0x40e0d0)
    await mackngo.send(embed=embed)
    bet = await client.wait_for("message")
    lostmoney = int(bet.content) *2
    if int(bet.content) > users[str(user.id)]["wallet"]:
        embed = discord.Embed(title="ยอดเงินคุณไม่เพียงพอที่จะลงเดิมพัน",color=0xff0000)
        await mackngo.send(embed=embed)
    else:
        while True:
            message = await mackngo.send("เป่า ยิ้ง ฉุบบ")
            await message.add_reaction("🔨")
            await message.add_reaction("✂️")
            await message.add_reaction("📄")
            number = random.randint(0,3)
            ans = ["Rock", "Paper", "Scissors", "My Love"]
            check = lambda r, u: u == mackngo.author and str(r.emoji) in "🔨✂️📄"
            try:
                reaction, user = await client.wait_for("reaction_add", check= check, timeout=60)
            except asyncio.TimeoutError:
                await mackngo.send("ช้าไปป่าวน้องง")
            if str(reaction.emoji) == "🔨":
                await mackngo.send("ฉันจะออกอะไรดีน้าาาา")
                if ans[number] == "Rock":
                    await mackngo.send("ฉันจะออก", file=discord.File("Rock.png"))
                    await mackngo.send("เสมอจ้าเอาใหม่อีกครั้งนะ")
                elif ans[number] == "Paper":
                    await mackngo.send("ฉันจะออก", file=discord.File("paper.png"))
                    await mackngo.send("ยินดีด้วยคุณเสียเงิน %d Coins" %lostmoney)
                    users[str(user.id)]["wallet"] -= lostmoney
                    break
                elif ans[number] == "My Love":
                    await mackngo.send("เสียใจด้วยนะแต่ความรักของฉันจะชนะทุกอย่าง", file=discord.File("Mylove.png"))
                    users[str(user.id)]["wallet"] -= lostmoney / 2
                    break
                else:
                    await mackngo.send("ฉันจะออก", file=discord.File("scissors.png"))
                    await mackngo.send("ยินดีด้วยคุณได้เงิน %d Coins" %lostmoney)
                    users[str(user.id)]["wallet"] += lostmoney / 2
                    break
            elif str(reaction.emoji) == "✂️":
                await mackngo.send("ฉันจะออกอะไรดีน้าาาา")
                if ans[number] == "Rock":
                    await mackngo.send("ฉันจะออก", file=discord.File("Rock.png"))
                    await mackngo.send("ยินดีด้วยคุณได้เสียเงิน %d Coins" %lostmoney)
                    users[str(user.id)]["wallet"] -= lostmoney
                    break
                elif ans[number] == "Paper":
                    await mackngo.send("ฉันจะออก", file=discord.File("paper.png"))
                    await mackngo.send("ยินดีด้วยคุณได้รับเงิน %d Coins" %lostmoney)
                    users[str(user.id)]["wallet"] += lostmoney / 2
                    break
                elif ans[number] == "My Love":
                    await mackngo.send("เสียใจด้วยนะแต่ความรักของเราจะชนะทุกอย่าง", file=discord.File("Mylove.png"))
                    users[str(user.id)]["wallet"] -= lostmoney / 2
                    break
                else:
                    await mackngo.send("ฉันจะออก", file=discord.File("scissors.png"))
                    await mackngo.send("เสมอจ้าเอาใหม่อีกครั้งนะ")
            else:
                await mackngo.send("ฉันจะออกอะไรดีน้าาาา")
                if ans[number] == "Rock":
                    await mackngo.send("ฉันจะออก", file=discord.File("Rock.png"))
                    await mackngo.send("ยินดีด้วยคุณได้รับเงิน %d Coins" %lostmoney)
                    users[str(user.id)]["wallet"] += lostmoney / 2
                    break
                elif ans[number] == "Paper":
                    await mackngo.send("ฉันจะออก", file=discord.File("paper.png"))
                    await mackngo.send("เสมอจ้าเอาใหม่อีกครั้งนะ")
                elif ans[number] == "My Love":
                    await mackngo.send("เสียใจด้วยนะแต่ความรักของเราจะชนะทุกอย่าง", file=discord.File("Mylove.png"))
                    users[str(user.id)]["wallet"] -= lostmoney / 2
                    break
                else:
                    await mackngo.send("ฉันจะออก", file=discord.File("scissors.png"))
                    await mackngo.send("ยินดีด้วยคุณเสียเงิน %d Coins" %lostmoney)
                    users[str(user.id)]["wallet"] -= lostmoney
                    break
    with open("bank.json", "w") as f:
        json.dump(users, f)
    gak = discord.Embed(title = f"ตอนนี้คุณ {mackngo.author.name}'s", color = discord.Color.dark_gold())
    gak.add_field(name= "มีเงินทั้งหมด", value= users[str(user.id)]["wallet"])
    await mackngo.send(embed = gak)

@client.command()
async def guess(mackngo): #เกมทายเลข
    await open_account(mackngo.author)
    users = await databank()
    user = mackngo.author
    embed = discord.Embed(title="ต้องการลงเดิมพันเท่าไหร่",color=0xc04df9)
    await mackngo.send(embed=embed)
    bet = await client.wait_for("message")
    if int(bet.content) > users[str(user.id)]["wallet"]:
        embed = discord.Embed(title="ยอดเงินคุณไม่เพียงพอที่จะลงเดิมพัน",color=0xff3f3f)
        await mackngo.send(embed=embed)
    else:
        tbet = int(bet.content)
        users[str(user.id)]["wallet"] -= tbet
        number = random.randint(0, 100)
        em = discord.Embed(title = f"สวัสดีดีคุณ {mackngo.author.name} ยินดีที่คุณมาเล่นเกมส์กับเรา",\
            description = "ในห้องเกมทายใจของเราๆจะสุ่มตัวเลขขึ้นมา 1 ตัวและให้คุณทาย ถ้าคุณทายถูกรับ ไปเลย เงิน 2 เท่า จากเงินเดิมพัน เอาล่ะถ้าพร้อมแล้วพิมพ์เลขลงมาเลย!!", color = discord.Color.dark_gold())
        await mackngo.send(embed = em)
        for i in range(5):
            respone = await client.wait_for("message")
            num = int(respone.content)
            if num > number:
                embed = discord.Embed(title="มากไป",color=0xd11141)
                await mackngo.send(embed=embed)
                if 5 - (i+1) == 0:
                    embed = discord.Embed(title="เสียใจด้วยและคำตอบที่ถูกต้องก็คืออออ %d!!!" %number,color=0xffc425)
                    await mackngo.send(embed=embed)
            elif num < number:
                embed = discord.Embed("น้อยไป",color=0xf37735)
                await mackngo.send(embed=embed)
                if 5 - (i+1) == 0:
                    embed = discord.Embed(title="เสียใจด้วยและคำตอบที่ถูกต้องก็คืออออ %d!!!" %number,color=0xffc425)
                    await mackngo.send(embed=embed)
            else:
                embed = discord.Embed(title='ยินดีด้วย!!คุณได้รับเงินเป็นจำนวน %d Coin!!' %(tbet*2),color=0x00aedb)
                await mackngo.send(embed=embed)
                users[str(user.id)]["wallet"] += tbet * 2
                break
        with open("bank.json", "w") as f:
            json.dump(users, f)
    gak = discord.Embed(title = f"ตอนนี้คุณ {mackngo.author.name}'s", color = discord.Color.dark_gold())
    gak.add_field(name= "มีเงินทั้งหมด", value= users[str(user.id)]["wallet"])
    await mackngo.send(embed = gak)

async def open_account(user): #เปิดบัญชี

    users = await databank()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("bank.json", "w") as f:
        json.dump(users, f)
    return True

@client.command()
async def test(ctx):
    embed = discord.Embed(color=0x00ff00) #creates embed
    embed.set_image(url="https://lh3.googleusercontent.com/HBrh0QUd2MjeFDiEi_epX4Pq5ChH3kgpqxIbr-BxaiX5PYSHnZmqvrAY2ArBaoJ3IM2aeg=s85")
    await ctx.send(embed=embed)

@client.command()
async def quiz(ctx): #เกมตอบคำถาม
    await open_account(ctx.author)
    users = await databank()
    user = ctx.author
    
    with open("allquestion.json", "r") as f:
        ask = json.load(f)
    question = random.choice(list(ask.keys()))
    ans = ask[question][2]
    
    em = discord.Embed(title = 'Question', color = discord.Color.lighter_grey())
    em.add_field(name=question, value= '**1) ** %s\n**2) ** %s' %(ask[question][0], ask[question][1]))
    await ctx.send(embed = em)
    
    ansuser = await client.wait_for("message")
    if ansuser.content == '1':
        answer = ask[question][0]
    if ansuser.content == '2':
        answer = ask[question][1]
    if ans == answer:
        em = discord.Embed(title = 'ถูกต้องนะคร้าบบบบบ รับไปเลย 10 coins', color = discord.Color.random())
        await ctx.send(embed = em)
        users[str(user.id)]["wallet"] += 10
    else:
        em = discord.Embed(title = 'ทำไมโง่อ่า ตอบ %s ตะหาก' %(ans), color = discord.Color.red())
        await ctx.send(embed = em)

@client.command()
async def addquiz(ctx): #เพิ่มโจทย์
    await ctx.send("ระบุคำถาม")
    quiz = await client.wait_for("message")
    await ctx.send("ระบุตัวเลือกที่ 1")
    ch1 = await client.wait_for("message")
    await ctx.send("ระบุตัวเลือกที่ 2")
    ch2 = await client.wait_for("message")
    await ctx.send("ระบุคำตอบ")
    ans = await client.wait_for("message")
    with open("allquestion.json", "r") as f:
        allquiz = json.load(f)
    allquiz.update({quiz.content: [ch1.content, ch2.content, ans.content]})
    json.dump(allquiz, open("allquestion.json", "w"))

@client.command()
async def bj(ctx): #สลอต
    await open_account(ctx.author)
    users = await databank()
    user = ctx.author
    bed = discord.Embed(title="ต้องการลงเดิมพันเท่าไหร่",color=0xc04df9)
    await ctx.send(embed=bed)
    usercoin = await client.wait_for("message")
    if int(usercoin.content) > users[str(user.id)]["wallet"]:
        embest = discord.Embed(title="ยอดเงินคุณไม่เพียงพอที่จะลงเดิมพัน",color=0xff3f3f)
        await ctx.send(embed=embest)
    else:
        tbet = int(usercoin.content)
        emoji = ["A ♣", "2 ♣", "3 ♣", "4 ♣", "5 ♣", "6 ♣", "7 ♣", "8 ♣", "9 ♣", "10 ♣", "J ♣", "Q ♣", "K ♣", \
        "A ♠", "2 ♠", "3 ♠", "4 ♠", "5 ♠", "6 ♠", "7 ♠", "8 ♠", "9 ♠", "10 ♠", "J ♠", "Q ♠", "K ♠", \
            "A ♥", "2 ♥", "3 ♥", "4 ♥", "5 ♥", "6 ♥", "7 ♥", "8 ♥", "9 ♥", "10 ♥", "J ♥", "Q ♥", "K ♥", \
                "A ♦", "2 ♦", "3 ♦", "4 ♦", "5 ♦", "6 ♦", "7 ♦", "8 ♦", "9 ♦", "10 ♦", "J ♦", "Q ♦", "K ♦"]
        scoreplayer = 0
        scorebanker = 0
        checka = 0
        checkb = 0
        player = ""
        banker = ""
        for _ in range(2):
            players = random.choice(emoji)
            emoji.remove(players)
            if players[0] == "A":
                scoreplayer += 1
                checka += 1
            elif players[0] == "J" or players[0] == "Q" or players[0] == "K" or players[0] == "1":
                scoreplayer += 10
            else:
                scoreplayer += int(players[0])
            player += players + " "
        while scorebanker <= 12:
            bankers = random.choice(emoji)
            emoji.remove(bankers)
            if bankers[0] == "A":
                scorebanker += 1
                checkb += 1
            elif bankers[0] == "J" or bankers[0] == "Q" or bankers[0] == "K" or bankers[0] == "1":
                scorebanker += 10
            else:
                scorebanker += int(bankers[0])
            banker += bankers + " "
        if scorebanker <= 11 and checkb > 0:
            scorebanker += 10
        while True:
            if scorebanker == 21:
                break
            elif scoreplayer >= 21:
                break
            embed = discord.Embed(title = "Blackjack Game", color = discord.Color.random())
            embed.add_field(name= "Rules", value= "ถ้าไพ่ของคุณใกล้เคียง 21 หรือมากกว่าฝ่ายของ Banker จะทำให้คุณ'ชนะ'แต่ถ้าไพ่คุณเกิน 21 ถือว่าคุณแพ้ทันที", inline=False)
            embed.add_field(name= "Player Cards", value= "%s\n Score %s" %(player, str(scoreplayer)), inline=True)
            embed.add_field(name= "Banker Cards", value= "❓ ❓\n Score ลุ้นหน่อยอร่อยแน่", inline=True)
            embed.set_footer(text="และ ถ้าเกิดคุณมีไพ่ A ละแต้มรวมของคุณน้อยกว่า 11 ไพ่ของคุณจะบวกทันที 10 แต้ม หรือถ้าคุณเสมอกะbankerก็จะถือว่าคุณแพ้")
            await ctx.send(embed = embed)
            em = discord.Embed(title = "Exclusive Rules!", color = discord.Color.random())
            em.add_field(name= "ถ้าคุณพิมคำว่า 'hit' ", value= "แปลว่าคุณต้องการไพ่เพิ่มแต่ถ้าไพ่คุณมากกว่า 21 จะถือว่าคุณแพ้ทันที!!")
            em.add_field(name= "แต่ถ้าคุณพิมพ์คำว่า 'stand'", value= "แปลว่าคุณไม่ต้องการไพ่เพิ่มและเริ่มนับคะแนนทันที")
            await ctx.send(embed = em)
            playersend = await client.wait_for("message")
            if playersend.content == "hit":
                players = random.choice(emoji)
                emoji.remove(players)
                if players[0] == "A":
                    scoreplayer += 1
                    checka += 1
                elif players[0] == "J" or players[0] == "Q" or players[0] == "K" or players[0] == "1":
                    scoreplayer += 10
                else:
                    scoreplayer += int(players[0])
                player += players + " "
            elif playersend.content == "stand":
                break
            else:
                await ctx.send("ส่งไรมาอะเห้ยยยไม่รู้เรื่องไปส่งมาใหม่")
    if scoreplayer <= 11 and checka > 0:
        scoreplayer += 10
    embed = discord.Embed(title = "Blackjack Game", color = discord.Color.random())
    embed.add_field(name= "Rules", value= "ถ้าไพ่ของคุณใกล้เคียง 21 หรือมากกว่าฝ่ายของ Banker จะทำให้คุณ'ชนะ'แต่ถ้าไพ่คุณเกิน 21 ถือว่าคุณแพ้ทันที", inline=False)
    embed.add_field(name= "Player Cards", value= "%s\n Score %s" %(player, str(scoreplayer)), inline=True)
    embed.add_field(name= "Banker Cards", value= "%s\n Score %s" %(banker, str(scorebanker)), inline=True)
    embed.set_footer(text="และ ถ้าเกิดคุณมีไพ่ A ละแต้มรวมของคุณน้อยกว่า 11 ไพ่ของคุณจะบวกทันที 10 แต้ม หรือถ้าคุณเสมอกะbankerก็จะถือว่าคุณแพ้")
    await ctx.send(embed = embed)
    lastmoney = tbet * 2
    if scoreplayer > 21:
        embed = discord.Embed(title = "เสียใจด้วยคุณแพ้ลองใหม่นะจ๊ะ", color = discord.Color.random())
        await ctx.send(embed = embed)
        users[str(user.id)]["wallet"] -= tbet
        with open("bank.json", "w") as f:
            json.dump(users, f)
    elif scoreplayer > 21 and scorebanker > 21:
        embed = discord.Embed(title = "เสียใจด้วยคุณแพ้ลองใหม่นะจ๊ะ", color = discord.Color.random())
        await ctx.send(embed = embed)
        users[str(user.id)]["wallet"] -= tbet
        with open("bank.json", "w") as f:
            json.dump(users, f)
    elif scoreplayer <= scorebanker:
        embed = discord.Embed(title = "เสียใจด้วยคุณแพ้ลองใหม่นะจ๊ะ", color = discord.Color.random())
        await ctx.send(embed = embed)
        users[str(user.id)]["wallet"] -= tbet
        with open("bank.json", "w") as f:
            json.dump(users, f)
    elif scorebanker > 21 or scorebanker <= scoreplayer:
        embed = discord.Embed(title = "ดีใจด้วยคุณชนะ!!คุณได้เงินจำนวน %d เอากำไรมาเล่นอีกรอบสิ อิอิ" %lastmoney, color = discord.Color.random())
        await ctx.send(embed = embed)
        users[str(user.id)]["wallet"] += tbet * 2
        users[str(user.id)]["wallet"] -= tbet
        with open("bank.json", "w") as f:
            json.dump(users, f)
    gak = discord.Embed(title = f"ตอนนี้คุณ {ctx.author.name}'s", color = discord.Color.dark_gold())
    gak.add_field(name= "มีเงินทั้งหมด", value= users[str(user.id)]["wallet"])
    await ctx.send(embed = gak)
@client.command()
async def slot(ctx): #สลอต
    await open_account(ctx.author)
    users = await databank()
    user = ctx.author

    emoji = ['🍎', '🍐', '🍊', '🍋', '🍉', '🍇', '🍓', '🥑', '🍑', '🌽', '🍆', '🥕', '🍍', '🌸', '🌻']
    i, j, k = random.choice(emoji), random.choice(emoji), random.choice(emoji)
    if i == j == k:
        result = 'Congrats! You received 250 coins.'
        users[str(user.id)]["wallet"] += 250
    elif i != j and j != k and i != k:
        result = 'Sorry, you lost 50 coins. How pathetic ;P'
        users[str(user.id)]["wallet"] -= 50
    else:
        result = 'Unfortunately, you neither recived nor lost. Pls try again'
    em = discord.Embed(title = 'Slot 🎰', color = discord.Color.random())
    em.add_field(name='Reels', value= '**> > %s %s %s <**\nResult: *%s*' %(i, j, k, result))
    await ctx.send(embed = em)
    
    with open("bank.json", "w") as f:
        json.dump(users, f)
@client.command()
async def rank(ctx): #แสดงบัญชีที่มียอดเงินสูงสุดสามคนแรก
    users = await databank()
    mylist = []
    with open("bank.json", "r") as f:
        user = json.load(f)
    
    for i in user:
        bal = [users[str(i)]["wallet"], users[str(i)]["bank"]]
        bals = bal[0] + bal[1]
        mylist.append([bals, str(i)])
        bal.clear()
    mylist.sort(reverse=True)
    gak = discord.Embed(title = "Rank", color = discord.Color.magenta())
    usersort = await client.fetch_user(mylist[0][1])
    usersort2 = await client.fetch_user(mylist[1][1])
    usersort3 = await client.fetch_user(mylist[2][1])
    gak.add_field(name="อันดับ", value = "1\n2\n3")
    gak.add_field(name="user", value = "%s\n%s\n%s" %(str(usersort)[:-5],str(usersort2)[:-5],str(usersort3)[:-5]))
    gak.add_field(name="Coins", value= "%s\n%s\n%s" %(mylist[0][0],mylist[1][0],mylist[2][0]))
    await ctx.send(embed = gak)

async def databank(): #ดึงข้อมูลจาก bank.json
    with open("bank.json", "r") as f:
        users = json.load(f)

    return users
    
async def update_bank(user, change=0, mode="wallet"): #อัพเดตยอดเงินใน bank.json
    users = await databank()

    users[str(user.id)][mode] += change

    with open("bank.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal

client.run(DISCORD_BOT_TOKEN)
