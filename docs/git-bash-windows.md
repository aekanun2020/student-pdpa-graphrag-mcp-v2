# คู่มือ Git Bash บน Windows สำหรับผู้ที่ไม่เคยใช้ Git

> **สถานะ: ยังไม่ได้ทดสอบบนเครื่อง Windows จริง และไม่มีภาพหน้าจอ**
> ชื่อหน้าและตัวเลือกของตัวติดตั้งคัดจากเว็บ git-scm.com และจากสคริปต์ตัวติดตั้งของ Git for Windows (อ่านเมื่อ 26 พ.ย. 2569)
> ข้อที่เขียนจากความรู้ทั่วไปและยังไม่มีแหล่งยืนยัน มีคำว่า "(ยังไม่ได้ยืนยัน)" กำกับ
> ย่อหน้าที่ขึ้นต้นว่า "สิ่งที่จะเห็น" บรรยายหน้าจอเป็นข้อความแทนภาพ ผู้เขียนยังไม่ได้เห็นหน้าจอจริงของรุ่นนี้ หน้าจอของคุณอาจต่างไปเล็กน้อย

คู่มือนี้พาติดตั้ง Git for Windows เปิดโปรแกรม Git Bash และใช้คำสั่งพื้นฐานเท่าที่ LAB ของคอร์สนี้ต้องใช้

## 1. Git Bash คืออะไร และทำไมต้องใช้

- **Git** คือโปรแกรมที่ใช้ดึงโค้ดของคอร์สจาก GitHub ลงเครื่อง
- **Git for Windows** คือชุดติดตั้ง Git สำหรับ Windows ในชุดนี้มีโปรแกรมชื่อ **Git Bash** มาด้วย
- **Git Bash** คือหน้าต่างพิมพ์คำสั่งแบบเดียวกับ Terminal ของ macOS และ Linux คำสั่งของ LAB ในสไลด์เขียนแบบนี้
  บางคำสั่ง เช่น `cmp` ใช้ใน Command Prompt ของ Windows ไม่ได้ จึงให้พิมพ์ใน Git Bash แทน

## 2. ดาวน์โหลดตัวติดตั้ง

1. เปิดเว็บ https://git-scm.com/install/windows
2. กดลิงก์ **Click here to download** ซึ่งเป็นตัวติดตั้งชื่อ "Git for Windows/x64 Setup"
   เครื่องที่ใช้ชิป ARM ให้เลือก "Git for Windows/ARM64 Setup" แทน
3. จะได้ไฟล์ `.exe` 1 ไฟล์ในโฟลเดอร์ Downloads

รุ่นล่าสุดเมื่อ 26 พ.ย. 2569 คือ 2.56.1 รุ่นที่ใหม่กว่านี้ใช้ได้เหมือนกัน หน้าตาของตัวติดตั้งอาจต่างจากคู่มือเล็กน้อย

**สิ่งที่จะเห็น:** หน้าเว็บมีบรรทัดบอกรุ่นล่าสุด (เช่น "Latest version: 2.56.1") และลิงก์ Click here to download
ใต้ลงมามีรายการตัวเลือกอื่น คือ "Git for Windows/x64 Setup", "Git for Windows/ARM64 Setup", "Git for Windows/x64 Portable" และ "Git for Windows/ARM64 Portable"
ผู้ใช้ทั่วไปใช้ตัวแรก ไม่ต้องใช้แบบ Portable

## 3. ติดตั้ง

ดับเบิลคลิกไฟล์ `.exe` ที่ดาวน์โหลดมา ถ้า Windows ถามว่าอนุญาตให้โปรแกรมนี้แก้ไขเครื่องหรือไม่ ให้กด Yes (ยังไม่ได้ยืนยัน)

ตัวติดตั้งมีหลายหน้า **ทุกหน้าให้ใช้ค่าที่ตั้งมาแล้ว แล้วกด Next** ไม่ต้องเปลี่ยนตัวเลือกใด
ตารางนี้บอกหน้าที่จะเจอเรียงตามลำดับ และค่าที่ตั้งมา เพื่อให้เทียบกับหน้าจอได้

