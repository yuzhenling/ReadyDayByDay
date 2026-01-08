import asyncio
from playwright.async_api import async_playwright

#本示例是通过playwright抓取动态网站的内容和图片
# 1.通过点击页面进行切iframe切换
# 2.通过# . 进行id 和class定位
# 3.通过screenshot 对定位div进行截取保存

async def run():
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)  # 调试时设为 False
        page = await browser.new_page()

        url = "https://sesa.cnse.e-cqs.cn/cnse-mobile//tContainerApproval/certView/***"
        await page.goto(url)
        await page.wait_for_load_state('networkidle')

        print("页面加载完成...")
        await asyncio.sleep(2)

        # 1. 点击“使用申请”选项卡
        # 使用 text 内容定位，这是最稳妥的方法
        await page.click("li:has-text('使用申请')")

        # 2. 等待 iframe 加载内容
        # 因为 iframe 的 src 可能是点击后才动态生成的，我们需要定位 id 为 "use" 的 iframe
        iframe_selector = "iframe#use"
        await page.wait_for_selector(iframe_selector)

        # 3. 获取 iframe 句柄
        # frame_locator 允许你像操作普通页面一样操作 iframe 内部
        use_frame = page.frame_locator(iframe_selector)

        # 4. 获取数据 (示例：获取隐藏 input 的 value)
        # 比如你想获取截图中的 useRegistrationFormUrl
        try:
            # 等待 iframe 内部的某个元素出现，确保页面已渲染
            equipment_span = use_frame.locator("#equipmentCode")
            await equipment_span.wait_for(state="attached")

            #产品名称
            product_name = await use_frame.locator("#productName").inner_text()
            #设备品种
            equipment_type = await use_frame.locator("#equipmentType").inner_text()
            #产品编号
            product_no = await use_frame.locator("#productNo").inner_text()
            #设备代码
            equipment_code = await equipment_span.inner_text()
            #单位内编号
            unit_number = await use_frame.locator("#unitNumber").inner_text()
            #使用单位
            unit_name = await use_frame.locator("#unitName").inner_text()

            print(f"{product_name}, {equipment_type}, {product_no}, {equipment_code}  {unit_number}, {unit_name}")


        except Exception as e:
            print(f"获取数据失败: {e}")

        await page.click("li:has-text('证书')")

        iframe_selector = "iframe#cert"
        await page.wait_for_selector(iframe_selector)

        # 3. 获取 iframe 句柄
        cert_frame = page.frame_locator(iframe_selector)

        try:
            cert_div = cert_frame.locator("div.weadmin-body")
            await cert_div.wait_for(state="visible")
            await cert_div.screenshot(
                path="playwright/合格证截图.jpg",
                type="jpeg",
                quality=90
            )


        except Exception as e:
            print(f"截图合格证失败: {e}")


        await asyncio.sleep(2)
        await browser.close()


asyncio.run(run())