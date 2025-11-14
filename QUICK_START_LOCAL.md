# 🚀 One-Minute Quick Start

## Do This (2 Steps):

### 1. Open PowerShell
```powershell
cd "C:\Users\Shujaat\Desktop\FingerPrint Based Bloodgroup"
python app.py
```
**Leave this terminal open!** You'll see:
```
Running on http://127.0.0.1:5000
```

### 2. Open NEW PowerShell (Ctrl+Shift+N)
```powershell
lt --port 5000
```
**You'll see something like:**
```
your-unique-url.loca.lt is forwarding to localhost:5000
```

## 3. Share the URL! 
Copy `https://your-unique-url.loca.lt` and send to anyone.

---

## ✅ That's it!

- **Browser:** https://your-unique-url.loca.lt
- **Mobile:** Same URL works on phone (using mobile data or WiFi)
- **Multiple Users:** Everyone with the link can access simultaneously
- **Keep running:** Both terminals must stay open

---

## If Something's Wrong:

| Problem | Fix |
|---------|-----|
| `lt: command not found` | Run: `npm install -g localtunnel` |
| Port 5000 in use | Run: `netstat -ano \| findstr :5000` then close that app |
| URL not working | Restart tunnel: `lt --port 5000` |
| Slow uploads | Check internet speed or restart tunnel |

---

## One-Click Start (Optional)

Double-click: `START_AND_SHARE.bat`
- Automatically starts both for you
- Simpler but less control

---

**Questions?** Read `LOCAL_SHARING_GUIDE.md` for detailed instructions.
