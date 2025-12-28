#!/usr/bin/env python3
"""
预录入100本经典高中、大学图书到数据库中
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.backend.database_manager import db_manager


def seed_books():
    """预录入100本经典图书"""
    print("开始预录入100本经典高中、大学图书...")
    
    # 定义100本经典图书列表
    classic_books = [
        # 文学经典
        {"title": "百年孤独", "authors": ["加西亚·马尔克斯"], "publisher": "南海出版公司", "year": 2011, "price": 55.00, "category": ["文学"], "isbn": "9787544253994"},
        {"title": "活着", "authors": ["余华"], "publisher": "作家出版社", "year": 1993, "price": 39.50, "category": ["文学"], "isbn": "9787506365437"},
        {"title": "1984", "authors": ["乔治·奥威尔"], "publisher": "北京十月文艺出版社", "year": 2010, "price": 28.00, "category": ["文学"], "isbn": "9787530210403"},
        {"title": "动物农场", "authors": ["乔治·奥威尔"], "publisher": "北京十月文艺出版社", "year": 2010, "price": 22.00, "category": ["文学"], "isbn": "9787530210410"},
        {"title": "了不起的盖茨比", "authors": ["F·斯科特·菲茨杰拉德"], "publisher": "人民文学出版社", "year": 2004, "price": 22.00, "category": ["文学"], "isbn": "9787020049276"},
        {"title": "麦田里的守望者", "authors": ["J·D·塞林格"], "publisher": "译林出版社", "year": 2008, "price": 25.00, "category": ["文学"], "isbn": "9787544707371"},
        {"title": "傲慢与偏见", "authors": ["简·奥斯汀"], "publisher": "译林出版社", "year": 2009, "price": 28.00, "category": ["文学"], "isbn": "9787544707463"},
        {"title": "简爱", "authors": ["夏洛蒂·勃朗特"], "publisher": "人民文学出版社", "year": 1999, "price": 29.00, "category": ["文学"], "isbn": "9787020030945"},
        {"title": "呼啸山庄", "authors": ["艾米莉·勃朗特"], "publisher": "人民文学出版社", "year": 1999, "price": 25.00, "category": ["文学"], "isbn": "9787020031492"},
        {"title": "德伯家的苔丝", "authors": ["托马斯·哈代"], "publisher": "人民文学出版社", "year": 1994, "price": 32.00, "category": ["文学"], "isbn": "9787020008850"},
        {"title": "大卫·科波菲尔", "authors": ["查尔斯·狄更斯"], "publisher": "人民文学出版社", "year": 1995, "price": 45.00, "category": ["文学"], "isbn": "9787020018911"},
        {"title": "双城记", "authors": ["查尔斯·狄更斯"], "publisher": "人民文学出版社", "year": 1993, "price": 29.00, "category": ["文学"], "isbn": "9787020018904"},
        {"title": "雾都孤儿", "authors": ["查尔斯·狄更斯"], "publisher": "人民文学出版社", "year": 1994, "price": 32.00, "category": ["文学"], "isbn": "9787020018898"},
        {"title": "悲惨世界", "authors": ["维克多·雨果"], "publisher": "人民文学出版社", "year": 1992, "price": 48.00, "category": ["文学"], "isbn": "9787020007914"},
        {"title": "巴黎圣母院", "authors": ["维克多·雨果"], "publisher": "人民文学出版社", "year": 1982, "price": 30.00, "category": ["文学"], "isbn": "9787020010525"},
        {"title": "红与黑", "authors": ["司汤达"], "publisher": "人民文学出版社", "year": 1999, "price": 28.00, "category": ["文学"], "isbn": "9787020024752"},
        {"title": "战争与和平", "authors": ["列夫·托尔斯泰"], "publisher": "人民文学出版社", "year": 1997, "price": 68.00, "category": ["文学"], "isbn": "9787020018052"},
        {"title": "安娜·卡列尼娜", "authors": ["列夫·托尔斯泰"], "publisher": "人民文学出版社", "year": 1996, "price": 56.00, "category": ["文学"], "isbn": "9787020015638"},
        {"title": "复活", "authors": ["列夫·托尔斯泰"], "publisher": "人民文学出版社", "year": 1989, "price": 35.00, "category": ["文学"], "isbn": "9787020003111"},
        {"title": "罪与罚", "authors": ["费奥多尔·陀思妥耶夫斯基"], "publisher": "人民文学出版社", "year": 1982, "price": 32.00, "category": ["文学"], "isbn": "9787020015805"},
        {"title": "卡拉马佐夫兄弟", "authors": ["费奥多尔·陀思妥耶夫斯基"], "publisher": "人民文学出版社", "year": 1981, "price": 58.00, "category": ["文学"], "isbn": "9787020013702"},
        {"title": "白夜", "authors": ["费奥多尔·陀思妥耶夫斯基"], "publisher": "人民文学出版社", "year": 1988, "price": 18.00, "category": ["文学"], "isbn": "9787020009000"},
        {"title": "童年", "authors": ["马克西姆·高尔基"], "publisher": "人民文学出版社", "year": 1988, "price": 20.00, "category": ["文学"], "isbn": "9787020023564"},
        {"title": "在人间", "authors": ["马克西姆·高尔基"], "publisher": "人民文学出版社", "year": 1988, "price": 22.00, "category": ["文学"], "isbn": "9787020023571"},
        {"title": "我的大学", "authors": ["马克西姆·高尔基"], "publisher": "人民文学出版社", "year": 1988, "price": 19.00, "category": ["文学"], "isbn": "9787020023588"},
        {"title": "老人与海", "authors": ["欧内斯特·海明威"], "publisher": "上海译文出版社", "year": 2004, "price": 15.00, "category": ["文学"], "isbn": "9787532734975"},
        {"title": "永别了，武器", "authors": ["欧内斯特·海明威"], "publisher": "上海译文出版社", "year": 2004, "price": 28.00, "category": ["文学"], "isbn": "9787532734982"},
        {"title": "太阳照常升起", "authors": ["欧内斯特·海明威"], "publisher": "上海译文出版社", "year": 2004, "price": 25.00, "category": ["文学"], "isbn": "9787532734968"},
        {"title": "了不起的盖茨比", "authors": ["F·斯科特·菲茨杰拉德"], "publisher": "上海译文出版社", "year": 2006, "price": 20.00, "category": ["文学"], "isbn": "9787532739641"},
        {"title": "麦田里的守望者", "authors": ["J·D·塞林格"], "publisher": "译林出版社", "year": 2018, "price": 32.00, "category": ["文学"], "isbn": "9787544774885"},
        {"title": "杀死一只知更鸟", "authors": ["哈珀·李"], "publisher": "译林出版社", "year": 2012, "price": 32.00, "category": ["文学"], "isbn": "9787544727403"},
        {"title": "阿甘正传", "authors": ["温斯顿·格鲁姆"], "publisher": "人民文学出版社", "year": 2002, "price": 20.00, "category": ["文学"], "isbn": "9787020037913"},
        {"title": "肖申克的救赎", "authors": ["斯蒂芬·金"], "publisher": "人民文学出版社", "year": 2018, "price": 48.00, "category": ["文学"], "isbn": "9787020140615"},
        {"title": "解忧杂货店", "authors": ["东野圭吾"], "publisher": "南海出版公司", "year": 2014, "price": 39.50, "category": ["文学"], "isbn": "9787544270878"},
        {"title": "挪威的森林", "authors": ["村上春树"], "publisher": "上海译文出版社", "year": 2007, "price": 29.00, "category": ["文学"], "isbn": "9787532744459"},
        {"title": "围城", "authors": ["钱钟书"], "publisher": "人民文学出版社", "year": 1991, "price": 25.00, "category": ["文学"], "isbn": "9787020002206"},
        {"title": "红楼梦", "authors": ["曹雪芹"], "publisher": "人民文学出版社", "year": 2008, "price": 88.00, "category": ["文学"], "isbn": "9787020002206"},
        {"title": "西游记", "authors": ["吴承恩"], "publisher": "人民文学出版社", "year": 2004, "price": 56.00, "category": ["文学"], "isbn": "9787020040270"},
        {"title": "三国演义", "authors": ["罗贯中"], "publisher": "人民文学出版社", "year": 1998, "price": 78.00, "category": ["文学"], "isbn": "9787020002206"},
        {"title": "水浒传", "authors": ["施耐庵"], "publisher": "人民文学出版社", "year": 1997, "price": 76.00, "category": ["文学"], "isbn": "9787020002206"},
        {"title": "诗经选", "authors": ["余冠英"], "publisher": "人民文学出版社", "year": 1986, "price": 26.00, "category": ["文学"], "isbn": "9787020018713"},
        {"title": "楚辞选", "authors": ["金开诚"], "publisher": "人民文学出版社", "year": 1998, "price": 32.00, "category": ["文学"], "isbn": "9787020018720"},
        {"title": "唐诗三百首", "authors": ["蘅塘退士"], "publisher": "中华书局", "year": 2009, "price": 26.00, "category": ["文学"], "isbn": "9787101068439"},
        {"title": "宋词三百首", "authors": ["上彊村民"], "publisher": "中华书局", "year": 2009, "price": 26.00, "category": ["文学"], "isbn": "9787101068446"},
        {"title": "古文观止", "authors": ["吴楚材"], "publisher": "中华书局", "year": 2010, "price": 38.00, "category": ["文学"], "isbn": "9787101074188"},
        {"title": "人间词话", "authors": ["王国维"], "publisher": "中华书局", "year": 2016, "price": 18.00, "category": ["文学"], "isbn": "9787101116805"},
        
        # 哲学思想
        {"title": "理想国", "authors": ["柏拉图"], "publisher": "商务印书馆", "year": 1986, "price": 48.00, "category": ["哲学"], "isbn": "9787100023035"},
        {"title": "形而上学", "authors": ["亚里士多德"], "publisher": "商务印书馆", "year": 1997, "price": 36.00, "category": ["哲学"], "isbn": "9787100020092"},
        {"title": "尼各马可伦理学", "authors": ["亚里士多德"], "publisher": "商务印书馆", "year": 2003, "price": 45.00, "category": ["哲学"], "isbn": "9787100035644"},
        {"title": "纯粹理性批判", "authors": ["伊曼努尔·康德"], "publisher": "人民出版社", "year": 2004, "price": 48.00, "category": ["哲学"], "isbn": "9787010042875"},
        {"title": "实践理性批判", "authors": ["伊曼努尔·康德"], "publisher": "人民出版社", "year": 2003, "price": 30.00, "category": ["哲学"], "isbn": "9787010042882"},
        {"title": "判断力批判", "authors": ["伊曼努尔·康德"], "publisher": "人民出版社", "year": 2002, "price": 35.00, "category": ["哲学"], "isbn": "9787010036196"},
        {"title": "存在与时间", "authors": ["马丁·海德格尔"], "publisher": "生活·读书·新知三联书店", "year": 2012, "price": 58.00, "category": ["哲学"], "isbn": "9787108040142"},
        {"title": "存在与虚无", "authors": ["让-保罗·萨特"], "publisher": "生活·读书·新知三联书店", "year": 2018, "price": 79.00, "category": ["哲学"], "isbn": "9787108061467"},
        {"title": "权力意志", "authors": ["弗里德里希·尼采"], "publisher": "商务印书馆", "year": 2007, "price": 48.00, "category": ["哲学"], "isbn": "9787100052166"},
        {"title": "查拉图斯特拉如是说", "authors": ["弗里德里希·尼采"], "publisher": "生活·读书·新知三联书店", "year": 2007, "price": 39.00, "category": ["哲学"], "isbn": "9787108027768"},
        {"title": "悲剧的诞生", "authors": ["弗里德里希·尼采"], "publisher": "商务印书馆", "year": 1986, "price": 28.00, "category": ["哲学"], "isbn": "9787100005113"},
        {"title": "资本论", "authors": ["卡尔·马克思"], "publisher": "人民出版社", "year": 2004, "price": 65.00, "category": ["哲学"], "isbn": "9787010002206"},
        {"title": "共产党宣言", "authors": ["卡尔·马克思", "弗里德里希·恩格斯"], "publisher": "人民出版社", "year": 2014, "price": 12.00, "category": ["哲学"], "isbn": "9787010132073"},
        {"title": "哲学研究", "authors": ["路德维希·维特根斯坦"], "publisher": "商务印书馆", "year": 2005, "price": 42.00, "category": ["哲学"], "isbn": "9787100042294"},
        {"title": "逻辑哲学论", "authors": ["路德维希·维特根斯坦"], "publisher": "商务印书馆", "year": 1996, "price": 22.00, "category": ["哲学"], "isbn": "9787100019301"},
        {"title": "工具论", "authors": ["亚里士多德"], "publisher": "中国人民大学出版社", "year": 2003, "price": 59.00, "category": ["哲学"], "isbn": "9787300044506"},
        {"title": "思想录", "authors": ["布莱兹·帕斯卡尔"], "publisher": "商务印书馆", "year": 1985, "price": 32.00, "category": ["哲学"], "isbn": "9787100001169"},
        {"title": "作为意志和表象的世界", "authors": ["阿图尔·叔本华"], "publisher": "商务印书馆", "year": 1982, "price": 46.00, "category": ["哲学"], "isbn": "9787100002159"},
        {"title": "人类理解论", "authors": ["约翰·洛克"], "publisher": "商务印书馆", "year": 1959, "price": 58.00, "category": ["哲学"], "isbn": "9787100001725"},
        {"title": "人性论", "authors": ["大卫·休谟"], "publisher": "商务印书馆", "year": 1980, "price": 56.00, "category": ["哲学"], "isbn": "9787100005809"},
        {"title": "政府论", "authors": ["约翰·洛克"], "publisher": "商务印书馆", "year": 1964, "price": 35.00, "category": ["哲学"], "isbn": "9787100012101"},
        {"title": "利维坦", "authors": ["托马斯·霍布斯"], "publisher": "商务印书馆", "year": 1985, "price": 58.00, "category": ["哲学"], "isbn": "9787100018745"},
        {"title": "社会契约论", "authors": ["让-雅克·卢梭"], "publisher": "商务印书馆", "year": 2003, "price": 36.00, "category": ["哲学"], "isbn": "9787100034609"},
        {"title": "论法的精神", "authors": ["查理·孟德斯鸠"], "publisher": "商务印书馆", "year": 2009, "price": 68.00, "category": ["哲学"], "isbn": "9787100002159"},
        {"title": "伦理学", "authors": ["巴鲁赫·斯宾诺莎"], "publisher": "商务印书馆", "year": 1983, "price": 30.00, "category": ["哲学"], "isbn": "9787100011678"},
        {"title": "第一哲学沉思集", "authors": ["勒内·笛卡尔"], "publisher": "商务印书馆", "year": 1986, "price": 32.00, "category": ["哲学"], "isbn": "9787100011647"},
        {"title": "谈谈方法", "authors": ["勒内·笛卡尔"], "publisher": "商务印书馆", "year": 2000, "price": 12.00, "category": ["哲学"], "isbn": "9787100032704"},
        {"title": "现象学的观念", "authors": ["埃德蒙德·胡塞尔"], "publisher": "商务印书馆", "year": 1986, "price": 20.00, "category": ["哲学"], "isbn": "9787100018387"},
        {"title": "精神现象学", "authors": ["格奥尔格·黑格尔"], "publisher": "商务印书馆", "year": 1979, "price": 78.00, "category": ["哲学"], "isbn": "9787100002159"},
        {"title": "小逻辑", "authors": ["格奥尔格·黑格尔"], "publisher": "商务印书馆", "year": 1980, "price": 48.00, "category": ["哲学"], "isbn": "9787100011425"},
        {"title": "哲学史讲演录", "authors": ["格奥尔格·黑格尔"], "publisher": "商务印书馆", "year": 1959, "price": 88.00, "category": ["哲学"], "isbn": "9787100002159"},
        {"title": "中国哲学史", "authors": ["冯友兰"], "publisher": "商务印书馆", "year": 1996, "price": 88.00, "category": ["哲学"], "isbn": "9787100028699"},
        {"title": "中国哲学简史", "authors": ["冯友兰"], "publisher": "北京大学出版社", "year": 2016, "price": 49.00, "category": ["哲学"], "isbn": "9787301272333"},
        {"title": "论语译注", "authors": ["杨伯峻"], "publisher": "中华书局", "year": 1980, "price": 20.00, "category": ["哲学"], "isbn": "9787101007410"},
        {"title": "孟子译注", "authors": ["杨伯峻"], "publisher": "中华书局", "year": 1960, "price": 26.00, "category": ["哲学"], "isbn": "9787101003953"},
        {"title": "道德经注译", "authors": ["陈鼓应"], "publisher": "中华书局", "year": 2009, "price": 39.00, "category": ["哲学"], "isbn": "9787101065704"},
        {"title": "庄子今注今译", "authors": ["陈鼓应"], "publisher": "中华书局", "year": 2007, "price": 58.00, "category": ["哲学"], "isbn": "9787101054610"},
        {"title": "周易正义", "authors": ["孔颖达"], "publisher": "北京大学出版社", "year": 1999, "price": 45.00, "category": ["哲学"], "isbn": "9787301039349"},
        
        # 科学经典
        {"title": "时间简史", "authors": ["斯蒂芬·霍金"], "publisher": "湖南科学技术出版社", "year": 2010, "price": 35.00, "category": ["科学"], "isbn": "9787535765444"},
        {"title": "万物简史", "authors": ["比尔·布莱森"], "publisher": "接力出版社", "year": 2017, "price": 78.00, "category": ["科学"], "isbn": "9787544850704"},
        {"title": "物种起源", "authors": ["查尔斯·达尔文"], "publisher": "商务印书馆", "year": 1972, "price": 58.00, "category": ["科学"], "isbn": "9787100001916"},
        {"title": "自然哲学的数学原理", "authors": ["艾萨克·牛顿"], "publisher": "商务印书馆", "year": 1992, "price": 55.00, "category": ["科学"], "isbn": "9787100029160"},
        {"title": "相对论", "authors": ["阿尔伯特·爱因斯坦"], "publisher": "商务印书馆", "year": 1961, "price": 25.00, "category": ["科学"], "isbn": "9787100001916"},
        {"title": "几何原本", "authors": ["欧几里得"], "publisher": "陕西科学技术出版社", "year": 2003, "price": 48.00, "category": ["科学"], "isbn": "9787536936124"},
        {"title": "天演论", "authors": ["托马斯·赫胥黎"], "publisher": "商务印书馆", "year": 1981, "price": 18.00, "category": ["科学"], "isbn": "9787100001916"},
        {"title": "DNA：生命的秘密", "authors": ["詹姆斯·沃森"], "publisher": "上海世纪出版集团", "year": 2005, "price": 48.00, "category": ["科学"], "isbn": "9787532378239"},
        {"title": "宇宙", "authors": ["卡尔·萨根"], "publisher": "天津社会科学院出版社", "year": 2009, "price": 39.80, "category": ["科学"], "isbn": "9787806884345"},
        {"title": "物理世界奇遇记", "authors": ["乔治·伽莫夫"], "publisher": "科学出版社", "year": 2008, "price": 35.00, "category": ["科学"], "isbn": "9787030218234"},
        {"title": "从一到无穷大", "authors": ["乔治·伽莫夫"], "publisher": "科学出版社", "year": 2002, "price": 39.00, "category": ["科学"], "isbn": "9787030107596"},
        {"title": "昆虫记", "authors": ["让-亨利·法布尔"], "publisher": "人民文学出版社", "year": 1997, "price": 38.00, "category": ["科学"], "isbn": "9787020021713"},
        {"title": "寂静的春天", "authors": ["蕾切尔·卡逊"], "publisher": "上海译文出版社", "year": 2007, "price": 28.00, "category": ["科学"], "isbn": "9787532743261"},
        {"title": "人类简史", "authors": ["尤瓦尔·赫拉利"], "publisher": "中信出版社", "year": 2014, "price": 68.00, "category": ["科学"], "isbn": "9787508647357"},
        {"title": "未来简史", "authors": ["尤瓦尔·赫拉利"], "publisher": "中信出版社", "year": 2017, "price": 68.00, "category": ["科学"], "isbn": "9787508672069"},
        {"title": "今日简史", "authors": ["尤瓦尔·赫拉利"], "publisher": "中信出版社", "year": 2018, "price": 68.00, "category": ["科学"], "isbn": "9787508687290"},
        {"title": "自私的基因", "authors": ["理查德·道金斯"], "publisher": "中信出版社", "year": 2012, "price": 58.00, "category": ["科学"], "isbn": "9787508631644"},
        {"title": "枪炮、病菌与钢铁", "authors": ["贾雷德·戴蒙德"], "publisher": "上海译文出版社", "year": 2006, "price": 58.00, "category": ["科学"], "isbn": "9787532740291"},
        {"title": "数学之美", "authors": ["吴军"], "publisher": "人民邮电出版社", "year": 2014, "price": 45.00, "category": ["科学"], "isbn": "9787115352104"},
        {"title": "从0到1", "authors": ["彼得·蒂尔"], "publisher": "中信出版社", "year": 2015, "price": 45.00, "category": ["科学"], "isbn": "9787508649715"},
        {"title": "精益创业", "authors": ["埃里克·莱斯"], "publisher": "中信出版社", "year": 2012, "price": 42.00, "category": ["科学"], "isbn": "9787508633403"},
        {"title": "黑客与画家", "authors": ["保罗·格雷厄姆"], "publisher": "人民邮电出版社", "year": 2011, "price": 49.00, "category": ["科学"], "isbn": "9787115250124"},
        {"title": "技术的本质", "authors": ["布莱恩·阿瑟"], "publisher": "浙江人民出版社", "year": 2014, "price": 45.00, "category": ["科学"], "isbn": "9787213061134"},
        {"title": "失控", "authors": ["凯文·凯利"], "publisher": "新星出版社", "year": 2010, "price": 88.00, "category": ["科学"], "isbn": "9787802259077"},
        {"title": "奇点临近", "authors": ["雷·库兹韦尔"], "publisher": "机械工业出版社", "year": 2011, "price": 88.00, "category": ["科学"], "isbn": "9787111358805"},
        {"title": "长尾理论", "authors": ["克里斯·安德森"], "publisher": "中信出版社", "year": 2006, "price": 49.00, "category": ["科学"], "isbn": "9787508606148"},
        {"title": "免费", "authors": ["克里斯·安德森"], "publisher": "中信出版社", "year": 2009, "price": 39.00, "category": ["科学"], "isbn": "9787508617030"},
        {"title": "认知盈余", "authors": ["克莱·舍基"], "publisher": "中国人民大学出版社", "year": 2011, "price": 49.80, "category": ["科学"], "isbn": "9787300136208"},
        {"title": "浅薄", "authors": ["尼古拉斯·卡尔"], "publisher": "中信出版社", "year": 2010, "price": 35.00, "category": ["科学"], "isbn": "9787508621832"},
        {"title": "黑天鹅", "authors": ["纳西姆·塔勒布"], "publisher": "中信出版社", "year": 2008, "price": 39.00, "category": ["科学"], "isbn": "9787508611542"},
        {"title": "反脆弱", "authors": ["纳西姆·塔勒布"], "publisher": "中信出版社", "year": 2014, "price": 68.00, "category": ["科学"], "isbn": "9787508643335"},
        {"title": "随机漫步的傻瓜", "authors": ["纳西姆·塔勒布"], "publisher": "中信出版社", "year": 2012, "price": 39.00, "category": ["科学"], "isbn": "9787508633502"},
        {"title": "魔鬼经济学", "authors": ["史蒂芬·列维特"], "publisher": "中信出版社", "year": 2006, "price": 39.00, "category": ["科学"], "isbn": "9787508605875"},
        {"title": "思考，快与慢", "authors": ["丹尼尔·卡尼曼"], "publisher": "中信出版社", "year": 2012, "price": 69.00, "category": ["科学"], "isbn": "9787508633557"},
        {"title": "怪诞行为学", "authors": ["丹·艾瑞里"], "publisher": "中信出版社", "year": 2008, "price": 39.00, "category": ["科学"], "isbn": "9787508612228"},
        {"title": "影响力", "authors": ["罗伯特·西奥迪尼"], "publisher": "中国人民大学出版社", "year": 2006, "price": 45.00, "category": ["科学"], "isbn": "9787300081173"}
    ]
    
    # 辅助函数：获取或创建作者ID
    def get_or_create_author(author_name):
        # 先查询是否存在
        result = db_manager.execute_query(
            "SELECT author_id FROM authors WHERE author_name = ?", 
            (author_name,)
        )
        if result['success'] and result['data']:
            return result['data'][0]['author_id']
        
        # 不存在则创建
        insert_result = db_manager.execute_query(
            "INSERT INTO authors (author_name) VALUES (?)", 
            (author_name,)
        )
        if insert_result['success']:
            return insert_result['data']['last_id']
        return None
    
    # 辅助函数：获取或创建出版社ID
    def get_or_create_publisher(publisher_name):
        # 先查询是否存在
        result = db_manager.execute_query(
            "SELECT publisher_id FROM publishers WHERE publisher_name = ?", 
            (publisher_name,)
        )
        if result['success'] and result['data']:
            return result['data'][0]['publisher_id']
        
        # 不存在则创建，默认国家为中国
        insert_result = db_manager.execute_query(
            "INSERT INTO publishers (publisher_name, country) VALUES (?, ?)", 
            (publisher_name, "中国")
        )
        if insert_result['success']:
            return insert_result['data']['last_id']
        return None
    
    # 辅助函数：获取或创建分类ID
    def get_or_create_category(category_name):
        # 先查询是否存在
        result = db_manager.execute_query(
            "SELECT category_id FROM categories WHERE category_name = ?", 
            (category_name,)
        )
        if result['success'] and result['data']:
            return result['data'][0]['category_id']
        
        # 不存在则创建
        insert_result = db_manager.execute_query(
            "INSERT INTO categories (category_name) VALUES (?)", 
            (category_name,)
        )
        if insert_result['success']:
            return insert_result['data']['last_id']
        return None
    
    # 遍历图书列表，插入数据库
    count = 0
    for book in classic_books:
        try:
            # 获取或创建出版社ID
            publisher_id = get_or_create_publisher(book['publisher'])
            if not publisher_id:
                print(f"跳过 {book['title']}：无法创建出版社")
                continue
            
            # 插入图书基本信息
            book_result = db_manager.execute_query(
                """
                INSERT INTO books (title, isbn, publisher_id, publication_year, price, stock)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    book['title'], 
                    book['isbn'], 
                    publisher_id, 
                    book['year'], 
                    book['price'], 
                    10  # 默认库存10本
                )
            )
            
            if not book_result['success']:
                print(f"跳过 {book['title']}：{book_result['error']}")
                continue
            
            book_id = book_result['data']['last_id']
            
            # 处理作者关系
            for author in book['authors']:
                author_id = get_or_create_author(author)
                if author_id:
                    db_manager.execute_query(
                        "INSERT INTO book_authors (book_id, author_id) VALUES (?, ?)",
                        (book_id, author_id)
                    )
            
            # 处理分类关系
            for category in book['category']:
                category_id = get_or_create_category(category)
                if category_id:
                    db_manager.execute_query(
                        "INSERT INTO book_categories (book_id, category_id) VALUES (?, ?)",
                        (book_id, category_id)
                    )
            
            count += 1
            print(f"已录入 {count}/100：{book['title']}")
        except Exception as e:
            print(f"处理 {book['title']} 时出错：{str(e)}")
            continue
    
    print(f"\n预录入完成！共录入 {count} 本经典高中、大学图书。")


if __name__ == "__main__":
    seed_books()
