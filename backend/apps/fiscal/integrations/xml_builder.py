from xml.etree.ElementTree import Element, SubElement, tostring


class NFeXmlBuilder:
    def build(self, nota):
        root = Element("NFe")
        inf = SubElement(root, "infNFe")
        SubElement(inf, "numero").text = str(nota.numero)
        SubElement(inf, "serie").text = str(nota.serie)
        SubElement(inf, "ambiente").text = nota.ambiente
        SubElement(inf, "emitente").text = nota.emitente.cnpj
        destinatario = nota.destinatario_cliente or nota.destinatario_fornecedor
        SubElement(inf, "destinatario").text = destinatario.documento if destinatario else ""
        itens = SubElement(inf, "itens")
        for item in nota.itens.all():
            item_node = SubElement(itens, "item")
            SubElement(item_node, "produto").text = item.produto.sku
            SubElement(item_node, "ncm").text = item.ncm
            SubElement(item_node, "cfop").text = item.cfop
            SubElement(item_node, "quantidade").text = str(item.quantidade)
            SubElement(item_node, "valorTotal").text = str(item.valor_total)
        return tostring(root, encoding="unicode")
