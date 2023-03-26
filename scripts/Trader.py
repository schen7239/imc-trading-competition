from typing import Dict, List
# FOR SUBMISSION USE
from datamodel import OrderDepth, TradingState, Order

# from ..classes.datamodel import OrderDepth, TradingState, Order

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        positions = state.position
        result = {}
        for product in state.order_depths.keys():
            if product == "BANANAS" or product == "PEARLS":
                position = positions.get(product, 0)
                print(position)
                
                buy_liquidity = min(state.order_depths[product].buy_orders)
                sell_liquidity = max(state.order_depths[product].sell_orders)
                buy_volume = sum(state.order_depths[product].buy_orders.values())
                sell_volume = sum(state.order_depths[product].sell_orders.values())
                consolidated_order_book = [0 for _ in range(sell_liquidity - buy_liquidity + 1)]
                
                order_book_bias = 0
                
                volume_sold = 0
                volume_bought = 0
                
                orders = list[Order]
                
                for key, value in state.order_depths[product].buy_orders.items():
                    consolidated_order_book[key - buy_liquidity] += value
                
                for key, value in state.order_depths[product].sell_orders.items():
                    consolidated_order_book[key - buy_liquidity] += value
                    
                for idx, val in enumerate(consolidated_order_book):
                    if val == 0:
                        continue
                    elif val > 0:
                        order_book_bias += (len(consolidated_order_book) - 1 - idx) * val
                    else:
                        order_book_bias += (idx) * val
                        
                if order_book_bias == 0 and len(state.order_depths[product].buy_orders) == len(state.order_depths[product].sell_orders):
                    return result
                
                print(state.order_depths[product].buy_orders)
                print(state.order_depths[product].sell_orders)
                
                for i in reversed(range(len(consolidated_order_book) - 1, 0, -1)):
                    if i == 0:
                        break
                    if consolidated_order_book[i] <= 0:
                        continue
                    # print(f'SELL {consolidated_order_book[i]} at {buy_liquidity + i}')
                    orders.append(Order(product, buy_liquidity + i, -consolidated_order_book[i]))
                    volume_sold += consolidated_order_book[i]
                    consolidated_order_book[i] = 0
                
                if volume_sold > 0:
                    # print("BUY", volume_sold)
                    orders.append(Order(product, buy_liquidity, volume_sold))
                    
                for i in range(len(consolidated_order_book) - 1):
                    if i == len(consolidated_order_book) - 1:
                        break
                    if consolidated_order_book[i] >= 0:
                        continue
                    # print(f'BUY {consolidated_order_book[i]} at {buy_liquidity + i}')
                    orders.append(Order(product, buy_liquidity + i, consolidated_order_book[i]))
                    volume_bought += consolidated_order_book[i]
                    consolidated_order_book[i] = 0
                
                if volume_bought < 0:
                    # print(f'SELL {volume_bought}',)
                    orders.append(Order(product, sell_liquidity, volume_bought))
                
                result[product] = orders
        
            
            
            
        return result