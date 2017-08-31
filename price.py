import argparse


MIN = 0
MAX = 999999
PRICES = (
    (MIN, 500, 1.99),
    (501, MAX, 0.006),
)


p = argparse.ArgumentParser(description='Trading tools')
ps = p.add_subparsers(help='Actions')
p_buy = ps.add_parser('buy', help='Compute price for a buy')
p_buy.add_argument('buy', metavar='PRICE', type=float, help='Quote price')
p_buy.add_argument('number', metavar='NUMBER', type=int, help='Number to buy')
p_sell = ps.add_parser('sell', help='Compute price for a sell')
p_sell.add_argument('sell', metavar='PRICE', type=float, help='Quote price')
p_sell.add_argument('number', metavar='NUMBER', type=int, help='Number to sell')




def compute_for_a_buy(trans_amount):
    return _compute_for('buy', trans_amount)

def compute_for_a_sell(trans_amount):
    return _compute_for('sell', trans_amount)

def _compute_for(op, trans_amount):
    trans_fees = 0
    for rmin, rmax, rfees in PRICES:
        if (trans_amount > rmin and
            trans_amount < rmax):
            if rfees >= 1.0:
                if op == 'buy':
                    trans_fees = trans_amount + rfees
                else:
                    trans_fees = trans_amount - rfees
            else:
                if op == 'buy':
                    trans_fees = (trans_amount * rfees) + trans_amount
                else:
                    trans_fees = trans_amount - (trans_amount * rfees)
            break
    return trans_fees


def main():

    args = p.parse_args()

    quote_fees = 0
    trans_fees = 0

    quote_price_to_sell = 0 # Only used when buying

    trans_count = args.number
    if 'buy' in args:
        quote_price = args.buy
        trans_amount = trans_count * quote_price
        trans_fees = compute_for_a_buy(trans_amount)

        quote_price_to_sell = quote_price
        while True:
            quote_price_to_sell += 0.01
            trans_fees_for_sell = compute_for_a_sell(
                trans_count * quote_price_to_sell)
            if (trans_fees_for_sell >= trans_fees):
                break
    else:
        quote_price = args.sell
        trans_amount = trans_count * quote_price
        trans_fees = compute_for_a_sell(trans_amount)
    quote_fees = trans_fees / trans_count

    print "Quantity\tPrice\tPrice R.\tTotal\t\tTotal R."
    print "%d\t\t%.2f\t%.2f\t\t%.2f\t\t%.2f" % (
        trans_count,
        quote_price,
        quote_fees,
        trans_amount,
        trans_fees)
    if quote_price_to_sell:
        print "--"
        for percent in (' 0', ' 1', ' 2', ' 3', ' 4', ' 5', ' 8', '10', '15',
                        '20', '50', '80'):
            price = (quote_price_to_sell +
                     (quote_price_to_sell * (int(percent)/100.0)))
            print "Sell %s%%: %.2f\t\t%.2f\t\t%.2f" % (
                percent,
                price,
                price * trans_count,
                price * trans_count - trans_amount
                )
                
main()
        
