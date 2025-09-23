# 🚀 Migração de Terraform State para Azure Blob Storage

Este projeto automatiza a **migração de arquivos `terraform.tfstate`** encontrados localmente para um **container no Azure Blob Storage**, garantindo que os estados do Terraform fiquem centralizados e seguros.

## 📋 Funcionalidades

- 🔍 Localiza recursivamente todos os arquivos `terraform.tfstate`.
- 🧩 Identifica diretórios que começam com números (útil para organizar ambientes/projetos).
- 🔑 Valida a **connection string** do Azure Blob Storage.
- ☁️ Cria/verifica a existência do container no Azure.
- 📤 Realiza o **upload dos arquivos `terraform.tfstate`** encontrados.
- 📊 Exibe um resumo da migração (sucessos e falhas).
- 📋 Lista os arquivos enviados para o container do Azure.

## ⚙️ Pré-requisitos

- Python **3.8+**
- Conta de **Azure Storage** com **Blob Storage** habilitado.
- Container criado previamente no Blob Storage.
- Biblioteca `azure-storage-blob` instalada:

```bash
pip install azure-storage-blob
🔧 Configuração
No arquivo main.py, edite as seguintes variáveis no método main():

python
Copiar código
CONNECTION_STRING = "sua_connection_string_aqui"
CONTAINER_NAME = "nome_do_container"
⚠️ Atenção: nunca versione sua connection string em repositórios públicos.

▶️ Como executar
Clone este repositório:

bash
Copiar código
git clone https://github.com/seu-repo/terraform-tfstate-migrator.git
cd terraform-tfstate-migrator
Execute o script:

bash
Copiar código
python main.py
Acompanhe a saída no terminal para ver:

Arquivos encontrados

Diretórios numéricos

Status da conexão com o Azure

Progresso e resumo do upload

Lista final dos arquivos no container

📊 Exemplo de saída
bash
Copiar código
🚀 Iniciando migração completa de tfstate para Azure Blob Storage...

📁 Arquivos encontrados:
  - 101/projectA/terraform.tfstate
  - 202/projectB/terraform.tfstate

📋 Diretórios numéricos encontrados (2):
   1. 101
   2. 202

🔄 Conectando ao Azure Blob Storage...
✅ Conexão estabelecida. Containers encontrados: 3
✅ Container 'mrttfstate' encontrado

📤 Iniciando upload de 2 arquivos terraform.tfstate...
✅ [ 1/2] 101/projectA/terraform.tfstate → 101/projectA/terraform.tfstate (12.4 KB)
✅ [ 2/2] 202/projectB/terraform.tfstate → 202/projectB/terraform.tfstate (15.1 KB)

📊 Resumo do Upload:
   ✅ Sucessos: 2/2
   ❌ Falhas: 0/2

📋 Arquivos no container 'mrttfstate':
   1. 101/projectA/terraform.tfstate (12.4 KB)
   2. 202/projectB/terraform.tfstate (15.1 KB)

🎯 Migração concluída com sucesso!
📤 2 arquivos terraform.tfstate migrados para Azure
📌 Estrutura do Projeto
bash
Copiar código
.
├── main.py         # Script principal da migração
├── README.md       # Este guia
🚨 Observações
Boa prática: use variáveis de ambiente ou Azure Key Vault para armazenar a connection string.

Caso o container não exista, o script abortará a execução.

Apenas arquivos chamados exatamente terraform.tfstate serão migrados.
