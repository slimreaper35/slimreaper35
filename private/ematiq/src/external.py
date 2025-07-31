import os

import cachetools
import httpx
import pendulum
import pydantic

CACHE_TTL_SECONDS = 2 * 60 * 60  # 2 hours
CACHE_MAX_SIZE = 1024

# https://freecurrencyapi.com/docs/currency-list
# Let's hardcode the list of available currencies for simplicity and to avoid unnecessary API calls
SUPPORTED_CURRENCIES = (
    "EUR", "USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK",
    "CHF", "ISK", "NOK", "HRK", "RUB", "TRY", "AUD", "BRL", "CAD", "CNY", "HKD",
    "IDR", "ILS", "INR", "KRW", "MXN", "MYR", "NZD", "PHP", "SGD", "THB", "ZAR",
)


class EuroExchangeRate(pydantic.BaseModel):
    """
    Basic model for Euro exchange rate.
    """

    date: str
    currency: str
    rate: float


class ExchangeRateError(Exception):
    """
    Custom exception for handling errors related to exchange rates.
    """


@cachetools.cached(cache=cachetools.TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL_SECONDS))
async def fetch_exchange_rate(date: str, currency: str) -> EuroExchangeRate:
    """
    Fetch the exchange rate for a given date and currency and cache the result.
    """
    if currency not in SUPPORTED_CURRENCIES:
        msg = f"Currency {currency} is not supported."
        raise ExchangeRateError(msg) from None

    request_url = "https://api.freecurrencyapi.com/v1/historical"

    api_key = os.getenv("FREECURRENCY_API_KEY")
    formatted_date = pendulum.parse(date).format("YYYY-MM-DD")
    params = {
        "apikey": api_key,
        "date": formatted_date,
        "base_currency": "EUR",
        "curencies": currency,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(request_url, params=params)
    except Exception as e:
        raise ExchangeRateError from e

    rate = response.json()["data"][formatted_date][currency]
    return EuroExchangeRate(date=formatted_date, currency=currency, rate=rate)
