import pyotp
import json
import requests


PUBG = 578080
PAY_DAY2 = 218620
KILLING_FLOOR_2 = 232090
RUST = 252490
DEPTH = 274940
UNTURNED = 304930
CSGO = 730
DOTA2 = 570
TF2 = 440


SORT_BY_CREATED = "created_at"
SORT_BY_PRICE = "price"
SORT_BY_WEAR_VALUE = "wear_value"
DESCENDING = "desc"
ASCENDING = "asc"
PAYPAL = "paypal"
SKRILL = "skrill"
INSTANT = "instant"
RESERVED_PRICE = 4895.11

class BitSkins:
    '''
    API Wrapper Class for the BitSkins API\n
    ---
    Arguments:
    * api_key - API Key for BitSkins
    * secret - Secret code given when activating API on Authy
    '''
    def __init__(self, api_key:str, secret:str):
        self.__api_key = api_key
        self.__secret = secret
    
    def getAccountBalance(self) -> dict:
        '''
        Allows you to retrieve your available and pending balance in all currencies supported by BitSkins.\n
        ---
        Return type: dictionary
        '''
        code = pyotp.TOTP(self.__secret).now()
        data = requests.get(f"https://bitskins.com/api/v1/get_account_balance/?api_key={self.__api_key}&code={code}").json()

        if data['status'] == "fail":
            raise Exception(data['data']['error_message'])

        return data

    def getAllItemPrices(self, game:int=CSGO) -> dict:
        '''
        Allows you to retrieve the entire price database used at BitSkins.\n
        ---
        Arguments:
        * game - The app_id for the inventory's game (defaults to CSGO if not specified). (optional)
        ---
        Return type: dictionary
        '''
        code = pyotp.TOTP(self.__secret).now()
        data = requests.get(f"https://bitskins.com/api/v1/get_all_item_prices/?api_key={self.__api_key}&code={code}&app_id={game}").json()

        if data['status'] == "fail":
            raise Exception(data['data']['error_message'])

        return data

    def getMarkePriceData(self, game:int=CSGO) -> dict:
        '''
        Allows you to retrieve basic price data for items currently on sale at BitSkins.\n
        Arguments:
        * game - The app_id for the inventory's game (defaults to CSGO if not specified). (optional)
        ---
        Return type: dictionary
        '''
        code = pyotp.TOTP(self.__secret).now()
        data = requests.get(f"https://bitskins.com/api/v1/get_price_data_for_items_on_sale/?api_key={self.__api_key}&code={code}&app_id={game}").json()

        if data['status'] == "fail":
            raise Exception(data['data']['error_message'])

        return data

    def getAccountInventory(self, game:int=CSGO, page:int=1) -> dict:
        '''
        Allows you to retrieve your account's available inventory on Steam (items listable for sale), your BitSkins inventory (items currently on sale), and your pending withdrawal inventory (items you delisted or purchased).\n
        As of January 20th 2016, only the newest 5,000 items are shown by default for the BitSkins inventory. Use page numbers to see all items.\n
        ---
        Arguments:
        * game - The app_id for the inventory's game (defaults to CSGO if not specified). (optional)
        * page - Page number for BitSkins inventory. (optional)
        ---
        Return type: dict
        '''
        code = pyotp.TOTP(self.__secret).now()
        data = requests.get(f"https://bitskins.com/api/v1/get_my_inventory/?api_key={self.__api_key}&code={code}&page={page}&app_id={game}").json()

        if data['status'] == "fail":
            raise Exception(data['data']['error_message'])

        return data

    def getInventoryOnSale(self, game:int=CSGO, page:int=1, sort_by:str=None, order:str=None, market_hash_name:str=None, min_price:float=None, 
    max_price:float=None, has_stickers:int=None, is_stattrak:int=None, is_souvenir:int=None, per_page:int=None, show_trade_delayed_items:int=None) -> dict:
        '''
        Retrieve dict of BitSkins inventory currently on sale\n
        ---
        Arguments:
        * page - Page number. (optional)\n
        * game - The app_id for the inventory's game (defaults to CSGO if not specified). (optional)\n
        * sort_by - {SORT_BY_CREATED|SORT_BY_PRICE}. CSGO only: SORT_BY_WEAR_VALUE. (optional)\n
        * order - {DESCENDING|ASCENDING} (optional)\n
        * market_hash_name - Full or partial item name (optional)\n
        * min_price - Minimum price (optional)\n
        * max_price - Maximum price (optional)\n
        * has_stickers - {False|None|True}. For CSGO only. (optional)\n
        * is_stattrak - {False|None|True}. For CSGO only. (optional)\n
        * is_souvenir - {False|None|True}. For CSGO only. (optional)\n
        * per_page - esults per page. Must be 24, 30, 60, 64, 120, 128, 240 or 480 (optional)\n
        * show_trade_delayed_items - {False|None|True}. For CSGO only.\n
        ---
        Return type: dictionary
        '''
        code = pyotp.TOTP(self.__secret).now()    
        request_str = f"https://bitskins.com/api/v1/get_inventory_on_sale/?api_key={self.__api_key}&code={code}&page={page}&app_id={game}"

        #format request
        if sort_by != None:
            if sort_by == SORT_BY_WEAR_VALUE and game != CSGO:
                raise Exception("SORT_BY_WEAR_VALUE only applies to CSGO")
            else:
                request_str += f"&sort_buy={sort_by}"

        if order != None:
            request_str += f"&order={order}"

        if market_hash_name != None:
            request_str += f"&market_hash_name={market_hash_name}"
        
        if min_price != None:
            request_str += f"&min_price={min_price}"

        if max_price != None:
            request_str += f"&max_price={max_price}"

        if has_stickers == None:
            if game == CSGO:
                request_str += f"&has_stickers=0"
        else:
            if game == CSGO:
                request_str += f"&has_stickers={int(has_stickers)}"
            else:
                raise Exception("has_stickers only applies to CSGO")

        if is_stattrak == None:
            if game == CSGO:
                request_str += f"&is_stattrak=0"
        else:
            if game == CSGO:
                request_str += f"&is_stattrak={int(is_stattrak)}"
            else:
                raise Exception("is_stattrak only applies to CSGO")

        if is_souvenir == None:
            if game == CSGO:
                request_str += f"&is_souvenir=0"
        else:
            if game == CSGO:
                request_str += f"&is_souvenir={int(is_souvenir)}"
            else:
                raise Exception("is_souvenir only applies to CSGO")

        if show_trade_delayed_items == None:
            if game == CSGO:
                request_str += f"&show_trade_delayed_items=0"
        else:
            if game == CSGO:
                request_str += f"&show_trade_delayed_items={int(show_trade_delayed_items)}"
            else:
                raise Exception("show_trade_delayed_items only applies to CSGO")

        page_nums = [24,30,60,64,120,128,240,480]
        if per_page != None:
            if per_page in page_nums:
                request_str += f"&per_page={per_page}"
            else:
                raise Exception(f"per_page must be one of the following: {page_nums}")
        
        data = requests.get(request_str).json()

        if data['status'] == "fail":
            raise Exception(data['data']['error_message'])

        return data

    def getSpecificItemsOnSale(self, item_ids:list=None, game:int=CSGO) -> dict:
        '''
        Allows you to retrieve data for specific Item IDs that are currently on sale. To gather Item IDs you wish to track/query, see the 'Get Inventory on Sale' API call for items currently on sale.\n
        ---
        Arguments:
        * Upto 250 item ID's in a list of strings
        * game - The app_id for the inventory's game (defaults to CSGO if not specified). (optional)\n
        ---
        Return type: dict
        '''
        if item_ids == None:
            raise Exception("Must provide item id's for API call")

        comma_seperated_ids = str(item_ids)[1:-1]
        comma_seperated_ids = comma_seperated_ids.replace("'", "")
        comma_seperated_ids = comma_seperated_ids.replace(" ", "")

        code = pyotp.TOTP(self.__secret).now()   
        data = requests.get(f"https://bitskins.com/api/v1/get_specific_items_on_sale/?api_key={self.__api_key}&code={code}&item_ids={comma_seperated_ids}&app_id={game}").json()

        if data['status'] == "fail":
            raise Exception(data['data']['error_message'])

        return data
        
    def getResetPriceItems(self, game:int=CSGO, page:int=1) -> dict:
        '''
        Returns a paginated list of items that need their prices reset. Items need prices reset when Steam changes tracker 
        so we are unable to match specified prices to the received items when you list them for sale. Upto 30 items per page. 
        Items that need price resets always have the reserved price of 4985.11. Use variable RESERVED_PRICE when needed.\n
        ---
        Arguments:
        * game - The app_id for the inventory's game (defaults to CSGO if not specified). (optional)
        * page - Page number for BitSkins inventory. (optional)
        ---
        Return type: dict
        '''
        code = pyotp.TOTP(self.__secret).now()   
        data = requests.get(f"https://bitskins.com/api/v1/get_reset_price_items/?api_key={self.__api_key}&code={code}&page={page}&app_id={game}").json()

        if data['status'] == "fail":
            raise Exception(data['data']['error_message'])

        return data

    def getMoneyEvents(self, page:int = 1) -> dict:
        '''
        Allows you to retrieve historical events that caused changes in your balance. Upto 30 items per page.\n
        ---
        Arguments:
        * page - Page number. (optional)
        ---
        Return type: dict
        '''
        code = pyotp.TOTP(self.__secret).now()
        data = requests.get(f"https://bitskins.com/api/v1/get_money_events/?api_key={self.__api_key}&code={code}&page={page}").json()

        if data['status'] == "fail":
            raise Exception(data['data']['error_message'])

        return data

    def widthdrawMoney(self, amount:float, withdrawal_method:str):
        '''
        Allows you to request withdrawal of available balance on your BitSkins account. All withdrawals are finalized 15 days after this request on a rolling basis.\n
        *Multiple simultaneous calls to this method may result in 'Failed to acquire lock' errors.*\n
        ---
        Arguments:
        * amount - Amount in USD to withdraw. Must be at most equal to available balance, and over $5.00 USD.
        * withdrawal_method - Can be PAYPAL, or SKRILL.
        ---
        Return type: dict
        '''
        code = pyotp.TOTP(self.__secret).now()
        data = requests.get(f"https://bitskins.com/api/v1/request_withdrawal/?api_key={self.__api_key}&code={code}&amount={amount}&withdrawal_method={withdrawal_method}").json()

        if data['status'] == "fail":
            raise Exception(data['data']['error_message'])

    def buyItems(self, game:int=CSGO, item_ids:list=None, prices:list=None, auto_trade:bool=None, allow_trade_delay_purchases:bool=None):
        '''
        Allows you to buy the item currently on sale on BitSkins. Item must not be currently be on sale to you. Requires 2FA (Secure Purchases) to be enabled on your account if not logged in.\n
        *Multiple simultaneous calls to this method may result in 'Failed to acquire lock' errors.*\n
        ---
        Arguments:
        * item_ids - list of item IDs as strings.
        * prices - list of prices at which you want to make the purchase. Important to specify this in case the prices change by the time you make this call.
        * game - The app_id for the inventory's game (defaults to CSGO if not specified). (optional)
        * auto_trade - Initiate trade offer for purchased items' delivery. Default: True. (optional)
        * allow_trade_delayed_purchases - Use True if you want to purchase items that are trade-delayed. Default: False (True if signed in via the browser).
        ---
        Return type: dict
        '''
        code = pyotp.TOTP(self.__secret).now()

        if item_ids == None:
            raise Exception("Must provide item ids for api call")
        else:
            comma_seperated_ids = str(item_ids)[1:-1]
            comma_seperated_ids = comma_seperated_ids.replace("'", "")
            comma_seperated_ids = comma_seperated_ids.replace(" ", "")
        if prices == None:
            raise Exception("Must provide prices for api call")
        else:
            comma_seperated_prices = str(prices)[1:-1]
            comma_seperated_prices = comma_seperated_prices.replace("'", "")
            comma_seperated_prices = comma_seperated_prices.replace(" ", "")

        request = f'https://bitskins.com/api/v1/buy_item/?api_key={self.__api_key}&code={code}&item_ids={comma_seperated_ids}&prices={comma_seperated_prices}&app_id={game}'
        
        #auto trade
        if auto_trade != None:
            if auto_trade == True:
                auto_trade = "true"
            elif auto_trade == False:
                auto_trade == "false"
            else:
                raise Exception("auto_trade must be either true or false")
            request += f"&auto_trade={auto_trade}"

        if allow_trade_delay_purchases != None:
            if allow_trade_delay_purchases == True:
                allow_trade_delay_purchases = "true"
            elif allow_trade_delay_purchases == False:
                allow_trade_delay_purchases == "false"
            else:
                raise Exception("allow_trade_delay_purchases must be either true or false")
            request += f"&allow_trade_delay_purchases={allow_trade_delay_purchases}"

        data = requests.get(request).json()

        if data['status'] == "fail":
            raise Exception(data['data']['error_message'])

    def sellItems(self, game:int=CSGO, item_ids:list=None, prices:list=None):
        '''
        Allows you to list an item for sale. This item comes from your Steam inventory. If successful, 
        a BitSkins bot will ask you to trade in the item you want listed for sale. Check for instant sale 
        prices in the 'Get All Item Prices' endpoint if selling items instantly.\n
        ---
        Arguments:
        * item_ids - list of item IDs from your Steam inventory.
        * prices - list of prices for each item ID you want to list for sale (order is respective to order of item_ids). Use INSTANT if selling instantly.
        * game - The app_id for the inventory's game (defaults to CSGO if not specified). (optional)
        ---
        Return type: dict
        '''
        code = pyotp.TOTP(self.__secret).now()

        if item_ids == None:
            raise Exception("Must provide item ids for api call")
        else:
            comma_seperated_ids = str(item_ids)[1:-1]
            comma_seperated_ids = comma_seperated_ids.replace("'", "")
            comma_seperated_ids = comma_seperated_ids.replace(" ", "")
        if prices == None:
            raise Exception("Must provide prices for api call")
        else:
            comma_seperated_prices = str(prices)[1:-1]
            comma_seperated_prices = comma_seperated_prices.replace("'", "")
            comma_seperated_prices = comma_seperated_prices.replace(" ", "")

        request = f"https://bitskins.com/api/v1/list_item_for_sale/?api_key={self.__api_key}&code={code}&item_ids={comma_seperated_ids}&prices={comma_seperated_prices}&app_id={game}"

        data = requests.get(request).json()

        if data['status'] == "fail":
            raise Exception(data['data']['error_message'])

if __name__ == "__main__":
    with open("bitskins/api.txt", "r") as f:
        lines = f.read().splitlines()
        api_key = lines[0]
        secret = lines[1]
        wrapper = BitSkins(api_key, secret)