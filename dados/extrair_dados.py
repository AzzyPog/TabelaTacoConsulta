import pypdfium2 as pdfium
import json
import re

def extrair_taco():
    alimentos = []
    

    padrao = re.compile(
        r'^(\d+)\s+(.+?)\s+([\d,]+|NA|Tr|\*)\s+([\d,]+|NA|Tr|\*)\s+([\d,]+|NA|Tr|\*)\s+'
        r'([\d,]+|NA|Tr|\*)\s+([\d,]+|NA|Tr|\*)\s+([\d,]+|NA|Tr|\*)\s+([\d,]+|NA|Tr|\*)\s+'
        r'([\d,]+|NA|Tr|\*)\s+([\d,]+|NA|Tr|\*)\s+([\d,]+|NA|Tr|\*)\s+([\d,]+|NA|Tr|\*)$'
    )

    def parse_num(val):
        if val in ('NA', '*', '', None): return None
        if val == 'Tr': return 0.0 
        return float(val.replace(',', '.'))

    print("Lendo o PDF e extraindo dados...")
    

    pdf = pdfium.PdfDocument("tabela_taco_apenas_dados.pdf")
    for i in range(len(pdf)):
        pagina = pdf[i]
        texto = pagina.get_textpage().get_text_range()
        if not texto: continue
            
        for linha in texto.splitlines():
            match = padrao.match(linha.strip())
            if match:
                energia_1 = parse_num(match.group(4))
                energia_2 = parse_num(match.group(5))
                
                kcal = None
                if energia_1 is not None and energia_2 is not None:
                    kcal = min(energia_1, energia_2)
                elif energia_1 is not None:
                    kcal = energia_1

                descricao = match.group(2).strip()
                estado = 'cru'
                desc_lower = descricao.lower()
                if 'cozido' in desc_lower or 'cozida' in desc_lower: estado = 'cozido'
                elif 'assado' in desc_lower or 'assada' in desc_lower: estado = 'assado'
                elif 'frito' in desc_lower or 'frita' in desc_lower: estado = 'frito'
                elif 'grelhado' in desc_lower or 'grelhada' in desc_lower: estado = 'grelhado'

                alimentos.append({
                    "codigo": int(match.group(1)),
                    "descricao": descricao,
                    "estado_preparo": estado,
                    "nutrientes": {
                        "energia_kcal": kcal,
                        "proteina_g": parse_num(match.group(6)),
                        "lipideos_g": parse_num(match.group(7)),
                        "carboidrato_g": parse_num(match.group(9)),
                        "fibra_g": parse_num(match.group(10))
                    }
                })
    
    with open('taco.json', 'w', encoding='utf-8') as f:
        json.dump(alimentos, f, ensure_ascii=False, indent=2)
        
    print(f"Extração concluída com sucesso! {len(alimentos)} itens salvos em taco.json.")

if __name__ == '__main__':
    extrair_taco()