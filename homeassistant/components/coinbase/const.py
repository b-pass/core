"""Constants used for Coinbase."""

CONF_CURRENCIES = "account_balance_currencies"
CONF_EXCHANGE_BASE = "exchange_base"
CONF_EXCHANGE_RATES = "exchange_rate_currencies"
CONF_OPTIONS = "options"
DOMAIN = "coinbase"

# These are constants used by the previous YAML configuration
CONF_YAML_API_TOKEN = "api_secret"

# Constants for data returned by Coinbase API
API_ACCOUNT_AMOUNT = "amount"
API_ACCOUNT_BALANCE = "balance"
API_ACCOUNT_CURRENCY = "currency"
API_ACCOUNT_ID = "id"
API_ACCOUNT_NATIVE_BALANCE = "native_balance"
API_ACCOUNT_NAME = "name"
API_ACCOUNTS_DATA = "data"
API_RATES = "rates"
API_RESOURCE_TYPE = "type"
API_TYPE_VAULT = "vault"

WALLETS = {
    "1INCH": "1INCH",
    "AAVE": "AAVE",
    "ADA": "ADA",
    "AED": "AED",
    "AFN": "AFN",
    "ALGO": "ALGO",
    "ALL": "ALL",
    "AMD": "AMD",
    "AMP": "AMP",
    "ANG": "ANG",
    "ANKR": "ANKR",
    "AOA": "AOA",
    "ARS": "ARS",
    "ATOM": "ATOM",
    "AUD": "AUD",
    "AWG": "AWG",
    "AZN": "AZN",
    "BAL": "BAL",
    "BAM": "BAM",
    "BAND": "BAND",
    "BAT": "BAT",
    "BBD": "BBD",
    "BCH": "BCH",
    "BDT": "BDT",
    "BGN": "BGN",
    "BHD": "BHD",
    "BIF": "BIF",
    "BMD": "BMD",
    "BND": "BND",
    "BNT": "BNT",
    "BOB": "BOB",
    "BOND": "BOND",
    "BRL": "BRL",
    "BSD": "BSD",
    "BSV": "BSV",
    "BTC": "BTC",
    "BTN": "BTN",
    "BWP": "BWP",
    "BYN": "BYN",
    "BYR": "BYR",
    "BZD": "BZD",
    "CAD": "CAD",
    "CDF": "CDF",
    "CGLD": "CGLD",
    "CHF": "CHF",
    "CHZ": "CHZ",
    "CLF": "CLF",
    "CLP": "CLP",
    "CLV": "CLV",
    "CNH": "CNH",
    "CNY": "CNY",
    "COMP": "COMP",
    "COP": "COP",
    "CRC": "CRC",
    "CRV": "CRV",
    "CTSI": "CTSI",
    "CUC": "CUC",
    "CVC": "CVC",
    "CVE": "CVE",
    "CZK": "CZK",
    "DAI": "DAI",
    "DASH": "DASH",
    "DJF": "DJF",
    "DKK": "DKK",
    "DNT": "DNT",
    "DOGE": "DOGE",
    "DOP": "DOP",
    "DOT": "DOT",
    "DZD": "DZD",
    "EGP": "EGP",
    "ENJ": "ENJ",
    "EOS": "EOS",
    "ERN": "ERN",
    "ETB": "ETB",
    "ETC": "ETC",
    "ETH": "ETH",
    "ETH2": "ETH2",
    "EUR": "EUR",
    "FET": "FET",
    "FIL": "FIL",
    "FJD": "FJD",
    "FKP": "FKP",
    "FORTH": "FORTH",
    "GBP": "GBP",
    "GBX": "GBX",
    "GEL": "GEL",
    "GGP": "GGP",
    "GHS": "GHS",
    "GIP": "GIP",
    "GMD": "GMD",
    "GNF": "GNF",
    "GRT": "GRT",
    "GTC": "GTC",
    "GTQ": "GTQ",
    "GYD": "GYD",
    "HKD": "HKD",
    "HNL": "HNL",
    "HRK": "HRK",
    "HTG": "HTG",
    "HUF": "HUF",
    "ICP": "ICP",
    "IDR": "IDR",
    "ILS": "ILS",
    "IMP": "IMP",
    "INR": "INR",
    "IQD": "IQD",
    "ISK": "ISK",
    "JEP": "JEP",
    "JMD": "JMD",
    "JOD": "JOD",
    "JPY": "JPY",
    "KEEP": "KEEP",
    "KES": "KES",
    "KGS": "KGS",
    "KHR": "KHR",
    "KMF": "KMF",
    "KNC": "KNC",
    "KRW": "KRW",
    "KWD": "KWD",
    "KYD": "KYD",
    "KZT": "KZT",
    "LAK": "LAK",
    "LBP": "LBP",
    "LINK": "LINK",
    "LKR": "LKR",
    "LPT": "LPT",
    "LRC": "LRC",
    "LRD": "LRD",
    "LSL": "LSL",
    "LTC": "LTC",
    "LYD": "LYD",
    "MAD": "MAD",
    "MANA": "MANA",
    "MATIC": "MATIC",
    "MDL": "MDL",
    "MGA": "MGA",
    "MIR": "MIR",
    "MKD": "MKD",
    "MKR": "MKR",
    "MLN": "MLN",
    "MMK": "MMK",
    "MNT": "MNT",
    "MOP": "MOP",
    "MRO": "MRO",
    "MTL": "MTL",
    "MUR": "MUR",
    "MVR": "MVR",
    "MWK": "MWK",
    "MXN": "MXN",
    "MYR": "MYR",
    "MZN": "MZN",
    "NAD": "NAD",
    "NGN": "NGN",
    "NIO": "NIO",
    "NKN": "NKN",
    "NMR": "NMR",
    "NOK": "NOK",
    "NPR": "NPR",
    "NU": "NU",
    "NZD": "NZD",
    "OGN": "OGN",
    "OMG": "OMG",
    "OMR": "OMR",
    "OXT": "OXT",
    "PAB": "PAB",
    "PEN": "PEN",
    "PGK": "PGK",
    "PHP": "PHP",
    "PKR": "PKR",
    "PLN": "PLN",
    "POLY": "POLY",
    "PYG": "PYG",
    "QAR": "QAR",
    "QNT": "QNT",
    "RLY": "RLY",
    "REN": "REN",
    "REP": "REP",
    "REPV2": "REPV2",
    "RLC": "RLC",
    "RON": "RON",
    "RSD": "RSD",
    "RUB": "RUB",
    "RWF": "RWF",
    "SAR": "SAR",
    "SBD": "SBD",
    "SCR": "SCR",
    "SEK": "SEK",
    "SGD": "SGD",
    "SHIB": "SHIB",
    "SHP": "SHP",
    "SKL": "SKL",
    "SLL": "SLL",
    "SNX": "SNX",
    "SOL": "SOL",
    "SOS": "SOS",
    "SRD": "SRD",
    "SSP": "SSP",
    "STD": "STD",
    "STORJ": "STORJ",
    "SUSHI": "SUSHI",
    "SVC": "SVC",
    "SZL": "SZL",
    "THB": "THB",
    "TJS": "TJS",
    "TMM": "TMM",
    "TMT": "TMT",
    "TND": "TND",
    "TOP": "TOP",
    "TRB": "TRB",
    "TRY": "TRY",
    "TTD": "TTD",
    "TWD": "TWD",
    "TZS": "TZS",
    "UAH": "UAH",
    "UGX": "UGX",
    "UMA": "UMA",
    "UNI": "UNI",
    "USD": "USD",
    "USDC": "USDC",
    "USDT": "USDT",
    "UYU": "UYU",
    "UZS": "UZS",
    "VES": "VES",
    "VND": "VND",
    "VUV": "VUV",
    "WBTC": "WBTC",
    "WST": "WST",
    "XAF": "XAF",
    "XAG": "XAG",
    "XAU": "XAU",
    "XCD": "XCD",
    "XDR": "XDR",
    "XLM": "XLM",
    "XOF": "XOF",
    "XPD": "XPD",
    "XPF": "XPF",
    "XPT": "XPT",
    "XRP": "XRP",
    "XTZ": "XTZ",
    "YER": "YER",
    "YFI": "YFI",
    "ZAR": "ZAR",
    "ZEC": "ZEC",
    "ZMW": "ZMW",
    "ZRX": "ZRX",
    "ZWL": "ZWL",
}

