# Sompong100

## Project setup
[วิธีสร้าง Discord bot](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)

Install requirements
```python
pip install -r requirements.txt
```

คำสั่ง run
```python
py main.py
```

- เมื่อบอทพร้อมทำงาน จะขึ้น ```Bot Started!``` ใน terminal

หมายเหตุ:
- บรรทัดที่ 15 ```os.chdir("PROJECT_PATH")``` ให้แทนที่ PROJECT_PATH ด้วย path ของโฟลเดอร์โปรเจค
- บรรทัดสุดท้าย ```client.run("DISCORD_BOT_TOKEN")``` ให้แทนที่ DISCORD_BOT_TOKEN ด้วย Token ของ bot ที่สร้างขึ้น

## ระบบภายในบอท
1. ระบบแสดงยอดเงินของผู้เล่น 
คำสั่ง
```
e!balance
```
ระบบที่แสดงยอด token คงเหลือของผู้เล่นแต่ละคน โดยจะแบ่งออกเป็น  wallet balance (สามารถติดลบได้) กับ bank balance (ไม่สามารถติดลบได้) ซึ่ง coin ที่ใช้ในการเล่นเกมต่าง ๆ จะมากจากส่วนของ wallet balance และ coin ที่ใช้สำหรับการทำธุรกรรมระหว่างผู้เล่น จะเป็นส่วนของ bank balance ซึ่ง ถ้าจะใช้งาน bank balance ต้องทำการโอน coin มาจาก wallet balanceก่อน

2. ระบบโอนเงินให้ผู้เล่นคนอื่น
คำสั่ง
```
e!send (account) (amount)
```
ระบบที่ให้ผู้เล่นโอน coin จาก bank balance ของตัวเองให้กับ bank balance ของผู้เล่นคนอื่น โดยที่ coin ในส่วนนี้ไม่สามารถติดลบได้

3. ระบบถอนเงิน
คำสั่ง
```
e!withdraw (amount)
```
เป็นการถอน coin จาก bank balance ไปยัง wallet balance

4. ระบบฝากเงิน
คำสั่ง
```
e!deposit (amount)
```
เป็นการฝาก coin จาก wallet balance ไปยัง bank balance โดยก่อนที่จะฝาก token เข้าไปใน bank balance ยอด coin ใน wallet balance จะต้องไม่ติดลบ

5. ระบบจัดอันดับผู้เล่นจากยอดเงินสะสม
คำสั่ง
```
e!rank
```
เป็นการแสดง ผู้ใช้งาน3อันดับแรก ที่มี coinในระบบมากที่สุด

6. เกมทายตัวเลข 1-100
คำสั่ง
```
e!guess
```
เป็นเกมที่ให้โอกาส 5 ครั้ง กับผู้เล่นในการสุ่มเลขขึ้นมาให้ตรงกับเลขที่ระบบได้สุ่มมา

7. เกมเสี่ยงดวงรับหรือเสียเงิน
คำสั่ง
```
e!bet
```
เป็นการสุ่ม coin เข้ามาอยู่ในกระเป๋าตัง ตัวระบบก็ จะทำการสุ่ม ว่า ผู้เล่นจะเสียเงิน ได้ coin หรือ เท่าทุน coin ที่ได้ก็จะเป็นเงินในส่วนของwallet balance

8. เกมเป่ายิงฉุบ
คำสั่ง
```
e!rps
```
มีการเดิมพัน และ เป็นการกดอิโมจิตามสิ่งที่ต้องการจะออกเหมือนกับเล่น เป่ายิงฉุบจริง ๆ และระบบก็จะแสดงว่าตัวระบบใช้อะไรมาสู้กับเรา และก็จะแสดงยอด coin รวมในระบบของเราที่ได้เพิ่มจากการเดิมพัน ถ้าชนะ ก็จะได้ยอด coin เป็นสองเท่าของที่เดิมพัน

9. เกมตอบคำถาม
คำสั่ง
```
e!quiz
```
เป็นเกมที่จะมีคำถาม ทั้งคำถามที่เป็นความรู้ทั่วไป  คำถามกวนๆเบาสมอง และ ให้ผู้เล่นเลือกคำตอบที่ถูกต้อง ถ้าตอบถูก ก็จะได้ 10 coins

10. เกม SLOT
คำสั่ง
```
e!slot
```
เป็นการสุ่มอิโมจิ ให้เรียงสามตัว และ ถ้าเกิด อิโมจินั้นออกมาไม่เหมือนกันทั้ง3ตัว ก็จะโดนหักไป 50 coins และ ถ้า อิโมจิออกมาเหมือนกัน2ตัว ก็จะไม่ได้และไม่เสีย coin แต่ถ้า อิโมจิออกมาเหมือนกันทั้งหมด ก็จะ ได้รับ 250 coins

11. เกม black jack
คำสั่ง
```
e!bj
```
เป็นการเดิมพันที่ต้องรวมไพ่ในมือให้ได้เท่ากับ 21 หรือน้อยกว่า 21 แต่มากกว่า banker ถึงจะชนะ โดยที่ผู้เล่นจะไม่สามารถรู้ค่าของไพ่ของ banker ได้ ในตอนแรกไพ่จะสุ่มออกมาให้ผู้เล่น 2 ใบ หากผู้เล่นพอใจในผลรวมของไพ่แล้วให้กด stand แต่หากยังต้องการจั่วไพ่เพิ่มให้กด hit หากชนะจะได้เงินเป็นสองเท่าของเงินที่วางเดิมพัน
