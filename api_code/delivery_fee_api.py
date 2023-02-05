import logging
import sys
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

def calculate_delivery_fee(cart_value, delivery_distance, number_of_items, time):
        
    def calculate_small_order_surcharge(cart_value):
        return 10 - cart_value if cart_value < 10 else 0

    def calculate_delivery_distance_fee(delivery_distance):
        delivery_distance_in_km = delivery_distance / 1000
        fee = 2 + (delivery_distance_in_km - 1) // 0.5
        return max(1, fee)

    def calculate_number_of_items_surcharge(number_of_items):
        surcharge = (number_of_items - 4) * 0.5 if number_of_items >= 5 else 0
        surcharge += 1.2 if number_of_items >= 13 else 0
        return surcharge

    def calculate_rush_hour_multiplier(time):
        try:
            time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
            if time.hour >= 15 and time.hour <= 19 and time.weekday() == 4:
                return 1.2
        except:
            pass
        return 1

    if cart_value >= 100:
        return 0

    fee = calculate_small_order_surcharge(cart_value)
    fee += calculate_delivery_distance_fee(delivery_distance)
    fee += calculate_number_of_items_surcharge(number_of_items)
    fee *= calculate_rush_hour_multiplier(time)

    return min(fee, 15)

@app.route('/delivery_fee', methods=['POST'])
def delivery_fee():
    request_data = request.get_json()
    app.logger.debug("Received request data: %s", request_data)
    cart_value = request_data.get('cart_value')
    delivery_distance = request_data.get('delivery_distance')
    number_of_items = request_data.get('number_of_items')
    time = request_data.get('time')

    fee = calculate_delivery_fee(cart_value, delivery_distance, number_of_items, time)
    
    response = {
        "delivery_fee": fee
    }

    app.logger.info("Calculated delivery fee: %s", fee)

    return jsonify(response)

if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.run(debug=True)
