import zipfile
import xml.etree.ElementTree as ET
import os

def extract_pptx_colors(pptx_file):
    print(f"Extracting colors from {pptx_file}...")
    try:
        with zipfile.ZipFile(pptx_file, 'r') as z:
            # Usually theme1.xml has the main color scheme
            if 'ppt/theme/theme1.xml' in z.namelist():
                xml_content = z.read('ppt/theme/theme1.xml')
                root = ET.fromstring(xml_content)
                
                # Namespaces
                ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
                
                clr_scheme = root.find('.//a:clrScheme', ns)
                if clr_scheme is None:
                    print("No color scheme found in theme1.xml")
                    return
                
                colors = {}
                # Map of theme color names
                theme_colors = ['dk1', 'lt1', 'dk2', 'lt2', 'accent1', 'accent2', 'accent3', 'accent4', 'accent5', 'accent6']
                
                for color_name in theme_colors:
                    node = clr_scheme.find(f'.//a:{color_name}', ns)
                    if node is not None:
                        # Check for srgbClr (RGB Hex)
                        srgb = node.find('.//a:srgbClr', ns)
                        if srgb is not None:
                            val = srgb.get('val')
                            colors[color_name] = f"#{val}"
                        else:
                            # Check for sysClr (System Color) - often used for black/white
                            sys = node.find('.//a:sysClr', ns)
                            if sys is not None:
                                last_clr = sys.get('lastClr')
                                val = sys.get('val')
                                colors[color_name] = f"#{last_clr}" if last_clr else f"Example: {val}"
                
                print("\nExtracted Theme Colors:")
                for k, v in colors.items():
                    print(f"{k}: {v}")
                    
                # Store them?
                with open('extracted_colors.txt', 'w') as f:
                    for k, v in colors.items():
                        f.write(f"{k}: {v}\n")
                        
            else:
                print("ppt/theme/theme1.xml not found")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_pptx_colors('Style.pptx')
