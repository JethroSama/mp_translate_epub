from asyncio.windows_events import NULL
from json import JSONDecoder
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


def init():
    driver = webdriver.Firefox()

    driver.get("https://www.deepl.com/translator")

    driver.implicitly_wait(10)

    # set input language to chinese
    lang_input_element = driver.find_element(
        by=By.CSS_SELECTOR, value="div.lmt__language_select--source>button")
    lang_input_element.click()

    lang_input_element = driver.find_element(
        by=By.CSS_SELECTOR, value="button[dl-test='translator-lang-option-zh']")
    lang_input_element.click()

    # set output language to english
    lang_input_element = driver.find_element(
        by=By.CSS_SELECTOR, value="div.lmt__language_select--target>button")
    lang_input_element.click()

    lang_input_element = driver.find_element(
        by=By.CSS_SELECTOR, value="button[dl-test='translator-lang-option-en-US']")
    lang_input_element.click()


def get_translation(text):
    input_textarea = driver.find_element(
        by=By.CSS_SELECTOR, value='textarea.lmt__source_textarea')

    input_textarea.clear()
    input_textarea.send_keys(text)

    # wait if lmt__progress_popup is visible
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.lmt__progress_popup")))
    # the loading is started, wait until it is finished
    WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.lmt__progress_popup")))

    # Loading has ended

    output_textarea = driver.find_element(
        by=By.CSS_SELECTOR, value='#target-dummydiv')

    print("translation is done")
    print(output_textarea.get_attribute("innerHTML"))

    # make a post request to http://localhost:3000/createBook
    # with the following data:

    requests.post("http://localhost:3000/createBook", json={
        "text": output_textarea.get_attribute("innerHTML"),
        "title": "Mp",
        "author": "Momo",
        "imageUrl": "",
        "publisher": "Jet"
    },)


