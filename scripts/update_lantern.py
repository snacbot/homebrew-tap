"""Sync Lantern's cask from its public Mac feed and immutable GitHub asset."""
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET

FEED = 'https://raw.githubusercontent.com/snacbot/lantern-releases/main/appcast.xml'
REPO = 'https://api.github.com/repos/snacbot/lantern-releases'
SPARKLE = '{http://www.andymatuschak.org/xml-namespaces/sparkle}'


def read(url):
    headers = {'User-Agent': 'Khaos-Homebrew-Sync'}
    if url.startswith('https://api.github.com/') and os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
        return response.read()


def version_tuple(version):
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError(f'Unsupported version: {version!r}')
    return tuple(map(int, version.split('.')))


def update(cask, fetch=read):
    items = ET.fromstring(fetch(FEED)).findall('./channel/item')
    if not items:
        raise ValueError('Mac feed contains no releases')
    item = max(items, key=lambda entry: int(entry.findtext(SPARKLE + 'version')))
    version = item.findtext(SPARKLE + 'shortVersionString', '')
    version_tuple(version)
    text = cask.read_text()
    current = re.search(r'^  version "([^"]+)"$', text, re.M).group(1)
    if version_tuple(version) < version_tuple(current):
        raise ValueError('Refusing to downgrade Lantern')
    tag = f'mac-v{version}'
    name = f'Lantern-{version}.dmg'
    url = f'https://github.com/snacbot/lantern-releases/releases/download/{tag}/{name}'
    enclosure = item.find('enclosure')
    if enclosure is None or enclosure.get('url') != url:
        raise ValueError('Feed does not reference the immutable Mac release DMG')
    release = json.loads(fetch(f'{REPO}/releases/tags/{tag}'))
    # Published previews are intentional; Windows releases and drafts are excluded.
    if release.get('draft') or release.get('tag_name') != tag or not release.get('published_at'):
        raise ValueError('Mac release is not published')
    asset = next(asset for asset in release['assets'] if asset['name'] == name)
    if asset.get('browser_download_url') != url or asset.get('state') != 'uploaded':
        raise ValueError('Mac release asset is not ready')
    digest = asset.get('digest', '')
    if not re.fullmatch(r'sha256:[a-f0-9]{64}', digest):
        raise ValueError('GitHub asset has no valid SHA-256 digest')
    expected = digest.removeprefix('sha256:')
    current_sha = re.search(r'^  sha256 "([a-f0-9]{64})"$', text, re.M).group(1)
    if version == current:
        if current_sha != expected:
            raise ValueError('Published DMG checksum changed in place')
        print(f'Lantern {version} is already current')
        return False
    data = fetch(url)
    if len(data) != int(enclosure.get('length')) or len(data) != asset['size']:
        raise ValueError('DMG size does not match feed and GitHub')
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('Downloaded DMG checksum does not match GitHub')
    text = re.sub(r'^  version "[^"]+"$', f'  version "{version}"', text, count=1, flags=re.M)
    text = re.sub(r'^  sha256 "[^"]+"$', f'  sha256 "{expected}"', text, count=1, flags=re.M)
    cask.write_text(text)
    print(f'Updated Lantern {current} -> {version}')
    return True


if __name__ == '__main__':
    update(Path(__file__).resolve().parents[1] / 'Casks/lantern.rb')
