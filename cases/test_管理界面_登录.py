from selenium.webdriver.common.by import By

import time,pytest

from lib.webUI_smp import smpUI


def test_SMP_login_001():
    smpUI.login('byhy','sdfsdf' )

    # time.sleep(1)
    nav = smpUI.wd.find_elements(By.TAG_NAME, 'nav')

    assert nav != []



@pytest.fixture     ##初始化清除
def clearAlert():
    yield
    try:
        smpUI.wd.switch_to.alert.accept()       ##考虑未弹出弹框的bug
    except Exception as e:
        print(e)

@pytest.mark.parametrize('username, password, expectedalert', [     ##数据驱动，简化重复操作的用例
            (None, 'sdfsdf', '请输入用户名'),
            ('byhy', None, '请输入密码'),       
            ('byhy', 'sdfsd',   '登录失败： 用户名或者密码错误'),
            ('byhy', 'sdfsdff', '登录失败： 用户名或者密码错误'),
            ('byh', 'sdfsdf',   '登录失败： 用户名不存在'),
            ('byhyy', 'sdfsdf', '登录失败： 用户名不存在'),
        ]
                                )

def test_SMP_login_002(username, password, expectedalert, clearAlert):

    smpUI.login(username, password)

    # time.sleep(1)

    alert = smpUI.wd.switch_to.alert
    assert alert.text == expectedalert

