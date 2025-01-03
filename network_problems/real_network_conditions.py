from network_conditions import NetworkConditions

CONDITIONS_LTE = NetworkConditions(
    delay=40, delay_delta=10, distribution_type="normal", loss=0.5, bandwidth=100
)
CONDITIONS_3G = NetworkConditions(
    delay=250, delay_delta=50, distribution_type="normal", loss=2, bandwidth=2
)
CONDITIONS_WIFI = NetworkConditions(
    delay=40, delay_delta=10, distribution_type="normal", loss=0.2, bandwidth=30
)
CONDITIONS_FAST_WITHOUT_DELAY = NetworkConditions(
    delay=0, delay_delta=0, distribution_type="normal", loss=0.5, bandwidth=20
)

REAL_CONDITIONS = {
    "lte": CONDITIONS_LTE,
    "wifi": CONDITIONS_WIFI,
    "3g": CONDITIONS_3G,
    "without-delay": CONDITIONS_FAST_WITHOUT_DELAY,
}
