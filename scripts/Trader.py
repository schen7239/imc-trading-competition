from typing import Dict, List
import math
# FOR SUBMISSION USE
from datamodel import OrderDepth, TradingState, Order

# from ..classes.datamodel import OrderDepth, TradingState, Order

def calculate_vwap(state, product):
    market_directional_bias = 0
    directional_delta = 0
    buy_volume = sum(state.order_depths[product].buy_orders.values())
    sell_volume = sum(state.order_depths[product].sell_orders.values())
    buy_liquidity = min(state.order_depths[product].buy_orders.keys())
    sell_liquidity = max(state.order_depths[product].sell_orders.keys())
    total_volume = buy_volume + abs(sell_volume)
    for k, v in state.order_depths[product].buy_orders.items():
        market_directional_bias += (k - buy_liquidity) * v
    for k, v in state.order_depths[product].sell_orders.items():
        market_directional_bias += (sell_liquidity - k) * v
    directional_delta = market_directional_bias / total_volume
    vwap = (sell_liquidity + buy_liquidity) / 2 - directional_delta
    return buy_volume, sell_volume, buy_liquidity, sell_liquidity, total_volume, directional_delta, vwap

def calculate_bias_to_trading_position(state, directional_bias, trade_type):
    if state.timestamp == 0 or state.timestamp == 100 and trade_type == "BUY":
        return directional_bias
    elif trade_type == "BUY":
        return directional_bias * 5/(math.log(state.timestamp / 100))
    elif state.timestamp == 40000 or state.timestamp == 40100:
        return directional_bias
    return directional_bias * 5/(math.log((state.timestamp - 40000) / 100))
         

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
        max_position_size = {
            "BANANAS": 20,
            "PEARLS": 20,
            "BERRIES": 250,
            "DIVING_GEAR": 50
        }
        for product in state.order_depths.keys():
            if product == "PEARLS":
                holdings = state.position.get(product, 0)
                orders: list[Order] = []
                buy_volume = 0
                sell_volume = 0
                for k, v in state.order_depths[product].buy_orders.items():
                    if holdings + sell_volume < -math.ceil(2/3*max_position_size[product]):
                        break
                    if k > market_price[product] and v > 0:
                        orders.append(Order(product, k, -v))
                        sell_volume += v
                        
                for k, v in state.order_depths[product].sell_orders.items():
                    if holdings + buy_volume > math.ceil(2/3*max_position_size[product]):
                        break
                    if k < market_price[product] and v < 0:
                        orders.append(Order(product, k, -v))
                        buy_volume += v
                        
                orders.append(Order(product, market_price[product], buy_volume + sell_volume))
                result[product] = orders
            if product == "BANANAS":
                holding = state.position.get(product, 0)
                orders: list[Order] = []
                buy_volume, sell_volume, buy_liquidity, sell_liquidity, total_volume, directional_delta, vwap = calculate_vwap(state, product)
                volume_bought = 0
                volume_sold = 0
                vwap_ceiling = math.ceil(vwap)
                vwap_floor = math.floor(vwap)
                for k, v in state.order_depths[product].buy_orders.items():
                    if holding + volume_sold < -math.ceil(2/3*max_position_size[product]):
                        break
                    if k > vwap_ceiling and v > 0:
                        orders.append(Order(product, k, -v))
                        volume_sold += v
                for k, v in state.order_depths[product].sell_orders.items():
                    if holding + volume_bought > math.ceil(2/3*max_position_size[product]):
                        break
                    if k < vwap_floor and v < 0:
                        orders.append(Order(product, k, -v))
                        volume_bought += v
                if volume_bought + volume_sold > 0:
                    orders.append(Order(product, vwap_floor, volume_bought + volume_sold))
                elif volume_bought + volume_sold < 0:
                    orders.append(Order(product, vwap_ceiling, volume_bought + volume_sold))
                result[product] = orders
            elif product == "COCONUTS":
                # print(state.order_depths[product].buy_orders)
                # print(state.order_depths[product].sell_orders)
                pass
            elif product == "BERRIES":
                orders: list[Order] = []
                holding = state.position.get(product, 0)
                buy_volume, sell_volume, buy_liquidity, sell_liquidity, total_volume, directional_delta, vwap = calculate_vwap(state, product)
                if state.timestamp < 40000:
                    for k, v in state.order_depths[product].sell_orders.items():
                        if k < vwap + calculate_bias_to_trading_position(state, directional_delta, "BUY") and v < 0:
                            orders.append(Order(product, k, -v))
                elif state.timestamp < 80000 or holding > 0:
                    for k, v in state.order_depths[product].buy_orders.items():
                        if k > vwap - calculate_bias_to_trading_position(state, directional_delta, "SELL") and v > 0:
                            orders.append(Order(product, k, -v))
                else:
                    for k, v in state.order_depths[product].sell_orders.items():
                        if k < (buy_liquidity + sell_liquidity) / 2 and v < 0:
                            orders.append(Order(product, k, -v))
                result[product] = orders
            elif product == "DIVING_GEAR":
                # every 40000
                orders: list[Order] = []
                holding = state.position.get(product, 0)
                buy_volume, sell_volume, buy_liquidity, sell_liquidity, total_volume, directional_delta, vwap = calculate_vwap(state, product)
                print(holding)
                if state.timestamp < 35000:
                    for k, v in state.order_depths[product].sell_orders.items():
                        if k < vwap + calculate_bias_to_trading_position(state, directional_delta, "BUY") and v < 0:
                            orders.append(Order(product, k, -v))
                elif state.timestamp < 70000 or holding > 0:
                    for k, v in state.order_depths[product].buy_orders.items():
                        if k > vwap - calculate_bias_to_trading_position(state, directional_delta, "SELL") and v > 0:
                            orders.append(Order(product, k, -v))
                else:
                    for k, v in state.order_depths[product].sell_orders.items():
                        if k < (buy_liquidity + sell_liquidity) / 2 and v < 0:
                            orders.append(Order(product, k, -v))
                result[product] = orders
                     
                    
                     
            
        return result