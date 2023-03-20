
# Folder to PDF
[folder_to_pdf.py](folder_to_pdf.py)

## 程序逻辑
我准备要写一个python程序，将给定文件夹下所有的文件转换成一个PDF。
请先描述这个程序运行的逻辑，以函数式编程的风格，并将这个程序的逻辑成像成多个函数。给出每个函数的输入输出说明。

这个程序的逻辑可以分为以下几个步骤：

获取给定文件夹下的所有文件路径
对于每个文件，调用相应的转换函数将其转换为PDF格式
将所有转换后的PDF文件合并成一个PDF文件
可以将这个程序分为以下几个函数：

get_file_paths(folder_path: str) -> List[str]：输入文件夹路径，输出该文件夹下所有文件的路径列表。
convert_to_pdf(file_path: str) -> str：输入文件路径，输出转换后的PDF文件路径。
merge_pdfs(pdf_paths: List[str], output_path: str) -> None：输入PDF文件路径列表和输出PDF文件路径，将所有PDF文件合并成一个PDF文件。

其中，convert_to_pdf 函数可以使用第三方库 pdfkit 来实现，
merge_pdfs 函数可以使用第三方库PyMuPDF 来实现。

## 代码实现
写一个python程序，将给定文件夹下所有的文件转换成一个PDF。
这个程序的逻辑可以分为以下几个步骤：

获取给定文件夹下的所有文件路径
对于每个文件，调用相应的转换函数将其转换为PDF格式
将所有转换后的PDF文件合并成一个PDF文件
可以将这个程序分为以下几个函数：

get_file_paths(folder_path: str) -> List[str]：输入文件夹路径，输出该文件夹下所有文件的路径列表。
convert_to_pdf(file_path: str) -> str：输入文件路径，输出转换后的PDF文件路径。
merge_pdfs(pdf_paths: List[str], output_path: str) -> None：输入PDF文件路径列表和输出PDF文件路径，将所有PDF文件合并成一个PDF文件。

其中，convert_to_pdf 函数可以使用第三方库 pdfkit 来实现，
在convert_to_pdf 中，应当先将不同格式的文件先统一转换成html
可以使用repo_to_pdf中的convert_to_html(path)来实现
from repo_to_pdf import convert_to_html

merge_pdfs 函数可以使用第三方库PyMuPDF 来实现。

要求：
* 以函数式编程的风格撰写代码，并最终以main()调用.
* 不要使用subprocess实现，而是使用第三方库来实现。
* 注意在使用pdfkit转换pdf文件时，需要加载options和configuration
参考
options = {'quiet': '','page-size': 'Letter','encoding': 'utf-8',}
pdfkit.from_file(file_path, pdf_path, options=options, configuration=pdfkit.configuration(wkhtmltopdf=get_wkhtmltopdf_path()))

* 需要转换成PDF的文件类型放在一个列表中，其中至少应当包含
".txt", ".md", ".py", ".html", ".ipynb"
* 注意ipynb文件中可能存在有不被支持的格式，应当先使用
remove_unsupported_output(notebook)实现将不支持的格式去除
from repo_to_pdf import remove_unsupported_output
* 应当去除在转换过程中临时产生的pdf文件

