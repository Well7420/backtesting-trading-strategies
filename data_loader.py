import ccxt
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import os
from datetime import datetime
import time


class DataLoader:
    def __init__(self, start_date: str, end_date: str, cache_dir: str = "data"):
        self.exchange = ccxt.binance({
            'apiKey': 'API_KEY',  # Сюди потрібно вказати API-ключ свого Binance акаунту
            'secret': 'SECRET_KEY',  # Сюди потрібно вказати секретний ключ
            'enableRateLimit': True,  # Увімкнення обмеження частоти запитів
        })
        self.start_ts = int(datetime.strptime(
            start_date, "%Y-%m-%d").timestamp() * 1000)
        self.end_ts = int(datetime.strptime(
            end_date, "%Y-%m-%d").timestamp() * 1000)
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_top_pairs(self, n: int = 100) -> list:
        # Функція отримує список топ-N пар до BTC за обсягом торгів.
        markets = self.exchange.load_markets()
        btc_pairs = [m for m in markets if m.endswith("/BTC")]
        # Для реального сортування за обсягом потрібен запит до API, тут просто перші n пар
        return btc_pairs[:n]

    def fetch_ohlcv(self, symbol: str, timeframe: str = "1m", limit: int = 1000) -> pd.DataFrame:
        # Функція завантажує OHLCV-дані з Binance з розбиттям на частини.
        cache_file = f"{self.cache_dir}/{symbol.replace('/', '_')}_1m.parquet"
        if os.path.exists(cache_file):
            print(f"Loading cached data for {symbol} from {cache_file}")
            return pd.read_parquet(cache_file)

        all_data = []
        current_ts = self.start_ts

        while current_ts < self.end_ts:
            # Цикл завантажує дані по частинам, поки не досягнуто кінцевого таймстемпу
            try:
                print(
                    f"Fetching {symbol} from {datetime.fromtimestamp(current_ts / 1000)}")
                ohlcv = self.exchange.fetch_ohlcv(
                    symbol=symbol,
                    timeframe=timeframe,
                    since=current_ts,
                    limit=limit
                )
                if not ohlcv:
                    break  # Якщо даних більше немає, цикл завершується

                all_data.extend(ohlcv)
                # Наступний запит після останнього таймстемпу
                current_ts = ohlcv[-1][0] + 1
                time.sleep(0.1)  # Пауза для дотримання лімітів API

            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                break

        if not all_data:
            raise ValueError(f"No data fetched for {symbol}")

        # Перетворюємо в DataFrame
        df = pd.DataFrame(all_data, columns=[
                          "timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        # Зберігаємо в .parquet
        pq.write_table(pa.Table.from_pandas(
            df), cache_file, compression="snappy")
        print(f"Saved data for {symbol} to {cache_file}")
        return df

    def load_all_data(self, pairs: list) -> dict:
        """Завантажує дані для всіх пар."""
        return {pair: self.fetch_ohlcv(pair) for pair in pairs}


# Приклад використання
if __name__ == "__main__":
    loader = DataLoader("2025-02-01", "2025-02-28")
    pairs = loader.get_top_pairs(5)  # Тестуємо на 5 парах для швидкості
    data = loader.load_all_data(pairs)
    print(f"Loaded data for {len(data)} pairs.")
