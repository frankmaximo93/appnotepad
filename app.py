import tkinter as tk
from tkinter import messagebox, scrolledtext, font, ttk, filedialog
import json
import os
from PIL import Image, ImageTk, UnidentifiedImageError
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Nome do arquivo JSON
ARQUIVO_NOTAS = 'minhas_notas_gui.json'

notas = []
indice_nota_editando = None

def carregar_notas():
    # ... (função carregar_notas - sem alterações) ...
    global notas
    try:
        if os.path.exists(ARQUIVO_NOTAS):
            with open(ARQUIVO_NOTAS, 'r', encoding='utf-8') as f:
                try:
                    notas = json.load(f)
                    print("Notas carregadas do arquivo:", ARQUIVO_NOTAS)
                except json.JSONDecodeError:
                    notas = []
                    print("Erro ao decodificar JSON. Iniciando com notas vazias.")
        else:
            notas = []
            print("Arquivo de notas não encontrado. Iniciando com notas vazias.")
    except Exception as e:
        print(f"Erro ao carregar notas: {e}")
        notas = []
    return notas

def salvar_notas():
    # ... (função salvar_notas - sem alterações) ...
    global notas
    try:
        with open(ARQUIVO_NOTAS, 'w', encoding='utf-8') as f:
            json.dump(notas, f, indent=4, ensure_ascii=False)
        print("Notas salvas no arquivo:", ARQUIVO_NOTAS)
    except Exception as e:
        print(f"Erro ao salvar notas: {e}")

def salvar_nota_gui():
    # ... (função salvar_nota_gui - sem alterações) ...
    global notas, indice_nota_editando
    titulo = titulo_entry.get()
    categoria = categoria_entry.get()
    conteudo = conteudo_text.get("1.0", tk.END).strip()

    if not titulo:
        messagebox.showerror("Erro", "Título não pode estar vazio.")
        return

    if indice_nota_editando is not None:
        notas[indice_nota_editando] = {"titulo": titulo, "categoria": categoria, "conteudo": conteudo}
        indice_nota_editando = None
        botao_salvar.config(text="Salvar Nota")
        messagebox.showinfo("Sucesso", "Nota editada e salva!")
    else:
        nova_nota = {"titulo": titulo, "categoria": categoria, "conteudo": conteudo}
        notas.append(nova_nota)
        messagebox.showinfo("Sucesso", "Nova nota salva!")

    salvar_notas()
    listar_notas_gui()
    nova_nota_gui()

def listar_notas_gui():
    """Lista todas as notas no listbox."""
    listbox_notas.delete(0, tk.END)
    if notas:
        for i, nota in enumerate(notas):
            listbox_notas.insert(tk.END, f"{i + 1}. {nota['titulo']} ({nota['categoria']})")

def listar_notas_por_categoria_gui():
    # ... (função listar_notas_por_categoria_gui - sem alterações) ...
    categoria_pesquisa = categoria_pesquisa_entry.get().strip().lower()
    if not categoria_pesquisa:
        messagebox.showerror("Erro", "Digite uma categoria para listar.")
        return

    listbox_notas.delete(0, tk.END)
    notas_encontradas = [nota for nota in notas if nota['categoria'].lower() == categoria_pesquisa]
    if not notas_encontradas:
        messagebox.showinfo("Informação", f"Nenhuma nota em '{categoria_pesquisa}'.")
    else:
        for i, nota in enumerate(notas_encontradas):
            listbox_notas.insert(tk.END, f"{i + 1}. {nota['titulo']} ({nota['categoria']})")

