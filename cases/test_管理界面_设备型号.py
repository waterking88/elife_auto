from selenium.webdriver.common.by import By

import time,pytest

from lib.webUI_smp import smpUI

from cfg import *



@pytest.fixture(scope='module')
def inDeviceModelMgr():

    print('** inDeviceModelMgr setup **')
    smpUI.login('byhy','sdfsdf' )

    smpUI.wd.get(SMP_URL_DEVICE_MODEL)
    # smpUI.del_all_item()
    yield


    print('** inDeviceModelMgr teardown **')


@pytest.fixture()
def delAddedDeviceModel():

    print('** 删除添加的设备型号 setup **')
    yield

    print('** 删除添加的设备型号 teardown')
    smpUI.del_first_item()



def test_SMP_device_model_001(inDeviceModelMgr, delAddedDeviceModel):
    # 点击添加按钮
    topBtn = smpUI.wd.find_element(By.CSS_SELECTOR,'.add-one-area > span')
    if topBtn.text == '添加':
        topBtn.click()

    smpUI.add_device_model(
        "存储柜",
        'elife-canbinlocker-g22-10-20-40',
        '南京e生活存储柜-10大20中40小')

    dms = smpUI.get_first_page_device_models()
    assert  dms == [[
        "存储柜",
        'elife-canbinlocker-g22-10-20-40',
        '南京e生活存储柜-10大20中40小'
    ]]



def test_SMP_device_model_002(inDeviceModelMgr, delAddedDeviceModel):
    # 点击添加按钮
    topBtn = smpUI.wd.find_element(By.CSS_SELECTOR,'.add-one-area > span')
    if topBtn.text == '添加':
        topBtn.click()


    smpUI.add_device_model(
        "存储柜",
        '韩'*100,
        '南京e生活存储柜-10大20中40小')

    dms = smpUI.get_first_page_device_models()
    assert  dms == [[
        "存储柜",
        '韩'*100,
        '南京e生活存储柜-10大20中40小'
    ]]
