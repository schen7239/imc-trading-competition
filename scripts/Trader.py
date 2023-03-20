from typing import Dict, List
# FOR SUBMISSION USE
from datamodel import OrderDepth, TradingState, Order

# from ..classes.datamodel import OrderDepth, TradingState, Order


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        
        result = {}
        for product in state.order_depths.keys():
            order_depth: OrderDepth = state.order_depths[product]
            print(f'Product: {product}')
            print(order_depth.buy_orders)
            print(order_depth.sell_orders)
            print("\n\n")
        return result