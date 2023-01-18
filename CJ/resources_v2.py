

class CJProduct:
    get_categories = "api2.0/v1/product/getCategory"
    view_category = "api2.0/v1/product/list"
    view_product = "api2.0/v1/product/query"
    product_ships_from = "api2.0/v1/product/stock/queryByVid"


class CJOrder:
    create_order = "api2.0/v1/shopping/order/createOrder"
    view_orders = "api2.0/v1/shopping/order/list"
    view_order = "api2.0/v1/shopping/order/getOrderDetail"
    update_order = "api/order/upOrders"
    delete_order = "api2.0/v1/shopping/order/deleteOrder"
    confirm_order = "api2.0/v1/shopping/order/confirmOrder"