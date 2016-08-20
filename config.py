

#http://download.finance.yahoo.com/d/quotes.csv?s=FB&f=n

import os

usd_in_gbp = 0.64
eur_in_gpb = 0.78


aliases = {}
aliases['NYSE'] = ''
aliases['NASDAQ'] = ''
aliases['LON'] = '_L'
aliases['EPA'] = '_PA'
aliases['ETR'] = '_F'


home_path = os.path.dirname(os.path.realpath(__file__))
ukcompanies = os.path.join(home_path, 'ukcomp', "UKcompanies.csv")
ukoutputfolder = os.path.join(home_path, 'ukcomp')
usoutputfolder = os.path.join(home_path, "uscomp")

current_ticker = os.path.join(home_path, "current_tick.txt")
current_ticker_fnm = os.path.join(home_path, "current_tick_us.txt")


blank = 'N/A'
sleep_sec = 0

currency_dict = {'GB': 'GBP', 'IE': 'EUR', 'JE': 'GBP', 'IM': 'GBP', 'GI': 'GBP', 'US': 'USD', 'GG': 'GBP', 'RU': 'RUB', 'IT': 'EUR', 'VG': 'GBP', 'ZA': 'GBP', 'FI': 'GBP', 'CY':'GBP', 'KY':'GBP', 'BM': 'GBP', 'CN': 'GBP', 'SG': 'GBP', 'CH': 'GBP', 'QA': 'GBP', 'CY': 'GBP', 'KY': 'GBP'}


yahoo_exchange = {}
yahoo_exchange['NYQ'] = 'NYSE'
yahoo_exchange['NCM'] = 'NASDAQ'
yahoo_exchange['NMS'] = 'NASDAQ'
yahoo_exchange['NGM'] = 'NASDAQ'
yahoo_exchange['NIM'] = 'NASDAQ'
yahoo_exchange['NAS'] = 'NASDAQ'
yahoo_exchange['NASDAQ'] = 'NASDAQ'
yahoo_exchange['NYSE'] = 'NYSE'


yahoo_exchange['ASE'] = 'NYSE'
yahoo_exchange['PCX'] = 'NYSE'
yahoo_exchange['N/A'] = 'N/A'
yahoo_exchange['NA'] = 'NA'
yahoo_exchange['PNK'] = 'OTC'
yahoo_exchange['OBB'] = 'OTC'
yahoo_exchange['OTC'] = 'OTC'


yahoo_code = {}
yahoo_code['dividend'] = 'd'

yahoo_code['earnings_ps'] = 'e'
yahoo_code['dividend_yield'] = 'y'
#yahoo_code['div_yield'] = 'y'
yahoo_code['ex_dividend_date'] = 'q'
yahoo_code['dividend_pay_date'] = 'r1'
yahoo_code['pe'] = 'r'
yahoo_code['price'] = 'a'
yahoo_code['price2'] = 'b2'

#yahoo_code['symbol'] = 's'
yahoo_code['market_cap'] = 'j1'
yahoo_code['market_cap2'] = 'j3'
yahoo_code['name'] = 'n'

yahoo_code['exchange'] = 'x'
yahoo_code['EBITDA'] = 'j4'
yahoo_code['close_price'] = 'p'
yahoo_code['volume'] = 'v'
yahoo_code['open'] = 'o'
yahoo_code['52_low'] = 'j'
yahoo_code['52_high'] = 'k'

yahoo_code['notes'] = 'n4'
yahoo_code['year_gain'] = 'g3'





	
