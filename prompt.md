
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
merge_pdfs 函数可以使用第三方库PyMuPDF 来实现。

要求：
以函数式编程的风格撰写代码，并最终以main()调用.
不要使用subprocess实现，而是使用第三方库来实现。
