#!/usr/bin/env node
// SoulInTime statement verifier, sit-statement/0.1. One file, Node 18+ built-ins only (WebCrypto Ed25519). Works offline.
//   node verify_statement.mjs statement.json [--file FILE | --hash SHA256] [--ots proof.ots]
// Checks shape, sha256 of your file (or the hash you pass), the Ed25519 signature over the RFC 8785 (JCS) canonical JSON of
// every field except sig against the published key, and with --ots the .ots digest; then prints the OpenTimestamps command.
import {readFileSync} from 'node:fs';
import {createHash,webcrypto} from 'node:crypto';
const KEYS={'0a64aa45b8ce17a7':'GrcQ1ZzlNQAtU8GyezaWCmyFjzjP2NEknvkAd5CQXxc'}; // also at https://soulintime.com/protocol#statements
const b64u=s=>Buffer.from(s.replace(/-/g,'+').replace(/_/g,'/'),'base64');
const jcs=v=>v===null?'null':typeof v==='string'?JSON.stringify(v):typeof v==='number'?(Number.isSafeInteger(v)?String(v):(()=>{throw Error('non-integer number')})()):typeof v==='boolean'?String(v):(typeof v==='object'&&!Array.isArray(v))?'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+jcs(v[k])).join(',')+'}':(()=>{throw Error('unsupported value')})();
const HEX=/^[0-9a-f]{64}$/;
function shape(st){const base=['v','sha256','status','block_height','block_hash','ots_sha256','issued_at','issuer','kid','sig'];const want=(st.status==='refused'?[...base,'reason']:st.priority===true?[...base,'priority']:base).sort();
 if(JSON.stringify(Object.keys(st).sort())!==JSON.stringify(want))return 'fields mismatch';if(st.v!=='sit-statement/0.1')return 'unknown version';
 if(!HEX.test(st.sha256)||!HEX.test(st.block_hash)||!Number.isSafeInteger(st.block_height)||st.block_height<=0)return 'bad hash/block';
 if(st.status==='confirmed')return HEX.test(st.ots_sha256)?null:'confirmed needs ots_sha256';
 if(st.status==='refused')return st.ots_sha256===null&&['not_found','not_confirmed'].includes(st.reason)?null:'bad refusal';
 return 'status must be confirmed or refused (pending is never a statement)';}
const args=process.argv.slice(2);const opt=n=>{const i=args.indexOf(n);return i>=0?args[i+1]:null};
let st=JSON.parse(readFileSync(args[0],'utf8'));if(st&&st.statement)st=st.statement;
let ok=true;const res=(c,m)=>{ok=ok&&c;console.log((c?'PASS ':'FAIL ')+m)};
const e=shape(st);res(!e,'shape sit-statement/0.1'+(e?': '+e:''));if(e)process.exit(1);
if(opt('--file')){const h=createHash('sha256').update(readFileSync(opt('--file'))).digest('hex');res(h===st.sha256,'sha256(file) = '+h)}
else if(opt('--hash'))res(opt('--hash').trim().toLowerCase()===st.sha256,'given hash equals statement sha256');
const pk=KEYS[st.kid];res(!!pk,'key id '+st.kid+' is a published key');
if(pk){const raw=b64u(pk);res(createHash('sha256').update(raw).digest('hex').slice(0,16)===st.kid,'kid = first 16 hex of sha256(public key)');
 const {sig,...body}=st;const key=await webcrypto.subtle.importKey('raw',raw,{name:'Ed25519'},false,['verify']);
 res(await webcrypto.subtle.verify({name:'Ed25519'},key,b64u(sig),new TextEncoder().encode(jcs(body))),'Ed25519 signature over JCS(all fields but sig)');}
if(opt('--ots')){const ob=readFileSync(opt('--ots'));if(st.status==='confirmed')res(createHash('sha256').update(ob).digest('hex')===st.ots_sha256,'sha256(.ots) = ots_sha256');res(ob.length>=65&&ob.subarray(33,65).toString('hex')===st.sha256,'.ots commits to statement sha256');}
if(st.status==='confirmed'){console.log('Block check (OpenTimestamps):');console.log('  ots verify -d '+st.sha256+' '+(opt('--ots')||'proof.ots'));console.log('  expected: block '+st.block_height+', whose hash on any explorer is '+st.block_hash);}
else console.log('Signed refusal: not confirmed ('+st.reason+') as of block '+st.block_height+'. Do not cite a block.');
console.log('RESULT: '+(ok?'all checks passed':'FAILED'));process.exit(ok?0:1);