def visualizar_nota_gui():
    """Visualiza a nota selecionada na lista."""
    global indice_nota_editando, botao_salvar
    indice_selecionado = listbox_notas.curselection()
    if not indice_selecionado:
        messagebox.showinfo("Informação", "Selecione uma nota para visualizar.")
        return

    indice = indice_selecionado[0]
    index_nota = int(listbox_notas.get(indice).split('.')[0]) - 1
    if 0 <= index_nota < len(notas):
        nota_selecionada = notas[index_nota]
        titulo_entry.delete(0, tk.END)
        titulo_entry.insert(0, nota_selecionada['titulo'])
        categoria_entry.delete(0, tk.END)
        categoria_entry.insert(0, nota_selecionada['categoria'])
        conteudo_text.delete("1.0", tk.END)

        # Carregar conteúdo, lidando com texto e possivelmente placeholders de imagem (se implementado posteriormente)
        conteudo_text.insert(tk.END, nota_selecionada['conteudo'])

        indice_nota_editando = index_nota
        botao_salvar.config(text="Salvar Edição")
    else:
        messagebox.showerror("Erro", "Índice inválido.")

def deletar_nota_gui():
    # ... (função deletar_nota_gui - sem alterações) ...
    global notas
    indice_selecionado = listbox_notas.curselection()
    if not indice_selecionado:
        messagebox.showinfo("Informação", "Selecione uma nota para deletar.")
        return

    indice = indice_selecionado[0]
    index_nota = int(listbox_notas.get(indice).split('.')[0]) - 1
    if 0 <= index_nota < len(notas):
        nota_a_deletar = notas[index_nota]['titulo']
        confirmacao = messagebox.askyesno("Confirmação", f"Deletar nota '{nota_a_deletar}'?")
        if confirmacao:
            del notas[index_nota]
            salvar_notas()
            listar_notas_gui()
            nova_nota_gui()
            messagebox.showinfo("Sucesso", "Nota deletada!")
    else:
        messagebox.showerror("Erro", "Índice inválido.")

def buscar_nota_por_conteudo_gui():
    # ... (função buscar_nota_por_conteudo_gui - sem alterações) ...
    termo_busca = busca_entry.get().strip().lower()
    if not termo_busca:
        messagebox.showerror("Erro", "Digite algo para buscar no conteúdo.")
        return

    listbox_notas.delete(0, tk.END)
    notas_encontradas = [nota for nota in notas if termo_busca in nota['conteudo'].lower()]
    if not notas_encontradas:
        messagebox.showinfo("Informação", f"Nenhuma nota com '{termo_busca}' no conteúdo.")
    else:
        for i, nota in enumerate(notas_encontradas):
            listbox_notas.insert(tk.END,
                                 f"{i + 1}. {nota['titulo']} ({nota['categoria']}) - Conteúdo: '{termo_busca[:20]}...'")

def nova_nota_gui():
    # ... (função nova_nota_gui - sem alterações) ...
    global indice_nota_editando, botao_salvar
    titulo_entry.delete(0, tk.END)
    categoria_entry.delete(0, tk.END)
    conteudo_text.delete("1.0", tk.END)
    listbox_notas.selection_clear(0, tk.END)
    indice_nota_editando = None
    botao_salvar.config(text="Salvar Nota")

def aplicar_estilo(estilo):
    """Aplica estilo (negrito, itálico) ao texto selecionado."""
    try:
        inicio = conteudo_text.index("sel.first")
        fim = conteudo_text.index("sel.last")
        if inicio and fim:
            print(f"Aplicando estilo: {estilo}, Seleção: {inicio} - {fim}") # DEBUG
            fonte_atual = font.Font(conteudo_text, conteudo_text.cget("font"))
            print(f"Fonte atual ANTES da alteração: {fonte_atual.actual()}") # DEBUG

            if estilo == 'negrito':
                fonte_negrito = font.Font(weight="bold", family=fonte_atual.actual('family'), size=fonte_atual.actual('size'))
                conteudo_text.tag_config("negrito", font=fonte_negrito)
                conteudo_text.tag_add("negrito", inicio, fim)
            elif estilo == 'italico':
                fonte_italico = font.Font(slant="italic", family=fonte_atual.actual('family'), size=fonte_atual.actual('size'))
                conteudo_text.tag_config("italico", font=fonte_italico)
                conteudo_text.tag_add("italico", inicio, fim)

            fonte_depois = font.Font(conteudo_text, conteudo_text.cget("font"))
            print(f"Fonte DEPOIS da alteração: {fonte_depois.actual()}") # DEBUG
            print(f"Tags aplicadas na seleção: {conteudo_text.tag_names(inicio)}") # DEBUG

    except tk.TclError:
        pass

