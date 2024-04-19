from utils.strategy.indicators.sma import SMA
from utils import constants

sme = SMA(constants.Indicators.EMA, constants.Timeframe.D1,
          length=20, source=constants.Sources.CLOSE)

print(sme.name.name)
