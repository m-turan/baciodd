import requests
import xml.etree.ElementTree as ET
import os
from pathlib import Path

def download_xml(url):
    print(f"XML indiriliyor: {url}")
    response = requests.get(url)
    response.raise_for_status()
    print(f"XML başarıyla indirildi. Boyut: {len(response.content)} bytes")
    
    # İlk 1000 karakteri göster
    content_str = response.content.decode('utf-8')
    print(f"İlk 1000 karakter:")
    print(content_str[:1000])
    
    return response.content

def convert_and_save_xml(source_xml_content, output_filename="baciodeneme.xml"):
    # Kaynak XML'i parse et
    root = ET.fromstring(source_xml_content)
    print(f"XML parse edildi. Kök element: {root.tag}")
    
    # Yeni kök oluştur
    new_root = ET.Element("products")

    # Her ürün için dönüştür
    products = root.findall(".//product")
    print(f"Toplam {len(products)} ürün bulundu")
    
    for i, product in enumerate(products, 1):
        print(f"\n--- Ürün {i} dönüştürülüyor ---")
        
        # İlk ürünün tüm alt elementlerini göster
        if i == 1:
            print("İlk ürünün alt elementleri:")
            for child in product:
                print(f"  - {child.tag}: {child.text}")
        
        new_product = ET.SubElement(new_root, "product")
        
        # <id>
        product_id = product.findtext("id") or str(i)
        print(f"  ID: {product_id}")
        ET.SubElement(new_product, "id").text = product_id
        
        # <productCode>
        sku = product.findtext("sku") or ""
        print(f"  SKU: {sku}")
        ET.SubElement(new_product, "productCode").text = sku.strip()
        
        # <barcode>
        ET.SubElement(new_product, "barcode").text = ""
        
        # <main_category>
        ET.SubElement(new_product, "main_category").text = "İÇ GİYİM"
        
        # <top_category>
        categories = product.findtext("categories") or ""
        print(f"  Categories: {categories}")
        ET.SubElement(new_product, "top_category").text = categories.strip()
        
        # <sub_category>
        ET.SubElement(new_product, "sub_category").text = categories.strip()
        
        # <sub_category_>
        ET.SubElement(new_product, "sub_category_").text = ""
        
        # <categoryID>
        ET.SubElement(new_product, "categoryID").text = "44"
        
        # <category>
        main_cat = "İÇ GİYİM"
        top_cat = categories.strip()
        category_text = f"{main_cat} >>> {top_cat}"
        ET.SubElement(new_product, "category").text = category_text
        
        # <active>
        ET.SubElement(new_product, "active").text = "1"
        
        # <brandID>
        ET.SubElement(new_product, "brandID").text = "2"
        
        # <brand>
        ET.SubElement(new_product, "brand").text = "BACIO"
        
        # <name>
        title = product.findtext("title") or ""
        print(f"  Title: {title}")
        ET.SubElement(new_product, "name").text = title.strip()
        
        # <description>
        description = product.findtext("description") or ""
        print(f"  Description length: {len(description)}")
        ET.SubElement(new_product, "description").text = description.strip()
        
        # <variants>
        variants_elem = ET.SubElement(new_product, "variants")
        variations = product.find("variations")
        first_price = "0.00"
        first_special_price = "0.00"
        
        if variations is not None:
            variation_count = len(variations.findall("variation"))
            print(f"  Variations found: {variation_count}")
            for i, variation in enumerate(variations.findall("variation")):
                variant_elem = ET.SubElement(variants_elem, "variant")
                ET.SubElement(variant_elem, "name1").text = variation.findtext("variationname1") or "Renk"
                ET.SubElement(variant_elem, "value1").text = variation.findtext("variationvalue1") or ""
                ET.SubElement(variant_elem, "name2").text = variation.findtext("variationname2") or "Beden"
                ET.SubElement(variant_elem, "value2").text = variation.findtext("variationvalue2") or ""
                ET.SubElement(variant_elem, "quantity").text = variation.findtext("variationqty") or "0"
                ET.SubElement(variant_elem, "barcode").text = ""
                
                # İlk variation'dan fiyatları al
                if i == 0:
                    first_price = variation.findtext("price") or "0.00"
                    first_special_price = variation.findtext("special_price") or "0.00"
        else:
            print("  No variations found")
        
        # <image1>, <image2>, <image3>
        images = product.find("images")
        if images is not None:
            img_items = images.findall("image")
            print(f"  Images found: {len(img_items)}")
            for idx in range(3):
                img_elem = ET.SubElement(new_product, f"image{idx+1}")
                if idx < len(img_items):
                    img_elem.text = (img_items[idx].text or "").strip()
                else:
                    img_elem.text = ""
        else:
            print("  No images found")
            for idx in range(3):
                ET.SubElement(new_product, f"image{idx+1}").text = ""
        
        # <listPrice>
        print(f"  Price: {first_price}")
        ET.SubElement(new_product, "listPrice").text = first_price
        
        # <price>
        print(f"  Special Price: {first_special_price}")
        ET.SubElement(new_product, "price").text = first_special_price
        
        # <tax>
        ET.SubElement(new_product, "tax").text = "0.1"
        
        # <currency>
        ET.SubElement(new_product, "currency").text = "TRY"
        
        # <desi>
        ET.SubElement(new_product, "desi").text = "1"
        
        # <quantity>
        total_qty = product.findtext("total_qty") or "0"
        print(f"  Total Qty: {total_qty}")
        ET.SubElement(new_product, "quantity").text = total_qty

    # Masaüstü yolu
    desktop = Path.home() / "Desktop"
    output_path = desktop / output_filename

    # XML'i kaydet
    tree = ET.ElementTree(new_root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"\nXML başarıyla kaydedildi: {output_path}")

def main():
    url = "https://bacioicgiyim.com.tr/priodcutsxml/products.xml"
    try:
        xml_content = download_xml(url)
        convert_and_save_xml(xml_content)
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main()
