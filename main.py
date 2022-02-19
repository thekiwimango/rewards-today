import time

from data import get_addresses, get_reference
from substrate.substrate import get_subscan_rewards
from cardano.cardano import get_cardano_rewards


# Aggregate rewards and print them out
def calculate():
    # Calculate rewards for all addresses
    rewards = []
    for _, address in enumerate(get_addresses()):
        if address['chain'] == "cardano":
            reward = get_cardano_rewards(address=address['address'], reference=get_reference())
            if reward:
                rewards.append(reward)
        else:
            reward = get_subscan_rewards(chain=address['chain'], address=address['address'], reference=get_reference())
            if reward:
                rewards.append(reward)
        #  Avoid API rate exceeded
        time.sleep(1)

    # Aggregate rewards, there must be a simpler way...
    rewards_aggr = {}
    for reward in rewards:
        if reward['chain'] in rewards_aggr:
            rewards_aggr[reward['chain']]['today_coins'] = float(rewards_aggr[reward['chain']]['today_coins']) + float(reward['today_coins'])
            rewards_aggr[reward['chain']]['today_value'] = float(rewards_aggr[reward['chain']]['today_value']) + float(reward['today_value'])
            rewards_aggr[reward['chain']]['yesterday_coins'] = float(rewards_aggr[reward['chain']]['yesterday_coins']) + float(reward['yesterday_coins'])
            rewards_aggr[reward['chain']]['yesterday_value'] = float(rewards_aggr[reward['chain']]['yesterday_value']) + float(reward['yesterday_value'])
        else:
            rewards_aggr[reward['chain']] = reward

    # Display results
    print('')
    print('  REWARDS TODAY!')
    print('')
    print('  TODAY')
    total = 0
    for reward in list(rewards_aggr.values()):
        total = total + float(reward['today_value'])
        print('  - {} {:.2f} {} ({:.4f} {})'.format(reward['chain'].ljust(10),
                                                    float(reward['today_value']),
                                                    get_reference(),
                                                    float(reward['today_coins']),
                                                    reward['ticker']))
    print('  Total: {:.2f} {}'.format(total, get_reference()))
    print('')
    print('')
    print('  YESTERDAY')
    total = 0
    for reward in list(rewards_aggr.values()):
        total = total + float(reward['yesterday_value'])
        print('  - {} {:.2f} {} ({:.4f} {})'.format(reward['chain'].ljust(10),
                                                    float(reward['yesterday_value']),
                                                    get_reference(),
                                                    float(reward['yesterday_coins']),
                                                    reward['ticker']))
    print('  Total: {:.2f} {}'.format(total, get_reference()))
    print('')
    print('')


if __name__ == '__main__':
    calculate()
    input(" Press enter to exit")
