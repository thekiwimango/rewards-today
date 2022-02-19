from utils.utils import *

# Underlying queries
reward_query = 'http://cardano-mainnet.blockfrost.io/api/v0/accounts/{}/rewards'
epoch_query = 'http://cardano-mainnet.blockfrost.io/api/v0/epochs/latest'

# Blockfrost API key (make your own if this one reached its limit, its free)
project_id = 'mainnetz03MEGJcBKrMKRAX3TwYVxxkDKAsDpjm'


# Get rewards from today and yesterday
def get_cardano_rewards(address: str, reference: str):
    # Define ticker and decimal places
    chain = 'cardano'
    ticker = 'ADA'
    decimals = 6

    # Get reward data
    reward_data = query(query_path=reward_query.format(address))
    if not reward_data:
        return {}

    last_rewards = reward_data[-1]['amount']
    last_epoch = reward_data[-1]['epoch']

    # Get current epoch
    epoch_data = query(query_path=epoch_query)
    current_epoch = epoch_data['epoch']
    start_time = epoch_data['start_time']

    # Return directly if old rewards
    if current_epoch != last_epoch + 2:
        return create_entry(chain=chain,
                            ticker=ticker,
                            today_coins=0.0,
                            yesterday_coins=0.0,
                            price=get_current_price(from_sym=ticker, to_sym=reference)[reference])

    today_total = 0
    yesterday_total = 0

    # Check if rewards were today or yesterday
    if start_time > today():
        today_total = get_amount(last_rewards, decimals)
    elif start_time > yesterday():
        yesterday_total = get_amount(last_rewards, decimals)

    # Return result
    return create_entry(chain=chain,
                        ticker=ticker,
                        today_coins=today_total,
                        yesterday_coins=yesterday_total,
                        price=get_current_price(from_sym=ticker, to_sym=reference)[reference])


# Define API query
def query(query_path: str):
    data = {}
    header = {
        'Content-type': 'application/json',
        'project_id': project_id
    }
    return query_api(path=query_path, data=data, header=header)

