from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

chengqu = {'dongcheng': '东城区', 'xicheng': '西城区', 'chaoyang': '朝阳区', 'haidian': '海淀区', 'fengtai': '丰台区',
           'shijingshan': '石景山区',
           'tongzhou': '通州区', 'changping': '昌平区', 'daxing': '大兴区', 'shunyi': '顺义区', 'fangshan': '房山区'}
for cq in chengqu.keys():
    url = 'https://bj.lianjia.com/ershoufang/' + cq + '/'  # 组成所选城区的URL
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    total_page = re.sub('\D', '', bsObj.find('div', 'page-box fr').contents[0].attrs['page-data'])[:-1]  # 获取所选城区总页数
    print('total_page', total_page)

    for j in np.arange(1, int(total_page) + 1):
        page_url = url + 'pg' + str(j)  # 组成所选城区页面的URL
        print (page_url)
        page_html = urlopen(page_url)
        page_bsObj = BeautifulSoup(page_html)
        info = bsObj.findAll("div", {"class": "houseInfo"})
        position_info = bsObj.findAll("div", {"class": "positionInfo"})
        totalprice = bsObj.findAll("div", {"class": "totalPrice"})
        unitprice = bsObj.findAll("div", {"class": "unitPrice"})

        house_loc = []  # 房屋所在小区
        house_type = []  # 房屋户型
        house_area = []  # 房屋面积
        house_direction = []  # 房屋朝向
        house_decorating = []  # 房屋装修
        house_lift = []  # 有无电梯
        house_floor = []  # 房屋楼层
        house_year = []  # 建造年份
        house_position = []  # 房屋位置
        t_price = []  # 房屋总价
        u_price = []  # 房屋单价

        for i_info, i_pinfo, i_tp, i_up in zip(info, position_info, totalprice, unitprice):
            #if len(i_info.get_text().split('/')) == 6 and len(i_pinfo.get_text().split('/')) == 3:
                # 分列houseinfo并依次获取房屋所在小区、户型、面积、朝向、装修、有无电梯各字段
                house_loc.append(i_info.get_text().split('|')[0])
                house_type.append(i_info.get_text().split('|')[1])
                house_area.append(i_info.get_text().split('|')[2][:-2])
                house_direction.append(i_info.get_text().split('|')[3].replace(' ', ''))
                house_decorating.append(i_info.get_text().split('|')[4])
                house_lift.append(i_info.get_text().split('|')[5])
                # 分列positioninfo并依次获房屋楼层、建造年份、位置各字段
                house_floor.append(i_pinfo.get_text().split('/')[0])
                # house_year.append(i_pinfo.get_text().split('/')[1][:5])
                # house_position.append(i_pinfo.get_text().split('/')[2])
                # 获取房屋总价和单价
                t_price.append(i_tp.span.string)
                u_price.append(re.sub('\D', '', i_up.get_text()))
        # 将数据导入pandas之中生成数据表
        house_data = pd.DataFrame()
        house_data[u'城区'] = [chengqu[cq]] * len(house_loc)
        house_data[u'小区名称'] = house_loc
        house_data[u'房型'] = house_type
        house_data[u'面积'] = house_area
        house_data[u'朝向'] = house_direction
        house_data[u'装修'] = house_decorating
        house_data[u'有无电梯'] = house_lift
        house_data[u'楼层'] = house_floor
        # house_data[u'建造年份'] = house_year
        # house_data[u'位置'] = house_position
        house_data[u'总价'] = t_price
        house_data[u'单价'] = u_price
        # print (house_data)
        # 将数据存入到csv中，便于后续分析
        house_data.to_csv('house_bj.csv', mode='a', header=False, encoding='gb2312', index=None)
