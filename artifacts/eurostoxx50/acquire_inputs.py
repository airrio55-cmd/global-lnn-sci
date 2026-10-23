"""FRED/OECD monthly German yields and conservative cross-calendar timing."""
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

RATE_SERIES = 'IRLTLT01DEM156N'
RATE_SOURCE = Path('data/GERMANY_10Y_FRED_2010_2025.csv')


def parse_fred_monthly(payload):
    frame = pd.read_csv(io.BytesIO(payload), encoding='utf-8-sig', na_values=['.'])
    assert RATE_SERIES in frame.columns, 'FRED response does not contain the requested series'
    date_column = next((name for name in ['observation_date', 'DATE', 'date'] if name in frame.columns), None)
    assert date_column is not None, 'FRED response has no observation-date column'
    dates = pd.to_datetime(frame[date_column], errors='raise')
    assert dates.dt.day.eq(1).all(), 'Expected month-start observation labels'
    rates = pd.DataFrame({'DE10Y': pd.to_numeric(frame[RATE_SERIES], errors='raise').values}, index=dates)
    rates.index.name = 'Date'
    assert rates.index.is_unique and rates.index.is_monotonic_increasing
    return rates


def align_monthly_rates(rates, dates):
    """One monthly-period lag: January is usable from February 1 Europe/Berlin local time, not January.

    This follows the user-specified lag convention, not verified release dates.
    Initial dates before the first eligible month stay missing; never backfill.
    """
    events = rates.dropna().copy()
    events['observation_month'] = events.index
    available_dates = events.index + pd.DateOffset(months=1)
    events.index = available_dates.tz_localize('Europe/Berlin').tz_convert('UTC')
    cutoffs = (dates.tz_localize('Europe/Berlin') + pd.Timedelta(hours=17)).tz_convert('UTC')
    positions = events.index.searchsorted(cutoffs, side='right') - 1
    valid = positions >= 0
    chosen = events.iloc[positions[valid]]
    values = pd.Series(np.nan, index=dates, dtype=float)
    observation_months = pd.Series(pd.NaT, index=dates, dtype='datetime64[ns]')
    availability = pd.Series(pd.NaT, index=dates, dtype='datetime64[ns, UTC]')
    values.iloc[np.flatnonzero(valid)] = chosen.DE10Y.to_numpy()
    observation_months.iloc[np.flatnonzero(valid)] = chosen.observation_month.to_numpy()
    availability.iloc[np.flatnonzero(valid)] = chosen.index
    assert (pd.DatetimeIndex(availability[valid]) <= cutoffs[valid]).all()
    assert values[~valid].isna().all()
    return values, observation_months, availability


def day_end(date, zone):
    if pd.isna(date):
        return pd.NaT
    return (pd.Timestamp(date).normalize().tz_localize(zone) + pd.DateOffset(days=1)
            - pd.Timedelta(nanoseconds=1)).tz_convert('UTC')


