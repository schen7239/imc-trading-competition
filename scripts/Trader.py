from typing import Dict, List
# FOR SUBMISSION USE
# from datamodel import OrderDepth, TradingState, Order
from ..classes.datamodel import OrderDepth, TradingState, Order


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
		"""
		Takes all buy and sell orders for all symbols as an input,
		and outputs a list of orders to be sent
		"""
        result = {}
        return result