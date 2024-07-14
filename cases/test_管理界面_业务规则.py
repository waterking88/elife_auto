from selenium.webdriver.common.by import By

import time,pytest

from lib.webUI_smp import smpUI

from cfg import *



@pytest.fixture(scope='module')
def inServiceRuleMgr():

    print('** inServiceRuleMgr setup **')
    smpUI.login('byhy','sdfsdf' )

    smpUI.wd.get(SMP_URL_SERVICE_RULE)

    yield


@pytest.fixture()
def delAddedServiceRule():

    yield

    print('** 删除添加的业务规则')
    smpUI.del_first_item()



def test_SMP_service_rule_001(inServiceRuleMgr, delAddedServiceRule):
    # 点击添加按钮
    topBtn = smpUI.wd.find_element(By.CSS_SELECTOR,'.add-one-area > span')
    if topBtn.text == '添加':
        topBtn.click()

    smpUI.add_svc_rule(
        "全国-电瓶车充电费率1",
        "预付费-下发业务量",
        "0.1",
        "2",
        ['千瓦时', '1'],
        "")

    dms = smpUI.get_first_page_svc_rules()
    assert  dms == [["全国-电瓶车充电费率1",
                        "预付费-下发业务量",
                        {'最小消费':'0.1', '预估消费':'2', '费率':'单位：千瓦时 \n单价：1'},
                        ''
                    ]
            ]



