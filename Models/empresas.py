
# models/estabelecimentos.py
import os
import time
import uuid
from flask import session
from config import supabase

class Empresas:
    @staticmethod
    def upload_banner_empresa(file, empresa_id):
        """Faz upload do banner para o Supabase Storage, substituindo o anterior"""
        try:
            print(f"\n=== Iniciando upload de banner para empresa {empresa_id} ===")
            
            # Verifica se o arquivo existe e tem conteúdo
            if not file or file.filename == '':
                print("Erro: Nenhum arquivo fornecido ou nome de arquivo vazio")
                return None, "Nenhum arquivo fornecido"

            # Mostra informações do arquivo
            file.seek(0, 2)  # Vai para o final do arquivo
            file_size = file.tell()
            file.seek(0)  # Volta ao início
            print(f"Arquivo recebido: {file.filename}, Tamanho: {file_size} bytes, Tipo: {file.content_type}")

            # 1. Busca dados atuais da empresa
            print("\n1. Buscando dados atuais da empresa...")
            empresa_response = supabase.table('empresas').select('banner_imagem').eq('id', empresa_id).execute()
            empresa_data = empresa_response.data[0] if empresa_response.data else None
            print(f"Dados da empresa: {empresa_data}")
            
            # 2. Remove o banner antigo se existir
            if empresa_data and empresa_data.get('banner_imagem'):
                try:
                    old_url = empresa_data['banner_imagem']
                    print(f"\n2. Removendo banner antigo: {old_url}")
                    old_filename = old_url.split('/')[-1].split('?')[0]
                    print(f"Nome do arquivo antigo: {old_filename}")
                    delete_response = supabase.storage.from_('bannerempresas').remove([old_filename])
                    print(f"Resposta da remoção: {delete_response}")
                except Exception as e:
                    print(f"Erro ao remover banner antigo: {str(e)}")

            # 3. Validação do novo arquivo
            print("\n3. Validando arquivo...")
            ext = os.path.splitext(file.filename)[1].lower()
            print(f"Extensão do arquivo: {ext}")
            if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
                return None, "Formato de imagem inválido (use JPG, PNG, GIF ou WEBP)"

            # 4. Gera novo nome de arquivo
            filename = f"banner_{empresa_id}_{uuid.uuid4()}{ext}"
            print(f"\n4. Nome do arquivo gerado: {filename}")

            # 5. Upload do novo banner
            print("\n5. Fazendo upload para o Supabase Storage...")
            file_content = file.read()
            print(f"Tamanho do conteúdo a ser enviado: {len(file_content)} bytes")
            
            upload_response = supabase.storage.from_('bannerempresas').upload(
                file=file_content,
                path=filename,
                file_options={
                    "content-type": file.content_type,
                    "cache-control": "public, max-age=31536000"
                }
            )
            print(f"Resposta do upload: {upload_response}")

            if hasattr(upload_response, 'error'):
                print(f"Erro no upload: {upload_response.error}")
                return None, f"Erro no upload: {upload_response.error}"

            # 6. Gera URL pública
            new_url = supabase.storage.from_('bannerempresas').get_public_url(filename)
            print(f"\n6. URL pública gerada: {new_url}")
            
            # 7. Atualiza no banco de dados
            print("\n7. Atualizando banco de dados...")
            update_response = supabase.table('empresas').update(
                {'banner_imagem': new_url}
            ).eq('id', empresa_id).execute()
            print(f"Resposta da atualização: {update_response}")
            
            if hasattr(update_response, 'error'):
                print(f"Erro ao atualizar banner: {update_response.error}")
                return None, f"Erro ao atualizar banner: {update_response.error}"

            # 8. Retorna URL com timestamp para evitar cache
            final_url = f"{new_url}?t={int(time.time())}"
            print(f"\n=== Upload concluído com sucesso! URL final: {final_url} ===")
            return final_url, None

        except Exception as e:
            print(f"\n=== ERRO DURANTE UPLOAD ===")
            print(f"Tipo do erro: {type(e).__name__}")
            print(f"Mensagem: {str(e)}")
            print(f"Traceback completo:")
            import traceback
            traceback.print_exc()
            return None, f"Erro interno: {str(e)}"
        finally:
            file.seek(0)

    @staticmethod
    def criar_empresas(dados_empresa):
        try:
            response = supabase.table('empresas').insert(dados_empresa).execute()
            return response.data
        except Exception as e:
            print(f"Erro ao cadastrar empresa: {e}")
            return None

    @staticmethod
    def buscar_empresas():
        try:
            response = supabase.table('empresas').select('*').execute()
            print(response)
            return response.data
        except Exception as e:
            print(f"Erro ao buscar empresas: {e}")
            return None
            
    @staticmethod
    def buscar_empresa_id(id):
        try:
            response = supabase.table('empresas').select("*").eq("id", id).execute()
            print(response)
            return response.data[0]
        except Exception as e:
            print(f"Erro ao buscar empresa: {e}")
            return None
        
    @staticmethod
    def buscar_empresas_por_usuario(usuario_id):
        try:
            response = supabase.table('empresas').select("*").eq("usuario_id", usuario_id).execute()
            print(response)
            return response.data
        except Exception as e:
            print(f"Erro ao buscar empresas por usuário: {e}")
            return None

    @staticmethod
    def atualizar_empresa(empresa_id, dados_atualizados):
        try:
            response = supabase.table('empresas').update(dados_atualizados).eq('id', empresa_id).execute()
            return response.data[0] if response.data else None, None
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def buscar_empresa_categoria(categoria):
        try:
            response = supabase.table('empresas').select('*').eq("categoria", categoria).execute()
            return response.data
        except Exception as e:
            return None, str(e)