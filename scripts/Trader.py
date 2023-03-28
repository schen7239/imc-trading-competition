from typing import Dict, List
# FOR SUBMISSION USE
from datamodel import OrderDepth, TradingState, Order

# from ..classes.datamodel import OrderDepth, TradingState, Order

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}
        market_price = {
            "BANANAS": 5000,
            "PEARLS": 10000,
            'BAGUETTE': 0, 
            'BERRIES': 0, 
            'COCONUTS': 8000, 
            'DIP': 0, 
            'DIVING_GEAR': 0, 
            'PICNIC_BASKET': 0, 
            'PINA_COLADAS': 15000, 
            'UKULELE':0
        }
        for product in state.order_depths.keys():
            if product == "PEARLS":
                orders: list[Order] = []
                buy_volume = 0
                sell_volume = 0
                for k, v in state.order_depths[product].buy_orders.items():
                    if k > market_price[product] and v > 0:
                        orders.append(Order(product, k, -v))
                        sell_volume += v
                        
                for k, v in state.order_depths[product].sell_orders.items():
                    if k < market_price[product] and v < 0:
                        orders.append(Order(product, k, -v))
                        buy_volume += v
                        
                orders.append(Order(product, market_price[product], buy_volume + sell_volume))
                result[product] = orders
            if product == "BANANAS":
                orders: list[Order] = []
                market_directional_bias = 0
                directional_delta = 0
                buy_volume = sum(state.order_depths[product].buy_orders.values())
                sell_volume = sum(state.order_depths[product].sell_orders.values())
                buy_liquidity = min(state.order_depths[product].buy_orders.keys())
                sell_liquidity = max(state.order_depths[product].sell_orders.keys())
                total_volume = buy_volume + abs(sell_volume)
                volume_bought = 0
                for k, v in state.order_depths[product].buy_orders.items():
                    market_directional_bias += (k - buy_liquidity) * v
                for k, v in state.order_depths[product].sell_orders.items():
                    market_directional_bias += (sell_liquidity - k) * v
                directional_delta = market_directional_bias / total_volume
                vwap = (sell_liquidity + buy_liquidity) / 2 - directional_delta
                volume_bought = 0
                volume_sold = 0
                for k, v in state.order_depths[product].buy_orders.items():
                 if k > vwap and v > 0:
                        orders.append(Order(product, k, -v))
                        volume_sold += v
                        
                for k, v in state.order_depths[product].sell_orders.items():
                    if k < vwap and v < 0:
                        orders.append(Order(product, k, -v))
                        volume_bought += v
                orders.append(Order(product, vwap, volume_bought + volume_sold))
                print(volume_bought + volume_sold)
                result[product] = orders
                
            
        return result