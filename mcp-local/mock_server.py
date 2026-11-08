"""Test-only subprocess. Network is forbidden; ordered fixture responses replace HTTP."""
import json, os
import server
fixtures=json.loads(os.environ['MOCK_RESPONSES'])
def mocked(path,payload=None):
    assert fixtures, 'unexpected network call'
    item=fixtures.pop(0)
    assert path.startswith(item['path']), (path,item)
    assert (payload is not None)==item.get('post',False)
    return item['response']
server.request=mocked
server.mcp.run(transport='stdio')
