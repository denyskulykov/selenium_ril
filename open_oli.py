from utils import Utils
import helpers
import sys

conf = Utils.get_configuration()
driver = helpers.get_client_driver()

param_of_opening = sys.argv[1]


if param_of_opening == 'number':
    """number of node, using number_of_node"""

    ip_node = int(conf.get('start_octet'))
    helpers.oli_login(driver, ip_node)

    for _ in range(int(conf.get('number_of_node')) - 1):
        ip_node += 1

        helpers.ilo_next_page(driver)
        helpers.oli_login(driver, ip_node)


if param_of_opening == 'range':
    """ip range, from ip_node to last_ip"""

    ip_node = int(conf.get('start_octet'))
    helpers.oli_login(driver, ip_node)

    for _ in range(int(conf.get('end_octet')) - ip_node):
        ip_node += 1

        helpers.ilo_next_page(driver)
        helpers.oli_login(driver, ip_node)


if param_of_opening == 'single':
    """single page, open page with start_ip"""

    helpers.oli_login(driver, int(conf.get('start_octet')))
