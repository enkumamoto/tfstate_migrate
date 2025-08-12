import os
import glob
import re
from azure.storage.blob import BlobServiceClient


def find_terraform_states():
    """Encontra todos os arquivos terraform.tfstate"""
    current_dir = os.getcwd()
    print(f"Diretório atual: {current_dir}")

    tfstate_files = glob.glob("**/terraform.tfstate", recursive=True)
    return tfstate_files


def extract_numeric_directories(tfstate_files):
    """Extrai diretórios que iniciam com números"""
    numeric_dirs = set()

    for file_path in tfstate_files:
        dir_path = os.path.dirname(file_path)
        path_parts = dir_path.split(os.sep)

        for part in path_parts:
            if re.match(r'^\d', part):
                numeric_dirs.add(part)
                print(f"Diretório numérico encontrado: {part}")

    return list(numeric_dirs)


def validate_connection_string(connection_string):
    """Valida se a connection string está configurada"""
    if not connection_string or connection_string == "sua_connection_string_aqui":
        print("❌ ERRO: Connection string não configurada!")
        print(
            "Por favor, configure a CONNECTION_STRING com sua string de conexão do Azure.")
        return False
    return True


def create_blob_directories(connection_string, container_name, directory_list):
    """Cria diretórios no Azure Blob Storage"""
    try:
        if not validate_connection_string(connection_string):
            return False

        print(f"\n🔄 Conectando ao Azure Blob Storage...")
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string)

        # Testa conexão
        try:
            containers = list(blob_service_client.list_containers())
            print(
                f"✅ Conexão estabelecida. Containers encontrados: {len(containers)}")
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False

        # Verifica se o container existe
        try:
            container_client = blob_service_client.get_container_client(
                container_name)
            container_client.get_container_properties()
            print(f"✅ Container '{container_name}' encontrado")
        except Exception as e:
            print(f"❌ Container '{container_name}' não encontrado: {e}")
            return False

        return True

    except Exception as e:
        print(f"❌ Erro geral ao acessar Blob Storage: {e}")
        return False


def upload_tfstate_files(connection_string, container_name, tfstate_files):
    """Upload dos arquivos terraform.tfstate para o Azure Blob Storage"""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string)

        success_count = 0
        total_files = len(tfstate_files)

        print(
            f"\n📤 Iniciando upload de {total_files} arquivos terraform.tfstate...")

        for i, file_path in enumerate(tfstate_files, 1):
            try:
                # Extrai o nome do diretório do caminho
                directory_name = os.path.dirname(file_path)

                # Define o caminho no Blob Storage
                blob_name = f"{directory_name}/terraform.tfstate"

                # Verifica se o arquivo existe localmente
                if not os.path.exists(file_path):
                    print(
                        f"❌ [{i:2d}/{total_files}] Arquivo não encontrado: {file_path}")
                    continue

                # Lê o arquivo local
                with open(file_path, 'rb') as data:
                    blob_client = blob_service_client.get_blob_client(
                        container=container_name,
                        blob=blob_name
                    )

                    # Faz o upload
                    blob_client.upload_blob(data, overwrite=True)

                    # Verifica o tamanho do arquivo
                    file_size = os.path.getsize(file_path)
                    file_size_kb = file_size / 1024

                    print(
                        f"✅ [{i:2d}/{total_files}] {file_path} → {blob_name} ({file_size_kb:.1f} KB)")
                    success_count += 1

            except Exception as e:
                print(
                    f"❌ [{i:2d}/{total_files}] Erro ao fazer upload de '{file_path}': {e}")

        print(f"\n📊 Resumo do Upload:")
        print(f"   ✅ Sucessos: {success_count}/{total_files}")
        print(f"   ❌ Falhas: {total_files - success_count}/{total_files}")

        return success_count > 0

    except Exception as e:
        print(f"❌ Erro geral no upload: {e}")
        return False


def list_uploaded_files(connection_string, container_name):
    """Lista os arquivos que foram enviados para o Blob Storage"""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string)
        container_client = blob_service_client.get_container_client(
            container_name)

        print(f"\n📋 Arquivos no container '{container_name}':")

        blobs = list(container_client.list_blobs())
        tfstate_blobs = [
            blob for blob in blobs if blob.name.endswith('terraform.tfstate')]

        if tfstate_blobs:
            for i, blob in enumerate(tfstate_blobs, 1):
                size_kb = blob.size / 1024 if blob.size else 0
                print(f"   {i:2d}. {blob.name} ({size_kb:.1f} KB)")
        else:
            print("   Nenhum arquivo terraform.tfstate encontrado")

        return len(tfstate_blobs)

    except Exception as e:
        print(f"❌ Erro ao listar arquivos: {e}")
        return 0


def main():
    # 🔧 CONFIGURE AQUI SUA CONNECTION STRING
    CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=mrttfstatedev;AccountKey=306XvGE4zq3+oqCIu52gxp5CAGwHi20NdaHyUuR10PhHTZKkub5Y97/hqoPxIZioLDEPgYDixf9L+ASt7RUdjg==;EndpointSuffix=core.windows.net"
    CONTAINER_NAME = "mrttfstate"

    print("🚀 Iniciando migração completa de tfstate para Azure Blob Storage...")

    # 1. Encontrar arquivos terraform.tfstate
    tfstate_files = find_terraform_states()

    if not tfstate_files:
        print("❌ Nenhum arquivo terraform.tfstate encontrado")
        return

    print(f"\n📁 Arquivos encontrados:")
    for file in tfstate_files:
        print(f"  - {file}")

    # 2. Extrair diretórios que iniciam com números
    numeric_directories = extract_numeric_directories(tfstate_files)

    if not numeric_directories:
        print("\n❌ Nenhum diretório iniciado por número encontrado")
        return

    # 3. Exibir lista ordenada
    numeric_directories.sort()
    print(
        f"\n📋 Diretórios numéricos encontrados ({len(numeric_directories)}):")
    for i, dir_name in enumerate(numeric_directories, 1):
        print(f"  {i:2d}. {dir_name}")

    # 4. Validar conexão com Azure
    if not create_blob_directories(CONNECTION_STRING, CONTAINER_NAME, numeric_directories):
        print("\n💥 Falha na conexão com Azure. Abortando...")
        return

    # 5. Fazer upload dos arquivos terraform.tfstate
    if upload_tfstate_files(CONNECTION_STRING, CONTAINER_NAME, tfstate_files):
        print("\n🎉 Upload concluído!")

        # 6. Listar arquivos enviados para confirmação
        uploaded_count = list_uploaded_files(CONNECTION_STRING, CONTAINER_NAME)

        if uploaded_count > 0:
            print(f"\n🎯 Migração concluída com sucesso!")
            print(
                f"   📤 {uploaded_count} arquivos terraform.tfstate migrados para Azure")
        else:
            print("\n⚠️  Migração concluída, mas nenhum arquivo confirmado no Azure")
    else:
        print("\n💥 Falha no upload dos arquivos!")


if __name__ == "__main__":
    main()
