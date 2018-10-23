from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

driver = webdriver.Chrome("lib/chromedriver", options=chrome_options)
driver.get("https://www.rtd-denver.com/app/nextride/stop/12512")

# Wait for page to load
timeout = 10
try:
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'data-test-pattern-route')
        )
    )
except TimeoutException:
    print("Page load timeout")

# Disable auto-reload (it breaks things)
reload_button = driver.find_elements(By.CSS_SELECTOR, ".btn-text.reload-page")[0]
reload_button.click()

routes = driver.find_elements(By.CLASS_NAME, "data-test-pattern-route")

for route in routes:
    parent, = route.find_elements_by_xpath("..")
    route_name, = route.find_elements_by_css_selector(".nextride-pattern-route__shortname")
    route_name, = route_name.find_elements_by_tag_name("a")
    route_name = route_name.get_property("attributes")[0]['textContent']
    route_name = route_name.replace("/app/nextride/route/", "")
    route_name = route_name.split("?")[0]
    print(route_name)

    route_times = parent.find_elements_by_css_selector(".nextride-pattern-stoptime__prediction")
    for time in route_times:
        t = time.text
        t = t.replace("\n(real time prediction)", "")
        print(t)

driver.quit()
