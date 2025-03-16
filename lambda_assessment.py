import pytest
import time
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

'''Defining Capabilities
'''
LT_CAPABILITIES = [
    {
        "browserName": "Chrome",
        "browserVersion": "128.0",
        "platformName": "Windows 10",
        "LT:Options": {
            "build": "LambdaTest Selenium Test",
            "name": "Test Scenario 1 - Chrome",
            "network": True,
            "video": True,
            "console": True,
            "visual": True,
        },
    },
    {
        "browserName": "MicrosoftEdge",
        "browserVersion": "127.0",
        "platformName": "macOS Ventura",
        "LT:Options": {
            "build": "LambdaTest Selenium Test",
            "name": "Test Scenario 2 - Edge",
            "network": True,
            "video": True,
            "console": True,
            "visual": True,
        },
    },
]


@pytest.mark.parametrize("capabilities", LT_CAPABILITIES)
def test_lambdatest_integration(capabilities):
    #username ===============Geetha creds **************************
    #USERNAME = "geethanjali_b"  
    #ACCESS_KEY = "LT_iUsYVkdEw4cGBIquDgbfarjnIMiPIKsnFjFZsT3BzYdyaz7"

    grid_url = f"https://{USERNAME}:{ACCESS_KEY}@hub.lambdatest.com/wd/hub"

    driver1 = webdriver.Remote(command_executor=grid_url, options=webdriver.ChromeOptions() if capabilities["browserName"] == "Chrome" else webdriver.EdgeOptions())
    driver1.capabilities.update(capabilities)

    try:
        '''Step 1: Navigating to https://www.lambdatest.com
        '''
        driver1.get("https://www.lambdatest.com")
        driver1.maximize_window()

        '''Step 2: Perform an explicit wait till the time all the elements in the DOM are available
        '''
        WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        '''Step 3: Scroll to the WebElement ‘Explore all Integrations’ using the scrollIntoView() method. 
        You are free to use any of the available web locators (e.g., XPath, CssSelector, etc.)
        '''
        exploreAllIntegrations = WebDriverWait(driver1, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='wrapper']/section[9]/div/p/a[text()='Explore all Integrations']")))
        time.sleep(2)

        driver1.execute_script("arguments[0].scrollIntoView({block: 'center'});", exploreAllIntegrations)

        '''Step 4: Click on the link and ensure that it opens in the new tab
        '''
        driver1.execute_script("window.open('%s', '_blank')" % exploreAllIntegrations.get_attribute('href'))

        time.sleep(2)
        driver1.switch_to.window(driver1.window_handles[1])

        '''5. Save window IDs ************** Assertion
        '''
        window_handles = driver1.window_handles
        print("The window IDs are:", window_handles)
        assert len(window_handles) == 2, "New tab has not opened"

        '''Step 5: Save the window handles in a List (or array). Print the window handles of the opened windows 
        (now there are two windows open)
        '''
        window_handles = driver1.window_handles
        print("The window IDs are:", window_handles)
        print("The number of windows " + str((len(window_handles))))
        driver1.switch_to.window(driver1.window_handles[1])
        print("Switched to tab ", driver1.title)
        time.sleep(1)

        '''Step 6: Verify whether the URL is the same as the expected URL (if not, throw an Assert)
        '''
        expected_url = "https://www.lambdatest.com/integrations"
        assert driver1.current_url == expected_url
        time.sleep(1)

        '''Step 7: On that page, scroll to the page where the WebElement (Codeless Automation) is present 
        '''
        codelessAutomation = WebDriverWait(driver1,20).until(EC.presence_of_element_located((By.XPATH,"//a[text()='Codeless Automation']")))
        driver1.execute_script("arguments[0].scrollIntoView(true);", codelessAutomation)
        print("Successfully scrolled up to element on {browser}:", codelessAutomation.text)
        time.sleep(2)


        '''Step 8: Click the ‘INTEGRATE TESTING WHIZ WITH LAMBDATEST’ link for Testing Whiz. 
        The page should open in the same window
        '''
        integrateTestingWithLambdaWhiz = WebDriverWait(driver1, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[text() = 'Integrate Testing Whiz with LambdaTest']")))
        integrateTestingWithLambdaWhiz.click()
        testingWhizTitle = driver1.title
        print(testingWhizTitle)
        assert testingWhizTitle == "Running Automation Tests Using TestingWhiz LambdaTest | LambdaTest"

        '''Step 9: Check if the title of the page is ‘TestingWhiz Integration With LambdaTest’. 
        If not, raise an Assert.
        '''
        titleLambdaWhiz = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text() = 'TestingWhiz Integration With LambdaTest']")))
        print(titleLambdaWhiz.text)
        assert titleLambdaWhiz.text == "TestingWhiz Integration With LambdaTest"

        '''Step 10: Close the current window using the window handle [which we obtained in step (5)]
        '''
        driver1.close()
        driver1.switch_to.window(driver1.window_handles[0])
        time.sleep(2)

        '''Step 11: Print the current window count.
        '''
        window_handles = driver1.window_handles
        print("The window IDs are:", window_handles)
        print("The number of windows " + str((len(window_handles))))

        '''Step 12: On the current window, set the URL to https://www.lambdatest.com/blog
        '''
        driver1.get('https://www.lambdatest.com/blog')
        time.sleep(2)

        '''Step 13: Click on the ‘Community’ link and verify whether the URL is https://community.lambdatest.com/
        '''
        communityLink = WebDriverWait(driver1, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Community")))
        communityLink.click()
        WebDriverWait(driver1, 10).until(EC.url_to_be("https://community.lambdatest.com/"))
        assert driver1.current_url == "https://community.lambdatest.com/", "Community URL Mismatch"

        '''Step 14: Close the browser window
        '''
        driver1.quit()
    except Exception as e:
        print(f"Test run failed: {str(e)}")
        driver1.quit()
        raise