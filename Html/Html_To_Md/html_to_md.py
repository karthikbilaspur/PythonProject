import html2text
import argparse

def convert_html_to_md(html_file, md_file):
    with open(html_file, 'r') as f:
        html_content = f.read()
    
    h = html2text.HTML2Text()
    md_content = h.handle(html_content)
    
    with open(md_file, 'w') as f:
        f.write(md_content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert HTML to Markdown')
    parser.add_argument('-i', '--input', help='Input HTML file', required=True)
    parser.add_argument('-o', '--output', help='Output Markdown file', required=True)
    args = parser.parse_args()
    
    convert_html_to_md(args.input, args.output)