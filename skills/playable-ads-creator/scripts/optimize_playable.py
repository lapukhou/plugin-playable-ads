#!/usr/bin/env python3
"""
Optimize HTML5 playable ads for production.
- Minifies HTML, CSS, and JavaScript
- Inlines assets as base64
- Validates file size
- Removes debug code
"""

import argparse
import base64
import re
import sys
from pathlib import Path

def minify_html(html):
    """Basic HTML minification."""
    # Remove comments
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    # Remove unnecessary whitespace
    html = re.sub(r'\s+', ' ', html)
    html = re.sub(r'>\s+<', '><', html)
    return html.strip()

def minify_css(css):
    """Basic CSS minification."""
    # Remove comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    # Remove whitespace
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{}:;,])\s*', r'\1', css)
    return css.strip()

def minify_js(js):
    """Basic JavaScript minification."""
    # Stash string literals first so comment stripping cannot corrupt
    # content like https:// store URLs inside them
    strings = []

    def stash(match):
        strings.append(match.group(0))
        return f'\x00STR{len(strings) - 1}\x00'

    js = re.sub(
        r'"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'|`(?:\\.|[^`\\])*`',
        stash, js)
    # Remove single-line comments
    js = re.sub(r'//.*?$', '', js, flags=re.MULTILINE)
    # Remove multi-line comments
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    # Remove console logs (string args are stashed, so no nested parens remain)
    js = re.sub(r'console\.(log|debug|info|warn|error)\([^()]*\);?', '', js)
    # Remove extra whitespace
    js = re.sub(r'\s+', ' ', js)
    js = js.strip()
    # Restore string literals
    return re.sub(r'\x00STR(\d+)\x00', lambda m: strings[int(m.group(1))], js)

def inline_images_as_base64(html, html_dir):
    """Find image references and inline them as base64."""
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
    
    def replace_img(match):
        img_tag = match.group(0)
        img_path = match.group(1)
        
        # Skip data URIs
        if img_path.startswith('data:'):
            return img_tag
        
        # Try to find the image file
        full_path = html_dir / img_path
        if not full_path.exists():
            print(f"  Warning: Image not found: {img_path}")
            return img_tag
        
        # Read and encode
        try:
            with open(full_path, 'rb') as f:
                img_data = f.read()
            
            # Determine MIME type
            ext = full_path.suffix.lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp',
                '.svg': 'image/svg+xml'
            }
            mime_type = mime_types.get(ext, 'image/png')
            
            # Create data URI
            b64_data = base64.b64encode(img_data).decode('ascii')
            data_uri = f'data:{mime_type};base64,{b64_data}'
            
            # Replace src
            new_tag = re.sub(r'src=["\'][^"\']+["\']', f'src="{data_uri}"', img_tag)
            print(f"  ✓ Inlined: {img_path} ({len(img_data)} bytes)")
            return new_tag
        except Exception as e:
            print(f"  Error inlining {img_path}: {e}")
            return img_tag
    
    return re.sub(img_pattern, replace_img, html)

def optimize_playable(input_file, output_file=None, max_size_mb=5):
    """Optimize a playable ad HTML file."""
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_file}")
        return False
    
    print(f"Optimizing: {input_file}")
    
    # Read input
    html = input_path.read_text(encoding='utf-8')
    original_size = len(html.encode('utf-8'))
    print(f"  Original size: {original_size:,} bytes ({original_size/1024:.1f} KB)")
    
    # Extract and minify CSS
    def minify_style_block(match):
        css = match.group(1)
        return f'<style>{minify_css(css)}</style>'
    
    html = re.sub(r'<style>(.*?)</style>', minify_style_block, html, flags=re.DOTALL)
    
    # Extract and minify JavaScript
    def minify_script_block(match):
        js = match.group(1)
        return f'<script>{minify_js(js)}</script>'
    
    html = re.sub(r'<script>(.*?)</script>', minify_script_block, html, flags=re.DOTALL)
    
    # Inline images as base64
    html = inline_images_as_base64(html, input_path.parent)
    
    # Minify HTML structure
    html = minify_html(html)
    
    # Calculate final size
    final_size = len(html.encode('utf-8'))
    size_mb = final_size / (1024 * 1024)
    reduction = ((original_size - final_size) / original_size) * 100
    
    print(f"  Optimized size: {final_size:,} bytes ({final_size/1024:.1f} KB)")
    print(f"  Size reduction: {reduction:.1f}%")
    print(f"  Final size: {size_mb:.2f} MB")
    
    # Check size limit
    if size_mb > max_size_mb:
        print(f"  ⚠ Warning: File exceeds {max_size_mb}MB limit!")
    else:
        print(f"  ✓ Size is within {max_size_mb}MB limit")
    
    # Write output
    if output_file is None:
        output_file = input_path.parent / f"{input_path.stem}_optimized.html"
    else:
        output_file = Path(output_file)
    
    output_file.write_text(html, encoding='utf-8')
    print(f"  ✓ Saved to: {output_file}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Optimize playable ads for production')
    parser.add_argument('input', help='Input HTML file')
    parser.add_argument('--output', '-o', help='Output file (default: input_optimized.html)')
    parser.add_argument('--max-size', type=float, default=5.0,
                       help='Maximum file size in MB (default: 5.0)')
    
    args = parser.parse_args()
    
    if not optimize_playable(args.input, args.output, args.max_size):
        sys.exit(1)

if __name__ == '__main__':
    main()