| ลำดับ | ชื่อหน้า | ค่าที่ตั้งมา | ต้องทำอะไร |
|---|---|---|---|
| 1 | หน้าข้อตกลงการใช้งาน (GNU General Public License) | | กด Next |
| 2 | Select Destination Location | `C:\Program Files\Git` | กด Next |
| 3 | Select Components | มีเครื่องหมายถูกที่ "Windows Explorer integration" ซึ่งรวม "Open Git Bash here" | กด Next |
| 4 | Select Start Menu Folder | Git | กด Next |
| 5 | Choosing the default editor used by Git | Vim | กด Next |
| 6 | Adjusting the name of the initial branch in new repositories | Let Git decide | กด Next |
| 7 | Adjusting your PATH environment | Git from the command line and also from 3rd-party software | กด Next |
| 8 | Choosing the SSH executable | Use bundled OpenSSH | กด Next |
| 9 | Choosing HTTPS transport backend | Use the native Windows Secure Channel library | กด Next |
| 10 | Configuring the line ending conversions | Checkout Windows-style, commit Unix-style line endings | กด Next |
| 11 | Configuring the terminal emulator to use with Git Bash | Use MinTTY (the default terminal of MSYS2) | กด Next |
| 12 | Choose the default behavior of `git pull` | Merge | กด Next |
| 13 | Choose a credential helper | Git Credential Manager | กด Next |
| 14 | Configuring extra options | Enable file system caching | กด Install |
| 15 | หน้าสุดท้าย | "View Release Notes" มีเครื่องหมายถูก และ "Launch Git Bash" ไม่มี | เอาเครื่องหมายถูกที่ "View Release Notes" ออก ใส่ที่ "Launch Git Bash" แล้วกด Finish |

- บางเครื่องจะไม่เจอหน้าที่ 2, 4 และ 8 และบางรุ่นมีหน้าเพิ่ม เช่น "Configuring experimental options" ให้กด Next โดยไม่เลือกอะไร
- ชื่อหน้าที่ 2 และ 4 กับปุ่ม Install ในหน้าที่ 14 เขียนจากความรู้ทั่วไป (ยังไม่ได้ยืนยัน)

**หน้าที่ 10 เกี่ยวกับ LAB ของคอร์ส:** ค่าที่ตั้งมาทำให้ Git เปลี่ยนท้ายบรรทัดของไฟล์เป็นแบบ Windows ตอนดึงโค้ด ไฟล์ `.sh` ที่ถูกเปลี่ยนแล้วอาจรันไม่ได้
ไม่ต้องเปลี่ยนตัวเลือกในหน้านี้ แต่ตอนดึงโค้ดของคอร์สให้ใช้คำสั่งในหัวข้อ 7 ซึ่งสั่ง Git ไม่ให้เปลี่ยนท้ายบรรทัด

**สิ่งที่จะเห็นในหน้า Select Components:** รายการที่มีช่องให้ติ๊ก รายการที่ติ๊กมาแล้วคือ "Windows Explorer integration" (มีรายการย่อย "Open Git Bash here" และ "Open Git GUI here"),
"Git LFS (Large File Support)", "Associate .git* configuration files with the default text editor" และ "Associate .sh files to be run with Bash"
รายการที่ยังไม่ติ๊ก เช่น "On the Desktop", "Check daily for Git for Windows updates" และ "Add a Git Bash Profile to Windows Terminal" ปล่อยไว้ตามเดิม
ถ้าอยากได้ไอคอน Git Bash บน Desktop ติ๊ก "On the Desktop" เพิ่มได้

**สิ่งที่จะเห็นในหน้า Adjusting your PATH environment:** ตัวเลือก 3 ข้อให้เลือก 1 ข้อ

- Use Git from Git Bash only
- Git from the command line and also from 3rd-party software (ข้อนี้ถูกเลือกมาแล้ว และมีคำว่า Recommended)
- Use Git and optional Unix tools from the Command Prompt

**สิ่งที่จะเห็นในหน้า Configuring the line ending conversions:** ตัวเลือก 3 ข้อให้เลือก 1 ข้อ

- Checkout Windows-style, commit Unix-style line endings (ข้อนี้ถูกเลือกมาแล้ว)
- Checkout as-is, commit Unix-style line endings
- Checkout as-is, commit as-is

**สิ่งที่จะเห็นในหน้าสุดท้าย:** ข้อความว่าติดตั้งเสร็จ และช่องให้ติ๊ก 2 ช่อง คือ "Launch Git Bash" กับ "View Release Notes" พร้อมปุ่ม Finish

## 4. เปิด Git Bash

มี 2 วิธี

- **จากเมนู Start:** กดปุ่ม Windows พิมพ์ `Git Bash` แล้วกด Enter
- **จากโฟลเดอร์:** เปิด File Explorer ไปที่โฟลเดอร์ที่ต้องการ คลิกขวาที่ที่ว่างในโฟลเดอร์ แล้วเลือก "Open Git Bash here"
  บน Windows 11 ต้องเลือก "Show more options" ก่อน (ยังไม่ได้ยืนยัน)

