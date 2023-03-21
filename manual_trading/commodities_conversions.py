from collections import deque

class Graph:
    def __init__(self, trading_list: list, commodities: list) -> None:
        self.trading_list = trading_list
        self.commodities = commodities
        
class Graph:
    def __init__(self, trading_list: list[list], commodities: list[tuple]) -> None:
        self.trading_list = trading_list
        self.commodities = commodities
    
    def calculate_best_trades(self, num_possible_trades: int, starting_pos: int):
        res = deque([starting_pos])
        start_bal = 1
        num_items = ["shells", 1]
        iter = num_possible_trades
        while iter > 0:
            con = self.trading_list[res[0]]
            iter = iter - 1
            conv_to_shells = []
            for idx, i in enumerate(con):
                price_in_shells = self.trading_list[idx][starting_pos] * i * num_items[1]
                if idx == res[0]:
                    conv_to_shells.append(0)
                else:
                    conv_to_shells.append(price_in_shells)
            
            highest_conv = max(conv_to_shells)
            if highest_conv >= start_bal:
                start_bal = highest_conv
                highest_idx = conv_to_shells.index(highest_conv)
                num_items = [commodities_name[highest_idx][0], con[highest_idx] * num_items[1]]
                res.appendleft(highest_idx)
            else:
                break
            
            
        

trading_list = [
    [1, 0.5, 1.45, .75],
    [1.95, 1, 3.1, 1.49],
    [.67, .31, 1, .48],
    [1.34, 0.64, 1.98, 1]
]

commodities_name = [["pizza", 0], ["wasabi", 1], ["snowball", 2], ["shells", 3]]

g = Graph(trading_list, commodities_name)
g.calculate_best_trades(4, 3)