def alterar_tamanho_fonte(tamanho):
    """Altera o tamanho da fonte do texto selecionado."""
    try:
        inicio = conteudo_text.index("sel.first")
        fim = conteudo_text.index("sel.last")
        if inicio and fim:
            print(f"Alterando tamanho fonte para: {tamanho}, Seleção: {inicio} - {fim}") # DEBUG
            fonte_atual = font.Font(conteudo_text, conteudo_text.cget("font"))
            print(f"Fonte atual ANTES da alteração: {fonte_atual.actual()}") # DEBUG

            tag_tamanho = f"tamanho_{tamanho}"
            fonte_tamanho = font.Font(family="Arial", size=tamanho) # Force Arial
            conteudo_text.tag_config(tag_tamanho, font=fonte_tamanho)
            conteudo_text.tag_add(tag_tamanho, inicio, fim)

            fonte_depois = font.Font(conteudo_text, conteudo_text.cget("font"))
            print(f"Fonte DEPOIS da alteração: {fonte_depois.actual()}") # DEBUG
            print(f"Tags aplicadas na seleção: {conteudo_text.tag_names(inicio)}") # DEBUG

    except tk.TclError:
        pass

def inserir_imagem_com_tamanho_gui():
    """Abre diálogo para inserir imagem com tamanho personalizado."""
    dialog_tamanho_imagem = tk.Toplevel(root)
    dialog_tamanho_imagem.title("Definir Tamanho da Imagem")

    largura_label = tk.Label(dialog_tamanho_imagem, text="Largura:")
    largura_label.grid(row=0, column=0, padx=5, pady=5)
    largura_entry = tk.Entry(dialog_tamanho_imagem)
    largura_entry.grid(row=0, column=1, padx=5, pady=5)
    largura_entry.insert(0, "250")

    altura_label = tk.Label(dialog_tamanho_imagem, text="Altura:")
    altura_label.grid(row=1, column=0, padx=5, pady=5)
    altura_entry = tk.Entry(dialog_tamanho_imagem)
    altura_entry.grid(row=1, column=1, padx=5, pady=5)
    altura_entry.insert(0, "250")

    def inserir_imagem_tamanho_definido():
        """Função interna para inserir imagem com tamanho definido."""
        try:
            largura = int(largura_entry.get())
            altura = int(altura_entry.get())
            if largura <= 0 or altura <= 0:
                messagebox.showerror("Erro", "Largura e altura devem ser maiores que zero.")
                return

            arquivo_imagem = filedialog.askopenfilename(
                title="Selecionar Imagem",
                filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
            )
            if arquivo_imagem:
                try:
                    imagem_pil = Image.open(arquivo_imagem)
                    imagem_pil = imagem_pil.resize((largura, altura), Image.LANCZOS)
                    imagem_tk = ImageTk.PhotoImage(imagem_pil)

                    conteudo_text.image_object = imagem_tk
                    conteudo_text.image_create(tk.END, image=conteudo_text.image_object)
                    conteudo_text.insert(tk.END, "\n")
                    messagebox.showinfo("Informação", "Imagem inserida com sucesso!\n**Atenção:** Imagens não são salvas permanentemente neste exemplo.")
                except FileNotFoundError:
                    messagebox.showerror("Erro", "Arquivo de imagem não encontrado ou corrompido.")
                except UnidentifiedImageError:
                    messagebox.showerror("Erro", "Formato de imagem não suportado ou arquivo corrompido.")

            dialog_tamanho_imagem.destroy()

        except ValueError:
            messagebox.showerror("Erro", "Por favor, digite valores numéricos válidos para largura e altura.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir imagem: {e}")

    ok_button = tk.Button(dialog_tamanho_imagem, text="Inserir com Tamanho", command=inserir_imagem_tamanho_definido)
    ok_button.grid(row=2, column=0, columnspan=2, pady=10)

    dialog_tamanho_imagem.transient(root)
    dialog_tamanho_imagem.grab_set()
    root.wait_window(dialog_tamanho_imagem)