จะได้หน้าต่างสีดำที่มีบรรทัดลงท้ายด้วยเครื่องหมาย `$` เครื่องหมายนี้บอกว่าพร้อมรับคำสั่ง
ในคู่มือและในสไลด์ ไม่ต้องพิมพ์เครื่องหมาย `$` ให้พิมพ์เฉพาะคำสั่ง แล้วกด Enter

**สิ่งที่จะเห็นในเมนู Start:** หลังติดตั้งจะมีรายการของ Git 5 รายการ คือ Git Bash, Git CMD, Git GUI, Git Release Notes และ Git FAQs ให้เลือก **Git Bash**

**สิ่งที่จะเห็นในหน้าต่าง Git Bash:** บรรทัดบนเป็นชื่อผู้ใช้ ชื่อเครื่อง คำว่า `MINGW64` และโฟลเดอร์ปัจจุบัน บรรทัดถัดมาเป็นเครื่องหมาย `$` กับตัวชี้ตำแหน่งพิมพ์ หน้าตาประมาณนี้ (ยังไม่ได้ยืนยัน)

```text
somchai@DESKTOP-ABC123 MINGW64 ~
$
```

`~` ท้ายบรรทัดแรกบอกว่าตอนนี้อยู่ที่โฟลเดอร์หลักของผู้ใช้ เมื่อเข้าโฟลเดอร์อื่น ส่วนนี้จะเปลี่ยนตาม

## 5. ตรวจว่าติดตั้งสำเร็จ

พิมพ์คำสั่งนี้แล้วกด Enter

```sh
git --version
```

ต้องได้บรรทัดที่ขึ้นต้นว่า `git version` ตามด้วยเลขรุ่น ถ้าได้ข้อความว่าไม่พบคำสั่ง ให้ปิด Git Bash แล้วติดตั้งใหม่ตามหัวข้อ 3

**สิ่งที่จะเห็น:** บรรทัดเดียว หน้าตาประมาณนี้ เลขรุ่นจะตรงกับรุ่นที่ติดตั้ง (รูปแบบของบรรทัดยังไม่ได้ยืนยัน)

```text
$ git --version
git version 2.56.1.windows.1
```

## 6. คำสั่งพื้นฐานที่ต้องรู้

| คำสั่ง | ทำอะไร |
|---|---|
| `pwd` | บอกว่าตอนนี้อยู่ที่โฟลเดอร์ใด |
| `ls` | แสดงรายชื่อไฟล์และโฟลเดอร์ในโฟลเดอร์ปัจจุบัน |
| `cd ชื่อโฟลเดอร์` | เข้าโฟลเดอร์ |
| `cd ..` | ถอยออก 1 ชั้น |
| `cd ~` | กลับไปโฟลเดอร์หลักของผู้ใช้ |
| `clear` | ล้างหน้าจอ |

ข้อที่ต่างจาก Command Prompt

- **path ใช้เครื่องหมาย `/`** ไดรฟ์ C เขียนว่า `/c` เช่น `C:\Users\somchai\Documents` เขียนเป็น `/c/Users/somchai/Documents`
- **`~` คือโฟลเดอร์หลักของผู้ใช้** เช่น `C:\Users\somchai`
- **การวางข้อความ:** กด Shift+Insert หรือคลิกขวาแล้วเลือก Paste ส่วน Ctrl+V ใช้ไม่ได้ในค่าตั้งต้น (ยังไม่ได้ยืนยัน)
- **การคัดลอก:** ลากเมาส์คลุมข้อความ แล้วกด Ctrl+Insert (ยังไม่ได้ยืนยัน)
- **ปุ่มลูกศรขึ้น** เรียกคำสั่งที่เคยพิมพ์กลับมา และ **ปุ่ม Tab** ช่วยเติมชื่อไฟล์ให้ครบ
- **หยุดคำสั่งที่ค้างอยู่** ด้วย Ctrl+C

**สิ่งที่จะเห็น:** ตัวอย่างเมื่อเพิ่งเปิด Git Bash จากเมนู Start ชื่อผู้ใช้และรายชื่อโฟลเดอร์จะเป็นของเครื่องคุณ (ยังไม่ได้ยืนยัน)

```text
$ pwd
/c/Users/somchai
$ cd Documents
$ pwd
/c/Users/somchai/Documents
$ cd ..
$ pwd
/c/Users/somchai
```

