from substrate.substrate_assets import get_assets
from utils.utils import *

# Underlying query
reward_query = 'https://{}.api.subscan.io/api/scan/account/reward_slash'


# Get rewards from today and yesterday
def get_subscan_rewards(chain: str, address: str, reference: str):
    # Get ticker and decimal places
    ticker = get_assets()[chain]['ticker']
    decimals = get_assets()[chain]['decimals']

    # Get reward data
    payload = query(chain=chain, address=address)
    if payload['code'] != 0:
        print('Error retrieving data for {}: {}'.format(address, payload['message']))
        return {}
    data = payload['data']['list']

    today_total = 0
    yesterday_total = 0

    # Aggregate rewards from today and yesterday
    for e in data:
        if e['block_timestamp'] > today():
            today_total = today_total + get_amount(e['amount'], decimals)
        elif e['block_timestamp'] > yesterday():
            yesterday_total = yesterday_total + get_amount(e['amount'], decimals)

    # Return result
    return create_entry(chain=chain,
                        ticker=ticker,
                        today_coins=today_total,
                        yesterday_coins=yesterday_total,
                        price=get_current_price(from_sym=ticker, to_sym=reference)[reference])


# Define API query
def query(chain: str, address: str):
    path = reward_query.format(chain)
    data = {
        'address': address,
        'row': 20,
        'page': 0,
    }
    header = {
        'Content-type': 'application/json',
    }
    return query_api(path=path, data=data, header=header)
