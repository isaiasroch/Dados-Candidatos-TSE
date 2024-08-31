import requests
import zipfile
import os


urls = [
    "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand_complementar/consulta_cand_complementar_2024.zip",
    "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2024.zip",
    "https://cdn.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_2024.zip",
    "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_coligacao/consulta_coligacao_2024.zip",
    "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_vagas/consulta_vagas_2024.zip",
    "https://cdn.tse.jus.br/estatistica/sead/odsele/motivo_cassacao/motivo_cassacao_2024.zip",
    "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/rede_social_candidato_2024.zip"
]


output_dir = "db/bronze/"  

# Cria os diretórios para as camadas bronze e prata (se não existirem)
os.makedirs(output_dir, exist_ok=True)

def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # Tamanho do bloco de download em bytes
    progress_bar = 0

    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar += len(data)
            file.write(data)
            done = int(50 * progress_bar / total_size)
            print(f"\r[{'█' * done}{'.' * (50 - done)}] {progress_bar / total_size:.2%}", end='')

    print("\nDownload completo.")

# Função para descompactar o arquivo e filtrar arquivos que contenham "BRASIL" no nome
def unzip_and_filter(zip_filename, extract_dir):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if "BRASIL" in file_info.filename:
                zip_ref.extract(file_info, extract_dir)

# Criar a pasta de destino se ela não existir
os.makedirs(output_dir, exist_ok=True)

# Processar cada URL
for url in urls:
    # Nome do arquivo ZIP temporário
    zip_file = os.path.join(output_dir, os.path.basename(url))
    
    # Baixar o arquivo ZIP com progresso
    download_file(url, zip_file)
    
    # Descompactar o arquivo na pasta especificada e filtrar apenas os arquivos com "BRASIL"
    unzip_and_filter(zip_file, output_dir)
    
    # Remover o arquivo ZIP após descompactar (opcional)
    os.remove(zip_file)

print(f"Arquivos descompactados e filtrados com sucesso em: {output_dir}")