## 7. ดึงโค้ดของคอร์สลงเครื่อง

พิมพ์ 2 คำสั่งนี้ทีละบรรทัด

```sh
git clone -c core.autocrlf=false https://github.com/aekanun2020/student-pdpa-graphrag-mcp-v2.git
cd student-pdpa-graphrag-mcp-v2
```

- คำสั่งแรกสร้างโฟลเดอร์ `student-pdpa-graphrag-mcp-v2` ในโฟลเดอร์ที่อยู่ตอนนั้น แล้วดึงโค้ดทั้งหมดลงมา
- ส่วน `-c core.autocrlf=false` สั่ง Git ไม่ให้เปลี่ยนท้ายบรรทัดของไฟล์ ตามที่สไลด์ของ LAB 1 เขียนไว้สำหรับ Windows
- คำสั่งที่สองเข้าโฟลเดอร์ของโค้ด คำสั่งของทุก LAB ต้องรันจากโฟลเดอร์นี้

ครั้งต่อไปที่เปิด Git Bash ไม่ต้อง clone ซ้ำ ให้ `cd` เข้าโฟลเดอร์เดิม หรือเปิดด้วย "Open Git Bash here" จากโฟลเดอร์นั้น

**สิ่งที่จะเห็น:** คำสั่ง `git clone` พิมพ์บรรทัด `Cloning into 'student-pdpa-graphrag-mcp-v2'...` ตามด้วยบรรทัดบอกความคืบหน้าของการดึงไฟล์ แล้วกลับมาที่เครื่องหมาย `$`
หลังคำสั่ง `cd` บรรทัดบนของ Git Bash จะลงท้ายด้วยชื่อโฟลเดอร์ `student-pdpa-graphrag-mcp-v2` และมีคำว่า `(main)` ต่อท้าย ซึ่งเป็นชื่อ branch ของโค้ด (ส่วน `(main)` ยังไม่ได้ยืนยัน)

ตรวจว่าได้โค้ดครบด้วยคำสั่ง `ls` ต้องเห็นชื่อ เช่น `README.md`, `data`, `docs`, `examples`, `labs`, `lightrag` และ `scripts`

## 8. สิ่งที่ LAB ของคอร์สต้องใช้เพิ่ม

คำสั่งของแต่ละ LAB อยู่ในสไลด์และใน [README](../README.md) หัวข้อนี้บอกเฉพาะสิ่งที่ต่างบน Windows

| LAB | สิ่งที่ต่างบน Windows |
|---|---|
| LAB 2 และ LAB 3 | ใช้ `python` แทน `python3` ต้องติดตั้ง Python ก่อน |
| LAB 3 | คำสั่ง `cmp` มีใน Git Bash ไม่มีใน Command Prompt |
| LAB 4 | ไม่ต้องใช้ Git Bash: รัน `python labs/lab4/call_tools.py --url <URL ที่ผู้สอนให้>/mcp` แทนสคริปต์ `.sh` จึงไม่ต้องมี `curl` และ `jq` |

## 9. ปัญหาที่อาจเจอ

ทุกข้อในหัวข้อนี้เขียนจากความรู้ทั่วไป ยังไม่ได้ทดสอบบนเครื่อง Windows จริง

| อาการ | สาเหตุที่เป็นไปได้ | วิธีแก้ |
|---|---|---|
| `git: command not found` | ติดตั้งไม่สำเร็จ หรือเปิด Git Bash ค้างไว้ตั้งแต่ก่อนติดตั้ง | ปิดแล้วเปิด Git Bash ใหม่ ถ้ายังเป็น ให้ติดตั้งใหม่ |
| `python: command not found` | ยังไม่ได้ติดตั้ง Python หรือ Python ไม่อยู่ใน PATH | ติดตั้ง Python จาก python.org และเลือก "Add python.exe to PATH" ตอนติดตั้ง |
| รันไฟล์ `.sh` แล้วขึ้นข้อความที่มี `\r` | ไฟล์ถูกเปลี่ยนท้ายบรรทัดเป็นแบบ Windows | ลบโฟลเดอร์ของโค้ด แล้ว clone ใหม่ด้วยคำสั่งในหัวข้อ 7 |
| วางข้อความด้วย Ctrl+V ไม่ได้ | Git Bash ใช้ปุ่มวางคนละปุ่ม | กด Shift+Insert หรือคลิกขวาแล้วเลือก Paste |

ถ้าผลบนเครื่องของคุณต่างจากที่เขียนไว้ ให้แจ้งผู้สอน
