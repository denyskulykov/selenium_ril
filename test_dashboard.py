from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from ddt import ddt, data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import yaml
import random
import string
import unittest



def get_configuration():
    """function returns configuration for environment"""
    global_config_file = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "global_config.yaml")

    with open(global_config_file, 'r') as file:
        global_config = yaml.load(file)

    return global_config


def gen_rand_string(object_type, size=6):
    rand_string = ''.join(random.choice(string.digits) for _ in range(size))
    return 'selenium-{}-{}'.format(object_type, rand_string)


def login_for_user(driver, user, password):
    conf = get_configuration()

    driver.get("{}{}".format(conf.get('BASE_URI'), conf.get('login_page')))
    driver.find_element_by_id("id_username").send_keys(user)
    driver.find_element_by_id("id_password").send_keys(password)
    driver.find_element_by_id("loginBtn").submit()

    assert conf.get('login_page') not in driver.current_url, "Unauthorized"


def check_exists_by_xpath(driver, xpath, timeout):
    try:
        driver.implicitly_wait(5)
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    finally:
        driver.implicitly_wait(timeout)
    return True


@ddt
class TestForAdmin(unittest.TestCase):
    """Need user, with admin permission"""

    def setUp(self):
        self.conf = get_configuration()

        self.driver = webdriver.Firefox(
            capabilities={"marionette": False},
            executable_path='/usr/bin/firefox')
        self.driver.implicitly_wait(self.conf.get('timeout'))
        login_for_user(self.driver,
                       self.conf.get('admin_user'),
                       self.conf.get('admin_user_pass'))

    def tearDown(self):
        self.driver.close()

    def test_openstack_dashboard_split_pages(self):
        """"""
        # part for admin
        self.driver.get("{}{}".format(self.conf.get('BASE_URI'), '/admin/'))
        assert "Volumes" in self.driver.find_element_by_xpath(
            "//a[@href='/admin/volumes/']").text
        assert "Volume Snapshots" in self.driver.find_element_by_xpath(
            "//a[@href='/admin/volume_snapshots/']").text
        assert "Images" in self.driver.find_element_by_xpath(
            "//a[@href='/admin/images/']").text
        assert "Image Snapshots" in self.driver.find_element_by_xpath(
            "//a[@href='/admin/image_snapshots/']").text

        # part for project
        self.driver.get("{}{}".format(self.conf.get('BASE_URI'), '/project/'))
        assert "Volumes" in self.driver.find_element_by_xpath(
            "//a[@href='/project/volumes/']").text
        assert "Volume Snapshots" in self.driver.find_element_by_xpath(
            "//a[@href='/project/volume_snapshots/']").text
        assert "Images" in self.driver.find_element_by_xpath(
            "//a[@href='/project/images/']").text
        assert "Image Snapshots" in self.driver.find_element_by_xpath(
            "//a[@href='/project/image_snapshots/']").text

    def test_images_filter(self):
        """Extra filters on Images page"""

        self.driver.get("{}{}".format(
            self.conf.get('BASE_URI'), '/project/images'))

        filters = self.driver.find_elements_by_name("images__filter__q")
        filter_values = [f.text.split(" (")[0] for f in filters]
        expected_filters = ["Public & Protected", "Project", "Shared with Me",
                            "Public", "Protected"]
        self.assertEqual(len(expected_filters), len(filter_values))
        self.assertSequenceEqual(filter_values, expected_filters)

    def test_sortable_for_columns(self):
        """Instances screen columns ordering

        Images screen columns ordering
        Image Snapshots screen columns ordering
        Volumes screen columns ordering
        Volume Snapshots screen columns ordering
        """
        self.driver.get("{}{}".format(
            self.conf.get('BASE_URI'), '/project/instances'))
        for number in range(2, 11):

            # Skip column 'size'
            if number == 6:
                continue

            attribute = self.driver.find_element_by_xpath(
                # It doesnt look well ):
                "//*[@id='instances']/thead/tr[2]/th[{}]".format(number)) \
                .get_attribute("class")
            assert "sortable" in attribute, \
                "Page 'instances' has unsortable item"

        self.driver.get("{}{}".format(
            self.conf.get('BASE_URI'), '/project/images'))
        for number in range(2, 9):
            attribute = self.driver.find_element_by_xpath(
                "//*[@id='images']/thead/tr[2]/th[{}]".format(number))\
                .get_attribute("class")
            assert "sortable" in attribute, \
                "Page 'images' has unsortable item"

        self.driver.get("{}{}".format(
            self.conf.get('BASE_URI'), '/project/image_snapshots'))
        for number in range(2, 8):
            attribute = self.driver.find_element_by_xpath(
                "//*[@id='image_snapshots']/thead/tr[2]/th[{}]"
                .format(number)).get_attribute("class")
            assert "sortable" in attribute, \
                "Page 'image_snapshots' has unsortable item"

        self.driver.get("{}{}".format(
            self.conf.get('BASE_URI'), '/project/volumes'))
        for number in range(2, 9):
            attribute = self.driver.find_element_by_xpath(
                "//*[@id='volumes']/thead/tr[2]/th[{}]".format(number))\
                .get_attribute("class")
            assert "sortable" in attribute, \
                "Page 'volumes' has unsortable item"

        self.driver.get("{}{}".format(
            self.conf.get('BASE_URI'), '/project/volume_snapshots'))
        for number in range(2, 6):
            attribute = self.driver.find_element_by_xpath(
                "//*[@id='volume_snapshots']/thead/tr[2]/th[{}]"
                    .format(number)).get_attribute("class")
            assert "sortable" in attribute, \
                "Page 'volume_snapshots' has unsortable item"

    def test_title_for_snapshot_page(self):
        """Image Snapshots page title

        Volume Snapshots page title"""

        self.driver.get("{}{}".format(
            self.conf.get('BASE_URI'), '/project/image_snapshots'))
        assert "Image Snapshots" in self.driver.find_element_by_xpath(
            "//*[@id='content_body']//h1").text, \
            "The page '/project/image_snapshots' has wrong title"

        self.driver.get("{}{}".format(
            self.conf.get('BASE_URI'), '/admin/image_snapshots'))
        assert "Image Snapshots" in self.driver.find_element_by_xpath(
            "//*[@id='content_body']//h1").text, \
            "The page '/admin/image_snapshots' has wrong title"

        self.driver.get("{}{}".format(
            self.conf.get('BASE_URI'), '/project/volume_snapshots'))
        assert "Volume Snapshots" in self.driver.find_element_by_xpath(
            "//*[@id='content_body']//h1").text, \
            "The page '/project/volume_snapshots' has wrong title"

        self.driver.get("{}{}".format(
            self.conf.get('BASE_URI'), '/admin/volume_snapshots'))
        assert "Volume Snapshots" in self.driver.find_element_by_xpath(
            "//*[@id='content_body']//h1").text, \
            "The page '/admin/volume_snapshots' has wrong title"

    def test_checking_to_hide_external_network(self):
        """Hide external networks from instance creation screen"""

        self.driver.get("{}{}".format(
            self.conf.get('BASE_URI'), '/project/instances'))
        self.driver.find_element_by_id('instances__action_launch-ng').click()
        self.driver.find_element_by_xpath("//button[3]").click()

        # instead of sleep,
        self.driver.find_elements_by_xpath(
            '//wizard/div/div[5]/ng-include/div/div/transfer-table/div/div'
            '[2]/div[2]/available/table/tbody/tr')

        amount = len(self.driver.find_elements_by_xpath(
            '//wizard/div/div[5]/ng-include/div/div/transfer-table/div/div'
            '[2]/div[2]/available/table/tbody/tr'))

        assert amount > 1, "Check me"

        for number in range(1, amount):
            assert "ext-net" not in self.driver.find_element_by_xpath(
                '//wizard/div/div[5]/ng-include/div/div/transfer-table'
                '/div/div[2]/div[2]/available/table/tbody/tr[{}]'
                    .format(number)).text, \
                "ext-net network is  available for creating vm"


