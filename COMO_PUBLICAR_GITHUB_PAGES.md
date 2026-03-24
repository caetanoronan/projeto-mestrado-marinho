# 🚀 Como Publicar no GitHub Pages

## Passo 1: Criar Repositório no GitHub

1. Acesse [GitHub](https://github.com) e faça login
2. Clique no botão **"New"** (ou ícone +) para criar novo repositório
3. Preencha:
   - **Repository name:** `projeto-mestrado-marinho` (ou nome de sua escolha)
   - **Description:** "Projeto de Mestrado - Biodiversidade e Invasões Marinhas em Ilhas de SC"
   - **Visibility:** Public (para GitHub Pages funcionar gratuitamente)
   - ❌ NÃO marque "Add a README file" (já temos um)
4. Clique em **"Create repository"**

## Passo 2: Conectar Repositório Local ao GitHub

Após criar o repositório, o GitHub mostrará comandos. Use estes no terminal:

```powershell
# Adicionar o remoto (substitua SEU-USUARIO pelo seu username do GitHub)
git remote add origin https://github.com/SEU-USUARIO/projeto-mestrado-marinho.git

# Renomear branch para main (padrão do GitHub)
git branch -M main

# Enviar os arquivos para o GitHub
git push -u origin main
```

## Passo 3: Ativar GitHub Pages

1. No repositório do GitHub, vá em **Settings** (Configurações)
2. No menu lateral esquerdo, clique em **Pages**
3. Em **Source**, selecione:
   - **Branch:** `main`
   - **Folder:** `/ (root)`
4. Clique em **Save**
5. Aguarde 1-2 minutos

## Passo 4: Acessar seu Site

Após a publicação, o GitHub mostrará a URL:

```
https://SEU-USUARIO.github.io/projeto-mestrado-marinho/
```

## ✨ Páginas Disponíveis

- **Página inicial:** `https://SEU-USUARIO.github.io/projeto-mestrado-marinho/`
- **Apresentação completa:** `https://SEU-USUARIO.github.io/projeto-mestrado-marinho/Apresentacao_Projeto_Mestrado.html`
- **Mapa interativo:** `https://SEU-USUARIO.github.io/projeto-mestrado-marinho/Mapas_Gerados/mapa_interativo.html`

## 🔄 Atualizações Futuras

Sempre que fizer alterações nos arquivos:

```powershell
# Adicionar mudanças
git add .

# Criar commit
git commit -m "Descrição das mudanças"

# Enviar para GitHub
git push
```

Aguarde 1-2 minutos e as mudanças aparecerão no site.

## ✅ Checklist Rápido de Publicação (evitar divergência)

Antes de publicar, valide estes pontos:

1. **Arquivos espelhados**
- Se a página existe em `raiz` e em `docs/`, aplique a mesma alteração nos dois arquivos.
- Exemplo: `Apresentacao_Macrofitas_Publica.html`, `Apresentacao_Macrofitas_Publica.en.html`, `Apresentacao_Macrofitas_Publica.es.html`.

2. **Ordem/estrutura do conteúdo**
- Confirme no HTML a ordem dos blocos principais (título, texto introdutório, CTA, imagens).
- Evite mover conteúdo apenas em um idioma.

3. **Commit cirúrgico**
- Faça commit só dos arquivos da tarefa para evitar subir mudanças não relacionadas.

```powershell
git add -- "arquivo1" "arquivo2"
git commit -m "Descrição objetiva da mudança"
git push origin main
```

4. **Validação pós-push (sem cache)**
- Abra a URL com query string para evitar cache local:

```text
https://SEU-USUARIO.github.io/projeto-mestrado-marinho/sua_pagina.html?v=TIMESTAMP
```

5. **Se atualizar só um idioma**
- Verifique imediatamente PT/EN/ES para manter consistência visual e de navegação.

6. **Se o GitHub Pages parecer atrasado**
- Aguarde 1-5 minutos.
- Faça `Ctrl+F5` ou teste em aba anônima.
- Se necessário, faça um novo commit pequeno para forçar atualização.

## 📱 Compartilhar

Você pode compartilhar os links diretos:
- Com o Prof. Paulo Antunes Horta
- No currículo Lattes
- Em submissões de projetos
- Em apresentações

## ⚠️ Importante

- O repositório está configurado como **público** (necessário para GitHub Pages gratuito)
- Arquivos sensíveis estão no `.gitignore` (não serão publicados)
- O PDF do edital não foi incluído (privacidade)

## 🎨 Personalização

Para alterar a URL do README.md depois de publicar:

1. Edite `README.md`
2. Substitua `seu-usuario` pelo seu username real do GitHub
3. Faça commit e push das mudanças

## 💡 Dicas

- **Custom Domain:** Se tiver um domínio próprio, pode configurar em Settings > Pages
- **Analytics:** Adicione Google Analytics para ver visitantes
- **SEO:** Os meta tags já estão configurados para busca

---

**Resultado Final:** Um site profissional e interativo para apresentar seu projeto de mestrado! 🎉
