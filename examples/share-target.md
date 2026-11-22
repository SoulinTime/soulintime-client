# Bookmarklet and share target: sketch only (not built)

**Bookmarklet** (hashes the selected text in your browser; only the SHA-256 is sent). Example, paste as a bookmark URL:

```text
javascript:(async()=>{const t=String(getSelection());if(!t)return alert('Select text first');const b=new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(t)));const h=[...b].map(x=>x.toString(16).padStart(2,'0')).join('');const r=await fetch('https://soulintime.com/functions/createMoment',{method:'POST',headers:{'Content-Type':'application/json','X-SoulInTime-Client':'bookmarklet-example'},body:JSON.stringify({sha256Hash:h})});alert(r.status+' '+await r.text()+'\nStatement later: https://soulintime.com/statement?hash='+h)})()
```

It is the canonical curl in a browser. A 429 (rate_limited or already_stamped) is not a statement. The selected text's exact bytes matter:
the same characters in another encoding or with a trailing newline give a different hash.

**Share target** (Android/PWA "share to SoulInTime"): a Web Share Target in the site manifest would receive a shared file,
hash it on the device and call the same endpoint. Not built; the open question is whether a PWA install is worth it before demand exists.
