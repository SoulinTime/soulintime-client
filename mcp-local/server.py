"""SoulInTime local stdio adapter. No network I/O until a tool is invoked."""
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from pydantic import StrictInt

BASE = 'https://soulintime.com'
MAX_BODY = 1024 * 1024
DOOR = '019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f'

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def request(path, payload=None):
    """One bounded request, fixed origin, no redirects or automatic retries."""
    req = urllib.request.Request(BASE + path, data=None if payload is None else json.dumps(payload).encode(),
        headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'User-Agent': 'soulintime-local-mcp/0.1'})
    try:
        try:
            response = urllib.request.build_opener(NoRedirect()).open(req, timeout=15)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            data = response.read(MAX_BODY + 1)
            if len(data) > MAX_BODY:
                return {'http_status': response.code, 'error': 'response_too_large', 'citable': False}
            text = data.decode('utf-8', errors='replace')
            try:
                body = json.loads(text)
            except ValueError:
                body = text
            return {'http_status': response.code, 'body': body, 'raw_body': text,
                'rate_reset': response.headers.get('X-RateLimit-Reset'),
                'retry_after': response.headers.get('Retry-After')}
    except (OSError, urllib.error.URLError) as error:
        return {'http_status': None, 'error': type(error).__name__, 'detail': str(error), 'citable': False}

def valid_hash(value):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-fA-F]{64}', value):
        raise ValueError('hash must be exactly 64 hexadecimal characters')
    return value.lower()

def citation(result, expected_hash, max_height=None):
    body = result.get('body')
    height = body.get('blockHeight') if isinstance(body, dict) else None
    ok = (result.get('http_status') == 200 and isinstance(body, dict)
        and body.get('status') == 'confirmed' and isinstance(body.get('proofFile'), str)
        and bool(body['proofFile'].strip()) and isinstance(height, int) and not isinstance(height, bool)
        and height > 0 and isinstance(body.get('slug'), str) and bool(body['slug'])
        and (body.get('hash') or body.get('sha256Hash')) == expected_hash
        and (max_height is None or height <= max_height))
    return {'citable': bool(ok), 'citation': f"{body['slug']}@{height}" if ok else None,
        'citation_reason': 'confirmed with proofFile' if ok else 'refuse: confirmation, proofFile, hash, slug or height missing/mismatched'}

mcp = MCPServer('SoulInTime local adapter', version='0.1.0', instructions=
    'Cite slug@height only when status is confirmed and proofFile exists; otherwise refuse. '
    'The tip is never a receipt height. No keys; no truth claim. '
    'Evaluate without creating: call verify with Door hash '+DOOR+'. '
    'stamp creates a receipt only when explicitly invoked; do not use it to test. '
    'No automatic retry. On 429 respect rate_reset (Unix seconds); already_stamped never clears.')

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False, openWorldHint=True))
def stamp(hash: str) -> dict:
    """Submit one SHA-256 hash (not file bytes) to createMoment. Explicit invocation creates an unlisted receipt by default. May return pending or 429; never retries. Do not call for evaluation."""
    return request('/functions/createMoment', {'sha256Hash': valid_hash(hash)})

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def verify(hash: str) -> dict:
    """Read an existing receipt without creating one. Return upstream status/body plus citation only if confirmed with nonempty proofFile. Does not cryptographically verify .ots bytes locally. Pending and height_asserted refuse citing."""
    h = valid_hash(hash)
    result = request('/functions/v1Verify?' + urllib.parse.urlencode({'hash': h}))
    return {**result, **citation(result, h)}

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def first_at(hash: str, height: StrictInt | None = None) -> dict:
    """Read earliest confirmed PUBLIC receipt, optionally at or before height. Recheck v1Verify before citing; unlisted receipts excluded. height=0 returns no possible confirmed receipt without network. Not a chain-tip query."""
    h = valid_hash(hash)
    if height is not None and (isinstance(height, bool) or not isinstance(height, int) or height < 0):
        raise ValueError('height must be an integer >= 0')
    if height == 0:
        return {'http_status': None, 'body': None, 'citable': False, 'citation': None, 'citation_reason': 'No confirmed Bitcoin receipt at or before height 0; no request sent'}
    query = {'hash': h}
    if height is not None:
        query['atOrBefore'] = height
    first = request('/functions/v1FirstAt?' + urllib.parse.urlencode(query))
    body = first.get('body')
    if first.get('http_status') != 200 or not isinstance(body, dict):
        return {**first, 'citable': False, 'citation': None, 'citation_reason': 'No public first returned'}
    check = verify(h)
    same = (isinstance(check.get('body'), dict) and body.get('slug') == check['body'].get('slug')
        and body.get('blockHeight') == check['body'].get('blockHeight') and body.get('status') == 'confirmed')
    decision = citation(check, h, height)
    if not same:
        decision = {'citable': False, 'citation': None, 'citation_reason': 'first_at and v1Verify disagree; refuse'}
    return {**first, 'verification': check, **decision}

if __name__ == '__main__':
    mcp.run(transport='stdio')