def inserir_imagem_gui():
    """Função principal para inserir imagem, agora chama a com diálogo."""
    inserir_imagem_com_tamanho_gui()

def salvar_nota_como_txt():
    """Salva a nota atual como um arquivo de texto."""
    titulo = titulo_entry.get()
    categoria = categoria_entry.get()
    conteudo = conteudo_text.get("1.0", tk.END).strip()

    if not titulo:
        messagebox.showerror("Erro", "Título não pode estar vazio.")
        return

    arquivo_txt = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if arquivo_txt:
        try:
            with open(arquivo_txt, 'w', encoding='utf-8') as f:
                f.write(f"Título: {titulo}\n")
                f.write(f"Categoria: {categoria}\n")
                f.write("Conteúdo:\n")
                f.write(conteudo)
            messagebox.showinfo("Sucesso", "Nota salva como arquivo de texto!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo de texto: {e}")

def salvar_nota_como_pdf():
    """Salva a nota atual como um arquivo PDF."""
    titulo = titulo_entry.get()
    categoria = categoria_entry.get()
    conteudo = conteudo_text.get("1.0", tk.END).strip()

    if not titulo:
        messagebox.showerror("Erro", "Título não pode estar vazio.")
        return

    arquivo_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if arquivo_pdf:
        try:
            c = canvas.Canvas(arquivo_pdf, pagesize=letter)
            width, height = letter

            c.drawString(100, height - 100, f"Título: {titulo}")
            c.drawString(100, height - 120, f"Categoria: {categoria}")
            c.drawString(100, height - 140, "Conteúdo:")

            text = c.beginText(100, height - 160)
            text.setFont("Helvetica", 10)
            for line in conteudo.split('\n'):
                text.textLine(line)
            c.drawText(text)

            c.save()
            messagebox.showinfo("Sucesso", "Nota salva como arquivo PDF!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo PDF: {e}")

# --- Configuração da Interface ---
root = tk.Tk()
root.title("Meu Bloco de Notas Gráfico")

# --- Frames ---
frame_principal = tk.Frame(root)
frame_principal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

frame_campos = tk.Frame(frame_principal)
frame_campos.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

frame_listagem_acoes = tk.Frame(frame_principal)
frame_listagem_acoes.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

# --- Campos de Entrada (Frame Esquerdo) ---
titulo_label = tk.Label(frame_campos, text="Título:")
titulo_label.pack(anchor=tk.NW)
titulo_entry = tk.Entry(frame_campos, width=50)
titulo_entry.pack(fill=tk.X, pady=2)

categoria_label = tk.Label(frame_campos, text="Categoria:")
categoria_label.pack(anchor=tk.NW)
categoria_entry = tk.Entry(frame_campos, width=50)
categoria_entry.pack(fill=tk.X, pady=2)

conteudo_label = tk.Label(frame_campos, text="Conteúdo:")
conteudo_label.pack(anchor=tk.NW)

# --- Frame de formatação (Abaixo de "Conteúdo") ---
frame_formatacao = tk.Frame(frame_campos)
frame_formatacao.pack(fill=tk.X, pady=5)

botao_negrito = tk.Button(frame_formatacao, text="Negrito", command=lambda: aplicar_estilo('negrito'))
botao_negrito.pack(side=tk.LEFT, padx=5)

botao_italico = tk.Button(frame_formatacao, text="Itálico", command=lambda: aplicar_estilo('italico'))
botao_italico.pack(side=tk.LEFT, padx=5)

# --- Combobox para tamanho da fonte ---
tamanhos_fonte = [8, 10, 12, 14, 16, 18, 20]
tamanho_fonte_var = tk.IntVar(value=12)
combobox_tamanho_fonte = ttk.Combobox(frame_formatacao, width=5, values=tamanhos_fonte, textvariable=tamanho_fonte_var)
combobox_tamanho_fonte.pack(side=tk.LEFT, padx=5)
combobox_tamanho_fonte.bind("<<ComboboxSelected>>", lambda event: alterar_tamanho_fonte(tamanho_fonte_var.get()))

