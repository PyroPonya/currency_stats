import httpx
from typing import Dict, List

# Целевые валюты (пять основных)
CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CHF"]


async def fetch_rates() -> Dict[str, float]:
    """
    Асинхронно получает курсы RUB -> USD, EUR, GBP, JPY, CHF.
    Использует Frankfurter API v2 (бесплатно, без ключа).
    Возвращает словарь с курсами в рублях (сколько RUB стоит 1 единица валюты).
    """
    # Формируем строку целевых валют через запятую
    quotes_str = ",".join(CURRENCIES)
    url = f"https://api.frankfurter.dev/v2/rates?base=RUB&quotes={quotes_str}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()

            data: List[dict] = response.json()
            result = {}

            for item in data:
                currency = item["quote"]          # например "USD"
                rate_direct = item["rate"]        # сколько USD дают за 1 RUB
                # Нам нужно обратное: сколько RUB стоит 1 USD
                if rate_direct != 0:
                    result[currency.lower()] = 1 / rate_direct
                else:
                    # Защита от деления на ноль
                    result[currency.lower()] = 0.0

            # Проверяем, что получили все нужные валюты
            expected = {c.lower() for c in CURRENCIES}
            if not expected.issubset(result.keys()):
                missing = expected - result.keys()
                raise ValueError(f"Missing rates for currencies: {missing}")

            return result

        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"External API error: {e.response.status_code}")
        except (httpx.RequestError, ValueError) as e:
            print(f"Request/parse error: {e}")
            raise Exception(f"Failed to fetch or parse rates: {str(e)}")
