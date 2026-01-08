import os
from pdf2image import convert_from_path
import fitz  # PyMuPDF

def pdf_to_png(pdf_path, output_folder):
    """
    将指定路径的 PDF 转换为 PNG
    :param pdf_path: PDF 文件绝对路径
    :param output_folder: 图片保存的文件夹路径
    """
    # 1. 确保输出目录存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"创建目录: {output_folder}")

    try:
        print(f"正在转换: {pdf_path} ...")

        # 2. 核心转换代码
        # dpi=300 表示高清晰度
        images = convert_from_path(pdf_path, dpi=600, use_pdftocairo=True, strict=False)

        # 3. 循环保存每一页
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        for i, image in enumerate(images):
            # 拼接输出文件名，例如: test_page_1.png
            output_filename = f"{base_name}_page_{i + 1}.png"
            save_path = os.path.join(output_folder, output_filename)

            image.save(save_path, 'PNG')
            print(f"已保存: {save_path}")

        print("--- 转换完成 ---")

    except Exception as e:
        print(f"转换失败: {e}")





def pdf_to_png_high_contrast(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        # 4.0 约等于 288 DPI，如果你需要更高可以设为 6.0
        # colorspace=fitz.csGRAY 可以强制转为灰度，有时能让文字显得更黑
        mat = fitz.Matrix(6.0, 6.0)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        save_path = f"{output_folder}/page_{i + 1}.png"
        pix.save(save_path)
        print(f"已保存: {save_path}")
    doc.close()

# --- 使用示例 ---
if __name__ == "__main__":
    # 请修改为你实际的 PDF 路径
    my_pdf = "/Users/yuzhenling/harbour/qianyuan/docs/安徽大盘模板/长安A5合格证-20260108.pdf"
    # 图片存储路径
    my_output = "/Users/yuzhenling/harbour/qianyuan/docs/安徽大盘模板"

    pdf_to_png_high_contrast(my_pdf, my_output)