import re
import logging
from requests import Session
from bs4 import BeautifulSoup
from dogpile.cache import make_region

region = make_region().configure('dogpile.cache.memory',expiration_time=5)

log = logging.getLogger('main')

ARRIS_URL = "http://192.168.100.1/RgConnect.asp"

@region.cache_on_arguments()
def process():
    result_body = []
    s = Session()
    try:
        rs = s.get(ARRIS_URL)
        rs.raise_for_status()
    except Exception as e:
        log.error("exception: %s" % (e))
    html = re.sub(r'(\r|\n|\t)', '', rs.text)
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', attrs={"class": "simpleTable"})
    for table in tables:
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if (len(tds) == 7):
                if tds[0].get_text() == "Channel":
                    continue
                if tds[1].get_text() == "Locked":
                    locked = 1
                else:
                    locked = 0
                result_body.append("arris_upstream_locked{{index=\"{index}\",type=\"{modulation}\",channel_id=\"{channel}\",frequency=\"{freq}\"}} {locked}"
                        .format(
                            index=tds[0].get_text(),
                            modulation=tds[2].get_text(),
                            channel=tds[3].get_text(),
                            freq=tds[5].get_text().split(' ')[0],
                            locked=locked))

                result_body.append("arris_upstream_symbol_rate{{index=\"{index}\",type=\"{modulation}\",channel_id=\"{channel}\",frequency=\"{freq}\"}} {rate}"
                        .format(
                            index=tds[0].get_text(),
                            modulation=tds[2].get_text(),
                            channel=tds[3].get_text(),
                            freq=tds[5].get_text().split(' ')[0],
                            rate=tds[4].get_text().strip().split(' ')[0]))
                result_body.append("arris_upstream_power{{index=\"{index}\",type=\"{modulation}\",channel_id=\"{channel}\",frequency=\"{freq}\"}} {power}"
                        .format(
                            index=tds[0].get_text(),
                            modulation=tds[2].get_text(),
                            channel=tds[3].get_text(),
                            freq=tds[5].get_text().split(' ')[0],
                            power=tds[6].get_text().strip().split(' ')[0]))
            elif (len(tds) == 9):
                if tds[0].get_text() == "Channel":
                    continue
                if tds[1].get_text() == "Locked":
                    locked = 1
                else:
                    locked = 0
                result_body.append("arris_downstream_locked{{index=\"{index}\",modulation=\"{modulation}\",channel_id=\"{channel}\",frequency=\"{freq}\"}} {locked}"
                        .format(
                            index=tds[0].get_text(),
                            modulation=tds[2].get_text(),
                            channel=tds[3].get_text(),
                            freq=tds[4].get_text().split(' ')[0],
                            locked=locked))
                result_body.append("arris_downstream_packets_corrected{{index=\"{index}\",modulation=\"{modulation}\",channel_id=\"{channel}\",frequency=\"{freq}\"}} {corrected}"
                        .format(
                            index=tds[0].get_text(),
                            modulation=tds[2].get_text(),
                            channel=tds[3].get_text(),
                            freq=tds[4].get_text().split(' ')[0],
                            corrected=tds[7].get_text()))
                result_body.append("arris_downstream_packets_uncorrectable{{index=\"{index}\",modulation=\"{modulation}\",channel_id=\"{channel}\",frequency=\"{freq}\"}} {uncorrectable}"
                        .format(
                            index=tds[0].get_text(),
                            modulation=tds[2].get_text(),
                            channel=tds[3].get_text(),
                            freq=tds[4].get_text().split(' ')[0],
                            uncorrectable=tds[8].get_text()))
                result_body.append("arris_downstream_power{{index=\"{index}\",modulation=\"{modulation}\",channel_id=\"{channel}\",frequency=\"{freq}\"}} {power}"
                        .format(
                            index=tds[0].get_text(),
                            modulation=tds[2].get_text(),
                            channel=tds[3].get_text(),
                            freq=tds[4].get_text().split(' ')[0],
                            power=tds[5].get_text().strip().split(' ')[0]))
                result_body.append("arris_downstream_snr{{index=\"{index}\",modulation=\"{modulation}\",channel_id=\"{channel}\",frequency=\"{freq}\"}} {snr}"
                        .format(
                            index=tds[0].get_text(),
                            modulation=tds[2].get_text(),
                            channel=tds[3].get_text(),
                            freq=tds[4].get_text().split(' ')[0],
                            snr=tds[6].get_text().strip().split(' ')[0]))
            else:
                for tdstr in tds:
                    if re.search(r'Connectivity State',tdstr.get_text()):

                        if tds[1].get_text() == "OK":
                            state = 1
                        else:
                            state = 0
                        result_body.append("arris_connectivity_state{{}} {state}"
                            .format(state=state))
    return '\n'.join(str(x) for x in result_body)

