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
    elif state.timestamp == 40000 or state.timestamp == 40100 and trade_type == "SELL":
        return directional_bias
    elif trade_type == "SELL":
        return directional_bias * 5/(math.log((state.timestamp / 100 - 40)))
    return 0
         
def calculate_trading_position_for_price_trending_assets(vwap, price, max_volume, vol_range):
    calc_prob = abs(price - vwap) / vol_range
    # logit function - buy more volume as the price deviates more from the market price
    return math.ceil(max_volume * 0.02 * abs(math.log(calc_prob / (1 - calc_prob))))

class Trader:
    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}
        basket_item_price = {
            
        }
        basket_price = 0
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
            "DIVING_GEAR": 50,
            "COCONUTS": 600,
            "PINA_COLADAS": 300,
            "BAGUETTE": 150,
            "DIP": 300,
            "UKULELE": 70,
            "PICNIC_BASKET": 70
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
                holding = state.position.get(product, 0)
                orders: list[Order] = []
                buy_volume, sell_volume, buy_liquidity, sell_liquidity, total_volume, directional_delta, vwap = calculate_vwap(state, product)
                
                if market_price[product] - vwap < -200:
                    orders.append(Order(product, vwap, -calculate_trading_position_for_price_trending_assets(vwap, market_price[product], max_position_size[product], 120)))
                elif market_price[product] - vwap < -50:
                    orders.append(Order(product, vwap, calculate_trading_position_for_price_trending_assets(vwap, market_price[product], max_position_size[product], 120)))
                elif market_price[product] - vwap < 50:
                    orders.append(Order(product, vwap, -calculate_trading_position_for_price_trending_assets(vwap, market_price[product], max_position_size[product], 120)))
                elif market_price[product] - vwap < 200:
                    orders.append(Order(product, vwap, calculate_trading_position_for_price_trending_assets(vwap, market_price[product], max_position_size[product], 120)))
                result[product] = orders
                pass
            elif product == "PINA_COLADAS":
                holding = state.position.get(product, 0)
                orders: list[Order] = []
                buy_volume, sell_volume, buy_liquidity, sell_liquidity, total_volume, directional_delta, vwap = calculate_vwap(state, product)
                if market_price[product] - vwap < -200:
                    orders.append(Order(product, vwap, -calculate_trading_position_for_price_trending_assets(vwap, market_price[product], max_position_size[product], 200)))
                elif market_price[product] - vwap < -50:
                    orders.append(Order(product, vwap, calculate_trading_position_for_price_trending_assets(vwap, market_price[product], max_position_size[product], 200)))
                elif market_price[product] - vwap < 50:
                    orders.append(Order(product, vwap, -calculate_trading_position_for_price_trending_assets(vwap, market_price[product], max_position_size[product], 200)))
                elif market_price[product] - vwap < 200:
                    orders.append(Order(product, vwap, calculate_trading_position_for_price_trending_assets(vwap, market_price[product], max_position_size[product], 200)))
                result[product] = orders
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
                orders: list[Order] = []
                holding = state.position.get(product, 0)
                buy_volume, sell_volume, buy_liquidity, sell_liquidity, total_volume, directional_delta, vwap = calculate_vwap(state, product)
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
            elif product == "BAGUETTE":
                buy_volume, sell_volume, buy_liquidity, sell_liquidity, total_volume, directional_delta, vwap = calculate_vwap(state, product)
                basket_item_price[product] = vwap
            elif product == "PICNIC_BASKET":
                buy_volume, sell_volume, buy_liquidity, sell_liquidity, total_volume, directional_delta, vwap = calculate_vwap(state, product)
                basket_price = vwap
            elif product == "DIP":
                buy_volume, sell_volume, buy_liquidity, sell_liquidity, total_volume, directional_delta, vwap = calculate_vwap(state, product)
                basket_item_price[product] = vwap
            elif product == "UKULELE":
                buy_volume, sell_volume, buy_liquidity, sell_liquidity, total_volume, directional_delta, vwap = calculate_vwap(state, product)
                basket_item_price[product] = vwap
        # one picnic basket has 2 baguettes, 4 dips, and 1 ukelele
        # you can trade the price discrepancy between the finished product and the items that make up the picnic basket
        total_item_price = sum(basket_item_price.values())
            
        bag_order = []
        dip_order = []
        picnic_order = []
        uke_order = []
            
        if basket_price - total_item_price > 10:
            bag_order.append(Order("BAGUETTE", basket_item_price["BAGUETTE"], 2))
            dip_order.append(Order("DIP", basket_item_price["DIP"], 4))
            picnic_order.append(Order("PICNIC_BASKET", basket_price, -1))
            uke_order.append(Order("UKULELE", basket_item_price["UKULELE"], 1))
        elif basket_price - total_item_price < -10:
            bag_order.append(Order("BAGUETTE", basket_item_price["BAGUETTE"], -2))
            dip_order.append(Order("DIP", basket_item_price["DIP"], -4))
            picnic_order.append(Order("PICNIC_BASKET", basket_price, 1))
            uke_order.append(Order("UKULELE", basket_item_price["UKULELE"], -1))
            
        result["BAGUETTE"] = bag_order
        result["DIP"] = dip_order
        result["PICNIC_BASKET"] = picnic_order
        result["UKELELE"] = uke_order
                
        return result