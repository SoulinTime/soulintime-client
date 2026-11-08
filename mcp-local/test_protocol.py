import asyncio,json,os,sys,unittest
from pathlib import Path
from mcp import Client,StdioServerParameters
import server
ROOT=Path(__file__).parent
H=server.DOOR
CONF={'hash':H,'status':'confirmed','proofFile':'https://soulintime.com/proof.ots','blockHeight':965906,'slug':'door'}
def response(body,status=200):return {'http_status':status,'body':body,'rate_reset':'1800000000'}
def item(path,body,status=200,post=False):return {'path':path,'post':post,'response':response(body,status)}
def unpack(result):
    if result.structured_content is not None:return result.structured_content
    return json.loads(result.content[0].text)
async def run_case(name,tool,args,fixtures,check):
    env={**os.environ,'MOCK_RESPONSES':json.dumps(fixtures)}
    params=StdioServerParameters(command=sys.executable,args=[str(ROOT/'mock_server.py')],env=env)
    async with Client(params) as client:
        tools=await client.list_tools()
        assert {t.name for t in tools.tools}=={'stamp','verify','first_at'}
        result=await client.call_tool(tool,args)
        check(result)
    print('PASS initialize/tools/list/tools/call:',name)
def data_check(fn):return lambda result: (unittest.TestCase().assertFalse(result.is_error),fn(unpack(result)))
def eq(actual,expected):assert actual==expected,(actual,expected)
async def main():
    await run_case('stamp mocked success','stamp',{'hash':H},[item('/functions/createMoment',{'status':'pending'},post=True)],data_check(lambda x:eq(x['body']['status'],'pending')))
    for status in [400,429]:
        await run_case('stamp HTTP '+str(status),'stamp',{'hash':H},[item('/functions/createMoment',{'reason':'already_stamped','error':'test'},status,True)],data_check(lambda x:eq((x['http_status'],x['rate_reset']),(status,'1800000000'))))
    for status,proof,want in [('pending',True,False),('height_asserted',True,False),('confirmed',False,False),('confirmed',True,True)]:
        b={**CONF,'status':status}
        if not proof:b.pop('proofFile')
        await run_case(status+(' proof' if proof else ' missing proof'),'verify',{'hash':H},[item('/functions/v1Verify',b)],data_check(lambda x,w=want:eq(x['citable'],w)))
    await run_case('first null','first_at',{'hash':H},[item('/functions/v1FirstAt',None)],data_check(lambda x:eq(x['citable'],False)))
    for proof in [True,False]:
        b=dict(CONF)
        if not proof:b.pop('proofFile')
        await run_case('first rechecks proof '+str(proof),'first_at',{'hash':H,'height':965906},[item('/functions/v1FirstAt',CONF),item('/functions/v1Verify',b)],data_check(lambda x,p=proof:eq(x['citable'],p)))
    await run_case('height zero no HTTP','first_at',{'hash':H,'height':0},[],data_check(lambda x:eq(x['citable'],False)))
    for tool,args in [('stamp',{'hash':'no'}),('first_at',{'hash':H,'height':-1}),('first_at',{'hash':H,'height':True}),('first_at',{'hash':H,'height':1.5})]:
        await run_case('invalid '+str(args),tool,args,[],lambda r:eq(r.is_error,True))
    # Explicitly labelled our read-only probe; never stamp.
    async with Client(StdioServerParameters(command=sys.executable,args=[str(ROOT/'server.py')])) as client:
        result=await client.call_tool('verify',{'hash':H})
        d=unpack(result);assert d['citable'];assert d['citation'].endswith('@965906')
        (ROOT/'door_probe.json').write_text(json.dumps(d,indent=2))
        print('PASS OUR LIVE GET PROBE (not M1):',d['citation'])
if __name__=='__main__':asyncio.run(main())
