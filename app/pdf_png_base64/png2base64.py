import base64


def png_to_svg_embed(png_path, svg_output_path):
    with open(png_path, "rb") as image_file:
        # 1. 编码为 Base64
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # 2. 构建 SVG 字符串
    # 注意：这里可以根据需要动态调整 width 和 height
    svg_content = f'''{encoded_string}'''

    # 3. 写入文件
    with open(svg_output_path, "w") as svg_file:
        svg_file.write(svg_content)
    print(f"成功生成: {svg_output_path}")



png_to_svg_embed("/Users/yuzhenling/harbour/qianyuan/docs/安徽大盘模板/caa51.png", "pdf_png_base64/caa51.svg")
png_to_svg_embed("/Users/yuzhenling/harbour/qianyuan/docs/安徽大盘模板/caa52.png", "pdf_png_base64/caa52.svg")
