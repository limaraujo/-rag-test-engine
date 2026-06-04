Instalar o uv:
- curl -Ls https://astral.sh/uv/install.sh | sh

Instalar dependências:
- uv add nome-dependencia
- uv add -r requirements.txt

Rodar o projeto:
- uv run python main.py

Instalar o typst para o relatório:
- cargo install typst-cli

Se não tiver cargo/rustup:
1. Instale o Rust oficial: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
2. Recarregue o ambiente: source ~/.cargo/env
3. Atualize: rustup update
4. Instale o typst: cargo install typst-cli

Extensão vs-code:
- Tinymist Typst

Compilar o pdf em tempo real:
- typst watch --font-path relatorio/fonts relatorio/main.typ
