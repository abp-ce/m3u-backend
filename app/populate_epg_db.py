import gzip
import logging
import time
import xml.etree.ElementTree as Et
from datetime import datetime
from typing import Any, List, Tuple
from urllib.request import urlopen

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .constants import DATETIME_FORMAT, FILE_NAME, FILE_URL, ROWS_TO_COMMIT
from .database import engine
from .models import Base, Channel, Programme

logger = logging.getLogger('uvicorn')


def retrieve_file(file_url: str, file_name: str) -> None:
    with urlopen(file_url) as response:
        with open(file_name, 'wb') as xml_file:
            xml_file.write(gzip.decompress(response.read()))


async def recreate_tables(*args: str) -> None:
    async with engine.begin() as conn:
        tables = []
        for arg in args:
            tables.append(Base.metadata.tables[arg])
        await conn.run_sync(Base.metadata.drop_all,
                            tables=tables)
        await conn.run_sync(Base.metadata.create_all,
                            tables=tables[::-1])


async def add_and_commit(session: AsyncSession, model: Base,
                         insval: List[Base]) -> Tuple[int, List[Base]]:
    await session.execute(insert(model), insval)
    await session.commit()
    insval.clear()
    return 0, insval


def parse_channel(elem: Any) -> dict:
    result = {}
    result['ch_id'] = elem.attrib['id']
    result['disp_name'] = result['icon'] = None
    for c in elem:
        if c.tag == 'display-name':
            result['disp_name'] = c.text
        elif c.tag == 'icon':
            result['icon'] = c.attrib['src']
    return result


def parse_programme(elem: Any) -> dict:
    nm = {'title': 'title', 'desc': 'pdesc', 'category': 'cat'}
    result = {}
    result['channel'] = elem.attrib['channel']
    result['pstart'] = datetime.strptime(elem.attrib['start'],
                                         DATETIME_FORMAT)
    result['pstop'] = datetime.strptime(elem.attrib['stop'],
                                        DATETIME_FORMAT)
    result['title'] = result['pdesc'] = result['cat'] = None
    for c in elem:
        result[nm[c.tag]] = c.text
    return result


async def parse_file(session: AsyncSession, file_name: str) -> None:
    insval, cnt, flag = [], 0, True
    methods = {'channel': [Channel, parse_channel],
               'programme': [Programme, parse_programme]}
    for _, elem in Et.iterparse(file_name):
        if elem.tag in methods:
            if flag and elem.tag == 'programme':
                cnt, insval = await add_and_commit(session, Channel, insval)
                flag = False
            mthd = methods[elem.tag]
            insval.append(mthd[1](elem))
            cnt += 1
            if cnt == ROWS_TO_COMMIT:
                cnt, insval = await add_and_commit(session, mthd[0], insval)
    await add_and_commit(session, Programme, insval)


async def populate_epg_db(session: AsyncSession) -> None:
    start = time.ctime()
    logger.info(f'Start populate epg db at {start}')
    retrieve_file(FILE_URL, FILE_NAME)
    await recreate_tables('programme', 'channel')
    await parse_file(session, FILE_NAME)
    end = time.ctime()
    logger.info(f'Finish populate epg db at {end}')
