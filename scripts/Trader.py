from typing import Dict, List
# FOR SUBMISSION USE
from datamodel import OrderDepth, TradingState, Order

# from ..classes.datamodel import OrderDepth, TradingState, Order


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        positions = state.position
        result = {}
        for product in state.order_depths.keys():
            position = positions.get(product, 0)
            buy_liquidity = max(state.order_depths[product].buy_orders)
            sell_liquidity = min(state.order_depths[product].sell_orders)
            buy_volume = sum(state.order_depths[product].buy_orders.values())
            sell_volume = sum(state.order_depths[product].sell_orders.values())
            
            trade_volume = buy_volume + sell_volume + position
            if buy_volume + sell_volume == 0:
                continue
            elif trade_volume == 0:
                continue
            elif trade_volume > 0:
                result[product] = [Order(product, -trade_volume, sell_liquidity)]
            else:
                result[product] = [Order(product, trade_volume, buy_liquidity)]
            
            
        return result