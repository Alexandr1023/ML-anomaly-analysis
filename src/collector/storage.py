from collector import collect_metrics
from pandas import DataFrame, Timestamp
import asyncio, time
from inspect import iscoroutinefunction
from pathlib import Path

script_dir = Path(__file__).resolve() # this file path
project_root = script_dir.parent.parent.parent # going up 2 folders
output_dir = project_root / "data" / "raw" # .parquet saving path

cache = []
errors = []

metric_collect_interval = 1.0 # seconds
parquet_creating_interval = 10.0 # seconds

async def cache_data() -> None: # caching data with error serving
    data = collect_metrics()
    try:
        cache.append(data)
    except Exception as e:
        pd_time = Timestamp.now()
        pd_timestamp = pd_time.timestamp()
        ts = data.get_timestamp if data is not None else pd_timestamp
        error_message = f"Error occured while caching data, timestamp: {ts}. Error: {e}"
        errors.append(error_message)
        print(error_message)

def get_cached_dataframe(): # making dataframe from batch of cached metrics
    return DataFrame([m for m in cache])

def save_to_parquet() -> None: # saving data to .parquet
    df = get_cached_dataframe()
    if df.empty:
        return
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    df.to_parquet(output_dir / f"metrics_{timestamp}.parquet")
    cache.clear()


async def run_every(job, interval: float): # timer'ed function calling without interval losses
    start = time.monotonic()
    n = 0
    while True:
        if iscoroutinefunction(job):
            await job()
        else:
            job()
        n += 1
        next_target = start + n * interval
        await asyncio.sleep(max(0, next_target - time.monotonic()))
 
 
async def main(): # async calling timer manager
    await asyncio.gather(
        run_every(cache_data, metric_collect_interval),
        run_every(save_to_parquet, parquet_creating_interval),
    )
 
 
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped")