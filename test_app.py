import math
import pandas as pd

def compute_metrics(gdp_df, from_year, to_year, selected_countries):
    first_year = gdp_df[gdp_df['Year'] == from_year]
    last_year = gdp_df[gdp_df['Year'] == to_year]

    first_gdp_map = first_year.set_index('Country Code')['GDP'].to_dict()
    last_gdp_map = last_year.set_index('Country Code')['GDP'].to_dict()

    results = []
    for country in selected_countries:
        first_gdp_val = first_gdp_map.get(country, math.nan)
        last_gdp_val = last_gdp_map.get(country, math.nan)

        first_gdp = first_gdp_val / 1000000000
        last_gdp = last_gdp_val / 1000000000

        if math.isnan(first_gdp):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_gdp / first_gdp:,.2f}x'
            delta_color = 'normal'

        results.append({
            'country': country,
            'last_gdp': f'{last_gdp:,.0f}B',
            'growth': growth,
            'delta_color': delta_color
        })
    return results

def test_compute_metrics():
    df = pd.DataFrame([
        {'Country Code': 'DEU', 'Year': 2000, 'GDP': 2_000_000_000_000.0},
        {'Country Code': 'DEU', 'Year': 2020, 'GDP': 3_800_000_000_000.0},
        {'Country Code': 'FRA', 'Year': 2000, 'GDP': float('nan')},
        {'Country Code': 'FRA', 'Year': 2020, 'GDP': 2_600_000_000_000.0},
    ])

    metrics = compute_metrics(df, 2000, 2020, ['DEU', 'FRA'])

    assert metrics[0]['country'] == 'DEU'
    assert metrics[0]['last_gdp'] == '3,800B'
    assert metrics[0]['growth'] == '1.90x'
    assert metrics[0]['delta_color'] == 'normal'

    assert metrics[1]['country'] == 'FRA'
    assert metrics[1]['last_gdp'] == '2,600B'
    assert metrics[1]['growth'] == 'n/a'
    assert metrics[1]['delta_color'] == 'off'