def prepare_input_sources(ns):
    out = Path('artifacts/eurostoxx50')
    directory = out / 'sources'
    directory.mkdir(parents=True, exist_ok=True)
    metadata_path = out / 'sources_manifest.json'
    metadata = json.loads(metadata_path.read_text()) if metadata_path.exists() else {'sources': {}}
    downloader = ns['download_yf_series']
    specs = {'Close': '^STOXX50E', 'EUR_USD': 'EURUSD=X', 'VIX': '^VIX', 'SP500': '^GSPC'}
    loaded = {}

    def persist_metadata():
        metadata_path.write_text(json.dumps(metadata, indent=2))

    for name, ticker in specs.items():
        file = directory / (name + '.csv')
        if file.exists():
            assert hashlib.sha256(file.read_bytes()).hexdigest() == metadata['sources'][name]['sha256']
        else:
            frame = downloader(ticker, name)
            assert len(frame) > 3500 and frame.index.is_unique and frame.index.is_monotonic_increasing
            frame.to_csv(file, float_format='%.17g')
            metadata['sources'][name] = {'ticker': ticker, 'sha256': hashlib.sha256(file.read_bytes()).hexdigest(), 'downloaded_at_utc': datetime.now(timezone.utc).isoformat()}
            persist_metadata()
        loaded[name] = pd.read_csv(file, index_col=0, parse_dates=True, float_precision='round_trip')

    (out / 'unchanged_yahoo_sources.json').write_text(json.dumps({name: metadata['sources'][name]['sha256'] for name in specs}, indent=2))
    rates_file = directory / 'de10y_monthly.csv'
    payload = RATE_SOURCE.read_bytes()
    source_hash = hashlib.sha256(payload).hexdigest()
    if rates_file.exists():
        assert metadata['sources']['DE10Y']['series'] == RATE_SERIES
        assert metadata['sources']['DE10Y']['repository_csv_sha256'] == source_hash
        assert hashlib.sha256(rates_file.read_bytes()).hexdigest() == metadata['sources']['DE10Y']['sha256']
    else:
        rates = parse_fred_monthly(payload).loc[ns['START_DATE']:ns['END_DATE']]
        required = pd.date_range('2010-01-01', '2025-12-01', freq='MS')
        assert rates.reindex(required).DE10Y.notna().all(), 'Required monthly yield history has missing months'
        assert np.isfinite(rates.reindex(required).DE10Y).all()
        rates.to_csv(rates_file, float_format='%.17g')
        metadata['sources']['DE10Y'] = {'repository_csv': str(RATE_SOURCE), 'series': RATE_SERIES,
                                      'frequency': 'monthly', 'provider': 'FRED/OECD',
                                      'unit': 'percent per annum',
                                      'vintage': 'repository-provided historical values; real-time vintages not supplied',
                                      'sha256': hashlib.sha256(rates_file.read_bytes()).hexdigest(),
                                      'repository_csv_sha256': source_hash,
                                      'loaded_at_utc': datetime.now(timezone.utc).isoformat()}
        persist_metadata()
    rates = pd.read_csv(rates_file, index_col=0, parse_dates=True, float_precision='round_trip')
    dates = loaded['Close'].index
    assert dates.tz is None and dates.is_monotonic_increasing and dates.is_unique
    timing = pd.DataFrame(index=dates)
    timing.index.name = 'Date'
    timing['Close_available_at_utc'] = [day_end(date, 'Europe/Berlin') for date in dates]
    for name in ['EUR_USD', 'VIX', 'SP500']:
        source = loaded[name]
        lagged_values = source[name].shift(1)
        source_dates = pd.Series(source.index, index=source.index).shift(1).where(lagged_values.notna())
        source_dates = source_dates.reindex(dates).ffill()
        assert (source_dates.dropna() < source_dates.dropna().index).all()
        timing[name + '_source_date'] = source_dates
        timing[name + '_available_at_utc'] = [day_end(date, 'America/New_York') for date in source_dates]

    aligned, source_dates, rate_times = align_monthly_rates(rates, dates)
    pd.DataFrame({'DE10Y': aligned}, index=dates).to_csv(directory / 'de10y_lagged.csv', float_format='%.17g')
    timing['DE10Y_source_date'] = source_dates

    timing['DE10Y_available_at_utc'] = rate_times
    timing.to_csv(out / 'availability.csv')
    metadata['timing_policy'] = {'EUR_USD': 'one source-observation lag, then European reindex and forward-fill',
                                 'VIX': 'one U.S. source-observation lag, then European reindex and forward-fill',
                                 'SP500': 'one U.S. source-observation lag, then European reindex and forward-fill',
                                 'DE10Y': 'repository CSV only; one monthly-period lag; month M usable from first day of M+1 Europe/Berlin local time; backward as-of/forward-fill on European dates; initial missing values never backfilled',
                                 'Close': 'conservative European day-end availability',
                                 'US_inputs': 'conservative source-date New York day-end availability',
                                 'EURUSD_availability': 'Yahoo daily label is not an audited intraday publication timestamp. Bound availability at source-date New York day-end after one source-observation lag, and use only rows preceding target date; no same-day FX close is assumed available.',
                                 'no_bfill': True}
    metadata['availability_sha256'] = hashlib.sha256((out / 'availability.csv').read_bytes()).hexdigest()
    persist_metadata()

    def cached_download(ticker, out_name, start=ns['START_DATE'], end=ns['END_DATE']):
        if start == ns['START_DATE'] and end == ns['END_DATE'] and ticker in specs.values():
            name = next(name for name, value in specs.items() if value == ticker)
            frame = loaded[name].copy()
            frame.columns = [out_name]
            return frame
        raise RuntimeError('This run uses frozen inputs only; network input refresh is disabled')

    ns['download_yf_series'] = cached_download
    return metadata
