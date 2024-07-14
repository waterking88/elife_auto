from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


import time
from cfg import *

class SMP_UI:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])

        self.wd = webdriver.Chrome(options=options)     ##设置参数，使信息简洁
        self.wd.implicitly_wait(10)

    def login(self, username, password):
        self.wd.get(SMP_URL_LOGIN)      ## SMP_URL_LOGIN是cfg中定义的网址

        # time.sleep(3)

        if username is not None:
            self.wd.find_element(By.ID, 'username').send_keys(username)

        if password is not None:
            self.wd.find_element(By.ID, 'password').send_keys(password)

        # time.sleep(1)
        self.wd.find_element(By.ID, 'loginBtn').click()

    def add_device_model(self, devType, name, desc):

        # 创建Select对象
        select = Select(smpUI.wd.find_element(By.ID, "device-type"))

        # 通过 Select 对象选中
        select.select_by_visible_text(devType)

        ele = smpUI.wd.find_element(By.ID, 'device-model')
        ele.clear()
        ele.send_keys(name)

        ele = smpUI.wd.find_element(By.ID, 'device-model-desc')
        ele.clear()
        ele.send_keys(desc)

        smpUI.wd.find_element(By.CSS_SELECTOR, '.add-one-submit-btn-div .btn').click()

        time.sleep(1)

    def get_first_page_device_models(self):
        time.sleep(1)

        self.wd.implicitly_wait(0)
        values = self.wd.find_elements(By.CSS_SELECTOR,'.field-value')
        self.wd.implicitly_wait(10)

        deviceModels = []
        for idx, value in enumerate(values):
            if (idx+1) % 3 == 0:
                deviceModels.append(
                    [values[idx-2].text, values[idx-1].text, values[idx].text])

        return deviceModels


    def del_first_item(self) -> bool:

        self.wd.implicitly_wait(0)

        delBtn = self.wd.find_elements(By.CSS_SELECTOR,
                    '.result-list-item-btn-bar span:first-child')

        self.wd.implicitly_wait(10)

        if not delBtn:
            return False

        delBtn[0].click()

        self.wd.switch_to.alert.accept()


        return True

    # def del_all_item(self) -> bool:

    #     self.wd.implicitly_wait(0)

    #     delBtn = self.wd.find_elements(By.CSS_SELECTOR,
    #                 '.result-list-item:first-child .result-list-item-btn-bar span:first-child')

    #     self.wd.implicitly_wait(10)

    #     if not delBtn:
    #         print('** nothing to del **')
    #         return False

    #     for itemBtn in delBtn:
    #         itemBtn.click()
    #         self.wd.switch_to.alert.accept()


    #     return True

    def add_svc_rule(self, ruleName:str, ruleType:str,
                     minFee:str, estFee:str, feeRate=None, desc:str=None):
        """
        添加业务规则
        :param ruleName: 规则名称
        :param ruleType: 规则类型，只能是：后付费-上报业务量、预付费-下发费用、预付费-下发业务量
        :param minFee: 最小费用，不需要时，填写空字符串
        :param estFee: 预计费用，不需要时，填写空字符串
        :param desc: 描述
        :param feeRate: 费率， 如果ruleType是
           预付费-下发费用： 不用填写
           预付费-下发业务量： 格式为 ['千瓦时', '1']， 元素分别是 单位、单价
           后付费-上报业务量： 格式为 [
                ['10L', '小时','1'],
                ['20L', '小时','2'],
            ]， 每个元素里面分别是 ： 业务码、单位、单价
        :return:
        """
        # self.wd.get(SMP_URL_SVC_RULE)

        ele = self.wd.find_element(By.CSS_SELECTOR, '.add-one-form > .field:nth-child(1) >input')
        ele.clear()
        ele.send_keys(ruleName)


        select = Select(self.wd.find_element(By.CSS_SELECTOR, ".add-one-form select"))
        select.select_by_visible_text(ruleType)
        time.sleep(1)
        # input('press any key to continue')

        if ruleType != '后付费-上报业务量':
            ele = self.wd.find_element(By.CSS_SELECTOR, '.add-one-form > .field:nth-child(3) >input')
            ele.clear()
            if minFee:
                ele.send_keys(minFee)

            ele =  self.wd.find_element(By.CSS_SELECTOR, '.add-one-form > .field:nth-child(4) >input')
            ele.clear()
            if estFee:
                ele.send_keys(estFee)

        # 描述, 用xpath而不用 .field:nth-child 因为后付费-上报业务量 次序会变
        if desc:
            ele =  self.wd.find_element(By.XPATH,
                "//*[@class='add-one-submit-btn-div']/preceding-sibling::*[1]/input")
            ele.clear()
            ele.send_keys(desc)

        # 费率填写

        if ruleType == '预付费-下发费用':
            # 没有费率设置
            pass

        elif ruleType == '后付费-上报业务量':
            # 先删除上次添加遗留的费率
            self.wd.implicitly_wait(0)  # 先修改短等待时间
            while True:
                eles = self.wd.find_elements(By.CSS_SELECTOR, '.fee-rate span:last-child')
                if eles:
                    eles[0].click()
                    time.sleep(0.5)
                else:
                    break

            self.wd.implicitly_wait(10)  # 再改回来

            for one in feeRate:

                self.wd.find_element(By.CSS_SELECTOR,'.fee-rate-list button').click()

                entry = self.wd.find_element(By.CSS_SELECTOR,'div.fee-rate:nth-last-child(2)')

                # 业务码
                entry.find_element(By.CSS_SELECTOR,'input:nth-of-type(1)').send_keys(one[0])
                # 计费单位
                entry.find_element(By.CSS_SELECTOR,'input:nth-of-type(2)').send_keys(one[1])
                # 单位价格
                entry.find_element(By.CSS_SELECTOR,'input:nth-of-type(3)').send_keys(one[2])

        elif ruleType == '预付费-下发业务量':

            entry = self.wd.find_element(By.CSS_SELECTOR, 'div.fee-rate')

            # 计费单位
            entry.find_element(By.CSS_SELECTOR, 'input:nth-of-type(1)').send_keys(feeRate[0])
            # 单位价格
            entry.find_element(By.CSS_SELECTOR, 'input:nth-of-type(2)').send_keys(feeRate[1])
        else:
            raise Exception('ruleType 参数值错误')

        # 确定提交
        self.wd.find_element(By.CSS_SELECTOR, '.add-one-submit-btn-div .btn').click()

        time.sleep(1)


    def get_first_page_svc_rules(self):
        time.sleep(1)

        self.wd.implicitly_wait(0)
        items = self.wd.find_elements(By.CSS_SELECTOR,'.result-list-item-info')
        self.wd.implicitly_wait(10)

        rules = []
        for item in items:
            nameValueList = item.find_elements(By.CSS_SELECTOR, '.field>.field-name, .field>.field-value')
            itemInfo = []
            for idx, _ in enumerate(nameValueList):
                if (idx+1) % 2 == 0:
                    nameEle,valueEle = nameValueList[idx-1], nameValueList[idx]
                    if nameEle.text == '规则内容':
                        ruleContent = {}
                        sfns = valueEle.find_elements(By.CSS_SELECTOR,'.sub-field-name')
                        for sfnEle in sfns:
                            sfn = sfnEle.text #提取文字内容
                            sfvEle = sfnEle.find_element(By.XPATH, "following-sibling::*[1]")
                            # if sfn == '费率':
                            #     ruleContent[sfn] = sfvEle.text
                            # else:
                            ruleContent[sfn] = sfvEle.text

                        itemInfo.append(ruleContent)
                    else:
                        itemInfo.append(valueEle.text)


            rules.append(itemInfo)

        return rules

    def del_first_item(self) -> bool:

        self.wd.implicitly_wait(0)

        delBtn = self.wd.find_elements(By.CSS_SELECTOR,
                    # '.result-list-item:first-child .result-list-item-btn-bar span:first-child')
                    '.result-list-item-btn-bar span:first-child')

        self.wd.implicitly_wait(10)

        if not delBtn:
            return False

        delBtn[0].click()

        self.wd.switch_to.alert.accept()


        return True
smpUI = SMP_UI()