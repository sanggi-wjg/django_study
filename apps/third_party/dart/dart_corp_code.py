import os
import zipfile

import requests

from apps.third_party.dart.dart_settings import DART_API_KEY
from apps.third_party.util.utils import xml_to_dict
from sample.settings import MEDIA_ROOT

CORP_CODE_PATH = os.path.join(MEDIA_ROOT, 'dart')
CORP_CODE_ZIP_PATH = os.path.join(MEDIA_ROOT, 'dart', 'corp_code.zip')
CORP_CODE_XML_PATH = os.path.join(MEDIA_ROOT, 'dart', 'CORPCODE.xml')


def download_corp_code():
    url = 'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={}'.format(DART_API_KEY)
    response = requests.get(url)

    file = open(CORP_CODE_ZIP_PATH, 'wb')
    file.write(response.content)
    file.close()

    with zipfile.ZipFile(CORP_CODE_ZIP_PATH) as zf:
        zf.extractall(CORP_CODE_PATH)
        zf.close()


def get_corp_code_list():
    try:
        with open(CORP_CODE_XML_PATH) as xml:
            file = xml_to_dict(xml.read())

    except FileNotFoundError:
        download_corp_code()
        return get_corp_code_list()

    return file['result']['list']
