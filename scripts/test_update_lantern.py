import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from update_lantern import FEED, REPO, update


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.cask = Path(self.directory.name) / 'lantern.rb'
        self.original = 'cask "lantern" do\n  version "0.2.0"\n  sha256 "' + 'a' * 64 + '"\nend\n'
        self.cask.write_text(self.original)
        self.url = 'https://github.com/snacbot/lantern-releases/releases/download/mac-v0.3.0/Lantern-0.3.0.dmg'
        self.data = b'verified-dmg-fixture'
        self.asset = dict(name='Lantern-0.3.0.dmg', browser_download_url=self.url,
                          state='uploaded', size=len(self.data),
                          digest='sha256:' + hashlib.sha256(self.data).hexdigest())
        self.release = dict(tag_name='mac-v0.3.0', draft=False, prerelease=True,
                            published_at='2026-10-20T00:00:00Z', assets=[self.asset])
        self.feed = f'''<rss xmlns:s="http://www.andymatuschak.org/xml-namespaces/sparkle"><channel>
        <item><s:version>7</s:version><s:shortVersionString>0.3.0</s:shortVersionString>
        <enclosure url="{self.url}" length="{len(self.data)}"/></item>
        <item><s:version>6</s:version><s:shortVersionString>0.2.0</s:shortVersionString></item>
        </channel></rss>'''

    def fetch(self, url):
        if url == FEED:
            return self.feed.encode()
        if url == REPO + '/releases/tags/mac-v0.3.0':
            return json.dumps(self.release).encode()
        if url == self.url:
            return self.data
        raise AssertionError(url)

    def rejected(self):
        with self.assertRaises((ValueError, StopIteration)):
            update(self.cask, self.fetch)
        self.assertEqual(self.cask.read_text(), self.original)

    def test_published_preview_and_idempotent(self):
        self.assertTrue(update(self.cask, self.fetch))
        self.assertIn('version "0.3.0"', self.cask.read_text())
        self.assertFalse(update(self.cask, self.fetch))

    def test_draft(self):
        self.release['draft'] = True
        self.rejected()

    def test_unpublished(self):
        self.release['published_at'] = None
        self.rejected()

    def test_wrong_download(self):
        self.feed = self.feed.replace(self.url, 'https://example.com/untrusted.dmg')
        self.rejected()

    def test_checksum(self):
        self.asset['digest'] = 'sha256:' + 'b' * 64
        self.rejected()

    def test_size(self):
        self.asset['size'] += 1
        self.rejected()

    def test_missing_asset(self):
        self.release['assets'] = []
        self.rejected()

    def test_downgrade(self):
        self.original = self.original.replace('0.2.0', '0.4.0')
        self.cask.write_text(self.original)
        self.rejected()

    def test_replaced_asset(self):
        self.original = self.original.replace('0.2.0', '0.3.0')
        self.cask.write_text(self.original)
        self.rejected()


if __name__ == '__main__':
    unittest.main()