@ddt
class TestForNotAdmin(unittest.TestCase):
    """Need user, without admin permission"""

    def __init__(self, *args, **kwargs):
        super(TestForNotAdmin, self).__init__(*args, **kwargs)

    def setUp(self):
        self.conf = get_configuration()
        self.volume_uuid = None
        self.driver = webdriver.Firefox(
            capabilities={"marionette": False},
            executable_path='/usr/bin/firefox')
        self.driver.implicitly_wait(self.conf.get('timeout'))
        self.wait = WebDriverWait(self.driver, self.conf.get('timeout'))
        login_for_user(self.driver,
                       self.conf.get('not_admin_user'),
                       self.conf.get('not_admin_user_pass'))

    def tearDown(self):
        if self.volume_uuid:
            self.driver.get("{}{}".format(
                self.conf.get('BASE_URI'),
                '/project/volumes/{}/'.format(self.volume_uuid)))
            self.driver.find_element_by_css_selector(
                'a.btn.btn-default.btn-sm.dropdown-toggle').click()
            self.driver.find_element_by_id(
                "volumes__row_{}__action_delete".format(
                    self.volume_uuid)).click()
            confirm_delete = self.driver.find_element_by_css_selector(
                'a.btn.btn-primary')
            self.assertEqual(confirm_delete.text, "Delete Volume")
            confirm_delete.click()

        self.driver.close()

    @data("/admin/info/",
          "/admin/flavors/",
          "/admin/hypervisors/",
          "/admin/image_snapshots/",
          "/admin/routers/",
          "/admin/defaults/",
          "/admin/metadata_defs/")
    def test_for_admins_pages(self, value):

        self.driver.get("{}{}".format(self.conf.get('BASE_URI'), value))
        assert "Login - Private Cloud Dashboard" in self.driver.title, \
            "The page '{}' is available for non-admin".format(value)

    def test_button_image_create(self):
        """"Create Image" button available only for admin"""

        self.driver.get("{}{}".format(self.conf.get('BASE_URI'), "/project/images"))

        # Check there is something
        assert check_exists_by_xpath(
            self.driver,
            '//*[contains(@id, "images__row")]',
            self.conf.timeout), \
            "The page isnt valid"

        assert not check_exists_by_xpath(
            self.driver,
            "//*[@id='images__action_create']",
            self.conf.timeout), \
            "Create Image button is available for non-admin"

    def test_image_description_is_read_only(self):
        """Image description is read-only for non-admin

        Need to have an image"""
        self.driver.get("{}{}".format(self.conf.get('BASE_URI'), "/project/images"))

        # Check there is something
        assert check_exists_by_xpath(
            self.driver,
            '//*[contains(@id, "images__row")]',
            self.conf.get('timeout')),\
            "There isn't any images"

        assert not check_exists_by_xpath(
            self.driver,
            '//*[contains(@id, "images__row")]//button',
            self.conf.get('timeout')),\
            "Non-admin can change image description"

    def test_check_empty_name_for_volume(self):
        """Check "empty" volume 'name' field

        Need to have an image
        """
        self.driver.get("{}{}".format(
            self.conf.get('BASE_URI'), '/project/images'))

        # ToDo(den) do it better, choosing any image
        self.driver.find_element_by_xpath(
            "//*[@name='images__filter__q'][4]").click()

        try:
            cirros_image = self.driver.find_element_by_link_text(
                self.conf.get('default_image_name'))
        except NoSuchElementException:
            raise Exception("Default image '{}' was not found on Horizon "
                            "Images page".format(
                self.conf.get('default_image_name')))

        cirros_image.click()

        self.driver.find_element_by_css_selector(
            "a.btn.btn-default.btn-sm.dropdown-toggle").click()
        self.driver.find_element_by_link_text("Create Volume").click()
        self.driver.find_element_by_id('id_name').clear()
        volume_description = gen_rand_string('volume')
        self.driver.find_element_by_id('id_description').send_keys(
            volume_description)
        self.driver.find_element_by_xpath("//input[@type='submit']").submit()

        # wait redirection to Volumes page
        self.wait.until(EC.visibility_of_element_located(
            (By.ID, "volumes__action_create")))

        # get newest volume created
        volume = self.driver.find_elements_by_css_selector(
            "td.sortable.anchor.normal_column")[0]

        volume_name = volume.text
        # wait new volume is in stable state
        self.wait.until(EC.visibility_of_element_located(
            (By.ID, "volumes__row_{}__action_edit".format(volume_name))))

        # check redirection
        self.assertIn("project/volumes", self.driver.current_url)

        volume = self.driver.find_elements_by_css_selector(
            "td.sortable.anchor.normal_column")[0]
        volume.click()

        self.volume_uuid = self.driver.current_url.split('/')[-2]
        # check name is equal to ID
        self.assertEqual(volume_name, self.volume_uuid)
        # check volume description is expected (verify it is our volume)
        overview = self.driver.find_element_by_css_selector(
            "div.info.row.detail")
        self.assertTrue(volume_description in overview.text)


if __name__ == '__main__':
    unittest.main()
