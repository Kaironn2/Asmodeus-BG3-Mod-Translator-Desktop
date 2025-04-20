# 🎮 BG3 Mod Translator - Desktop App

## 🇮🇹 English

### 📟 Short Description

Desktop application to translate Baldur's Gate 3 mods. Uses LSLib to handle `.pak` files, translates `.xml` localization files using OpenAI or Google Translator, and stores translations in a SQLite database. Built with PySide6.

### 📄 Long Description

This desktop app simplifies the process of translating mods for **Baldur's Gate 3**. It automates the extraction, translation, and repacking of mod files using **LSLib** to handle `.pak` files.

The app supports multiple translation methods:

- Searches translations in a local **SQLite3** dictionary to avoid duplicate work.
- If no exact match is found, uses **RapidFuzz** to find similar entries in the database and send them as context to the **OpenAI API** (if provided).
- Alternatively, uses the **free Google Translator** (less accurate), with support for paid API key use as well.
- Manual translations can also be performed via the interface.

### 🔄 Process Flow

1. The user provides the path to a `.zip` or `.pak` file.
2. The app extracts the `.zip` if needed and then unpacks the `.pak` using LSLib.
3. It filters only the necessary files: `.xml` and `meta.lsx`.
4. It checks for existing translations in the database.
5. If none are found:
   - Uses fuzzy matching + AI for OpenAI translation.
   - Or translates directly via Google Translator.
6. Texts can be edited manually via the UI.
7. The result can be exported either as:
   - `.xml` files for Mod.io projects.
   - Fully zipped `.pak` for Nexus Mods.

The interface is developed with **PySide6**, and this desktop version is a fast-track implementation of a more complete **web-based version** being built using **Django** and **Vue.js**.

### 📚 Acknowledgements

This project uses [LSLib](https://github.com/Norbyte/lslib) by **Norbyte** for handling `.pak` files in Baldur's Gate 3.  
LSLib is an open-source project licensed under the MIT License.

---

## 🇧🇷 Português

### 📟 Descrição Curta

Aplicativo desktop para traduzir mods de Baldur's Gate 3. Utiliza LSLib para lidar com arquivos `.pak`, traduz arquivos `.xml` com OpenAI ou Google Translator e armazena traduções em banco de dados SQLite. Interface feita com PySide6.

### 📄 Descrição Longa

Este app desktop facilita o processo de tradução de mods do **Baldur's Gate 3**, automatizando a extração, tradução e reempacotamento dos arquivos usando a **LSLib** para tratar os `.pak`.

A tradução dos textos pode ser feita de diferentes formas:

- Procura por traduções no dicionário local (SQLite3) para evitar retrabalho.
- Se não encontrar, usa o **RapidFuzz** para buscar exemplos semelhantes e envia com contexto para a **API da OpenAI** (caso tenha chave).
- Alternativamente, usa o **Google Translator gratuito** (menos preciso), com suporte à versão paga via API key.
- Também é possível traduzir manualmente direto pela interface.

### 🔄 Fluxo do Processo

1. O usuário fornece o caminho para um `.zip` ou `.pak`.
2. O app descompacta o `.zip` (se houver) e depois extrai o `.pak` com a LSLib.
3. Filtra apenas os arquivos necessários: `.xml` e `meta.lsx`.
4. Verifica se já existe tradução no banco de dados.
5. Se não houver:
   - Usa fuzzy match + IA via OpenAI.
   - Ou traduz direto com o Google Translator.
6. Permite edição manual dos textos via interface.
7. Exporta os arquivos em dois formatos:
   - `.xml`, para uso em projetos da Mod.io.
   - `.pak` compactado, pronto para o Nexus Mods.

A interface é feita com **PySide6**. Esta versão desktop é uma implementação inicial de um projeto maior e futuro: uma aplicação web feita em **Django** e **Vue.js**.

### 📚 Agradecimentos

Este projeto utiliza o [LSLib](https://github.com/Norbyte/lslib), desenvolvido por **Norbyte**, para manipular arquivos `.pak` do Baldur's Gate 3.  
O LSLib é um projeto open-source licenciado sob a licença MIT.
