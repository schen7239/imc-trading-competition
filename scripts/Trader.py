from typing import Dict, List
# FOR SUBMISSION USE
from datamodel import OrderDepth, TradingState, Order

# from ..classes.datamodel import OrderDepth, TradingState, Order

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}
        market_price = {
            "BANANAS": 5000,
            "PEARLS": 10000
        }
        for product in state.order_depths.keys():
            if product == "PEARLS" or product == "BANANAS":
                orders: list[Order] = []
                buy_volume = 0
                sell_volume = 0
                print(market_price[product])
                for k, v in state.order_depths[product].buy_orders.items():
                    if k > market_price[product] and v > 0:
                        orders.append(Order(product, k, -v))
                        print("PEARL", )
                        sell_volume += v
                        
                for k, v in state.order_depths[product].sell_orders.items():
                    if k < market_price[product] and v < 0:
                        orders.append(Order(product, k, -v))
                        buy_volume += v
                        
                orders.append(Order(product, market_price[product], buy_volume + sell_volume))
                result[product] = orders
                
            
                
                
        
            
            
            
        return result