RATES = {
    "1INCH": "1INCH",
    "AAVE": "AAVE",
    "ADA": "ADA",
    "AED": "AED",
    "AFN": "AFN",
    "ALGO": "ALGO",
    "ALL": "ALL",
    "AMD": "AMD",
    "ANG": "ANG",
    "ANKR": "ANKR",
    "AOA": "AOA",
    "ARS": "ARS",
    "ATOM": "ATOM",
    "AUD": "AUD",
    "AWG": "AWG",
    "AZN": "AZN",
    "BAL": "BAL",
    "BAM": "BAM",
    "BAND": "BAND",
    "BAT": "BAT",
    "BBD": "BBD",
    "BCH": "BCH",
    "BDT": "BDT",
    "BGN": "BGN",
    "BHD": "BHD",
    "BIF": "BIF",
    "BMD": "BMD",
    "BND": "BND",
    "BNT": "BNT",
    "BOB": "BOB",
    "BRL": "BRL",
    "BSD": "BSD",
    "BSV": "BSV",
    "BTC": "BTC",
    "BTN": "BTN",
    "BWP": "BWP",
    "BYN": "BYN",
    "BYR": "BYR",
    "BZD": "BZD",
    "CAD": "CAD",
    "CDF": "CDF",
    "CGLD": "CGLD",
    "CHF": "CHF",
    "CLF": "CLF",
    "CLP": "CLP",
    "CLV": "CLV",
    "CNH": "CNH",
    "CNY": "CNY",
    "COMP": "COMP",
    "COP": "COP",
    "CRC": "CRC",
    "CRV": "CRV",
    "CUC": "CUC",
    "CVC": "CVC",
    "CVE": "CVE",
    "CZK": "CZK",
    "DAI": "DAI",
    "DASH": "DASH",
    "DJF": "DJF",
    "DKK": "DKK",
    "DNT": "DNT",
    "DOP": "DOP",
    "DZD": "DZD",
    "EGP": "EGP",
    "ENJ": "ENJ",
    "EOS": "EOS",
    "ERN": "ERN",
    "ETB": "ETB",
    "ETC": "ETC",
    "ETH": "ETH",
    "ETH2": "ETH2",
    "EUR": "EUR",
    "FET": "FET",
    "FIL": "FIL",
    "FJD": "FJD",
    "FKP": "FKP",
    "FORTH": "FORTH",
    "GBP": "GBP",
    "GBX": "GBX",
    "GEL": "GEL",
    "GGP": "GGP",
    "GHS": "GHS",
    "GIP": "GIP",
    "GMD": "GMD",
    "GNF": "GNF",
    "GRT": "GRT",
    "GTQ": "GTQ",
    "GYD": "GYD",
    "HKD": "HKD",
    "HNL": "HNL",
    "HRK": "HRK",
    "HTG": "HTG",
    "HUF": "HUF",
    "IDR": "IDR",
    "ILS": "ILS",
    "IMP": "IMP",
    "INR": "INR",
    "IQD": "IQD",
    "ISK": "ISK",
    "JEP": "JEP",
    "JMD": "JMD",
    "JOD": "JOD",
    "JPY": "JPY",
    "KES": "KES",
    "KGS": "KGS",
    "KHR": "KHR",
    "KMF": "KMF",
    "KNC": "KNC",
    "KRW": "KRW",
    "KWD": "KWD",
    "KYD": "KYD",
    "KZT": "KZT",
    "LAK": "LAK",
    "LBP": "LBP",
    "LINK": "LINK",
    "LKR": "LKR",
    "LRC": "LRC",
    "LRD": "LRD",
    "LSL": "LSL",
    "LTC": "LTC",
    "LYD": "LYD",
    "MAD": "MAD",
    "MANA": "MANA",
    "MATIC": "MATIC",
    "MDL": "MDL",
    "MGA": "MGA",
    "MKD": "MKD",
    "MKR": "MKR",
    "MMK": "MMK",
    "MNT": "MNT",
    "MOP": "MOP",
    "MRO": "MRO",
    "MTL": "MTL",
    "MUR": "MUR",
    "MVR": "MVR",
    "MWK": "MWK",
    "MXN": "MXN",
    "MYR": "MYR",
    "MZN": "MZN",
    "NAD": "NAD",
    "NGN": "NGN",
    "NIO": "NIO",
    "NKN": "NKN",
    "NMR": "NMR",
    "NOK": "NOK",
    "NPR": "NPR",
    "NU": "NU",
    "NZD": "NZD",
    "OGN": "OGN",
    "OMG": "OMG",
    "OMR": "OMR",
    "OXT": "OXT",
    "PAB": "PAB",
    "PEN": "PEN",
    "PGK": "PGK",
    "PHP": "PHP",
    "PKR": "PKR",
    "PLN": "PLN",
    "POLY": "POLY",
    "PYG": "PYG",
    "QAR": "QAR",
    "RLY": "RLY",
    "REN": "REN",
    "REP": "REP",
    "RON": "RON",
    "RSD": "RSD",
    "RUB": "RUB",
    "RWF": "RWF",
    "SAR": "SAR",
    "SBD": "SBD",
    "SCR": "SCR",
    "SEK": "SEK",
    "SGD": "SGD",
    "SHIB": "SHIB",
    "SHP": "SHP",
    "SKL": "SKL",
    "SLL": "SLL",
    "SNX": "SNX",
    "SOS": "SOS",
    "SRD": "SRD",
    "SSP": "SSP",
    "STD": "STD",
    "STORJ": "STORJ",
    "SUSHI": "SUSHI",
    "SVC": "SVC",
    "SZL": "SZL",
    "THB": "THB",
    "TJS": "TJS",
    "TMT": "TMT",
    "TND": "TND",
    "TOP": "TOP",
    "TRY": "TRY",
    "TTD": "TTD",
    "TWD": "TWD",
    "TZS": "TZS",
    "UAH": "UAH",
    "UGX": "UGX",
    "UMA": "UMA",
    "UNI": "UNI",
    "USD": "USD",
    "USDC": "USDC",
    "UYU": "UYU",
    "UZS": "UZS",
    "VES": "VES",
    "VND": "VND",
    "VUV": "VUV",
    "WBTC": "WBTC",
    "WST": "WST",
    "XAF": "XAF",
    "XAG": "XAG",
    "XAU": "XAU",
    "XCD": "XCD",
    "XDR": "XDR",
    "XLM": "XLM",
    "XOF": "XOF",
    "XPD": "XPD",
    "XPF": "XPF",
    "XPT": "XPT",
    "XTZ": "XTZ",
    "YER": "YER",
    "YFI": "YFI",
    "ZAR": "ZAR",
    "ZEC": "ZEC",
    "ZMW": "ZMW",
    "ZRX": "ZRX",
    "ZWL": "ZWL",
}