# loop twice
# get_translation('欢迎您的光临, 请记住本站地址: , 手机阅读, 以便随时阅读小说《武炼巅峰》最新章节... \n    赵星辰悠悠地盯着那个大月州弟子, 看的那人头皮发麻, 好一会功夫, 赵星辰才冷哼一声道: “既然孟兄这般说了, 那赵某就卖孟兄一个面子, 这次就算了, 若有下次, 定不轻饶!”\n    孟宏不禁松一口气, 赔笑道: “多谢赵兄大人大量.”\n    赵星辰不置可否, 扭头望着陈玥道: “玥儿, 你们大家相识一场也是缘分, 今日既然来了, 就敬孟兄等人一杯水酒吧.”\n    “好.”陈玥对赵星辰唯命是从, 上前来斟了一杯酒端在手上.\n    见她如此, 孟宏的表情愈发痛楚, 面上一片苍白, 暗恨自己实力不足, 没法给陈玥提供安全的庇护, 只能眼睁睁看着自己心爱的女人对人家投怀送抱, 当真是心如刀绞.\n    陈玥举杯, 美眸凝视孟宏道: “诸位师兄, 这一杯我敬你们, 以后你们若是有什么需要帮忙的, 尽管来找我, 小妹力所能及定不推辞.”\n    赵星辰也在一旁点头道: “不错, 在这里, 我赵星辰还是有几分薄面的, 你们以后若是遇到什么事就来找我.”\n    大月州三人皆都无奈举杯, 一饮而尽.\n    赵星辰的目光却是凝视着杨开, 面色有些不虞道: “这位朋友是不给面子吗?”进门之后他也没注意到杨开, 只不过如今陈玥听他吩咐敬酒, 杨开端坐不动, 一下子就显得特别显眼, 他自然看在眼中.\n    至于同样没有举杯的月荷, 他倒是不太想招惹, 毕竟人家是个五品开天, 赤星那边一直有意邀请月荷加入, 并毫不吝啬地许以一个大统领的位置, 可惜月荷并没有给出过明确的答复.\n    “我跟你很熟吗?”杨开抬眼看了看他, 淡淡道: “你的面子值几个钱?”\n    他一直坐在这里冷眼旁观, 将所有的事都看在眼中, 本来人家不招惹他, 他也懒得去插手, 谁知这赵星辰居然主动招惹过来, 杨开对他自然不会太客气.\n    虽然头一次见面, 也谈不上深交, 但赵星辰给他的感觉却是很不好, 对这种人, 杨开也懒得假以辞色.\n    一言出, 赵星辰的脸色顿时一沉: “朋友够狂, 怎么称呼?瞧着面生的很啊.”\n    孟宏也没想到杨开会来这么一出, 连忙打圆场道: “赵兄, 这位是杨开杨兄!”\n    “你就是杨开?”赵星辰闻言眼前一亮, 忍不住上下打量起杨开来.\n    杨开淡淡地望着他: “你认识我?”\n    赵星辰咧嘴一笑, 抱拳道: “原来是杨兄啊, 失敬失敬, 之前听玥儿提起过很多次了, 这次过来赵某本就有意要拜会一下杨兄, 没想到在这里见到了, 咱们可真是有缘.”\n    他态度热情至极, 这般说着, 竟是自己拉了把椅子坐了下来.\n    孟宏等人看的一头雾水, 皆都狐疑地朝陈玥望去, 也不知道她到底都跟赵星辰说过些什么, 这姓赵的对杨开的态度居然这般热忱.\n    杨开也若有所思地瞧了一眼陈玥, 后者忍不住脸色一红, 目光躲闪.\n    落座之后, 赵星辰挥手间在四周布下一层禁制, 隔绝内外, 从这一手力量的挥洒来看, 他的实力也算不俗, 比起孟宏等人似乎都要高出一截.\n    这才凑过来, 一脸放光地道: “杨兄, 我听玥儿说杨兄有驭兽之能?麾下收拢了一头赤蛟, 一头地龙?不知是真是假?”\n    孟宏听了, 脸色不禁一沉, 扭头看了陈玥一眼, 隐隐有些责怪之意.\n    陈玥虽攀高枝, 对赵星辰投怀送抱, 孟宏也只是自恨自己没本事留住佳人, 可透露杨开的这个情报就不应该了, 很多时候, 这些情报都牵扯到生死和利益, 更何况, 陈玥之前也得过杨开的救命之恩, 也是杨开将她一路带到这里来的, 她不知恩图报也就罢了, 如今将这么重要的信息透露给一个外人, 这不是吃里扒外吗?\n    陈玥也算是经由他才认识杨开, 这么一弄, 他颇有些无地自容之感.\n    “真又如何?假又如何?”杨开表情戏虐地望了陈玥一眼, 却见她一直低着脑袋, 表情局促不安.\n    想来她也知道, 自己这事干的有些不地道, 没脸见人.\n    赵星辰呵呵一笑: “玥儿既然这么说, 那应该就是真的了, 杨兄了得, 驭兽之能出神入化, 赵某佩服.来, 赵某敬你一杯.”\n    说着话, 端起酒杯举了过来.\n    杨开置若罔闻, 看都不看他一眼.\n    赵星辰脸上的皮肉微微跳动了一下, 呵呵笑了笑, 也不以为意, 将酒杯放下, 接着道: “是这样的杨兄, 赵某有个姐姐听闻这事, 对杨兄手下的一只异兽颇感兴趣, 挺想豢养一只的, 不知杨兄是否愿意割爱, 价钱方面都好说, 保管让你满意.”\n    “你姐姐想养一只?”杨开表情古怪地望着他, “想养哪一只?”\n    “家姐对那赤蛟比较感兴趣, 地龙就算了, 杨兄你也知道的, 地龙这东西模样有些不讨喜, 呵呵.”\n    杨开颔首道: “这倒也是.”\n    赵星辰道: “杨兄你开个价, 多少赵某都买了, 大家就当交个朋友, 日后杨兄若是有什么需要帮忙的, 只管开口, 赵某绝不推辞.”\n    杨开摇头道: “不好意思, 不管是赤蛟还是地龙, 都不卖.”\n    赵星辰一听就急了, 抬手道: “杨兄别忙着拒绝啊, 要不先听听赵某的报价再做决定如何?”\n    杨开依旧摇头: “不卖就是不卖, 你开多少钱都不卖!”\n    “当真不卖?”赵星辰微微眯眼.\n    杨开凝视着他: “同样的话, 我不想说第三遍!”\n    四目对视, 赵星辰眸中略有冷意, 杨开一脸淡然, 孟宏等人在旁紧张不安, 唯独月荷笑吟吟地, 手托着香腮坐在杨开身边, 侧眼瞧着他, 一瞬不移, 好似怎么也看不够.\n    好一会功夫, 赵星辰才笑了一声: “行, 杨兄既然这么说了, 那赵某就不夺人所爱.”话锋一转道: “咱们不说那两只异兽, 说说那龙血丹吧.”\n    杨开微微眯眼道: “你知道的还挺多.”\n    不用说了, 龙血丹的事也是陈玥透露出去的了, 之前杨开炼制了不少龙血丹, 除了自己服用和给小黑小红的之外, 孟宏等人也都得了几粒, 这东西稀释了之后服用, 对武者有强化肉身之效, 对任何人都有大用.\n    赵星辰既然得知龙血丹的存在, 又怎会不在意?\n    没理会杨开话语中的揶揄, 赵星辰神色一肃, 凝声道: “赤星方面想从杨兄手上收购一些龙血丹, 价格不是问题, 有多少要多少.”\n    他嘴皮子一碰, 己身直接就成了赤星的代表, 换言之, 是代表赤星来跟杨开谈这笔买卖, 尽可拿大势压人...\n    “赤星想买我龙血丹?”杨开失笑.\n    赵星辰颔首道: “不错!”\n    “不卖!”杨开果断回绝, 这么多年来, 好不容易碰到一批超越极品的龙血花, 花费了四个月时间炼制成龙血丹, 正是用来精进自身血脉的时候, 又怎么可能拿出去卖?\n    自己用都嫌不够呢.\n    赵星辰似早有预料, 闻言也只是淡淡一笑, 端起桌上的酒杯轻轻抿了一口, 好整以暇道: “杨兄, 我听说你最近一直在闭关, 可能对外面的局势不太了解.如今这整个星市, 都是我赤星的地盘, 进了这星市, 便得受我赤星管辖, 不服管的人在这里活不了太长时间.”\n    杨开笑吟吟地看着他, 老神在在道: “你在威胁我?”\n    “只是给杨兄分析一下局势.”赵星辰放下酒杯, “如今我赤星有七位当家人, 个个都是三品开天之上, 麾下三千众, 不客气的说, 这太墟境中能出赤星之右者, 寥寥无几!杨兄一路走来, 修炼至今, 能有今日之成就也不容易, 想必也懂的什么叫审时度势!赤星只是想从杨兄这里买一些龙血丹罢了, 杨兄又何必这般不近人情, 拒人于千里之外?”\n    言罢, 笑容绽放道: “而且杨兄既能炼制龙血丹, 想必在丹道上也颇有造诣, 我赤星缺的就是杨兄这样的人才, 赵某愿做个引荐人, 只要杨兄愿意, 来我赤星当个客卿炼丹师是绝无问题的, 日后大家就是一家人.”\n    “杨兄, 你觉得如何?”\n    最后一句话, 赵星辰目光灼灼逼视过来.\n    杨开道: “不卖就是不卖, 任你说的天花乱坠也无用.”\n    赵星辰面色一冷: “杨兄不再好好考虑考虑?我怕杨兄会后悔啊!”\n    杨开冷眼望去: “你再敢啰嗦, 我会叫你后悔坐下来!”\n    赵星辰面色一沉, 拍案而起, 怒视杨开, 一脸杀机, 好一会才转头望着月荷道: “月荷姑娘, 不如你劝劝他?”\n    月荷一脸花痴的表情, 幽幽道: “少爷说什么就是什么, 我都听少爷的.”\n    “好!”赵星辰怒极反笑, “很好!”\n    伸手一拍巴掌, 爆喝道: “来人!”\n    门外哗啦啦涌进来十几人, 个个气息雄浑, 立于赵星辰身后.\n    赵星辰把手一指前方: “本统领怀疑这些人是别家势力安插在这里的奸细, 统统都给我拿下!”')

def get_chapters():
    data = requests.get('http://localhost:3000/chapters')
    return data.json()


def get_chapter(num):
    chapters = get_chapters()
    # find chapter.text contains `第${number}章`
    for chapter in chapters:
        if '第' + str(num) + '章' in chapter['text']:
            return chapter
        else:
            return NULL


c = get_chapter(5)
print(c)