botao_inserir_imagem = tk.Button(frame_formatacao, text="Inserir Imagem", command=inserir_imagem_gui)
botao_inserir_imagem.pack(side=tk.LEFT, padx=5)

# --- Frame de botões para salvar como txt e pdf ---
frame_botoes_salvar = tk.Frame(frame_campos)
frame_botoes_salvar.pack(anchor=tk.E, pady=5)

botao_salvar_txt = tk.Button(frame_botoes_salvar, text="Salvar como TXT", command=salvar_nota_como_txt)
botao_salvar_txt.pack(side=tk.LEFT, padx=5)

botao_salvar_pdf = tk.Button(frame_botoes_salvar, text="Salvar como PDF", command=salvar_nota_como_pdf)
botao_salvar_pdf.pack(side=tk.LEFT, padx=5)

conteudo_text = scrolledtext.ScrolledText(frame_campos, height=20, font=("Arial", 12))
conteudo_text.pack(fill=tk.BOTH, expand=True, pady=2)

frame_botoes_campos = tk.Frame(frame_campos)
frame_botoes_campos.pack(anchor=tk.E, pady=5)

botao_salvar = tk.Button(frame_botoes_campos, text="Salvar Nota", command=salvar_nota_gui)
botao_salvar.pack(side=tk.LEFT, padx=5)
botao_nova_nota = tk.Button(frame_botoes_campos, text="Nova Nota", command=nova_nota_gui)
botao_nova_nota.pack(side=tk.LEFT, padx=5)

# --- Listagem e Ações (Frame Direito) ---
listbox_label = tk.Label(frame_listagem_acoes, text="Histórico de Notas:")
listbox_label.pack(anchor=tk.NW)
listbox_notas = tk.Listbox(frame_listagem_acoes, width=40, height=20)
listbox_notas.pack(fill=tk.BOTH, expand=True)

frame_acoes_listagem = tk.Frame(frame_listagem_acoes)
frame_acoes_listagem.pack(fill=tk.X, pady=5)

botao_listar_tudo = tk.Button(frame_acoes_listagem, text="Listar Todas", command=listar_notas_gui)
botao_listar_tudo.pack(side=tk.LEFT, padx=5)

categoria_pesquisa_label = tk.Label(frame_acoes_listagem, text="Categoria:")
categoria_pesquisa_label.pack(side=tk.LEFT, padx=5)
categoria_pesquisa_entry = tk.Entry(frame_acoes_listagem, width=10)
categoria_pesquisa_entry.pack(side=tk.LEFT, padx=5)
botao_listar_categoria = tk.Button(frame_acoes_listagem, text="Listar por Categoria", command=listar_notas_por_categoria_gui)
botao_listar_categoria.pack(side=tk.LEFT, padx=5)

busca_label = tk.Label(frame_acoes_listagem, text="Buscar Conteúdo:")
busca_label.pack(side=tk.LEFT, padx=5)
busca_entry = tk.Entry(frame_acoes_listagem, width=10)
busca_entry.pack(side=tk.LEFT, padx=5)
botao_buscar_conteudo = tk.Button(frame_acoes_listagem, text="Buscar", command=buscar_nota_por_conteudo_gui)
botao_buscar_conteudo.pack(side=tk.LEFT, padx=5)

frame_botoes_acoes = tk.Frame(frame_listagem_acoes)
frame_botoes_acoes.pack(anchor=tk.E, pady=5)

botao_visualizar = tk.Button(frame_botoes_acoes, text="Visualizar", command=visualizar_nota_gui)
botao_visualizar.pack(side=tk.LEFT, padx=5)
botao_deletar = tk.Button(frame_botoes_acoes, text="Deletar Nota", command=deletar_nota_gui)
botao_deletar.pack(side=tk.LEFT, padx=5)

# --- Carregar notas ao iniciar ---
carregar_notas()
listar_notas_gui()

root.mainloop()