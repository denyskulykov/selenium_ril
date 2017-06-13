from utils import Utils
import helpers
import sys

conf = Utils.get_configuration()
driver = helpers.get_client_driver()

param_of_opening = sys.argv[1]


if param_of_opening == 'number':
    """number of node, using number_of_node"""

    start_ip = int(conf.get('start_octet'))

    driver.get("{}{}".format(conf.get('ilo_url'), start_ip))
    helpers.oli_login(driver)

    for _ in range(int(conf.get('number_of_node')) - 1):
        helpers.ilo_next_page(driver)
        start_ip += 1
        driver.get("{}{}".format(conf.get('ilo_url'), start_ip))
        helpers.oli_login(driver)


if param_of_opening == 'range':
    """ip range, from start_ip to end """

    start_ip = int(conf.get('start_octet'))

    driver.get("{}{}".format(conf.get('ilo_url'), start_ip))
    helpers.oli_login(driver)

    for _ in range(int(conf.get('end_octet')) - start_ip):
        start_ip += 1
        helpers.ilo_next_page(driver)
        driver.get("{}{}".format(conf.get('ilo_url'), start_ip))
        helpers.oli_login(driver)

if param_of_opening == 'single':
    """single page, open page with start_ip"""

    driver.get("{}{}".format(conf.get('ilo_url'),
                             int(conf.get('start_octet'))))
    helpers.oli_login(driver)
