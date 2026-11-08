import io,json,unittest,urllib.error
from unittest.mock import patch
import server
class Reply(io.BytesIO):
    code=200
    headers={'X-RateLimit-Reset':'1234','Retry-After':'60'}
class TestHTTP(unittest.TestCase):
    def test_fixed_origin_timeout_body(self):
        class Opener:
            def open(self,req,timeout):
                self.req=req
                assert req.full_url=='https://soulintime.com/functions/createMoment'
                assert timeout==15
                assert json.loads(req.data)=={'sha256Hash':server.DOOR}
                return Reply(b'{"status":"pending"}')
        with patch('urllib.request.build_opener',return_value=Opener()):
            r=server.stamp(server.DOOR);self.assertEqual(r['rate_reset'],'1234');self.assertEqual(r['body']['status'],'pending')
    def test_http_error_preserved(self):
        error=urllib.error.HTTPError(server.BASE,429,'rate',{'X-RateLimit-Reset':'1234'},io.BytesIO(b'{"reason":"already_stamped"}'))
        with patch('urllib.request.OpenerDirector.open',side_effect=error) as call:
            r=server.stamp(server.DOOR)
            self.assertEqual(call.call_count,1);self.assertEqual(r['http_status'],429);self.assertEqual(r['body']['reason'],'already_stamped');self.assertEqual(r['rate_reset'],'1234')
    def test_bound(self):
        with patch('urllib.request.OpenerDirector.open',return_value=Reply(b'x'*(server.MAX_BODY+1))):
            self.assertEqual(server.verify(server.DOOR)['error'],'response_too_large')
    def test_no_redirect(self):
        self.assertIsNone(server.NoRedirect().redirect_request(None,None,302,'',{},'https://evil.example'))
    def test_offline_import_and_listing(self):
        # Protocol tests initialize/list with no fixtures: any unexpected request raises.
        self.assertEqual(server.BASE,'https://soulintime.com')
if __name__=='__main__':unittest.main(verbosity=2)
